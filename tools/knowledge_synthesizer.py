#!/usr/bin/env python3
"""
Knowledge synthesizer for docwise plugin.
Reads multiple knowledge files and generates a synthesis file that connects
them — showing how concepts from different topics work together in practice.

Uses only Python stdlib + urllib — zero extra dependencies.
Uses local Ollama LLM for synthesis (reasoning task).

Usage:
  python3 knowledge_synthesizer.py --topics "compose-state,kotlin-coroutines,hilt,android-lifecycle" \\
      --name "android-screen-architecture" \\
      --output /Users/bahung/knowledge/ \\
      --model qwen2.5:14b

  python3 knowledge_synthesizer.py --preset android-screen \\
      --output /Users/bahung/knowledge/ \\
      --model qwen2.5:14b
"""

import argparse
import datetime
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_TIMEOUT = 600  # seconds — large models need time on long prompts

_PRESETS = {
    "android-screen": {
        "topics": [
            "compose-state",
            "compose-lifecycle",
            "compose-side-effects",
            "compose-navigation",
            "hilt",
            "android-lifecycle",
            "kotlin-coroutines",
        ],
        "name": "android-screen-architecture",
    },
    "android-data": {
        "topics": [
            "room",
            "data-storage",
            "kotlin-coroutines",
            "kotlin-flow",
            "hilt",
        ],
        "name": "android-data-architecture",
    },
    "android-compose-full": {
        "topics": [
            "compose-state",
            "compose-lifecycle",
            "compose-side-effects",
            "compose-phases",
            "compose-performance",
            "compose-compositionlocal",
            "compose-navigation",
            "compose-architecture",
            "compose-layering",
        ],
        "name": "android-compose-full-architecture",
    },
}

# Sections to extract from each knowledge file (in priority order)
_EXTRACT_SECTIONS = [
    "Rules",
    "Code Patterns",
    "Pitfalls",
    "Common Mistakes",
    "Decision Framework",
    "Mental Model",
    "Core Concepts",
    "Key Relationships",
]

# Sections to skip entirely (too verbose, not useful for cross-topic synthesis)
_SKIP_SECTIONS = {
    "Guidelines",
    "Concepts (for graph)",
    "Internal Composition",
    "How It Works Internally",
    "Lifecycle & Timing",
    "Quality Report",
    "Source Topics",
}

# Max lines to extract per section per topic (keep context window bounded)
_MAX_LINES_PER_SECTION = 40

# ---------------------------------------------------------------------------
# Ollama HTTP call
# ---------------------------------------------------------------------------


