#!/usr/bin/env python3
"""
Repository scanner for docwise plugin.
Clones a GitHub repo and extracts reference examples (code patterns, conventions,
architecture) into a knowledge file compatible with the docwise pipeline.

Uses only Python stdlib — zero dependencies, zero LLM tokens.
Optionally enhances output with a local Ollama LLM (same as topic_extractor.py).

Usage:
  python3 repo_scanner.py --repo owner/name --topic TOPIC --output DIR/
  python3 repo_scanner.py --repo owner/name --topic TOPIC --output DIR/ --enhance --model qwen2.5:14b
  python3 repo_scanner.py --repo owner/name --topic TOPIC --output DIR/ --paths "*.kt,*.java"
"""

import argparse
import datetime
import fnmatch
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple


TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Architecture / pattern detection
# ---------------------------------------------------------------------------

# Layer keywords mapped to their canonical layer name (checked against dir path)
_LAYER_DIRS: List[Tuple[str, str]] = [
    ("domain",        "domain"),
    ("data",          "data"),
    ("presentation",  "presentation"),
    ("ui",            "ui"),
    ("core",          "core"),
    ("feature",       "feature"),
    ("common",        "common"),
    ("util",          "util"),
    ("di",            "di"),
    ("network",       "network"),
    ("database",      "database"),
    ("repository",    "repository"),
    ("usecase",       "usecase"),
    ("viewmodel",     "viewmodel"),
]

# Regex patterns that signal architectural significance inside a source file
_ARCH_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("Interface",           re.compile(r"\binterface\s+[A-Z][A-Za-z0-9]+")),
    ("AbstractClass",       re.compile(r"\babstract\s+class\s+[A-Z][A-Za-z0-9]+")),
    ("SealedClass",         re.compile(r"\bsealed\s+class\s+[A-Z][A-Za-z0-9]+")),
    ("UseCase",             re.compile(r"UseCase\b")),
    ("Repository",          re.compile(r"\bRepository\b")),
    ("ViewModel",           re.compile(r"\bViewModel\b|@HiltViewModel")),
    ("Composable",          re.compile(r"@Composable")),
    ("HiltModule",          re.compile(r"@Module|@InstallIn")),
    ("Inject",              re.compile(r"@Inject")),
    ("Entity",              re.compile(r"@Entity")),
    ("Dao",                 re.compile(r"@Dao")),
    ("Mapper",              re.compile(r"\bMapper\b|\bToDomain\b|\bToData\b")),
    ("Flow",                re.compile(r"\bFlow\b|\bStateFlow\b|\bSharedFlow\b")),
    ("Coroutines",          re.compile(r"\bsuspend\s+fun\b|\bcoroutineScope\b|\blaunch\b")),
]

# Docs / architecture files always included
_ALWAYS_INCLUDE = {"README.md", "ARCHITECTURE.md", "CONTRIBUTING.md",
                   "CHANGELOG.md", "BUILD.md", "MODULES.md"}

# File extensions we care about for source scanning
_SOURCE_EXTENSIONS = {".kt", ".java", ".gradle", ".kts", ".py", ".ts", ".tsx", ".js", ".jsx",
                      ".swift", ".dart", ".go", ".rs", ".cs"}

# Max lines to include per code snippet
_MAX_SNIPPET_LINES = 50

# Max number of source files to deep-analyse
_MAX_FILES = 30


# ---------------------------------------------------------------------------
# File collection
# ---------------------------------------------------------------------------

def collect_files(root: str, glob_patterns: Optional[List[str]] = None) -> List[str]:
    """
    Walk the repo and collect all files that match any of the glob patterns.
    If no patterns given, collect all source + doc files.
    Skips hidden directories and common non-source dirs.
    """
    skip_dirs = {".git", ".idea", ".gradle", "build", "__pycache__", "node_modules",
                 ".cache", "dist", "out", ".dart_tool", ".pub-cache"}

    all_files: List[str] = []
    for dirpath, dirs, files in os.walk(root):
        # Prune skipped directories in-place
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]

        for fname in files:
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, root)

            if glob_patterns:
                if not any(fnmatch.fnmatch(fname, pat) or fnmatch.fnmatch(rel, pat)
                           for pat in glob_patterns):
                    continue
            else:
                _, ext = os.path.splitext(fname)
                if ext not in _SOURCE_EXTENSIONS and fname not in _ALWAYS_INCLUDE:
                    continue

            all_files.append(full)

    return sorted(all_files)


