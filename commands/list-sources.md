---
name: list-sources
description: Show all registered sources with their status and extraction state.
---

You are running the `/list-sources` command for the buildSkillDocs plugin.

## Process

1. Read `sources.yaml`
2. Read `.cache/sync-state.yaml` for status info
3. Display a formatted table:

```
buildSkillDocs Sources (N total):

| # | Type | Source | Topic | Priority | Status | Extracted |
|---|------|--------|-------|----------|--------|-----------|
| 1 | doc  | developer.android.com/topic/architecture | architecture | official | clean | yes |
| 2 | repo | google/nowinandroid | architecture | reference | clean | no |
| 3 | doc  | kotlinlang.org/docs/coroutines-guide.html | concurrency | official | error | no |
```

Status values:
- `clean` — source unchanged since last check
- `dirty` — source changed, cache invalidated
- `error` — last fetch failed (show error message)
- `new` — never checked (just added)

If no sources registered, show: "No sources registered. Use /add-source to get started."
