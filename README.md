# docwise

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-orange.svg)](https://claude.com/claude-code)

> Claude Code plugin that gives AI up-to-date best practices from official docs, repos, and trusted sources — for any tech stack.

## Without docwise vs With docwise

```
Without docwise:
  You: "Create a ViewModel for the profile screen"
  AI: Creates ViewModel with LiveData, no UseCase, business logic in ViewModel
  You: "No, use StateFlow... and inject UseCase... and follow the architecture guide..."
  AI: "Oh, sorry. Let me redo that."

With docwise:
  You: "Create a ViewModel for the profile screen"
  AI: (silently loads best practices from official docs + reference repos)
      Creates ViewModel with StateFlow<UiState>, injects UseCase via Hilt,
      uses stateIn with WhileSubscribed(5_000), sealed interface for state.
  You: ship it.
```

## Requirements

- [Claude Code](https://claude.com/claude-code) CLI installed and configured

## Quick Start

```bash
# Install the plugin
claude plugin add nguyenbahung94/docwise

# Pick your tech stack
/setup

# Start coding — AI automatically follows best practices
```

That's it. The AI now references best practices while you code.

## How It Works

```
/add-source → scans for keywords (cheap, ~1K tokens per source)
/generate   → extracts rules + concepts → builds knowledge graph
coding      → skill reads graph → traverses connections → loads best files → applies rules
/update     → checks TTL → re-fetches stale → re-extracts if changed → rebuilds graph
```

1. **Add sources** — point docwise at official docs, GitHub repos, blog posts, or your team's conventions
2. **Extract** — AI reads each source, saves condensed rules with WHY annotations, before/after examples, and code snippets
3. **Verify** — community sources are automatically checked against official docs before trusting
4. **Code** — AI auto-loads relevant knowledge while you write, using a concept graph to find related practices across topics
5. **Stay fresh** — smart TTL tracking per source type, never blocks your coding

## Add Sources

```bash
# Official documentation
/add-source --doc "https://developer.android.com/topic/architecture"

# Reference repos — extracts code patterns and snippets, not full files
/add-source --repo "google/nowinandroid"

# Blog posts — automatically verified against official docs before trusting
/add-source --doc "https://medium.com/@someone/viewmodel-patterns" --priority community

# Your team's internal conventions (local file)
/add-source --doc "file:///Users/you/team-conventions.md" --priority team

# Extract knowledge from all added sources
/generate
```

> **Note:** The `file://` prefix followed by the absolute path lets you add local markdown files as team knowledge sources.

## Key Features

### Knowledge Graph

docwise doesn't just match keywords — it builds a **concept graph** that connects technologies across topics.

Writing a ViewModel? It automatically traverses the graph and pulls in related knowledge about StateFlow, UseCases, Hilt injection, and testing patterns — even though those live in different topic files.

### Per-Source Knowledge Files

Each source gets its own condensed file (~800 tokens). Adding or removing a source doesn't affect others. Each file includes:

- **DO/DON'T rules** with WHY they matter and when exceptions apply
- **Before/After examples** showing migration from old to new patterns
- **Code snippets** from reference repos showing real implementations
- **Decision tables** for choosing between approaches (when to use X vs Y)
- **Version info** for current recommended library versions

### Source Verification

Community sources (blogs, Medium articles) can contain wrong advice. docwise verifies them automatically:

| Result | What happens |
|---|---|
| Agrees with official docs | Applied confidently |
| Contradicts official docs | Rejected — warns you if your code follows the bad advice |
| New info not in official docs | Applied with "unverified" note so you know the source |

Official, team, and reference sources are trusted by default.

### Priority System

```
official > team > reference > community
```

When multiple sources cover the same topic, AI loads the highest-priority files first. Max 3 files per task (~2400 tokens total).

| Priority | What it is | Default TTL | Trusted? |
|---|---|---|---|
| **official** | Official docs (developer.android.com, react.dev) | 30 days | Yes |
| **team** | Your company's internal rules | 90 days | Yes |
| **reference** | Reference repos (nowinandroid, Next.js examples) | 14 days | Yes |
| **community** | Blogs, Medium, third-party | 90 days | Verified first |

### Smart Freshness

Different sources change at different speeds. docwise tracks TTL per source and never blocks your coding:

- **Within TTL** — knowledge used as-is, no network calls
- **Past TTL** — knowledge still used (never blocks), you get a notification:
  ```
  docwise: 2 sources for 'architecture' are stale. Run /update to refresh.
  ```
- **`/update`** — re-fetches stale sources, re-extracts only if content actually changed

### Best-Practice Linter

```bash
/check
```

Audits your current code against the knowledge base:

```
Checking: ProfileViewModel.kt

  Line 15: Uses LiveData — recommended: StateFlow
    Source: architecture/core.md (official)
    WHY: StateFlow integrates with coroutines, survives config changes

  Line 23: Business logic in ViewModel — move to UseCase
    Source: architecture/core.md (official)
    WHY: ViewModel should only map UI state, not contain business rules

  Line 8: Correct Hilt injection pattern
  Line 30: StateFlow with WhileSubscribed — matches best practice

Score: 2/4 practices followed
```

## Starter Profiles

Pre-configured source lists so you don't start from scratch:

| Profile | What's included | Sources |
|---|---|---|
| **Android** | Kotlin, Jetpack, Architecture, Room, Navigation, Hilt, nowinandroid | 7 sources |
| **React** | React fundamentals, Hooks, Next.js App Router | 3 sources |
| **Python** | Typing, FastAPI, Django | 3 sources |
| **iOS** | SwiftUI, Combine | 2 sources |
| **Custom** | Empty — add your own sources for any stack | 0 sources |

You can always add more sources on top of any profile with `/add-source`.

## All Commands

| Command | What it does |
|---|---|
| `/setup` | Pick a tech stack profile (first-time setup) |
| `/add-source` | Register a doc URL, GitHub repo, or local file |
| `/list-sources` | Show all sources with freshness and verification status |
| `/generate` | Extract best practices from new/changed sources |
| `/generate --all` | Force re-extract all sources |
| `/generate --topic <name>` | Extract sources for one topic only |
| `/generate --source <url>` | Force re-extract one specific source |
| `/generate --dry-run` | Preview what would be extracted (no cost) |
| `/update` | Refresh stale sources (past TTL) |
| `/update --force` | Check all sources regardless of TTL |
| `/diff` | Show cached status of all sources |
| `/remove-source <url>` | Remove a source and its knowledge file |
| `/check` | Audit current code against best practices |

## Contributing

Add a starter profile for your tech stack:

1. Fork the repo
2. Create `profiles/<stack>/sources.yaml` with doc URLs and repos for the stack
3. Optionally add `profiles/<stack>/knowledge/` with pre-built knowledge files
4. Submit a PR

See the [Design Spec](docs/superpowers/specs/2026-03-21-docwise-design.md) for architecture details.

## License

MIT