# ---------------------------------------------------------------------------
# Import frequency scoring
# ---------------------------------------------------------------------------

def count_import_frequency(files: List[str], root: str) -> Dict[str, int]:
    """
    Count how many files import each other file.
    Returns {absolute_path: import_count}.
    Higher count = more important file.
    """
    # Build a map from filename stem -> full path (for simple name matching)
    stem_map: Dict[str, str] = {}
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        stem_map[stem] = f  # last-one-wins is fine for approximate ranking

    # Also build a map from relative package-style path (e.g. "com.example.Foo")
    import_counts: Dict[str, int] = defaultdict(int)

    import_re = re.compile(
        r"^\s*import\s+([\w.]+)",
        re.MULTILINE,
    )

    for src_file in files:
        try:
            content = _read_file_safe(src_file)
        except OSError:
            continue

        for m in import_re.finditer(content):
            imported = m.group(1)
            # Match against class name (last segment)
            class_name = imported.rsplit(".", 1)[-1]
            if class_name in stem_map:
                target = stem_map[class_name]
                if target != src_file:
                    import_counts[target] += 1

    return dict(import_counts)


# ---------------------------------------------------------------------------
# Pattern-based scoring
# ---------------------------------------------------------------------------

def score_file(path: str, content: str, import_count: int) -> Tuple[int, List[str]]:
    """
    Score a file by:
    - Import frequency (weight 3 per import)
    - Each matching architecture pattern (weight 2 per match)
    - Architecture layer directory match (weight 1 per layer dir in path)

    Returns (score, [matched_pattern_names]).
    """
    score = import_count * 3
    matched: List[str] = []

    for name, pattern in _ARCH_PATTERNS:
        if pattern.search(content):
            score += 2
            matched.append(name)

    lower_path = path.lower()
    for dir_key, layer_name in _LAYER_DIRS:
        if f"/{dir_key}/" in lower_path or lower_path.endswith(f"/{dir_key}"):
            score += 1

    return score, matched


# ---------------------------------------------------------------------------
# Signature extraction
# ---------------------------------------------------------------------------

_KT_CLASS_RE = re.compile(
    r"^(?:(?:public|internal|private|protected|abstract|sealed|data|open|enum|annotation)\s+)*"
    r"(?:class|interface|object|enum\s+class|sealed\s+class|data\s+class|annotation\s+class)\s+"
    r"([A-Z][A-Za-z0-9_]+)",
    re.MULTILINE,
)

_KT_FUN_RE = re.compile(
    r"^[ \t]*(?:(?:public|internal|private|protected|override|suspend|abstract|open|inline|"
    r"operator|infix|tailrec|external|actual|expect)\s+)*"
    r"fun\s+(?:<[^>]*>\s*)?([a-zA-Z][A-Za-z0-9_]+)\s*\(",
    re.MULTILINE,
)

_JAVA_CLASS_RE = re.compile(
    r"^(?:(?:public|protected|private|abstract|final|static)\s+)*"
    r"(?:class|interface|enum|@interface)\s+([A-Z][A-Za-z0-9_]+)",
    re.MULTILINE,
)

_JAVA_METHOD_RE = re.compile(
    r"^[ \t]*(?:(?:public|protected|private|abstract|final|static|synchronized|native|default|"
    r"override)\s+)*"
    r"(?:[A-Za-z<>\[\]]+\s+)+([a-z][A-Za-z0-9_]+)\s*\(",
    re.MULTILINE,
)


