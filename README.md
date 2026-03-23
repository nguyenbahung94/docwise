# docwise

Claude Code plugin that gives AI up-to-date best practices from official docs, repos, and trusted sources — for any tech stack.

## The Problem

AI coding assistants use outdated patterns because their training data is frozen in time. You have to manually provide doc links to get correct, modern code.

## How docwise Solves It

1. **Add sources** — point docwise at official docs, GitHub repos, blog posts, or team conventions
2. **Extract** — AI reads each source and saves condensed rules with WHY annotations, before/after examples, and code snippets
3. **Verify** — community sources are automatically checked against official docs
4. **Code** — AI auto-loads relevant knowledge while you write code, using a concept graph to find related practices across topics
5. **Stay fresh** — smart TTL tracking per source type, never blocks your coding

## Quick Start

```bash
# Install
claude plugin add nguyenbahung94/docwise

# Pick your tech stack
/setup

# Start coding — AI automatically follows best practices
```

## Add Sources

```bash
# Official docs
/add-source --doc "https://developer.android.com/topic/architecture"

# Reference repos (extracts code patterns, not full files)
/add-source --repo "google/nowinandroid"

# Blog posts (verified against official docs before trusting)
/add-source --doc "https://medium.com/@someone/article" --priority community

# Your team's internal conventions
/add-source --doc "file:///path/to/team-rules.md" --priority team

# Generate knowledge
/generate
```

## Key Features

### Knowledge Graph
docwise doesn't just match keywords — it builds a concept graph that connects technologies across topics. Writing a ViewModel? It automatically pulls in related knowledge about StateFlow, UseCases, Hilt injection, and testing patterns.

### Per-Source Knowledge Files
Each source gets its own condensed file (~800 tokens). Adding or removing a source doesn't affect others. Knowledge files include:
- DO/DON'T rules with **WHY** they matter
- Before/After migration examples
- Code snippets from reference repos
- Decision tables (when to use X vs Y)

### Smart Freshness
Different sources update at different speeds. docwise tracks this:

| Source Type | Default TTL |
|---|---|
| Official docs | 30 days |
| Reference repos | 14 days |
| Team rules | 90 days |
| Blog posts | 90 days |

Stale knowledge is still used (never blocks coding) — you get a notification to run `/update` when ready.

### Source Verification
Community sources (blogs, Medium articles) are automatically compared against official documentation:
- Agrees with official → applied confidently
- Contradicts official → rejected with warning
- New info not in official → applied with "unverified" note

### Priority System
```
official > team > reference > community
```
When multiple sources cover the same topic, the AI loads the highest-priority files first (max 3 per task, ~2400 tokens).

### Best-Practice Linter
```bash
/check
```
Audits your current code against the knowledge base — shows what follows best practices and what doesn't, with line numbers and explanations.

## Starter Profiles

Pre-configured source lists for popular stacks:

| Profile | Sources |
|---|---|
| Android | Kotlin, Jetpack, nowinandroid |
| React | react.dev, Next.js |
| Python | typing, FastAPI, Django |
| iOS | SwiftUI, Combine |
| Custom | Empty — add your own |

## All Commands

| Command | Description |
|---|---|
| `/setup` | Pick a tech stack profile |
| `/add-source` | Register a doc URL, repo, or local file |
| `/list-sources` | Show sources with freshness and verification status |
| `/generate` | Extract best practices from sources |
| `/generate --source <url>` | Force re-extract one specific source |
| `/update` | Refresh stale sources past TTL |
| `/diff` | Show cached status of all sources |
| `/remove-source` | Remove a source |
| `/check` | Audit code against best practices |

## How It Works Under the Hood

```
/add-source → scans for keywords (cheap, ~1K tokens)
/generate   → extracts rules + concepts → builds knowledge graph
coding      → skill reads graph → traverses 2 hops → loads 3 best files → applies rules
/update     → checks TTL → re-fetches stale → re-extracts if changed → rebuilds graph
```

## Contributing

Add a starter profile for your tech stack:

1. Create `profiles/<stack>/sources.yaml` — list of doc URLs and repos
2. Create `profiles/<stack>/knowledge/` — pre-built knowledge files (optional)
3. Submit a PR

## License

MIT
