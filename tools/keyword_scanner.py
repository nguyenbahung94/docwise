#!/usr/bin/env python3
"""
Keyword scanner for docwise plugin.
Fetches a doc page or scans a GitHub repo and extracts keywords + sub-pages.
Uses only Python stdlib — zero dependencies, zero LLM tokens.

Usage:
  python3 keyword_scanner.py --doc URL [--topic TOPIC]
  python3 keyword_scanner.py --repo owner/name [--topic TOPIC] [--paths '*.md,*.kt']
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class DocPageParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.base_parsed = urlparse(base_url)
        self.keywords = set()
        self.sub_pages = []
        self.headings = []
        self._tag_stack = []
        self._current_data = ""
        self._in_code = False
        self._in_heading = False
        self._current_heading_level = None
        self._in_nav = False
        self._in_link = False
        self._current_href = None
        self._link_text = ""
        self._seen_urls = set()
        self._heading_tags = {"h1", "h2", "h3", "h4"}
        self._nav_tags = {"nav", "aside"}
        self._code_tags = {"code", "pre"}

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self._tag_stack.append(tag)

        if tag in self._nav_tags:
            self._in_nav = True
        if tag in self._heading_tags:
            self._in_heading = True
            self._current_heading_level = tag
            self._current_data = ""
        if tag in self._code_tags:
            self._in_code = True
            self._current_data = ""
        if tag == "a":
            href = attrs_dict.get("href", "")
            if href and not href.startswith("#") and not href.startswith("javascript:"):
                self._in_link = True
                self._current_href = href
                self._link_text = ""
        if tag == "strong" or tag == "b":
            self._current_data = ""

    def handle_endtag(self, tag):
        if tag in self._heading_tags and self._in_heading:
            self._in_heading = False
            text = self._current_data.strip()
            if text:
                self.headings.append(text)
                self._extract_keywords_from_text(text)

        if tag in self._code_tags and self._in_code:
            self._in_code = False
            code_text = self._current_data.strip()
            if code_text:
                self._extract_keywords_from_code(code_text)

        if tag == "a" and self._in_link:
            self._in_link = False
            if self._current_href:
                self._process_link(self._current_href, self._link_text.strip())
            self._current_href = None
            self._link_text = ""

        if tag == "strong" or tag == "b":
            text = self._current_data.strip()
            if text and len(text.split()) <= 4:
                self._extract_keywords_from_text(text)

        if tag in self._nav_tags:
            self._in_nav = False

        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()

    def handle_data(self, data):
        if self._in_heading or self._in_code:
            self._current_data += data
        if self._in_link:
            self._link_text += data

    # Common English words that look like PascalCase but aren't useful keywords
    STOP_WORDS = {
        "The", "This", "That", "These", "Those", "What", "When", "Where", "Which",
        "Who", "How", "Why", "About", "After", "Before", "Between", "Does", "More",
        "Most", "Much", "Many", "Some", "Other", "Each", "Every", "Both", "Such",
        "Into", "Over", "Under", "Also", "Just", "Only", "Very", "Will", "Can",
        "May", "Must", "Should", "Could", "Would", "Shall", "Here", "There",
        "Then", "Than", "From", "With", "Your", "They", "Their", "Have", "Has",
        "Had", "Not", "But", "All", "Any", "Are", "Was", "Were", "Been", "Being",
        "For", "And", "Nor", "Yet", "Its", "Our", "His", "Her", "You", "Get",
        "Set", "Use", "New", "Old", "See", "Try", "Run", "Add", "Let", "Put",
        "End", "Out", "Top", "Low", "Big", "Max", "Min", "Key", "Yes", "No",
        "Now", "Way", "Day", "Own", "Two", "One", "API", "APIs", "Pro", "Via",
        "Android", "Google", "Kotlin", "Java", "Gradle", "Overview", "Documentation",
        "Guide", "Tutorial", "Example", "Examples", "Note", "Warning", "Important",
        "Tip", "Caution", "Reference", "Learn", "Read", "Write", "Save", "Load",
        "Create", "Update", "Delete", "Remove", "Start", "Stop", "Open", "Close",
        "Show", "Hide", "Enable", "Disable", "Check", "Test", "Build", "Deploy",
        "Install", "Configure", "Setup", "Download", "Upload", "Send", "Receive",
        "Choose", "Select", "Find", "Search", "Sort", "Filter", "Group", "Count",
        "Size", "Name", "Type", "Value", "Data", "List", "Item", "Content",
        "Page", "View", "Text", "Image", "Icon", "Button", "Label", "Title",
        "Header", "Footer", "Body", "Main", "Home", "Back", "Next", "Previous",
        "First", "Last", "Left", "Right", "Center", "Above", "Below",
        "Releases", "Release", "Version", "Versions", "Feature", "Features",
        "Support", "Devices", "Device", "System", "Systems", "Platform",
        "Discover", "Explore", "Browse", "Navigate", "Return", "Returns",
        "Defined", "Define", "Using", "Used", "Makes", "Made", "Provides",
        "Provided", "Requires", "Required", "Includes", "Included",
        "Background", "Foreground", "Asynchronous", "Synchronous",
        "Alternative", "Alternatives", "Terminology", "Tasks", "Task",
        "Stay", "Connected", "Downloads",
    }

    def _extract_keywords_from_text(self, text):
        # Extract PascalCase, camelCase, UPPER_CASE identifiers
        identifiers = re.findall(r'\b[A-Z][a-zA-Z0-9]+(?:\.[A-Z][a-zA-Z0-9]+)*\b', text)
        for ident in identifiers:
            if len(ident) > 3 and ident not in self.STOP_WORDS:
                self.keywords.add(ident)
        # Extract @Annotation style
        annotations = re.findall(r'@[A-Z][a-zA-Z0-9]+', text)
        for ann in annotations:
            self.keywords.add(ann)

    def _extract_keywords_from_code(self, code):
        # Class/interface/object declarations
        for pattern in [
            r'\b(?:class|interface|object|enum|annotation)\s+([A-Z][a-zA-Z0-9]+)',
            r'\b(?:fun|val|var)\s+([a-z][a-zA-Z0-9]{3,})',
            r'@([A-Z][a-zA-Z0-9]{2,})',
            r'\b([A-Z][a-zA-Z0-9]*(?:\.[A-Z][a-zA-Z0-9]+)+)',  # Qualified names
            r'\b(Dispatchers\.\w+)',
        ]:
            matches = re.findall(pattern, code)
            for m in matches:
                if len(m) > 3 and m not in self.STOP_WORDS:
                    self.keywords.add(m)

    def _process_link(self, href, text):
        full_url = urljoin(self.base_url, href)
        parsed = urlparse(full_url)

        # Strip fragment
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if clean_url.endswith("/"):
            clean_url = clean_url[:-1]

        # Same domain only
        if parsed.netloc != self.base_parsed.netloc:
            return
        # Skip self-links
        base_path = self.base_parsed.path.rstrip("/")
        link_path = parsed.path.rstrip("/")
        if link_path == base_path:
            return
        # Skip already seen
        if clean_url in self._seen_urls:
            return
        # Skip non-doc links (images, downloads, etc.)
        if re.search(r'\.(png|jpg|gif|svg|zip|pdf|apk)$', link_path):
            return

        self._seen_urls.add(clean_url)

        # Sub-pages: children of this page (url starts with base_path/)
        # Plus siblings that share the base name as prefix (e.g. state-hoisting is sibling of state)
        base_name = base_path.rsplit("/", 1)[-1]  # e.g. "state"
        parent_path = base_path.rsplit("/", 1)[0]  # e.g. "/develop/ui/compose"
        link_name = link_path.rsplit("/", 1)[-1] if "/" in link_path else ""

        is_child = link_path.startswith(base_path + "/")
        is_named_sibling = (
            link_path.startswith(parent_path + "/")
            and link_name.startswith(base_name + "-")
            and link_path.count("/") == base_path.count("/")
        )
        if (is_child or is_named_sibling) and text:
            self.sub_pages.append({"title": text, "url": clean_url})


def fetch_page(url):
    """Fetch page HTML content."""
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (docwise-scanner/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    })
    try:
        with urlopen(req, timeout=15) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except (HTTPError, URLError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


def suggest_topic(url, headings):
    """Suggest a topic name from the URL path."""
    path = urlparse(url).path.rstrip("/")
    # Take last 1-2 meaningful segments
    segments = [s for s in path.split("/") if s and s not in ("develop", "guide", "training", "topic", "topics", "android", "libraries", "architecture", "use-graph")]
    if segments:
        topic = "-".join(segments[-2:]) if len(segments) >= 2 else segments[-1]
        return re.sub(r'[^a-z0-9-]', '', topic.lower())
    return "unknown"


def scan_doc(url, topic=None):
    """Scan a documentation page."""
    html = fetch_page(url)
    parser = DocPageParser(url)
    parser.feed(html)

    suggested_topic = topic or suggest_topic(url, parser.headings)

    # If no code-level keywords found, extract topic terms from headings and sub-page titles
    if len(parser.keywords) < 5:
        all_titles = [re.sub(r'\s+', ' ', h).strip().split('\n')[0] for h in parser.headings]
        all_titles += [sp["title"] for sp in parser.sub_pages]
        for title in all_titles:
            # Skip question headings and generic sections
            if title.endswith("?") or len(title) > 60:
                continue
            words = title.split()
            # Only keep short, concept-like headings (1-4 words)
            if 1 <= len(words) <= 4:
                # Skip if all words are stop words
                non_stop = [w for w in words if w not in parser.STOP_WORDS]
                if non_stop:
                    parser.keywords.add(title)

    # Deduplicate and sort keywords
    keywords = sorted(parser.keywords, key=lambda k: (-len(k), k))[:30]

    # Deduplicate sub-pages by URL
    seen = set()
    unique_sub_pages = []
    for sp in parser.sub_pages:
        if sp["url"] not in seen:
            seen.add(sp["url"])
            unique_sub_pages.append(sp)

    return {
        "keywords": keywords,
        "topic": suggested_topic,
        "sub_pages": unique_sub_pages,
        "headings": parser.headings[:20],
    }


def scan_repo(repo, topic=None, paths=None):
    """Scan a GitHub repo."""
    if paths is None:
        paths = ["**/*.md", "**/*.kt", "**/build.gradle*"]

    repo_name = repo.split("/")[-1]
    tmp_dir = os.path.join(tempfile.gettempdir(), "docwise-scan", repo_name)

    try:
        # Clone shallow
        subprocess.run(
            ["git", "clone", "--depth", "1", f"https://github.com/{repo}.git", tmp_dir],
            capture_output=True, text=True, timeout=30
        )

        keywords = set()
        directories = []

        # List top-level dirs
        for entry in sorted(os.listdir(tmp_dir)):
            full = os.path.join(tmp_dir, entry)
            if os.path.isdir(full) and not entry.startswith("."):
                directories.append({"path": entry, "description": entry})

        # Scan README
        readme = os.path.join(tmp_dir, "README.md")
        if os.path.exists(readme):
            with open(readme) as f:
                content = f.read()
            headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
            for h in headings:
                identifiers = re.findall(r'\b[A-Z][a-zA-Z0-9]+\b', h)
                keywords.update(identifiers)

        # Scan kt files for class names
        for root, dirs, files in os.walk(tmp_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith(".kt"):
                    name = f.replace(".kt", "")
                    if name[0].isupper():
                        keywords.add(name)

        suggested_topic = topic or repo_name.lower()

        return {
            "keywords": sorted(keywords)[:30],
            "topic": suggested_topic,
            "directories": directories,
        }
    finally:
        subprocess.run(["rm", "-rf", tmp_dir], capture_output=True)


def main():
    parser = argparse.ArgumentParser(description="docwise keyword scanner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doc", help="URL of documentation page")
    group.add_argument("--repo", help="GitHub repo (owner/name)")
    parser.add_argument("--topic", help="Pre-assigned topic name")
    parser.add_argument("--paths", help="Comma-separated glob patterns (repo only)")
    parser.add_argument("--format", choices=["json", "yaml"], default="json")
    args = parser.parse_args()

    if args.doc:
        result = scan_doc(args.doc, args.topic)
    else:
        paths = args.paths.split(",") if args.paths else None
        result = scan_repo(args.repo, args.topic, paths)

    if args.format == "yaml":
        # Simple YAML output without PyYAML
        print(f"keywords: {json.dumps(result['keywords'])}")
        print(f"topic: \"{result['topic']}\"")
        if "sub_pages" in result:
            print("sub_pages:")
            for sp in result["sub_pages"]:
                print(f"  - title: \"{sp['title']}\"")
                print(f"    url: \"{sp['url']}\"")
        if "directories" in result:
            print("directories:")
            for d in result["directories"]:
                print(f"  - path: \"{d['path']}\"")
                print(f"    description: \"{d['description']}\"")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
