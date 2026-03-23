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
    "Core Concepts", "Mental Model", "Lifecycle & Timing", "Decision Framework",
    "How It Works Internally", "Common Mistakes", "Key Relationships",
]

_PROMPT_TEMPLATE = """\
You are a staff-level Android engineer writing an internal knowledge base entry.
Your audience is mid-level developers who can read API docs but need the \
"why", "when", and "how things connect" that docs never spell out.

--- RAW EXTRACTED CONTENT ---
{content}
--- END ---

CRITICAL CONSTRAINT — GROUNDING RULE:
You must ONLY analyze concepts, APIs, and patterns that appear in the content above.
Do NOT add topics the doc doesn't cover. If the doc is about "UI architecture and \
data flow", do NOT add sections about DI, Testing, Navigation, or other topics \
unless the doc explicitly discusses them.

For every claim you make, you must be able to point to a specific heading, code \
block, rule, or guideline in the input that supports it. If you can't point to it, \
don't write it.

STEP 1 — Identify CORE CONCEPTS by emphasis:
Read the input carefully. Find:
- Concepts that appear in MULTIPLE headings → these are core
- Concepts repeated in rules AND guidelines AND code → these are core
- Patterns the doc explicitly says "should", "must", or "important" → these are core
- Concepts that only appear once in passing → these are secondary

List the top 3-5 core concepts BEFORE writing. Everything you write must center \
around these core concepts.

STEP 2 — For each core concept, ask:
1. What PROBLEM does it solve? What goes wrong WITHOUT it?
2. What is the PRECISE mechanism? (not vague — HOW does it work?)
3. What are the BOUNDARIES? (when does it apply, when does it NOT apply?)
4. What LOOKS correct but is actually wrong?
5. How does it CONNECT to the other core concepts in this doc?

STEP 3 — Write these sections:

## Core Concepts
List the 3-5 core concepts you identified and WHY they are core (what evidence \
from the doc). This anchors everything that follows.

## Mental Model
- **The Problem**: What specific problem does this doc's topic solve? (1-2 sentences)
- **Core Insight**: The single most important thing to understand (1 sentence)
- **How concepts connect**: Draw the relationship between core concepts. \
Use "A → B" format. Show how data/state/events flow between them.

## Lifecycle & Timing
ONLY if the doc discusses lifecycle-related APIs or timing.
Show EXACTLY when each API/concept activates. Use this format:
```
[trigger event]
  → [what happens]
  → [what changes]
[cleanup event]
  → [what gets cleaned up]
```
Then for each API: "API — triggers: X, cancels: Y, restarts when: Z"
SKIP this section entirely if the doc is not about lifecycle-aware APIs.

## Decision Framework
For concepts that developers commonly confuse or misuse:
| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
Only include rows for concepts ACTUALLY discussed in the doc.

## How It Works Internally
For concepts where the doc explains or implies internals:
- "X = Y + Z" format
- What this means practically
SKIP if the doc doesn't discuss internals.

## Common Mistakes
For each mistake (must be grounded in the doc's warnings, pitfalls, or "don't" rules):
- **Name** (short)
- **Looks like**: (wrong code — max 5 lines)
- **Why it breaks**: (PRECISE mechanism, not vague)
- **Correct**: (right code — max 5 lines)

## Key Relationships
ONLY relationships between concepts IN this doc:
- "X requires Y" / "X enables Y" / "X replaces Y"
- Flow: "Event → State → UI" or similar

HARD RULES:
- GROUNDED: Every section must trace back to content in the input. No hallucination.
- FOCUSED: Only analyze what the doc covers. Do NOT expand scope.
- PRECISE: "observable state triggers recomposition" NOT "avoid concurrency issues"
- CORE FIRST: Spend 80% of your output on core concepts, 20% on secondary
- NO FILLER: If a section has nothing grounded to add, SKIP IT entirely
- Start directly with "## Core Concepts" — no preamble
"""