def extract_signatures(path: str, content: str) -> Dict:
    """
    Extract public class/interface names and their function signatures.
    Returns {"classes": [...], "functions": [...]}.
    """
    ext = os.path.splitext(path)[1].lower()
    classes: List[str] = []
    functions: List[str] = []

    if ext == ".kt":
        classes = [m.group(1) for m in _KT_CLASS_RE.finditer(content)]
        functions = [m.group(1) for m in _KT_FUN_RE.finditer(content)]
    elif ext == ".java":
        classes = [m.group(1) for m in _JAVA_CLASS_RE.finditer(content)]
        functions = [m.group(1) for m in _JAVA_METHOD_RE.finditer(content)]
    else:
        # Generic: pick capitalised identifiers after class/interface keywords
        classes = re.findall(r"\b(?:class|interface|struct|trait|object)\s+([A-Z][A-Za-z0-9_]+)", content)
        functions = re.findall(r"\b(?:fun|def|func|fn)\s+([a-z][A-Za-z0-9_]+)", content)

    # De-duplicate, preserve order
    seen: Set[str] = set()
    unique_classes: List[str] = []
    for c in classes:
        if c not in seen:
            seen.add(c)
            unique_classes.append(c)

    seen = set()
    unique_functions: List[str] = []
    for f in functions:
        if f not in seen:
            seen.add(f)
            unique_functions.append(f)

    return {"classes": unique_classes, "functions": unique_functions[:20]}


# ---------------------------------------------------------------------------
# Code snippet extraction
# ---------------------------------------------------------------------------

def extract_snippet(content: str, max_lines: int = _MAX_SNIPPET_LINES) -> str:
    """
    Extract the most representative portion of a file as a code snippet.
    Prefers the beginning of the file (imports + first class/function declarations).
    Trims to max_lines.
    """
    lines = content.splitlines()

    # Find first class/function declaration
    first_decl = 0
    for i, line in enumerate(lines):
        if re.match(r"^(?:class|interface|object|fun|def|func|public|abstract|sealed|data)", line.strip()):
            first_decl = max(0, i - 2)  # include a couple of lines above (annotations)
            break

    snippet_lines = lines[first_decl:first_decl + max_lines]
    return "\n".join(snippet_lines)


# ---------------------------------------------------------------------------
# Naming convention detection
# ---------------------------------------------------------------------------

def detect_naming_conventions(files: List[str], root: str) -> List[str]:
    """
    Infer naming conventions from file names and class names found in the repo.
    """
    conventions: List[str] = []

    # File-level: collect basename stems grouped by suffix
    suffix_groups: Dict[str, int] = defaultdict(int)
    for f in files:
        stem = os.path.splitext(os.path.basename(f))[0]
        # Extract trailing word (e.g. "FooUseCase" -> "UseCase")
        m = re.search(r"([A-Z][a-z]+(?:[A-Z][a-z]+)*)$", stem)
        if m:
            suffix_groups[m.group(1)] += 1

    # Report suffixes that appear more than once
    for suffix, count in sorted(suffix_groups.items(), key=lambda x: -x[1]):
        if count >= 2 and len(suffix) >= 4:
            # Find which layer they tend to live in
            layer_hits: Dict[str, int] = defaultdict(int)
            for f in files:
                if f.endswith(suffix + ".kt") or f.endswith(suffix + ".java"):
                    for _, layer_name in _LAYER_DIRS:
                        if f"/{layer_name}/" in f.lower():
                            layer_hits[layer_name] += 1
                            break
            if layer_hits:
                dominant_layer = max(layer_hits, key=lambda k: layer_hits[k])
                conventions.append(f'Files named `*{suffix}` live in `{dominant_layer}/` layer ({count} found)')
            else:
                conventions.append(f'Files named `*{suffix}` ({count} found)')

    # Interface naming
    kt_files = [f for f in files if f.endswith(".kt")]
    interfaces_in_domain = 0
    interfaces_total = 0
    for f in kt_files[:50]:
        try:
            content = _read_file_safe(f)
        except OSError:
            continue
        for m in re.finditer(r"\binterface\s+([A-Z][A-Za-z0-9]+)", content):
            interfaces_total += 1
            if "/domain/" in f.lower():
                interfaces_in_domain += 1

    if interfaces_total > 0 and interfaces_in_domain > interfaces_total * 0.5:
        conventions.append("Interfaces are predominantly defined in the `domain/` layer")

    # Impl naming
    impl_count = sum(
        1 for f in files
        if os.path.basename(f).endswith("Impl.kt") or os.path.basename(f).endswith("Impl.java")
    )
    if impl_count >= 2:
        conventions.append(f"Implementation classes use `*Impl` suffix ({impl_count} found)")

    return conventions[:12]


