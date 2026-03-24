#!/usr/bin/env python3
"""
Rule extractor for docwise plugin.
Fetches a documentation page and extracts best-practice rules using regex.
Uses only Python stdlib — zero dependencies, zero LLM tokens.

Usage:
  python3 doc_extractor.py --url URL --topic TOPIC --priority PRIORITY --output PATH
  python3 doc_extractor.py --urls URL1,URL2 --topic TOPIC --priority PRIORITY --output PATH
"""

import argparse
import datetime
import html
import os
import re
import sys
from typing import Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_page(url: str) -> str:
    """Fetch a URL and return decoded HTML. Follows redirects automatically."""
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (docwise-extractor/1.0)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urlopen(req, timeout=15) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")
    except HTTPError as e:
        print(f"[doc_extractor] HTTP error fetching {url}: {e.code} {e.reason}", file=sys.stderr)
        return ""
    except URLError as e:
        print(f"[doc_extractor] URL error fetching {url}: {e.reason}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"[doc_extractor] Error fetching {url}: {e}", file=sys.stderr)
        return ""


# ---------------------------------------------------------------------------
# HTML cleaning helpers
# ---------------------------------------------------------------------------

# Tags whose entire content (including children) should be removed
_NOISE_TAGS = ["script", "style", "nav", "footer", "head", "noscript",
               "devsite-toc", "devsite-nav", "devsite-header", "devsite-footer"]


def strip_noise(raw_html: str) -> str:
    """Remove noisy block-level tags and their contents entirely."""
    for tag in _NOISE_TAGS:
        # Non-greedy removal of the whole element
        raw_html = re.sub(
            r"<" + tag + r"(?:\s[^>]*)?>.*?</" + tag + r">",
            " ", raw_html, flags=re.DOTALL | re.IGNORECASE,
        )
    return raw_html


def strip_tags(text: str) -> str:
    """Remove all HTML tags, unescape entities, normalise whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_inline(text: str) -> str:
    """Strip tags and unescape entities from a short inline snippet."""
    return strip_tags(text).strip()


def unescape_code(text: str) -> str:
    """Strip inner tags from a code block and unescape HTML entities."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return text.rstrip()


# ---------------------------------------------------------------------------
# Page title extraction
# ---------------------------------------------------------------------------

def extract_title(raw_html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    title = clean_inline(m.group(1))
    # Strip site suffix like " | Android Developers"
    title = re.split(r"\s*\|\s*|\s*-\s*Android", title)[0].strip()
    return title


# ---------------------------------------------------------------------------
# Block extraction via regex
# ---------------------------------------------------------------------------

def extract_headings(raw_html: str) -> List[Dict]:
    """Extract all h1-h6 tags → {type, level, text}."""
    blocks = []
    for m in re.finditer(r"<(h[1-6])[^>]*>(.*?)</h[1-6]>", raw_html, re.DOTALL | re.IGNORECASE):
        level = int(m.group(1)[1])
        text = clean_inline(m.group(2))
        if text:
            blocks.append({"type": "heading", "level": level, "text": text})
    return blocks


def extract_code_blocks(raw_html: str) -> List[Dict]:
    """Extract <pre> blocks, preferring Kotlin when tabs are labelled."""
    blocks = []
    for m in re.finditer(r"<pre[^>]*>(.*?)</pre>", raw_html, re.DOTALL | re.IGNORECASE):
        code = unescape_code(m.group(1)).strip()
        if len(code) < 10:
            continue
        # Detect language label from nearby data-label or class on a parent div/section
        # Search backwards ~500 chars for a data-label
        preceding = raw_html[max(0, m.start() - 500):m.start()]
        lang_label = ""
        lm = re.search(r'data-label=["\']([^"\']+)["\']', preceding)
        if lm:
            lang_label = lm.group(1).strip().lower()
        blocks.append({"type": "code", "text": code, "lang_label": lang_label})
    return blocks


def filter_kotlin_preferred(code_blocks: List[Dict]) -> List[Dict]:
    """
    When a sequence of code blocks has lang_labels like kotlin/java/groovy,
    keep only the Kotlin one. Unlabelled blocks are kept as-is.
    """
    result = []
    i = 0
    while i < len(code_blocks):
        block = code_blocks[i]
        label = block.get("lang_label", "")
        if label in ("kotlin", "java", "groovy", "kts"):
            # Collect the full group of language-labelled consecutive blocks
            group = [block]
            j = i + 1
            while j < len(code_blocks) and code_blocks[j].get("lang_label", "") in ("kotlin", "java", "groovy", "kts"):
                group.append(code_blocks[j])
                j += 1
            # Keep only Kotlin (or Kts) from the group; fall back to first if none
            kotlin_blocks = [b for b in group if b.get("lang_label", "") in ("kotlin", "kts")]
            result.extend(kotlin_blocks if kotlin_blocks else [group[0]])
            i = j
        else:
            result.append(block)
            i += 1
    return result


def extract_asides(raw_html: str) -> List[Dict]:
    """Extract <aside> warning/caution/note boxes."""
    blocks = []
    for m in re.finditer(r"<aside([^>]*)>(.*?)</aside>", raw_html, re.DOTALL | re.IGNORECASE):
        attrs = m.group(1)
        text = clean_inline(m.group(2))
        if not text:
            continue
        btype = "note"
        cls = (re.search(r'class=["\']([^"\']*)["\']', attrs) or re.Match)
        cls_val = ""
        cm = re.search(r'class=["\']([^"\']*)["\']', attrs)
        if cm:
            cls_val = cm.group(1).lower()
        if "warning" in cls_val or "important" in cls_val:
            btype = "warning"
        elif "caution" in cls_val:
            btype = "caution"
        elif "note" in cls_val or "tip" in cls_val:
            btype = "note"
        blocks.append({"type": btype, "text": text})
    return blocks


def extract_paragraphs(raw_html: str) -> List[Dict]:
    """Extract <p> tags."""
    blocks = []
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", raw_html, re.DOTALL | re.IGNORECASE):
        text = clean_inline(m.group(1))
        if len(text) > 20:
            blocks.append({"type": "paragraph", "text": text})
    return blocks


def extract_list_items(raw_html: str) -> List[Dict]:
    """Extract <li> tags."""
    blocks = []
    for m in re.finditer(r"<li[^>]*>(.*?)</li>", raw_html, re.DOTALL | re.IGNORECASE):
        text = clean_inline(m.group(1))
        if len(text) > 15:
            blocks.append({"type": "list_item", "text": text})
    return blocks


def extract_tables(raw_html: str) -> List[Dict]:
    """Extract <table> blocks → list of {type:'table', rows:[[cell,...]]}."""
    blocks = []
    for tm in re.finditer(r"<table[^>]*>(.*?)</table>", raw_html, re.DOTALL | re.IGNORECASE):
        table_html = tm.group(1)
        rows = []
        for rm in re.finditer(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL | re.IGNORECASE):
            row_html = rm.group(1)
            cells = []
            for cm in re.finditer(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, re.DOTALL | re.IGNORECASE):
                cells.append(clean_inline(cm.group(1)))
            if cells:
                rows.append(cells)
        if len(rows) >= 2:
            blocks.append({"type": "table", "rows": rows})
    return blocks


def extract_bold(raw_html: str) -> List[Dict]:
    """Extract <strong> and <b> tags as potential concepts."""
    blocks = []
    seen = set()
    for m in re.finditer(r"<(?:strong|b)>(.*?)</(?:strong|b)>", raw_html, re.DOTALL | re.IGNORECASE):
        text = clean_inline(m.group(1))
        words = text.split()
        if 1 <= len(words) <= 5 and text and text[0].isupper() and text not in seen:
            seen.add(text)
            blocks.append({"type": "bold", "text": text})
    return blocks


# ---------------------------------------------------------------------------
# Sequence-aware block list builder
# ---------------------------------------------------------------------------

def build_block_sequence(raw_html: str) -> List[Dict]:
    """
    Build an ordered flat list of blocks by scanning the HTML top-to-bottom.
    Each block: {type, text, level?, rows?, lang_label?}
    """
    # Strip noise sections first
    clean = strip_noise(raw_html)

    # We need position-aware extraction so we can interleave by source position.
    # Strategy: find each element by its start position, tag all with pos, then sort.
    tagged: List[Tuple[int, Dict]] = []

    # Headings
    for m in re.finditer(r"<(h[1-6])[^>]*>(.*?)</h[1-6]>", clean, re.DOTALL | re.IGNORECASE):
        level = int(m.group(1)[1])
        text = clean_inline(m.group(2))
        if text:
            tagged.append((m.start(), {"type": "heading", "level": level, "text": text}))

    # Asides
    for m in re.finditer(r"<aside([^>]*)>(.*?)</aside>", clean, re.DOTALL | re.IGNORECASE):
        attrs_str = m.group(1)
        text = clean_inline(m.group(2))
        if not text:
            continue
        btype = "note"
        cm2 = re.search(r'class=["\']([^"\']*)["\']', attrs_str)
        if cm2:
            cls_val = cm2.group(1).lower()
            if "warning" in cls_val or "important" in cls_val:
                btype = "warning"
            elif "caution" in cls_val:
                btype = "caution"
        tagged.append((m.start(), {"type": btype, "text": text}))

    # Tables — grab the whole table block
    for m in re.finditer(r"<table[^>]*>(.*?)</table>", clean, re.DOTALL | re.IGNORECASE):
        table_html = m.group(1)
        rows = []
        for rm in re.finditer(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL | re.IGNORECASE):
            cells = [clean_inline(cm3.group(1))
                     for cm3 in re.finditer(r"<t[dh][^>]*>(.*?)</t[dh]>", rm.group(1), re.DOTALL | re.IGNORECASE)]
            if cells:
                rows.append(cells)
        if len(rows) >= 2:
            tagged.append((m.start(), {"type": "table", "rows": rows}))

    # Code blocks — need lang_label from preceding context
    for m in re.finditer(r"<pre[^>]*>(.*?)</pre>", clean, re.DOTALL | re.IGNORECASE):
        code = unescape_code(m.group(1)).strip()
        if len(code) < 10:
            continue
        preceding = clean[max(0, m.start() - 600):m.start()]
        lang_label = ""
        lm = re.search(r'data-label=["\']([^"\']+)["\']', preceding)
        if lm:
            lang_label = lm.group(1).strip().lower()
        # Fallback: detect language from code content if no data-label
        if not lang_label:
            detected = detect_lang(code)
            if detected in ("kotlin", "java", "groovy"):
                lang_label = detected
        tagged.append((m.start(), {"type": "code", "text": code, "lang_label": lang_label}))

    # Paragraphs
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", clean, re.DOTALL | re.IGNORECASE):
        text = clean_inline(m.group(1))
        if len(text) > 20:
            tagged.append((m.start(), {"type": "paragraph", "text": text}))

    # List items
    for m in re.finditer(r"<li[^>]*>(.*?)</li>", clean, re.DOTALL | re.IGNORECASE):
        text = clean_inline(m.group(1))
        if len(text) > 15:
            tagged.append((m.start(), {"type": "list_item", "text": text}))

    # Bold phrases (potential concepts)
    seen_bold: set = set()
    for m in re.finditer(r"<(?:strong|b)>(.*?)</(?:strong|b)>", clean, re.DOTALL | re.IGNORECASE):
        text = clean_inline(m.group(1))
        words = text.split()
        if 1 <= len(words) <= 5 and text and text[0].isupper() and text not in seen_bold:
            seen_bold.add(text)
            tagged.append((m.start(), {"type": "bold", "text": text}))

    # Sort by document position
    tagged.sort(key=lambda x: x[0])
    blocks = [b for _, b in tagged]

    # Apply Kotlin preference to consecutive labelled code blocks
    blocks = _prefer_kotlin(blocks)

    # Final pass: remove any remaining Java/Groovy code blocks
    blocks = [b for b in blocks if not (
        b.get("type") == "code" and b.get("lang_label", "") in ("java", "groovy")
    )]

    return blocks


_LANG_TAB_HEADINGS = {"kotlin", "java", "groovy", "kts"}


def _is_lang_tab_heading(block: Dict) -> bool:
    """Return True if a heading block is just a language tab label (Kotlin/Java/Groovy/Kts)."""
    return (
        block.get("type") == "heading"
        and block.get("text", "").strip().lower() in _LANG_TAB_HEADINGS
    )


def _prefer_kotlin(blocks: List[Dict]) -> List[Dict]:
    """Remove Java/Groovy code blocks when a Kotlin equivalent is present in the same group.

    Groups are formed from consecutive code blocks where separating blocks are
    only language-tab headings (e.g. '### Kotlin', '### Java').  Those heading
    blocks are dropped entirely — they are tab labels, not real headings.

    Also filters out any remaining code blocks detected as Java/Groovy by content
    when a Kotlin block with the same heading name exists.
    """
    lang_labels = {"kotlin", "java", "groovy", "kts"}

    # Step 1: collapse heading-separated language groups into flat code-only groups.
    # Walk through all blocks; when we hit a code block with a lang_label (or a
    # lang-tab heading), collect a group until we reach something that is neither.
    result: List[Dict] = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        is_lang_code = block.get("type") == "code" and block.get("lang_label", "") in lang_labels
        is_lang_heading = _is_lang_tab_heading(block)

        if is_lang_code or is_lang_heading:
            # Collect the whole group (code blocks + intervening lang-tab headings)
            group_code: List[Dict] = []
            pending_lang = ""  # lang from a heading before a code block
            j = i
            while j < len(blocks):
                b = blocks[j]
                if _is_lang_tab_heading(b):
                    # Remember the language for the next code block
                    pending_lang = b.get("text", "").strip().lower()
                    j += 1
                elif b.get("type") == "code":
                    # Inherit lang from preceding heading if code has no label
                    if not b.get("lang_label") and pending_lang in lang_labels:
                        b["lang_label"] = pending_lang
                    if b.get("lang_label", "") in lang_labels:
                        group_code.append(b)
                        pending_lang = ""
                        j += 1
                    else:
                        break
                else:
                    break
            if group_code:
                kotlin_blocks = [b for b in group_code if b.get("lang_label", "") in ("kotlin", "kts")]
                result.extend(kotlin_blocks if kotlin_blocks else [group_code[0]])
            i = j
        else:
            result.append(block)
            i += 1
    return result


# ---------------------------------------------------------------------------
# Classification patterns
# ---------------------------------------------------------------------------

_RULE_PREFIXES = re.compile(
    r"^\s*(?:do\b|don'?t\b|avoid\b|never\b|always\b|must\b|should\s+not\b|use\b|prefer\b|recommend)",
    re.IGNORECASE,
)
_DONT_PREFIXES = re.compile(
    r"^\s*(?:don'?t\b|avoid\b|never\b|must\s+not\b|should\s+not\b|do\s+not\b)",
    re.IGNORECASE,
)
_DO_PREFIXES = re.compile(
    r"^\s*(?:do\b(?!\s+not)|always\b|must\b(?!\s+not)|use\b|prefer\b|recommend)",
    re.IGNORECASE,
)
_CAUTION_KW = re.compile(
    r"\b(avoid|never|don'?t|do\s+not|must\s+not|warning|caution|careful|dangerous|deprecated|pitfall|anti-pattern)\b",
    re.IGNORECASE,
)
_POSITIVE_KW = re.compile(
    r"\b(should|always|recommend|prefer|best\s+practice|correct|right\s+way)\b",
    re.IGNORECASE,
)

# Patterns that identify boilerplate/noise lines that should never appear as guidelines
_NOISE_GUIDELINES = re.compile(
    r"^(?:"
    r"android\s+developers"
    r"|content\s+and\s+code\s+samples"
    r"|content\s+license"
    r"|last\s+updated"
    r"|stay\s+organized\s+with\s+collections"
    r"|save\s+and\s+categorize\s+content"
    r")"
    r"|\d{4}-\d{2}-\d{2}\s+utc\.?"   # bare date lines
    r"|\bLast\s+updated\b"
    r"|\bContent\s+and\s+code\s+samples\s+on\s+this\s+page\b",
    re.IGNORECASE,
)

# Actionable words that make a guideline worth keeping
_ACTIONABLE_KW = re.compile(
    r"\b(should|must|recommend|ensure|avoid|always|never|prefer|use|don'?t|do\s+not|consider|make\s+sure)\b",
    re.IGNORECASE,
)

_WHY_PATTERN = re.compile(
    r"(?:because|since|this\s+(?:is\s+)?(?:ensures?|prevents?|avoids?|allows?)|so\s+that)\s+(.+?)(?:\.|$)",
    re.IGNORECASE,
)


def _extract_why(text: str) -> str:
    m = _WHY_PATTERN.search(text)
    if m:
        return m.group(1).strip().rstrip(".")[:200]
    return ""


def _is_meaningful(text: str) -> bool:
    if len(text.strip()) < 15:
        return False
    if re.match(r"^(home|back|next|previous|skip|more|less|show|hide)\b", text, re.IGNORECASE):
        return False
    return True


# ---------------------------------------------------------------------------
# Knowledge builder
# ---------------------------------------------------------------------------

class KnowledgeBuilder:
    def __init__(self, url: str, topic: str) -> None:
        self.url = url
        self.topic = topic
        self.rules: List[Dict] = []
        self.code_patterns: List[Dict] = []
        self.pitfalls: List[Dict] = []
        self.decision_tables: List[Dict] = []
        self.concepts: List[str] = []
        self.guidelines: List[str] = []
        self._seen: set = set()

    def _key(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()[:80])

    def add_rule(self, rule_type: str, text: str, why: str = "") -> None:
        text = text.strip()
        if not _is_meaningful(text):
            return
        k = self._key(text)
        if k in self._seen:
            return
        self._seen.add(k)
        self.rules.append({"type": rule_type, "text": text[:300], "why": why[:200]})

    def add_code(self, name: str, code: str) -> None:
        code = code.strip()
        if len(code) < 10:
            return
        # Use hash of full code to avoid dropping DO/DON'T pairs with same prefix
        import hashlib
        k = hashlib.md5(code.encode()).hexdigest()
        if k in self._seen:
            return
        self._seen.add(k)
        # Don't double-tag if process_blocks already tagged it
        pass
        self.code_patterns.append({"name": name[:80], "code": code})

    def add_pitfall(self, text: str, why: str = "") -> None:
        text = text.strip()
        if not _is_meaningful(text):
            return
        k = self._key(text)
        if k in self._seen:
            return
        self._seen.add(k)
        self.pitfalls.append({"text": text[:300], "why": why[:200]})

    def add_guideline(self, text: str) -> None:
        text = text.strip()
        if not _is_meaningful(text) or len(text) > 400:
            return
        if _NOISE_GUIDELINES.search(text):
            return
        if len(text) < 25 and not _ACTIONABLE_KW.search(text):
            return
        k = self._key(text)
        if k not in self._seen:
            self._seen.add(k)
            self.guidelines.append(text)

    # Exact strings that are not real concepts — just tab labels or UI noise
    _CONCEPT_BLOCKLIST: set = {
        "Kotlin", "Java", "Groovy", "Kts",
        "Caution", "Caution:", "Note", "Note:", "Warning", "Warning:",
        "Overview", "Example", "Examples",
    }

    # Common short English words that appear bold but carry no API meaning
    _COMMON_WORDS = re.compile(
        r"^(?:the|a|an|it|is|are|was|were|be|been|being|have|has|had|do|does|did"
        r"|will|would|could|should|may|might|can|shall|to|of|in|on|at|for|with|by"
        r"|and|or|not|no|yes|all|any|if|as|so|but|that|this|these|those|more|less"
        r"|some|each|every|other|also|only|just|very|well|new|old|good|bad|best"
        r"|right|left|top|bottom|first|last|next|prev|see|use|get|set|add|run"
        r"|open|close|start|stop|load|save|send|read|write|view|page|item|list"
        r"|type|name|value|data|state|time|date|key|id|url|app|code|file|test"
        r"|build|check|show|find|make|call|click|tap|update|change|help)$",
        re.IGNORECASE,
    )

    def add_concept(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        if len(text) < 3:
            return
        if text in self._CONCEPT_BLOCKLIST:
            return
        if "Stay organized" in text or "Save and categorize" in text:
            return
        # Single-word concepts: only keep PascalCase API names, not plain English words
        if " " not in text and not re.match(r"^[A-Z][a-z]+[A-Z]", text):
            if self._COMMON_WORDS.match(text):
                return
        if text not in self.concepts:
            self.concepts.append(text)

    def has_content(self) -> bool:
        return bool(self.rules or self.code_patterns or self.pitfalls or self.decision_tables or self.guidelines)

    def process_blocks(self, blocks: List[Dict]) -> None:
        last_heading = ""
        last_heading_level = 0

        for i, block in enumerate(blocks):
            btype = block["type"]
            text = block.get("text", "").strip()

            if btype == "heading":
                last_heading = text
                last_heading_level = block.get("level", 2)
                # Extract heading as a concept
                if last_heading_level <= 3 and text:
                    self.add_concept(text)
                continue

            if btype in ("warning", "caution"):
                why = _extract_why(text)
                self.add_pitfall(text, why)
                continue

            if btype == "note":
                if _CAUTION_KW.search(text):
                    self.add_pitfall(text, _extract_why(text))
                else:
                    self.add_guideline(text)
                continue

            if btype == "code":
                name = last_heading or "Code example"
                # Check heading OR code content for DON'T/DO tags
                is_dont = bool(
                    re.search(r"\bbefore\b|\bold\s+way\b|\bdon.?t\b", last_heading, re.IGNORECASE)
                    or re.search(r"//\s*DON[\u2019']?T\b|//\s*DO\s+NOT\b|//\s*AVOID\b|//\s*BAD\b|//\s*WRONG\b", text)
                )
                is_do = bool(
                    re.search(r"\bafter\b|\bnew\s+way\b|\bcorrect\b|\bdo\s+this\b", last_heading, re.IGNORECASE)
                    or re.search(r"//\s*DO\s+THIS\b|//\s*CORRECT\b|//\s*GOOD\b|//\s*RIGHT\b", text)
                )
                if is_dont:
                    self.add_code(f"[DON'T] {name}", text)
                elif is_do:
                    self.add_code(f"[DO] {name}", text)
                else:
                    self.add_code(name, text)
                continue

            if btype == "table":
                rows = block.get("rows", [])
                if len(rows) >= 2:
                    headers = rows[0]
                    data_rows = rows[1:]
                    if len(headers) >= 2:
                        entries = [r for r in data_rows if len(r) >= 2]
                        if entries:
                            self.decision_tables.append({
                                "question": last_heading or "Decision table",
                                "headers": headers,
                                "rows": entries,
                            })
                continue

            if btype in ("list_item", "paragraph"):
                if _DONT_PREFIXES.match(text):
                    self.add_rule("dont", text, _extract_why(text))
                elif _DO_PREFIXES.match(text):
                    self.add_rule("do", text, _extract_why(text))
                elif _CAUTION_KW.search(text) and btype == "list_item":
                    if re.search(r"\bpitfall|mistake|avoid|common\s+error\b", last_heading, re.IGNORECASE):
                        self.add_pitfall(text, _extract_why(text))
                    else:
                        self.add_rule("dont", text, _extract_why(text))
                elif _POSITIVE_KW.search(text) and btype == "list_item":
                    self.add_rule("do", text, _extract_why(text))
                else:
                    self.add_guideline(text)
                continue

            if btype == "bold":
                self.add_concept(text)
                continue


# ---------------------------------------------------------------------------
# Concept relationship extraction (heuristic)
# ---------------------------------------------------------------------------

_RELATION_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+(?:exposes?|returns?)\s+(?:state\s+(?:via|through|using))?\s*([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "exposes state via"),
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+(?:delegates?|passes?)\s+(?:logic\s+)?to\s+([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "delegates logic to"),
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+(?:persists?|stores?|saves?)\s+(?:data\s+)?(?:in|with|using)\s+([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "persists with"),
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+(?:replaces?|supersedes?)\s+([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "replaces"),
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+requires?\s+([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "requires"),
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+(?:extends?|inherits?\s+from)\s+([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "extends"),
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+implements?\s+([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "implements"),
    (re.compile(r"\b([A-Z][a-zA-Z0-9]+)\s+(?:uses?|wraps?)\s+([A-Z][a-zA-Z0-9]+)", re.IGNORECASE), "uses"),
]

_CONCEPT_STOP = {
    "The", "This", "That", "A", "An", "It", "If", "When", "Where",
    "Note", "See", "Also", "For", "You", "Use", "Not",
}


def extract_concept_relations(blocks: List[Dict]) -> List[str]:
    """Infer X → Y relationships from text blocks."""
    all_text = " ".join(b["text"] for b in blocks if b["type"] not in ("code",) and "text" in b)
    concepts = []
    seen: set = set()
    for pattern, relation in _RELATION_PATTERNS:
        for m in pattern.finditer(all_text):
            a, b = m.group(1), m.group(2)
            if a in _CONCEPT_STOP or b in _CONCEPT_STOP:
                continue
            if len(a) < 3 or len(b) < 3:
                continue
            key = f"{a}|{b}|{relation}"
            if key not in seen:
                seen.add(key)
                concepts.append(f"{a} → {b} ({relation})")
    return concepts[:12]


# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------

def detect_lang(code: str) -> str:
    # Kotlin checks first (most common in Android docs)
    if re.search(r"\bfun\s+\w+|val\s+\w+|var\s+\w+\s*=|\.collect\s*\{|coroutineScope|suspend\s+fun", code):
        return "kotlin"
    if re.search(r"import\s+androidx\.|import\s+android\.|import\s+kotlin\.|import\s+com\.", code):
        return "kotlin"
    if re.search(r"@Composable|@Inject|@Module|@Provides|@HiltViewModel", code):
        return "kotlin"
    # Kotlin-style dependencies block
    if re.search(r'implementation\s*\(', code):
        return "kotlin"
    # XML
    if re.search(r"<\w+[^>]*>.*</\w+>|android:|xmlns:", code, re.DOTALL):
        return "xml"
    # Java (after Kotlin to avoid false positives)
    if re.search(r"\bpublic\s+class\b|\bpublic\s+void\b|@Override|import\s+java\.", code):
        return "java"
    # Groovy-style dependencies
    if re.search(r"implementation\s+[\"']|dependencies\s*\{.*\n.*implementation\s+[\"']", code, re.DOTALL):
        return "groovy"
    return ""


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------

def render_knowledge_file(
    builder: "KnowledgeBuilder",
    title: str,
    urls: List[str],
    topic: str,
    priority: str,
    today: str,
    relation_concepts: List[str],
) -> str:
    lines: List[str] = []

    for u in urls:
        lines.append(f"<!-- Source: {u} -->")
    lines.append(f"<!-- Type: {priority} -->")
    lines.append(f"<!-- Priority: high -->")
    lines.append(f"<!-- Topic: {topic} -->")
    lines.append(f"<!-- Extracted: {today} -->")
    lines.append(f"<!-- Verified: — -->")
    lines.append("")

    clean_title = title or topic.replace("-", " ").title()
    lines.append(f"# {clean_title}")
    lines.append("")

    if builder.rules:
        lines.append("## Rules")
        for rule in builder.rules:
            prefix = "DO" if rule["type"] == "do" else "DON'T"
            lines.append(f"- {prefix}: {rule['text']}")
            if rule.get("why"):
                lines.append(f"  WHY: {rule['why']}")
        lines.append("")

    if builder.code_patterns:
        lines.append("## Code Patterns")
        for pat in builder.code_patterns:
            lines.append(f"### {pat['name']}")
            lang = detect_lang(pat["code"])
            lines.append(f"```{lang}")
            lines.append(pat["code"])
            lines.append("```")
            lines.append("")

    if builder.pitfalls:
        lines.append("## Pitfalls")
        for p in builder.pitfalls:
            lines.append(f"- {p['text']}")
            if p.get("why"):
                lines.append(f"  WHY: {p['why']}")
        lines.append("")

    if builder.decision_tables:
        lines.append("## Decision Tables")
        for dt in builder.decision_tables:
            lines.append(f"### {dt['question']}")
            headers = dt["headers"]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in dt["rows"]:
                padded = row + [""] * (len(headers) - len(row))
                lines.append("| " + " | ".join(padded[:len(headers)]) + " |")
            lines.append("")

    if builder.guidelines:
        lines.append("## Guidelines")
        actionable = [g for g in builder.guidelines if _ACTIONABLE_KW.search(g)]
        if actionable:
            selected_guidelines = actionable[:20]
        else:
            selected_guidelines = builder.guidelines[:15]
        for g in selected_guidelines:
            lines.append(f"- {g}")
        lines.append("")

    # Concepts: heading-derived + relation-derived, deduplicated
    all_concepts: List[str] = []
    seen_c: set = set()
    for c in (builder.concepts + relation_concepts):
        if c not in seen_c:
            seen_c.add(c)
            all_concepts.append(c)

    if all_concepts:
        lines.append("## Concepts (for graph)")
        for c in all_concepts[:12]:
            lines.append(f"- {c}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Per-URL processing
# ---------------------------------------------------------------------------

def process_url(url: str, topic: str) -> Tuple["KnowledgeBuilder", str, List[str]]:
    """Fetch, parse, and return (builder, page_title, relation_concepts)."""
    raw_html = fetch_page(url)
    if not raw_html:
        return KnowledgeBuilder(url, topic), "", []

    title = extract_title(raw_html)
    blocks = build_block_sequence(raw_html)

    builder = KnowledgeBuilder(url, topic)
    builder.process_blocks(blocks)

    # Fallback: if nothing structured was found, promote guidelines from headings+paragraphs
    if not builder.has_content():
        last_heading = ""
        for block in blocks:
            btype = block["type"]
            text = block.get("text", "").strip()
            if btype == "heading" and block.get("level", 99) <= 3:
                last_heading = text
            elif btype in ("paragraph", "list_item") and last_heading:
                builder.add_guideline(text)
            elif btype == "code":
                builder.add_code(last_heading or "Example", text)

    relation_concepts = extract_concept_relations(blocks)
    return builder, title, relation_concepts


# ---------------------------------------------------------------------------
# Multi-URL merger
# ---------------------------------------------------------------------------

def merge_builders(builders: List["KnowledgeBuilder"], topic: str) -> "KnowledgeBuilder":
    merged = KnowledgeBuilder("multi", topic)
    for b in builders:
        for rule in b.rules:
            merged.add_rule(rule["type"], rule["text"], rule.get("why", ""))
        for pat in b.code_patterns:
            merged.add_code(pat["name"], pat["code"])
        for p in b.pitfalls:
            merged.add_pitfall(p["text"], p.get("why", ""))
        for dt in b.decision_tables:
            key = dt["question"][:40]
            if not any(d["question"][:40] == key for d in merged.decision_tables):
                merged.decision_tables.append(dt)
        for g in b.guidelines:
            merged.add_guideline(g)
        for c in b.concepts:
            merged.add_concept(c)
    return merged


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="docwise doc extractor — extracts best-practice rules from documentation pages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 doc_extractor.py --url https://developer.android.com/topic/libraries/architecture/viewmodel \\
      --topic viewmodel --priority official --output knowledge/viewmodel/core.md

  python3 doc_extractor.py \\
      --urls https://developer.android.com/kotlin/flow,https://developer.android.com/kotlin/flow/stateflow-and-sharedflow \\
      --topic flow --priority official --output knowledge/flow/core.md
        """,
    )

    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument("--url", help="Single documentation URL to extract from")
    url_group.add_argument("--urls", help="Comma-separated list of URLs for batch extraction")

    parser.add_argument("--topic", required=True, help="Topic name (slug, e.g. viewmodel, flow, room)")
    parser.add_argument(
        "--priority",
        choices=["official", "team", "reference", "community"],
        default="official",
        help="Source priority (default: official)",
    )
    parser.add_argument("--output", required=True, help="Output file path (will be created)")

    args = parser.parse_args()

    if args.url:
        urls = [args.url.strip()]
    else:
        urls = [u.strip() for u in args.urls.split(",") if u.strip()]

    if not urls:
        print("[doc_extractor] No valid URLs provided.", file=sys.stderr)
        sys.exit(1)

    today = datetime.date.today().isoformat()

    all_builders: List[KnowledgeBuilder] = []
    all_titles: List[str] = []
    all_relations: List[str] = []

    for url in urls:
        print(f"[doc_extractor] Fetching: {url}", file=sys.stderr)
        b, title, relations = process_url(url, args.topic)
        all_builders.append(b)
        if title:
            all_titles.append(title)
        all_relations.extend(relations)

    merged = merge_builders(all_builders, args.topic)
    page_title = all_titles[0] if all_titles else args.topic.replace("-", " ").title()

    # Deduplicate relation concepts
    seen_r: set = set()
    unique_relations: List[str] = []
    for r in all_relations:
        if r not in seen_r:
            seen_r.add(r)
            unique_relations.append(r)

    output_text = render_knowledge_file(
        builder=merged,
        title=page_title,
        urls=urls,
        topic=args.topic,
        priority=args.priority,
        today=today,
        relation_concepts=unique_relations,
    )

    output_path = args.output
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"[doc_extractor] Written: {output_path}", file=sys.stderr)
    except OSError as e:
        print(f"[doc_extractor] Failed to write {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

    # Summary
    print(
        f"[doc_extractor] rules={len(merged.rules)} code={len(merged.code_patterns)} "
        f"pitfalls={len(merged.pitfalls)} tables={len(merged.decision_tables)} "
        f"guidelines={len(merged.guidelines)} concepts={len(merged.concepts)}",
        file=sys.stderr,
    )

    if not merged.has_content():
        print("[doc_extractor] WARNING: No structured content extracted. Output may be sparse.", file=sys.stderr)


if __name__ == "__main__":
    main()