def call_ollama(base_url: str, model: str, prompt: str) -> str:
    """POST to Ollama /api/generate with streaming, return full response text."""
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
                f"[synthesizer] Error: model '{model}' not found on Ollama.\n"
                f"  Run: ollama pull {model}",
                file=sys.stderr,
            )
        else:
            print(
                f"[synthesizer] Ollama HTTP error {exc.code}: {exc.reason}",
                file=sys.stderr,
            )
        sys.exit(1)
    except URLError as exc:
        print(
            f"[synthesizer] Cannot reach Ollama at {base_url}.\n"
            f"  Make sure Ollama is running: ollama serve\n"
            f"  Reason: {exc.reason}",
            file=sys.stderr,
        )
        sys.exit(1)
    except TimeoutError:
        print(
            f"[synthesizer] Timeout connecting to Ollama.\n"
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
# Knowledge file reading and extraction
# ---------------------------------------------------------------------------


def find_knowledge_file(knowledge_dir: str, topic: str) -> str:
    """Resolve the path to a topic's knowledge file.

    Tries:
      <knowledge_dir>/<topic>/<topic>.md  (canonical layout)
      <knowledge_dir>/<topic>.md          (flat layout)
    """
    canonical = os.path.join(knowledge_dir, topic, f"{topic}.md")
    if os.path.isfile(canonical):
        return canonical
    flat = os.path.join(knowledge_dir, f"{topic}.md")
    if os.path.isfile(flat):
        return flat
    return ""


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        print(f"[synthesizer] Cannot read {path}: {exc}", file=sys.stderr)
        return ""


def _parse_sections(content: str) -> dict:
    """Split a knowledge file into named sections.

    Returns {section_name: section_body_text}.
    """
    sections = {}
    # Match ## headings
    section_re = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    matches = list(section_re.finditer(content))
    for idx, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        sections[name] = content[start:end].strip()
    return sections


def _extract_do_dont_patterns(section_body: str) -> list:
    """Extract [DO] / [DON'T] tagged lines from a Code Patterns section body.

    Returns a list of strings (the annotated lines/blocks).
    """
    lines = section_body.splitlines()
    results = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # [DO] or [DON'T] markers
        if re.search(r"\[DO\]|\[DON'?T\]|\[DONT\]", line, re.IGNORECASE):
            # Grab this line plus the next few (code block context)
            block = [line]
            j = i + 1
            while j < len(lines) and j < i + 8:
                block.append(lines[j])
                j += 1
            results.append("\n".join(block))
            i = j
        else:
            i += 1
    return results


def _truncate_lines(text: str, max_lines: int) -> str:
    """Truncate text to at most max_lines lines, appending a note if truncated."""
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    truncated = "\n".join(lines[:max_lines])
    omitted = len(lines) - max_lines
    return truncated + f"\n... ({omitted} more lines omitted)"


def extract_relevant_content(topic: str, content: str) -> str:
    """Extract Rules, Code Patterns ([DO]/[DON'T] only), Pitfalls, and key
    sections from a knowledge file.  Returns a compact, labeled block.
    """
    if not content:
        return f"[{topic}] (no content available)"

    sections = _parse_sections(content)
    parts = [f"=== {topic} ==="]

    for section_name in _EXTRACT_SECTIONS:
        # Exact match first, then case-insensitive
        body = sections.get(section_name)
        if body is None:
            for key in sections:
                if key.lower() == section_name.lower():
                    body = sections[key]
                    break
        if not body:
            continue
        if section_name in _SKIP_SECTIONS:
            continue

        # For Code Patterns: only keep [DO]/[DON'T] annotated blocks
        if section_name == "Code Patterns":
            do_dont = _extract_do_dont_patterns(body)
            if do_dont:
                parts.append(f"### {section_name} (DO/DON'T patterns)")
                # Cap at 5 patterns to stay within context
                for pattern in do_dont[:5]:
                    parts.append(pattern)
            continue

        # For other sections: truncate to max lines
        truncated = _truncate_lines(body, _MAX_LINES_PER_SECTION)
        parts.append(f"### {section_name}")
        parts.append(truncated)

    if len(parts) == 1:
        # Nothing extracted — include a short raw excerpt as fallback
        raw_lines = content.splitlines()
        parts.append("### (raw excerpt)")
        parts.append("\n".join(raw_lines[:30]))

    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

_SYNTHESIS_PROMPT = """\
You are a staff-level Android engineer writing an internal knowledge base SYNTHESIS file.
Your audience: mid-level developers who have already read individual topic files and need
to understand how ALL these topics connect when building a real Android feature.

--- KNOWLEDGE FROM INDIVIDUAL TOPICS ---
{combined_content}
--- END OF TOPIC KNOWLEDGE ---

IMPORTANT CONSTRAINTS:
1. DO NOT repeat individual topic rules. Those already exist in separate files.
2. DO show how topics COMBINE and interact when building real features.
3. Every item must cite which topic(s) it draws from using format: (see: topic-name)
4. Be concrete and actionable — not generic architecture advice.
5. Use Kotlin code examples only (no Java).
6. Keep code examples short (5-10 lines max each).

Generate EXACTLY these sections in order:

## Building a Screen (step-by-step)
Walk through building a typical screen using ALL the provided topics.
Number each step. For each step state: what you do, which topic's rules apply, and any
cross-topic concern. Example format:
  1. **Define UI state** — use a sealed class/data class. Apply compose-state hoisting rules.
     Cross-topic: hilt injects the ViewModel that owns this state (see: compose-state, hilt)

## Common Combinations
Show 3-5 concrete patterns where MULTIPLE topics interact. For each:
- Pattern name (bold)
- 1 sentence: what these topics do TOGETHER
- Short code snippet showing the interaction (Kotlin, 5-10 lines)
- Which topics are involved (see: topic-a, topic-b)

Example patterns to aim for (adapt to the actual topics provided):
- ViewModel + Room + Flow: data flows from DB to UI
- Hilt + ViewModel + UseCase: DI wires the layers
- LaunchedEffect + Coroutines + Navigation: one-shot side effects

## Cross-Topic Pitfalls
Mistakes that ONLY appear when combining these topics (not in individual files).
For each pitfall:
- **Name** (short, bold)
- What goes wrong (1-2 sentences, precise failure mode)
- Correct approach (1 sentence or short code snippet)
- Which topics interact to create this pitfall (see: topic-a, topic-b)

Focus on pitfalls like:
- Collecting Flow in Composable without lifecycle awareness
- Wrong scope for coroutines (viewModelScope vs lifecycleScope vs rememberCoroutineScope)
- Hilt ViewModel injection vs manual ViewModel factory
- State hoisting across navigation boundaries

## Decision Map
A quick reference: when building feature X, which topics apply and how.
Format as a table or bullet list:

| Feature type | Topics | Key rule |
|---|---|---|
| New screen with list | topic-a, topic-b | one-liner on the critical constraint |
| One-shot API call | ... | ... |
| Background sync | ... | ... |
| Navigation with args | ... | ... |

Include at least 4 rows covering the most common scenarios for the given topics.
Cite which topic each rule comes from (see: topic-name) in the Key rule column.

STYLE RULES:
- Start directly with "## Building a Screen" — no preamble, no title
- Be dense and precise — every sentence must be actionable
- Prefer "X must Y" over "X should probably Y"
- If two topics conflict (e.g. two ways to pass state), call it out explicitly
"""


def build_prompt(combined_content: str) -> str:
    return _SYNTHESIS_PROMPT.replace("{combined_content}", combined_content)


# ---------------------------------------------------------------------------
# Output file construction
# ---------------------------------------------------------------------------


def build_output_content(
    name: str,
    topics: list,
    llm_output: str,
    knowledge_dir: str,
) -> str:
    """Build the full synthesis .md file content with metadata header."""
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    topics_csv = ", ".join(topics)

    header_lines = [
        f"<!-- Type: synthesis -->",
        f"<!-- Topics: {topics_csv} -->",
        f"<!-- Generated: {now} -->",
        "",
        f"# {name} (Synthesis)",
        "",
        llm_output,
        "",
        "## Source Topics",
    ]

    for topic in topics:
        # Emit canonical path relative to knowledge_dir
        rel_path = os.path.join("knowledge", topic, f"{topic}.md")
        header_lines.append(f"- {topic} → {rel_path}")

    header_lines.append("")
    return "\n".join(header_lines)


def write_output(path: str, content: str) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    except OSError as exc:
        print(f"[synthesizer] Cannot write {path}: {exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a synthesis knowledge file connecting multiple topics via Ollama.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # From explicit topics
  python3 knowledge_synthesizer.py \\
      --topics "compose-state,kotlin-coroutines,hilt,android-lifecycle" \\
      --name "android-screen-architecture" \\
      --output /Users/bahung/knowledge/ \\
      --model qwen2.5:14b

  # From preset
  python3 knowledge_synthesizer.py \\
      --preset android-screen \\
      --output /Users/bahung/knowledge/ \\
      --model qwen2.5:14b

Built-in presets:
  android-screen       compose-state, compose-lifecycle, compose-side-effects,
                       compose-navigation, hilt, android-lifecycle, kotlin-coroutines
  android-data         room, data-storage, kotlin-coroutines, kotlin-flow, hilt
  android-compose-full compose-state, compose-lifecycle, compose-side-effects,
                       compose-phases, compose-performance, compose-compositionlocal,
                       compose-navigation, compose-architecture, compose-layering
""",
    )

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        "--topics",
        help='Comma-separated topic slugs (e.g. "compose-state,kotlin-coroutines,hilt")',
    )
    source_group.add_argument(
        "--preset",
        choices=list(_PRESETS.keys()),
        help="Use a built-in topic preset",
    )

    parser.add_argument(
        "--name",
        help="Output file name slug (required with --topics, derived from --preset otherwise)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Knowledge root directory (synthesis goes to <output>/_synthesis/<name>.md)",
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Ollama model name (e.g. qwen2.5:14b)",
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Base URL of the Ollama server (default: http://localhost:11434)",
    )
    parser.add_argument(
        "--knowledge-dir",
        default=None,
        help=(
            "Directory containing per-topic knowledge files. "
            "Defaults to --output (i.e. topics live at <output>/<topic>/<topic>.md)"
        ),
    )
    return parser


def resolve_topics_and_name(args: argparse.Namespace) -> tuple:
    """Return (topics: list[str], name: str) from parsed args."""
    if args.preset:
        preset = _PRESETS[args.preset]
        topics = preset["topics"]
        name = args.name or preset["name"]
        return topics, name

    # --topics mode
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    if not topics:
        print("[synthesizer] Error: --topics is empty.", file=sys.stderr)
        sys.exit(1)
    if not args.name:
        print(
            "[synthesizer] Error: --name is required when using --topics.",
            file=sys.stderr,
        )
        sys.exit(1)
    return topics, args.name


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    topics, name = resolve_topics_and_name(args)
    output_root = args.output.rstrip("/")
    knowledge_dir = (args.knowledge_dir or output_root).rstrip("/")
    output_path = os.path.join(output_root, "_synthesis", f"{name}.md")

    print(f"[synthesizer] Reading {len(topics)} topic files...")

    topic_contents = []
    missing = []
    for topic in topics:
        file_path = find_knowledge_file(knowledge_dir, topic)
        if not file_path:
            print(
                f"[synthesizer]   WARNING: knowledge file not found for '{topic}' "
                f"(looked in {knowledge_dir}/{topic}/{topic}.md)",
                file=sys.stderr,
            )
            missing.append(topic)
            continue
        content = read_file(file_path)
        if not content:
            print(
                f"[synthesizer]   WARNING: '{topic}' file is empty: {file_path}",
                file=sys.stderr,
            )
            missing.append(topic)
            continue
        extracted = extract_relevant_content(topic, content)
        topic_contents.append(extracted)
        print(f"[synthesizer]   OK: {topic} ({file_path})")

    available_topics = [t for t in topics if t not in missing]

    if not topic_contents:
        print(
            "[synthesizer] Error: no topic content could be read. Aborting.",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(topic_contents) < 2:
        print(
            f"[synthesizer] Warning: only {len(topic_contents)} topic(s) available — "
            "synthesis works best with 2+ topics.",
            file=sys.stderr,
        )

    if missing:
        print(
            f"[synthesizer] Proceeding with {len(available_topics)}/{len(topics)} topics "
            f"(missing: {', '.join(missing)})"
        )

    combined_content = "\n\n".join(topic_contents)

    print(f"[synthesizer] Generating synthesis with model '{args.model}'...")
    prompt = build_prompt(combined_content)
    llm_output = call_ollama(args.ollama_url, args.model, prompt)

    if not llm_output:
        print(
            "[synthesizer] Error: Ollama returned empty response. Aborting.",
            file=sys.stderr,
        )
        sys.exit(1)

    output_content = build_output_content(name, available_topics, llm_output, knowledge_dir)

    print(f"[synthesizer] Writing synthesis to: {output_path}")
    write_output(output_path, output_content)
    print("[synthesizer] Done.")


if __name__ == "__main__":
    main()
