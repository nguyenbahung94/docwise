---
name: list-sources
description: Show all registered sources with their status, extraction state, freshness, and verification status.
---

You are running the `/list-sources` command for the buildSkillDocs plugin.

## Process

1. Read `sources.yaml`
2. Read `.cache/sync-state.yaml` for status info
3. For each source, compute freshness:
   - If `fetched_at` is null → "—"
   - If `fetched_at + ttl_days >= today` → "yes (Nd left)" where N = days remaining
   - If `fetched_at + ttl_days < today` → "stale (Nd)" where N = days past expiry
4. For each source, determine verification display:
   - `verified` field absent or null → "—"
   - `verified: false` → "unverified"
   - `verified: "verified"` → "verified"
   - `verified: "partial"` → "partial"
   - `verified: "trusted"` → "trusted"
   - `verified: "rejected"` → "rejected"
5. Display a formatted table:

```
buildSkillDocs Sources (N total):

| # | Type | Source | Topic | Priority | Status | Extracted | Fresh | Verified |
|---|------|--------|-------|----------|--------|-----------|-------|----------|
| 1 | doc  | developer.android.com/topic/architecture | architecture | official | clean | yes | yes (12d left) | — |
| 2 | repo | google/nowinandroid | architecture | reference | clean | no | stale (3d) | — |
| 3 | doc  | kotlinlang.org/docs/coroutines-guide.html | concurrency | official | error | no | — | — |
| 4 | doc  | medium.com/@someone/article | architecture | community | clean | yes | yes (45d left) | partial |
```

Status values:
- `clean` — source unchanged since last check
- `dirty` — source changed, cache invalidated
- `error` — last fetch failed (show error message)
- `new` — never checked (just added)

Fresh values:
- `yes (Nd left)` — within TTL, N days remaining
- `stale (Nd)` — past TTL by N days
- `—` — never fetched

Verified values:
- `trusted` — all community rules verified against official sources
- `verified` — majority of rules verified
- `partial` — some rules verified, some unverified
- `unverified` — not yet verified or verification failed
- `rejected` — rules contradict official sources
- `—` — not applicable (official/team/reference sources)

If no sources registered, show: "No sources registered. Use /add-source to get started."