# Pass 2: Review & Deepen
_REVIEW_PROMPT_TEMPLATE = """\
You are reviewing a knowledge base entry. Your job is to find 2 types of problems:

1. **HALLUCINATION** — content that was NOT in the original doc
2. **GAPS** — core concepts from the doc that are missing or shallow

--- CURRENT KNOWLEDGE FILE ---
{content}
--- END ---

REVIEW STEP 1 — HALLUCINATION CHECK:
Look at every section. For each claim, ask: "Is this grounded in the Rules, \
Code Patterns, Pitfalls, or Guidelines sections above?"
- If a section discusses topics NOT present in the extracted content → REMOVE IT
- If a claim can't be traced to the input → FLAG IT
- Common hallucinations: adding DI/Testing/Navigation when doc doesn't cover them

REVIEW STEP 2 — CORE CONCEPT DEPTH CHECK:
Look at the "## Core Concepts" section. For each core concept listed:
- Is it explained with PRECISE mechanism (not vague)?
- Does it explain WHAT GOES WRONG without it? (the failure mode)
- Are boundaries clear? (when it applies vs when it doesn't)
- Is the connection to other core concepts explicit?

REVIEW STEP 3 — PRECISION CHECK:
Find vague language and replace with precise language:
- "avoid issues" → WHAT specific issue?
- "can cause problems" → WHAT problem, WHEN?
- "improves performance" → HOW, by preventing WHAT?
- "concurrency issues" → is it really concurrency, or is it about observability?

REVIEW STEP 4 — MISSING DISTINCTIONS:
Look at the doc's content. Are there important distinctions the analysis missed?
Examples of distinctions docs commonly make:
- State vs Event (render vs action)
- Where state lives vs who reads it
- Observable state vs plain variables
- Hoisting direction (up) vs data flow direction (down)

OUTPUT FORMAT:

## [Section Name] (deepened)
[Improved content — more precise, better grounded]

## Hallucination Report
[List any sections or claims that should be REMOVED because they're not in the doc]

RULES:
- REMOVE hallucinated content — don't just flag it, mark it for removal
- DEEPEN with precision — replace vague with specific
- GROUND everything — if it's not in the doc, it doesn't belong
- Start directly with improvements — no preamble
"""

# Pass 3: Fix — rewrite sections based on self-check findings
_FIX_PROMPT_TEMPLATE = """\
You are rewriting a knowledge base entry to fix problems found during review.

--- CURRENT KNOWLEDGE FILE ---
{content}
--- END ---

--- REVIEW FINDINGS ---
{review}
--- END ---

Your job: produce a COMPLETE rewrite of ONLY the semantic sections \
(everything from "## Core Concepts" to just before "## Concepts (for graph)").

INSTRUCTIONS:
1. Read the review findings carefully.
2. REMOVE any content flagged as hallucination.
3. DEEPEN any content flagged as shallow — use the reviewer's suggestions.
4. ADD any missing core concepts the reviewer identified.
5. FIX any vague language the reviewer flagged — make it precise.
6. KEEP content the reviewer said was good — don't regress.

OUTPUT:
Write the COMPLETE set of semantic sections, fully rewritten. Include ALL sections \
(Core Concepts, Mental Model, etc.) even if only some need changes — this output \
will REPLACE the existing semantic sections entirely.

Start directly with "## Core Concepts" — no preamble.
"""

# Pass 4: Verify — final check, confirm quality
_VERIFY_PROMPT_TEMPLATE = """\
You are doing a FINAL quality check on a knowledge base entry before it ships.

--- KNOWLEDGE FILE ---
{content}
--- END ---

Score each section on a 1-5 scale:

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | ? | ? |
| Mental Model | ? | ? |
| Decision Framework | ? | ? |
| Common Mistakes | ? | ? |
| Key Relationships | ? | ? |

Scoring:
- 5: Precise, grounded, actionable, no hallucination
- 4: Good, minor improvements possible
- 3: Missing depth or has vague claims
- 2: Contains hallucination or misses core concepts
- 1: Wrong or completely off-topic

Then for any section scoring < 4, provide a ONE-LINE fix suggestion.

Finally, output a single verdict:
- PASS: All sections ≥ 4. Ready to ship.
- NEEDS_FIX: Some sections < 4. List which ones.

OUTPUT FORMAT:
## Quality Report

[Score table]

## Verdict: PASS or NEEDS_FIX

## Fixes (only if NEEDS_FIX)
[One-line fix per section that scored < 4]

Start directly with "## Quality Report" — no preamble.
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
        description="Enhance a docwise knowledge file with semantic sections via Ollama.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Pipeline modes:
  --passes 1  Generate only (fast, rough)
  --passes 2  Generate + Self-check (default, good balance)
  --passes 4  Generate + Self-check + Fix + Verify (best quality)
""",
    )
    parser.add_argument("--input", required=True, help="Path to the knowledge .md file to enhance")
    parser.add_argument("--model", required=True, help="Ollama model name (e.g. qwen2.5:14b)")
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
    parser.add_argument(
        "--passes",
        type=int,
        default=4,
        choices=[1, 2, 4],
        help="Pipeline: 1=generate, 2=generate+check, 4=generate+check+fix+verify (default: 4)",
    )
    return parser


def extract_raw_content(full_file: str) -> str:
    """Extract the raw extracted content (before semantic sections)."""
    # Find first semantic section
    for name in _NEW_SECTION_NAMES:
        idx = full_file.find(f"\n## {name}")
        if idx != -1:
            return full_file[:idx].rstrip()
    return full_file


