# buildSkillDocs

A Claude Code plugin that indexes official documentation and GitHub repos, then provides AI with up-to-date best-practice guidance while coding.

## Problem

AI coding assistants use outdated patterns because their training data is frozen in time. You have to manually provide doc links to get correct code.

## Solution

buildSkillDocs solves this with a two-tier approach:
1. **Cheap indexing** — scans sources for keywords (Tier 1, ~1K tokens per source)
2. **On-demand extraction** — extracts full rules only when AI needs them (Tier 2, cached after first use)

## Quick Start

### Install
```bash
claude plugin add buildSkillDocs
```

### Add sources
```bash
/add-source --doc "https://developer.android.com/topic/architecture"
/add-source --repo "google/nowinandroid"
```

### Start coding
The plugin auto-triggers when you write code. It matches keywords from your code against the index and provides best-practice guidance.

### Pre-build for your team (optional)
```bash
/generate          # Extract all sources
git commit + push  # Team gets pre-built knowledge
```

## Commands

| Command | Description |
|---|---|
| `/add-source` | Register a doc URL or GitHub repo |
| `/list-sources` | Show all sources with status |
| `/generate` | Force extract best practices from sources |
| `/update` | Check for source changes |
| `/diff` | Show what changed since last sync |
| `/remove-source` | Remove a source |

## How it works

See [Design Spec](docs/superpowers/specs/2026-03-21-buildSkillDocs-design.md) for the full architecture.