# ---------------------------------------------------------------------------
# Architecture detection
# ---------------------------------------------------------------------------

def detect_architecture(root: str, files: List[str]) -> Dict:
    """
    Detect module structure, layer pattern, and dependency direction from the file tree.
    """
    # Top-level directories (candidate modules)
    try:
        top_entries = sorted(os.listdir(root))
    except OSError:
        top_entries = []

    modules = [
        e for e in top_entries
        if os.path.isdir(os.path.join(root, e))
        and not e.startswith(".")
        and e not in {"build", "gradle", ".gradle", ".idea", "node_modules"}
    ]

    # Detect layers from directory names found across all file paths
    detected_layers: Set[str] = set()
    for f in files:
        rel = os.path.relpath(f, root).replace("\\", "/")
        parts = rel.split("/")
        for part in parts:
            for dir_key, layer_name in _LAYER_DIRS:
                if part.lower() == dir_key:
                    detected_layers.add(layer_name)

    # Infer dependency direction from import patterns
    # domain -> never imports data/presentation
    # data -> may import domain
    # presentation -> may import domain
    dep_clues: List[str] = []
    domain_files = [f for f in files if "/domain/" in f.lower()]
    data_files = [f for f in files if "/data/" in f.lower()]
    presentation_files = [f for f in files if "/presentation/" in f.lower() or "/ui/" in f.lower()]

    domain_imports_data = _any_file_imports_layer(domain_files, "data")
    domain_imports_presentation = _any_file_imports_layer(domain_files, "presentation")

    if domain_files:
        if not domain_imports_data and not domain_imports_presentation:
            dep_clues.append("domain → (nothing) — clean architecture boundary respected")
        else:
            dep_clues.append("domain layer has unexpected dependencies (boundary violation detected)")

    if data_files and _any_file_imports_layer(data_files, "domain"):
        dep_clues.append("data → domain (data implements domain interfaces)")

    if presentation_files and _any_file_imports_layer(presentation_files, "domain"):
        dep_clues.append("presentation → domain (presentation depends on domain only)")

    return {
        "modules": modules[:15],
        "layers": sorted(detected_layers),
        "dependency_direction": dep_clues if dep_clues else ["Could not determine — insufficient layer structure"],
    }


def _any_file_imports_layer(files: List[str], layer: str) -> bool:
    """Return True if any file in the list imports something from the given layer path."""
    import_re = re.compile(rf"\bimport\b.*\b{re.escape(layer)}\b", re.IGNORECASE)
    for f in files[:20]:
        try:
            content = _read_file_safe(f)
        except OSError:
            continue
        if import_re.search(content):
            return True
    return False


# ---------------------------------------------------------------------------
# Concept extraction
# ---------------------------------------------------------------------------

def extract_concepts(ranked_files: List[Tuple[str, int, List[str], Dict]]) -> List[str]:
    """
    Extract concept names (classes / interfaces) from the top-ranked files.
    Returns a deduplicated list of concept names suitable for the graph.
    """
    concepts: List[str] = []
    seen: Set[str] = set()

    for path, score, patterns, sigs in ranked_files:
        for cls in sigs.get("classes", []):
            if cls not in seen and len(cls) > 2:
                seen.add(cls)
                concepts.append(cls)

    return concepts[:20]


# ---------------------------------------------------------------------------
# Key API extraction
# ---------------------------------------------------------------------------

