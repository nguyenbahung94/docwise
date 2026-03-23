#!/usr/bin/env python3
"""
Topic extractor for docwise plugin.
Orchestrates the full extraction pipeline for a topic with sub-pages.

Usage:
  python3 topic_extractor.py --url URL --topic TOPIC --output DIR/
  python3 topic_extractor.py --url URL --topic TOPIC --output DIR/ --enhance --model qwen2.5:14b
  python3 topic_extractor.py --url URL --topic TOPIC --output DIR/ --no-subpages
  python3 topic_extractor.py --urls "url1,url2,url3" --topic TOPIC --output DIR/
"""

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional, Tuple


TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------

def run_keyword_scanner(url: str) -> Dict:
    """Call keyword_scanner.py and return parsed JSON result."""
    cmd = [sys.executable, os.path.join(TOOLS_DIR, "keyword_scanner.py"),
           "--doc", url, "--format", "json"]
    print(f"[topic_extractor] Scanning sub-pages: {url}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"[topic_extractor] Warning: keyword_scanner failed for {url}", file=sys.stderr)
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
            return {}
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"[topic_extractor] Warning: keyword_scanner timed out for {url}", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"[topic_extractor] Warning: could not parse keyword_scanner output: {e}", file=sys.stderr)
        return {}


def run_doc_extractor(urls: List[str], topic: str, output_path: str) -> bool:
    """Call doc_extractor.py with --urls (batch). Returns True on success."""
    urls_arg = ",".join(urls)
    cmd = [sys.executable, os.path.join(TOOLS_DIR, "doc_extractor.py"),
           "--urls", urls_arg,
           "--topic", topic,
           "--output", output_path]
    print(f"[topic_extractor] Extracting {len(urls)} URL(s) -> {output_path}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        # doc_extractor prints progress to stderr — forward it
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"  {line}")
        if result.returncode != 0:
            print(f"[topic_extractor] Error: doc_extractor exited with code {result.returncode}",
                  file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("[topic_extractor] Error: doc_extractor timed out.", file=sys.stderr)
        return False


def run_llm_summarizer(input_path: str, model: str, passes: int = 2) -> bool:
    """Call llm_summarizer.py to enhance a knowledge file. Returns True on success."""
    cmd = [sys.executable, os.path.join(TOOLS_DIR, "llm_summarizer.py"),
           "--input", input_path,
           "--model", model,
           "--passes", str(passes)]
    print(f"[topic_extractor] Enhancing with LLM ({model}, {passes} passes): {input_path}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"  {line}")
        if result.stdout:
            for line in result.stdout.strip().splitlines():
                print(f"  {line}")
        if result.returncode != 0:
            print(f"[topic_extractor] Warning: llm_summarizer exited with code {result.returncode}",
                  file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("[topic_extractor] Warning: llm_summarizer timed out.", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

def _find_knowledge_files(root_dir: str) -> List[str]:
    """Recursively find all .md files under root_dir."""
    md_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(".md"):
                md_files.append(os.path.join(dirpath, fname))
    return sorted(md_files)


def _parse_topic_from_path(file_path: str, root_dir: str) -> str:
    """Derive a topic slug from the file's path relative to root_dir."""
    rel = os.path.relpath(file_path, root_dir)
    parts = rel.replace("\\", "/").split("/")
    # knowledge/<topic>/<file>.md -> use directory name as topic
    if len(parts) >= 2:
        return parts[0]
    return os.path.splitext(parts[0])[0]


def _parse_graph_sections(content: str, rel_path: str) -> Tuple[List[str], List[Dict]]:
    """
    Parse concepts and edges from a knowledge .md file.

    Concepts come from:
      - ## Concepts (for graph)  bullet lines
      - ## Key Relationships     "X = Y + Z" or "X requires Y" style lines
      - ## Internal Composition  "X = Y + Z" style lines

    Edges come from:
      - ## Key Relationships     lines with relation keywords
      - ## Internal Composition  "X = Y + Z" -> edges with relation "built on" / "composed of"
    """
    nodes: List[str] = []
    edges: List[Dict] = []

    # Locate relevant sections
    sections: Dict[str, str] = {}
    section_re = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    matches = list(section_re.finditer(content))
    for idx, m in enumerate(matches):
        name = m.group(1).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        sections[name] = content[start:end]

    # --- Concepts (for graph) ---
    concepts_body = sections.get("Concepts (for graph)", "")
    for line in concepts_body.splitlines():
        line = line.strip().lstrip("-").strip()
        if line and len(line) < 80:
            nodes.append(line)

    # --- Internal Composition ---
    composition_body = sections.get("Internal Composition", "")
    eq_re = re.compile(r"[`'\"]?([A-Za-z][A-Za-z0-9_.]+)[`'\"]?\s*=\s*([A-Za-z].+)")
    for line in composition_body.splitlines():
        line = line.strip().lstrip("-").strip()
        m = eq_re.search(line)
        if m:
            lhs = m.group(1).strip()
            rhs_raw = m.group(2).strip()
            nodes.append(lhs)
            # Split rhs on "+" to find components
            parts = [p.strip().strip("`'\"") for p in re.split(r"\s*\+\s*", rhs_raw)]
            for part in parts:
                # Keep only the first token if it looks like an identifier
                first = re.match(r"([A-Za-z][A-Za-z0-9_.]+)", part)
                if first:
                    target = first.group(1)
                    nodes.append(target)
                    edges.append({
                        "from": lhs,
                        "to": target,
                        "relation": "composed of",
                        "source": rel_path,
                    })

    # --- Key Relationships ---
    rel_body = sections.get("Key Relationships", "")
    # Equivalences: "X = Y + Z"
    for line in rel_body.splitlines():
        line = line.strip().lstrip("-").strip()
        if not line:
            continue
        m = eq_re.search(line)
        if m:
            lhs = m.group(1).strip()
            rhs_raw = m.group(2).strip()
            nodes.append(lhs)
            parts = [p.strip().strip("`'\"") for p in re.split(r"\s*\+\s*", rhs_raw)]
            for part in parts:
                first = re.match(r"([A-Za-z][A-Za-z0-9_.]+)", part)
                if first:
                    target = first.group(1)
                    nodes.append(target)
                    edges.append({
                        "from": lhs,
                        "to": target,
                        "relation": "built on",
                        "source": rel_path,
                    })
            continue

        # Relation keywords: "X requires/extends/uses/depends on Y"
        rel_kw_re = re.compile(
            r"[`'\"]?([A-Z][A-Za-z0-9_.]+)[`'\"]?\s+"
            r"(requires?|extends?\s+with|extends?|uses?|wraps?|depends?\s+on|delegates?\s+to|"
            r"supersedes?|replaces?|builds?\s+on)\s+"
            r"[`'\"]?([A-Z][A-Za-z0-9_.]+)[`'\"]?",
            re.IGNORECASE,
        )
        m2 = rel_kw_re.search(line)
        if m2:
            src_node = m2.group(1)
            relation = re.sub(r"\s+", " ", m2.group(2)).strip().rstrip("s")
            tgt_node = m2.group(3)
            nodes.append(src_node)
            nodes.append(tgt_node)
            edges.append({
                "from": src_node,
                "to": tgt_node,
                "relation": relation,
                "source": rel_path,
            })

    return nodes, edges


def _yaml_str(value: str) -> str:
    """Wrap a string in double-quotes, escaping internal double-quotes."""
    return '"' + value.replace('"', '\\"') + '"'


def build_graph(knowledge_root: str) -> None:
    """
    Scan all knowledge .md files, extract concepts/relationships, write graph.yaml.
    graph.yaml is always rebuilt from scratch.
    """
    md_files = _find_knowledge_files(knowledge_root)
    if not md_files:
        print("[topic_extractor] No knowledge files found — graph not built.")
        return

    # node_name -> {topics: set, files: set}
    node_map: Dict[str, Dict] = {}
    all_edges: List[Dict] = []

    for file_path in md_files:
        rel_path = os.path.relpath(file_path, knowledge_root).replace("\\", "/")
        topic = _parse_topic_from_path(file_path, knowledge_root)
        try:
            with open(file_path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except OSError:
            continue

        concepts, edges = _parse_graph_sections(content, rel_path)
        all_edges.extend(edges)

        for concept in concepts:
            concept = concept.strip()
            if not concept or len(concept) > 100:
                continue
            if concept not in node_map:
                node_map[concept] = {"topics": set(), "files": set()}
            node_map[concept]["topics"].add(topic)
            node_map[concept]["files"].add(rel_path)

        # Also register edge endpoints as nodes
        for edge in edges:
            for key in ("from", "to"):
                name = edge[key]
                if name not in node_map:
                    node_map[name] = {"topics": set(), "files": set()}
                node_map[name]["topics"].add(topic)
                node_map[name]["files"].add(rel_path)

    # Deduplicate edges (same from/to/relation)
    seen_edges: set = set()
    unique_edges: List[Dict] = []
    for e in all_edges:
        key = (e["from"], e["to"], e["relation"])
        if key not in seen_edges:
            seen_edges.add(key)
            unique_edges.append(e)

    # Write YAML (manual, no PyYAML dependency)
    graph_path = os.path.join(knowledge_root, "graph.yaml")
    lines = ["nodes:"]
    for name in sorted(node_map):
        entry = node_map[name]
        topics_list = sorted(entry["topics"])
        files_list = sorted(entry["files"])
        lines.append(f"  - name: {_yaml_str(name)}")
        lines.append(f"    topics: [{', '.join(_yaml_str(t) for t in topics_list)}]")
        lines.append(f"    files: [{', '.join(_yaml_str(f) for f in files_list)}]")

    lines.append("")
    lines.append("edges:")
    for edge in unique_edges:
        lines.append(f"  - from: {_yaml_str(edge['from'])}")
        lines.append(f"    to: {_yaml_str(edge['to'])}")
        lines.append(f"    relation: {_yaml_str(edge['relation'])}")
        lines.append(f"    source: {_yaml_str(edge['source'])}")

    try:
        with open(graph_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"[topic_extractor] Graph written: {graph_path} "
              f"({len(node_map)} nodes, {len(unique_edges)} edges)")
    except OSError as e:
        print(f"[topic_extractor] Warning: could not write graph: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def collect_parent_urls(args: argparse.Namespace) -> List[str]:
    """Return the list of parent URLs from --url or --urls."""
    if args.urls:
        return [u.strip() for u in args.urls.split(",") if u.strip()]
    return [args.url.strip()]


def run(args: argparse.Namespace) -> int:
    parent_urls = collect_parent_urls(args)
    topic = args.topic
    output_dir = args.output.rstrip("/")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{topic}.md")

    # Infer knowledge root: parent of output_dir when output_dir looks like
    # knowledge/<topic>/. Fall back to output_dir itself.
    knowledge_root = os.path.dirname(output_dir) if os.path.dirname(output_dir) else output_dir

    # ------------------------------------------------------------------
    # Step 1: Scan sub-pages for every parent URL
    # ------------------------------------------------------------------
    sub_pages: List[Dict] = []

    if not args.no_subpages:
        for parent_url in parent_urls:
            scan_result = run_keyword_scanner(parent_url)
            found = scan_result.get("sub_pages", [])
            # Deduplicate across parents
            existing_urls = {sp["url"] for sp in sub_pages}
            for sp in found:
                if sp["url"] not in existing_urls:
                    sub_pages.append(sp)
                    existing_urls.add(sp["url"])

        if sub_pages:
            print(f"[topic_extractor] Found {len(sub_pages)} sub-page(s):")
            for sp in sub_pages:
                print(f"  - {sp['title']}: {sp['url']}")
        else:
            print("[topic_extractor] No sub-pages found — extracting parent URL(s) only.")
    else:
        print("[topic_extractor] --no-subpages set: skipping sub-page scan.")

    # ------------------------------------------------------------------
    # Step 2: Extract all URLs into one merged knowledge file
    # ------------------------------------------------------------------
    all_urls = parent_urls + [sp["url"] for sp in sub_pages]
    print(f"[topic_extractor] Total URLs to extract: {len(all_urls)}")

    ok = run_doc_extractor(all_urls, topic, output_file)
    if not ok:
        print(f"[topic_extractor] Extraction failed. Aborting.", file=sys.stderr)
        return 1

    print(f"[topic_extractor] Knowledge file written: {output_file}")

    # ------------------------------------------------------------------
    # Step 3: Optional LLM enhancement
    # ------------------------------------------------------------------
    if args.enhance:
        model = args.model or "qwen2.5:14b"
        ok = run_llm_summarizer(output_file, model, passes=2)
        if not ok:
            print("[topic_extractor] Warning: LLM enhancement failed — continuing without it.",
                  file=sys.stderr)

    # ------------------------------------------------------------------
    # Step 4: Build/update knowledge graph
    # ------------------------------------------------------------------
    build_graph(knowledge_root)

    print(f"[topic_extractor] Done. Topic '{topic}' ready at: {output_file}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="docwise topic extractor — orchestrates the full extraction pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic: extract topic with sub-pages
  python3 topic_extractor.py --url "https://developer.android.com/develop/ui/compose/state" \\
      --topic "compose-state" --output knowledge/compose-state/

  # With LLM enhancement
  python3 topic_extractor.py --url "https://developer.android.com/develop/ui/compose/state" \\
      --topic "compose-state" --output knowledge/compose-state/ \\
      --enhance --model qwen2.5:14b

  # Skip sub-page scan
  python3 topic_extractor.py --url "..." --topic "..." --output "..." --no-subpages

  # Multiple parent URLs
  python3 topic_extractor.py --urls "url1,url2,url3" --topic "..." --output "..."
        """,
    )

    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument("--url", help="Single parent documentation URL")
    url_group.add_argument("--urls", help="Comma-separated parent URLs for one topic")

    parser.add_argument("--topic", required=True,
                        help="Topic slug (e.g. compose-state, viewmodel)")
    parser.add_argument("--output", required=True,
                        help="Output directory (created if missing)")
    parser.add_argument("--no-subpages", action="store_true",
                        help="Skip sub-page discovery and extract only the given URL(s)")
    parser.add_argument("--enhance", action="store_true",
                        help="Enhance the knowledge file with a local LLM via Ollama")
    parser.add_argument("--model", default="qwen2.5:14b",
                        help="Ollama model name for --enhance (default: qwen2.5:14b)")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    sys.exit(run(args))


if __name__ == "__main__":
    main()