def replace_semantic_sections(full_file: str, new_sections: str) -> str:
    """Replace all semantic sections with new_sections, preserving raw content and Concepts."""
    raw = extract_raw_content(full_file)
    new_sections = new_sections.strip()

    # Find Concepts section to preserve
    concepts = ""
    anchor_idx = full_file.find(_SECTION_ANCHOR)
    if anchor_idx != -1:
        concepts = full_file[anchor_idx:]

    result = raw + "\n\n" + new_sections + "\n"
    if concepts:
        result += "\n" + concepts
    return result


def main() -> None:
    args = build_arg_parser().parse_args()
    output_path = args.output or args.input
    total = args.passes

    print(f"[llm_summarizer] Reading: {args.input}")
    original_content = read_knowledge_file(args.input)

    # ── Pass 1: Generate ──────────────────────────────────────────────
    print(f"[llm_summarizer] Pass 1/{total}: Generate semantic sections ...")
    prompt = _PROMPT_TEMPLATE.replace("{content}", original_content)
    new_sections = call_ollama(args.ollama_url, args.model, prompt)

    if not new_sections:
        print("[llm_summarizer] Warning: Ollama returned empty. File not modified.", file=sys.stderr)
        sys.exit(1)

    enhanced = insert_new_sections(original_content, new_sections)
    added = count_sections_added(new_sections)
    print(f"[llm_summarizer] Pass 1 done: {len(added)} section(s) ({', '.join(added)})")

    if total < 2:
        write_knowledge_file(output_path, enhanced)
        print(f"[llm_summarizer] Written: {output_path}")
        return

    # ── Pass 2: Self-check ────────────────────────────────────────────
    print(f"[llm_summarizer] Pass 2/{total}: Self-check (find problems) ...")
    review_prompt = _REVIEW_PROMPT_TEMPLATE.replace("{content}", enhanced)
    review_findings = call_ollama(args.ollama_url, args.model, review_prompt)

    if review_findings:
        print(f"[llm_summarizer] Pass 2 done: review findings generated")
        # Show summary of findings
        import re as _re
        hallucinations = _re.findall(r"hallucin|REMOVE|not in the doc|not grounded", review_findings, _re.IGNORECASE)
        gaps = _re.findall(r"missing|shallow|vague|gap", review_findings, _re.IGNORECASE)
        print(f"[llm_summarizer]   Hallucinations flagged: {len(hallucinations)}, Gaps found: {len(gaps)}")
    else:
        print(f"[llm_summarizer] Pass 2: no findings (looks clean)")
        review_findings = ""

    if total < 4:
        # 2-pass mode: merge review findings directly
        if review_findings:
            enhanced = insert_new_sections(enhanced, review_findings)
        write_knowledge_file(output_path, enhanced)
        print(f"[llm_summarizer] Written: {output_path}")
        return

    # ── Pass 3: Fix ───────────────────────────────────────────────────
    print(f"[llm_summarizer] Pass 3/{total}: Fix (rewrite based on findings) ...")
    fix_prompt = _FIX_PROMPT_TEMPLATE.replace("{content}", enhanced).replace("{review}", review_findings)
    fixed_sections = call_ollama(args.ollama_url, args.model, fix_prompt)

    if fixed_sections:
        enhanced = replace_semantic_sections(enhanced, fixed_sections)
        fixed_count = count_sections_added(fixed_sections)
        print(f"[llm_summarizer] Pass 3 done: rewrote {len(fixed_count)} section(s) ({', '.join(fixed_count)})")
    else:
        print(f"[llm_summarizer] Pass 3: no rewrite produced, keeping previous")

    # ── Pass 4: Verify ────────────────────────────────────────────────
    print(f"[llm_summarizer] Pass 4/{total}: Verify (final quality check) ...")
    verify_prompt = _VERIFY_PROMPT_TEMPLATE.replace("{content}", enhanced)
    verdict = call_ollama(args.ollama_url, args.model, verify_prompt)

    if verdict:
        # Extract verdict line
        import re as _re
        verdict_match = _re.search(r"Verdict:\s*(PASS|NEEDS_FIX)", verdict)
        if verdict_match:
            result = verdict_match.group(1)
            print(f"[llm_summarizer] Pass 4 done: {result}")
            if result == "NEEDS_FIX":
                # Extract fix suggestions
                fixes = _re.findall(r"^- (.+)$", verdict, _re.MULTILINE)
                for fix in fixes[:5]:
                    print(f"[llm_summarizer]   → {fix}")
        else:
            print(f"[llm_summarizer] Pass 4 done: verdict unclear")

        # Append quality report as HTML comment at end of file
        enhanced = enhanced.rstrip() + "\n\n<!-- Quality Report\n" + verdict + "\n-->\n"
    else:
        print(f"[llm_summarizer] Pass 4: no verdict returned")

    print(f"[llm_summarizer] Writing: {output_path}")
    write_knowledge_file(output_path, enhanced)
    print("[llm_summarizer] Done.")


if __name__ == "__main__":
    main()
