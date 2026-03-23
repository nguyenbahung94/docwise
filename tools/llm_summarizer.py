#!/usr/bin/env python3
"""
LLM summarizer for docwise plugin.
Reads a raw knowledge file produced by doc_extractor.py and enhances it with
semantic sections (Mental Model, Lifecycle & Timing, Decision Framework, Internal Composition, Cost & Performance, Anti-Patterns, Key
Relationships) via a local Ollama model.

Uses only Python stdlib + urllib — zero extra dependencies.

Usage:
  python3 llm_summarizer.py --input knowledge/side-effects/compose-side-effects.md --model qwen2.5:32b
  python3 llm_summarizer.py --input knowledge/foo.md --model llama3.1 --output knowledge/foo-enhanced.md
  python3 llm_summarizer.py --input knowledge/foo.md --model mistral --ollama-url http://localhost:11434
"""

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_TIMEOUT = 600  # seconds — 32B models need 3-5 min for long prompts
_SECTION_ANCHOR = "## Concepts (for graph)"
_NEW_SECTION_NAMES = [
    "Mental Model", "Lifecycle & Timing", "Decision Framework",
    "Internal Composition", "Cost & Performance", "Anti-Patterns", "Key Relationships",
]

_PROMPT_TEMPLATE = """\
You are a staff-level Android engineer writing an internal knowledge base entry.
Your audience is mid-level developers who can read API docs but need the \
"why", "when", and "how things connect" that docs never spell out.

--- RAW EXTRACTED CONTENT ---
{content}
--- END ---

The content above was mechanically extracted from official docs. It has code \
and surface-level rules, but LACKS:
- The mental model (why these APIs exist at all)
- Lifecycle timing (exactly when each thing runs/cancels/restarts)
- Direct comparisons (when to pick X over Y)
- Composition relationships (X = Y + Z under the hood)
- Architecture context (how this topic fits into app architecture)
- Cost/performance implications (why something is expensive, what it allocates)
- The anti-patterns that LOOK correct but break in subtle ways

STEP 1 — Before writing, ask yourself these questions about the content:
1. What PROBLEM does this topic solve? Why can't you just write normal code?
2. For EACH API/concept mentioned: when exactly does it trigger, cancel, restart?
3. Which APIs are commonly confused with each other? What's the difference?
4. What is each API made of internally? (e.g. "X = Y + Z")
5. What looks correct but is actually wrong? Why?
6. How does this topic interact with the broader architecture (ViewModel, navigation, lifecycle)?
7. What would a lifecycle/timing DIAGRAM look like?
8. What are the performance costs? What gets allocated/tracked?

STEP 2 — Now write these sections based on your answers:

## Mental Model
- **The Problem**: What specific problem does this topic solve? (1-2 sentences, sharp)
- **Core Insight**: The single most important thing to understand (1 sentence)
- **Classification**: Group/categorize the APIs by their PURPOSE (not alphabetically):
  - Category 1: [name] — APIs that do X
  - Category 2: [name] — APIs that do Y
- **Architecture Context**: How does this fit with ViewModel, Repository, Navigation?

## Lifecycle & Timing
Show EXACTLY when each API runs. Use this format:
```
Enter Composition
  → [what starts]
Recomposition
  → [what runs]
Key changes
  → [what cancels, what restarts]
Leave Composition
  → [what cleans up]
```
Then for each API, one line: "API — triggers: X, cancels: Y, restarts when: Z"

## Decision Framework
A comparison table. For EACH pair of similar APIs, explain the difference:
| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| [concrete scenario] | [correct API] | [wrong API] | [specific reason] |

Include at least 5 rows covering real scenarios.

## Internal Composition
How APIs are built from each other:
- "X = Y + Z" format
- What this means practically (when knowing the internals helps you debug)

## Cost & Performance
For each API that has performance implications:
- What it allocates/tracks internally
- When it becomes expensive
- How to minimize cost

## Anti-Patterns
For each anti-pattern:
- **Name** (short, memorable)
- **Looks like**: (the wrong code — short snippet)
- **Why it breaks**: (specific, not vague)
- **Fix**: (the correct code — short snippet)

At least 3 anti-patterns. Focus on mistakes that LOOK correct.

## Key Relationships
- Equivalences: "X = Y + Z"
- Dependencies: "X requires Y to work correctly"
- Ordering: "X must happen before Y"
- Conflicts: "Never use X together with Y because..."

RULES:
- Output ONLY the sections above — nothing else
- Do NOT repeat Rules, Code Patterns, Pitfalls, or Guidelines from the input
- Be SPECIFIC — no "ensure proper handling" or "be careful with lifecycle"
- Every claim must be concrete: name the API, name the callback, name the dispatcher
- Use Kotlin snippets only when they make the point clearer (max 5 lines each)
- Start directly with "## Mental Model" — no preamble
"""

