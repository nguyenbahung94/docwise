#!/usr/bin/env python3
"""
LLM summarizer for docwise plugin.
Reads a raw knowledge file produced by doc_extractor.py and enhances it with
semantic sections (Mental Model, Decision Framework, Anti-Patterns, Key
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

_TIMEOUT = 120  # seconds — LLM generation can be slow for large prompts
_SECTION_ANCHOR = "## Concepts (for graph)"
_NEW_SECTION_NAMES = ["Mental Model", "Decision Framework", "Anti-Patterns", "Key Relationships"]

_PROMPT_TEMPLATE = """\
You are a senior Android developer analyzing extracted documentation.

Given this raw knowledge file (produced by a regex-based extractor), add the \
following NEW sections. These sections capture semantic understanding that the \
regex extractor cannot derive on its own.

--- KNOWLEDGE FILE START ---
{content}
--- KNOWLEDGE FILE END ---

Add ONLY these four new sections, in this order:

## Mental Model
Explain the conceptual framework:
- WHY do these APIs exist? What problem do they solve?
- How do they relate to each other? (e.g. "X is built on top of Y")
- What is the key lifecycle insight a developer must internalize?

## Decision Framework
A table showing: given situation X, use API Y instead of Z.
Format exactly as:
| Situation | Use | Why |
| --- | --- | --- |
| ... | ... | ... |

## Anti-Patterns
- When NOT to use each API
- Common mistakes that go beyond the Pitfalls already listed above
- Include a short Kotlin snippet for each anti-pattern where helpful

## Key Relationships
- List equivalences and compositions, e.g.:
  - "produceState = LaunchedEffect + remember { mutableStateOf() }"
  - "DisposableEffect = LaunchedEffect + onDispose cleanup"
- Include any important ordering or dependency constraints between APIs

IMPORTANT RULES:
- Output ONLY the four new sections above — nothing else
- Do NOT repeat or summarise any Rules, Code Patterns, Pitfalls, Guidelines, or \
Concepts already in the file
- Be concise and actionable; prefer bullet points over long paragraphs
- Use Kotlin code examples where they make a point clearer
- Do not include a preamble or closing remarks — start directly with "## Mental Model"
"""

# ---------------------------------------------------------------------------
# Ollama HTTP call
# ---------------------------------------------------------------------------


def call_ollama(base_url: str, model: str, prompt: str) -> str:
    """POST to Ollama /api/generate and return the response text."""
    url = base_url.rstrip("/") + "/api/generate"
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=_TIMEOUT) as resp:
            body = resp.read().decode("utf-8", errors="replace")
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
            f"[llm_summarizer] Timeout after {_TIMEOUT}s waiting for Ollama.\n"
            f"  Try a smaller model or increase _TIMEOUT in the script.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        print(f"[llm_summarizer] Unexpected response from Ollama (not JSON): {exc}", file=sys.stderr)
        sys.exit(1)

    if "error" in data:
        print(f"[llm_summarizer] Ollama error: {data['error']}", file=sys.stderr)
        sys.exit(1)

    return data.get("response", "").strip()


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
    prompt = _PROMPT_TEMPLATE.format(content=original_content)
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
