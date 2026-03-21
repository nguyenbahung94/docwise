# buildSkillDocs

A Claude Code plugin that gives AI up-to-date best-practice knowledge from official docs, GitHub repos, and trusted sources — for any tech stack.

## Problem

AI coding assistants use outdated patterns because their training data is frozen in time. You have to manually provide doc links to get correct code.

## Solution

buildSkillDocs indexes your documentation sources and delivers best-practice guidance while you code:

- **Per-source knowledge** — each source gets its own condensed file with rules, WHY annotations, and code examples
- **Priority-weighted** — official docs first, then team rules, then reference repos, then verified community
- **Smart freshness** — TTL-based staleness tracking, never blocks coding
- **Source verification** — community sources checked against official docs
- **Any tech stack** — configurable file triggers with starter profiles

## Quick Start

```bash
# Install
claude plugin add your-username/buildSkillDocs

# Pick your stack
/setup

# Start coding — AI automatically follows best practices
```

## Add More Sources

```bash
/add-source --doc "https://developer.android.com/topic/architecture"
/add-source --repo "google/nowinandroid"
/add-source --doc "https://medium.com/@someone/article" --priority community
/add-source --doc "file:///path/to/team-rules.md" --priority team
```

## Commands

| Command | Description |
|---|---|
| `/setup` | Pick a tech stack profile |
| `/add-source` | Register a doc URL or GitHub repo |
| `/list-sources` | Show all sources with freshness and verification |
| `/generate` | Force extract best practices from sources |
| `/update` | Refresh stale sources (past TTL) |
| `/diff` | Show cached source status |
| `/remove-source` | Remove a source |
| `/check` | Audit current code against best practices |

## How It Works

1. **Add sources** — official docs, repos, blogs
2. **Extract** — AI reads sources, saves condensed rules with WHY annotations
3. **Verify** — community sources checked against official docs
4. **Code** — AI auto-loads relevant rules while you work (max 3 files, ~2400 tokens)
5. **Stay fresh** — TTL tracks staleness, /update refreshes

See [Design Spec](docs/superpowers/specs/2026-03-21-buildSkillDocs-design.md) for full architecture.

## Contributing

Add a starter profile for your tech stack! Create a PR with:
- `profiles/<stack>/sources.yaml` — sources for the stack
- `profiles/<stack>/knowledge/` — pre-built knowledge files (optional)