# ---------------------------------------------------------------------------
# Ollama HTTP call
# ---------------------------------------------------------------------------


def call_ollama(base_url: str, model: str, prompt: str) -> str:
    """POST to Ollama /api/generate with streaming and return the full response text."""
    url = base_url.rstrip("/") + "/api/generate"
    payload = json.dumps({"model": model, "prompt": prompt, "stream": True}).encode()
    req = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urlopen(req, timeout=_TIMEOUT)
    except HTTPError as exc:
        if exc.code == 404:
            print(
                f"[llm_summarizer] Error: model '{model}' not found on Ollama.\n"
                f"  Run: ollama pull {model}",
                file=sys.stderr,
            )
        else:
            print(f"[llm_summarizer] Ollama HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        sys.exit(1)
    except URLError as exc:
        print(
            f"[llm_summarizer] Cannot reach Ollama at {base_url}.\n"
            f"  Make sure Ollama is running: ollama serve\n"
            f"  Reason: {exc.reason}",
            file=sys.stderr,
        )
        sys.exit(1)
    except TimeoutError:
        print(
            f"[llm_summarizer] Timeout connecting to Ollama.\n"
            f"  Make sure Ollama is running: ollama serve",
            file=sys.stderr,
        )
        sys.exit(1)

    # Read streaming response line by line
    full_response = []
    token_count = 0
    try:
        for line in resp:
            line = line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError:
                continue
            text = chunk.get("response", "")
            if text:
                full_response.append(text)
                token_count += 1
                if token_count % 50 == 0:
                    print(".", end="", flush=True, file=sys.stderr)
            if chunk.get("done", False):
                break
    finally:
        resp.close()
    print(file=sys.stderr)  # newline after dots
    return "".join(full_response).strip()


# ---------------------------------------------------------------------------
# File manipulation
# ---------------------------------------------------------------------------


def read_knowledge_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        print(f"[llm_summarizer] Input file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"[llm_summarizer] Cannot read {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def write_knowledge_file(path: str, content: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    except OSError as exc:
        print(f"[llm_summarizer] Cannot write {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def insert_new_sections(original: str, new_sections: str) -> str:
    """
    Insert new_sections into original immediately before '## Concepts (for graph)'.
    If that anchor is absent, append at the end.
    """
    new_sections = new_sections.strip()
    if not new_sections.endswith("\n"):
        new_sections += "\n"

    anchor_idx = original.find(_SECTION_ANCHOR)
    if anchor_idx == -1:
        # No Concepts section — append at end
        separator = "\n" if original.endswith("\n") else "\n\n"
        return original + separator + new_sections

    # Insert before the anchor, preserving a blank line on both sides
    before = original[:anchor_idx].rstrip("\n") + "\n\n"
    after = original[anchor_idx:]
    return before + new_sections + "\n\n" + after


def count_sections_added(new_sections: str) -> list:
    """Return list of section names that were actually generated."""
    found = []
    for name in _NEW_SECTION_NAMES:
        if f"## {name}" in new_sections:
            found.append(name)
    return found


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Enhance a docwise knowledge file with semantic sections via Ollama."
    )
    parser.add_argument("--input", required=True, help="Path to the knowledge .md file to enhance")
    parser.add_argument("--model", required=True, help="Ollama model name (e.g. qwen2.5:32b)")
    parser.add_argument(
        "--output",
        default=None,
        help="Output path (default: overwrite --input)",
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Base URL of the Ollama server (default: http://localhost:11434)",
    )
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()

    output_path = args.output or args.input

    print(f"[llm_summarizer] Reading: {args.input}")
    original_content = read_knowledge_file(args.input)

    print(f"[llm_summarizer] Sending to Ollama model '{args.model}' at {args.ollama_url} ...")
    prompt = _PROMPT_TEMPLATE.replace("{content}", original_content)
    new_sections = call_ollama(args.ollama_url, args.model, prompt)

    if not new_sections:
        print("[llm_summarizer] Warning: Ollama returned an empty response. File not modified.", file=sys.stderr)
        sys.exit(1)

    enhanced = insert_new_sections(original_content, new_sections)

    print(f"[llm_summarizer] Writing: {output_path}")
    write_knowledge_file(output_path, enhanced)

    added = count_sections_added(new_sections)
    print(
        f"[llm_summarizer] Enhanced: added {len(added)} new section(s) "
        f"({', '.join(added) if added else 'none detected in output'})"
    )


if __name__ == "__main__":
    main()