def extract_key_apis(ranked_files: List[Tuple[str, int, List[str], Dict]], root: str) -> List[str]:
    """
    Build a bullet list of public interfaces/classes with their key methods.
    """
    apis: List[str] = []
    for path, score, patterns, sigs in ranked_files[:15]:
        classes = sigs.get("classes", [])
        functions = sigs.get("functions", [])
        if not classes:
            continue
        rel = os.path.relpath(path, root).replace("\\", "/")
        for cls in classes[:3]:
            methods = [f for f in functions if f != cls][:5]
            if methods:
                method_str = ", ".join(f"`{m}()`" for m in methods)
                apis.append(f"`{cls}` ({rel}): {method_str}")
            else:
                apis.append(f"`{cls}` ({rel})")

    return apis[:20]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read_file_safe(path: str, max_bytes: int = 200_000) -> str:
    """Read a file, skipping binary files and capping size."""
    with open(path, "rb") as fh:
        raw = fh.read(max_bytes)
    # Heuristic: if more than 10% of bytes are non-text, treat as binary
    non_text = sum(1 for b in raw[:1000] if b > 127 or (b < 32 and b not in (9, 10, 13)))
    if non_text > 100:
        return ""
    return raw.decode("utf-8", errors="replace")


def _detect_lang_from_path(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return {
        ".kt": "kotlin", ".kts": "kotlin",
        ".java": "java",
        ".gradle": "groovy",
        ".py": "python",
        ".ts": "typescript", ".tsx": "typescript",
        ".js": "javascript", ".jsx": "javascript",
        ".swift": "swift",
        ".dart": "dart",
        ".go": "go",
        ".rs": "rust",
        ".cs": "csharp",
    }.get(ext, "")


# ---------------------------------------------------------------------------
# Clone
# ---------------------------------------------------------------------------

def clone_repo(repo: str, tmp_dir: str) -> bool:
    """Clone a GitHub repo shallowly into tmp_dir. Returns True on success."""
    url = f"https://github.com/{repo}.git"
    print(f"[repo_scanner] Cloning {url} ...")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", url, tmp_dir],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(f"[repo_scanner] Clone failed:\n{result.stderr.strip()}", file=sys.stderr)
        return False
    print(f"[repo_scanner] Clone complete: {tmp_dir}")
    return True


# ---------------------------------------------------------------------------
# Knowledge file renderer
# ---------------------------------------------------------------------------

def render_knowledge_file(
    repo: str,
    topic: str,
    today: str,
    arch: Dict,
    naming_conventions: List[str],
    ranked_files: List[Tuple[str, int, List[str], Dict]],
    key_apis: List[str],
    concepts: List[str],
    root: str,
) -> str:
    repo_name = repo.split("/")[-1]
    lines: List[str] = []

    # Header (matches doc_extractor.py format)
    lines.append(f"<!-- Source: https://github.com/{repo} -->")
    lines.append(f"<!-- Type: reference -->")
    lines.append(f"<!-- Priority: reference -->")
    lines.append(f"<!-- Topic: {topic} -->")
    lines.append(f"<!-- Extracted: {today} -->")
    lines.append(f"<!-- Verified: — -->")
    lines.append("")

    lines.append(f"# {topic.replace('-', ' ').title()} (Reference: {repo_name})")
    lines.append("")

    # Architecture section
    lines.append("## Architecture")
    if arch["modules"]:
        lines.append(f"- Module structure: {', '.join(f'`{m}`' for m in arch['modules'])}")
    if arch["layers"]:
        lines.append(f"- Layer pattern: {', '.join(f'`{l}`' for l in arch['layers'])}")
    for dep in arch["dependency_direction"]:
        lines.append(f"- Dependency direction: {dep}")
    lines.append("")

    # Naming conventions
    if naming_conventions:
        lines.append("## Naming Conventions")
        for conv in naming_conventions:
            lines.append(f"- {conv}")
        lines.append("")

    # Code patterns from top-ranked files
    code_pattern_entries: List[Tuple[str, str, str]] = []
    for path, score, patterns, sigs in ranked_files:
        if not patterns:
            continue
        try:
            content = _read_file_safe(path)
        except OSError:
            continue
        snippet = extract_snippet(content)
        if not snippet.strip():
            continue
        rel = os.path.relpath(path, root).replace("\\", "/")
        label = ", ".join(patterns[:3])
        lang = _detect_lang_from_path(path)
        code_pattern_entries.append((f"{label} ({rel})", snippet, lang))

    if code_pattern_entries:
        lines.append("## Code Patterns")
        for name, snippet, lang in code_pattern_entries[:10]:
            lines.append(f"### {name}")
            lines.append(f"```{lang}")
            lines.append(snippet)
            lines.append("```")
            lines.append("")

    # Key APIs
    if key_apis:
        lines.append("## Key APIs")
        for api in key_apis:
            lines.append(f"- {api}")
        lines.append("")

    # Concepts (for graph)
    if concepts:
        lines.append("## Concepts (for graph)")
        for c in concepts:
            lines.append(f"- {c}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM enhancement
# ---------------------------------------------------------------------------

def run_llm_summarizer(input_path: str, model: str, passes: int = 2) -> bool:
    """Call llm_summarizer.py to enhance the knowledge file. Returns True on success."""
    summarizer = os.path.join(TOOLS_DIR, "llm_summarizer.py")
    if not os.path.exists(summarizer):
        print("[repo_scanner] Warning: llm_summarizer.py not found — skipping enhancement.",
              file=sys.stderr)
        return False

    cmd = [sys.executable, summarizer,
           "--input", input_path,
           "--model", model,
           "--passes", str(passes)]
    print(f"[repo_scanner] Enhancing with LLM ({model}, {passes} passes): {input_path}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"  {line}")
        if result.stdout:
            for line in result.stdout.strip().splitlines():
                print(f"  {line}")
        if result.returncode != 0:
            print(f"[repo_scanner] Warning: llm_summarizer exited with code {result.returncode}",
                  file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("[repo_scanner] Warning: llm_summarizer timed out.", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(args: argparse.Namespace) -> int:
    repo = args.repo.strip()
    topic = args.topic.strip()
    output_dir = args.output.rstrip("/")
    today = datetime.date.today().isoformat()

    # Parse --paths glob patterns
    glob_patterns: Optional[List[str]] = None
    if args.paths:
        glob_patterns = [p.strip() for p in args.paths.split(",") if p.strip()]

    # Prepare output
    os.makedirs(output_dir, exist_ok=True)
    repo_name = repo.split("/")[-1]
    output_file = os.path.join(output_dir, f"{repo_name}-reference.md")

    # Create temp directory
    tmp_base = tempfile.mkdtemp(prefix="docwise-repo-")
    tmp_dir = os.path.join(tmp_base, repo_name)

    try:
        # Step 1 — Clone
        if not clone_repo(repo, tmp_dir):
            return 1

        # Step 2 — Collect files
        print("[repo_scanner] Scanning file structure ...")
        all_files = collect_files(tmp_dir, glob_patterns)
        print(f"[repo_scanner] Found {len(all_files)} candidate files")

        # Always include doc files from root
        doc_files_root: List[str] = []
        for fname in _ALWAYS_INCLUDE:
            candidate = os.path.join(tmp_dir, fname)
            if os.path.exists(candidate) and candidate not in all_files:
                doc_files_root.append(candidate)
        all_files = doc_files_root + all_files

        # Step 3 — Import frequency analysis
        print("[repo_scanner] Analysing import frequency ...")
        import_counts = count_import_frequency(all_files, tmp_dir)

        # Step 4 — Score and rank files
        print("[repo_scanner] Ranking files by importance ...")
        scored: List[Tuple[int, str, List[str]]] = []
        for path in all_files:
            try:
                content = _read_file_safe(path)
            except OSError:
                continue
            if not content:
                continue
            imp_count = import_counts.get(path, 0)
            score, patterns = score_file(path, content, imp_count)
            scored.append((score, path, patterns))

        # Sort descending by score
        scored.sort(key=lambda x: -x[0])

        # Take top _MAX_FILES but always include the always-include docs
        top_scored = scored[:_MAX_FILES]

        # Build ranked list with signatures
        ranked_files: List[Tuple[str, int, List[str], Dict]] = []
        for score, path, patterns in top_scored:
            try:
                content = _read_file_safe(path)
            except OSError:
                content = ""
            sigs = extract_signatures(path, content) if content else {"classes": [], "functions": []}
            ranked_files.append((path, score, patterns, sigs))

        print(f"[repo_scanner] Top {len(ranked_files)} files selected for extraction")

        # Step 5 — Architecture detection
        print("[repo_scanner] Detecting architecture ...")
        arch = detect_architecture(tmp_dir, all_files)

        # Step 6 — Naming conventions
        print("[repo_scanner] Detecting naming conventions ...")
        naming_conventions = detect_naming_conventions(all_files, tmp_dir)

        # Step 7 — Key APIs and concepts
        key_apis = extract_key_apis(ranked_files, tmp_dir)
        concepts = extract_concepts(ranked_files)

        # Step 8 — Render knowledge file
        print("[repo_scanner] Rendering knowledge file ...")
        content_out = render_knowledge_file(
            repo=repo,
            topic=topic,
            today=today,
            arch=arch,
            naming_conventions=naming_conventions,
            ranked_files=ranked_files,
            key_apis=key_apis,
            concepts=concepts,
            root=tmp_dir,
        )

        # Write output
        with open(output_file, "w", encoding="utf-8") as fh:
            fh.write(content_out)

        print(f"[repo_scanner] Knowledge file written: {output_file}")

    finally:
        # Step 9 — Clean up temp directory
        print("[repo_scanner] Cleaning up temp directory ...")
        subprocess.run(["rm", "-rf", tmp_base], capture_output=True)

    # Step 10 — Optional LLM enhancement
    if args.enhance:
        model = args.model or "qwen2.5:14b"
        ok = run_llm_summarizer(output_file, model, passes=2)
        if not ok:
            print("[repo_scanner] Warning: LLM enhancement failed — continuing without it.",
                  file=sys.stderr)

    print(f"[repo_scanner] Done. Reference knowledge ready at: {output_file}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="docwise repo scanner — extracts reference knowledge from a GitHub repository.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic scan
  python3 repo_scanner.py --repo android/architecture-samples \\
      --topic "android-architecture" --output knowledge/android-architecture/

  # Scan only Kotlin and Java files
  python3 repo_scanner.py --repo android/architecture-samples \\
      --topic "android-architecture" --output knowledge/android-architecture/ \\
      --paths "*.kt,*.java"

  # With LLM enhancement
  python3 repo_scanner.py --repo android/architecture-samples \\
      --topic "android-architecture" --output knowledge/android-architecture/ \\
      --enhance --model qwen2.5:14b
        """,
    )
    parser.add_argument("--repo", required=True,
                        help="GitHub repository in owner/name format (e.g. android/architecture-samples)")
    parser.add_argument("--topic", required=True,
                        help="Topic slug for the knowledge file (e.g. android-architecture)")
    parser.add_argument("--output", required=True,
                        help="Output directory (created if it does not exist)")
    parser.add_argument("--paths",
                        help="Comma-separated glob patterns to restrict scanned files "
                             "(e.g. '*.kt,*.java'). Defaults to all source + doc files.")
    parser.add_argument("--enhance", action="store_true",
                        help="Enhance the output knowledge file with a local LLM via Ollama")
    parser.add_argument("--model", default="qwen2.5:14b",
                        help="Ollama model name for --enhance (default: qwen2.5:14b)")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    # Basic validation
    if "/" not in args.repo:
        print(f"[repo_scanner] Error: --repo must be in 'owner/name' format, got: {args.repo!r}",
              file=sys.stderr)
        sys.exit(1)

    sys.exit(run(args))


if __name__ == "__main__":
    main()
