---
name: diff
description: Show the current status of all sources from the cache, including freshness info. Zero cost — reads only local state files, no network calls.
---

You are running the `/diff` command for the docwise plugin.

## Process

This command is purely local — it reads cached state only. No network calls, no fetching.

1. Read `.cache/sync-state.yaml` and `sources.yaml`

2. For each source, compute freshness from `fetched_at` and `ttl_days`:
   - If `fetched_at` is null → "never fetched"
   - If `fetched_at + ttl_days >= today` → "yes (Nd left)" where N = days remaining
   - If `fetched_at + ttl_days < today` → "stale (Nd ago)" where N = days past expiry

3. Display the current cached status of each source:

```
docwise Source Status:

  [clean]     developer.android.com/topic/architecture
              Last checked: 2026-03-20 | Extracted: yes | Fresh: yes (12d left)

  [dirty]     google/nowinandroid
              Changed since: 2026-03-15 | Extracted: no (cache invalidated) | Fresh: stale (3d ago)

  [clean]     kotlinlang.org/docs/coroutines-guide.html
              Last checked: 2026-03-18 | Extracted: yes | Fresh: yes (27d left)

  [clean]     medium.com/@someone/article
              Last checked: 2026-03-10 | Extracted: yes | Fresh: yes (45d left) | Verified: partial

  [error]     developer.android.com/topic/libraries/architecture/workmanager
              Error: timeout on last check | Extracted: no | Fresh: stale (5d ago)

  [new]       square.github.io/retrofit/
              Never checked | Extracted: no | Fresh: never fetched

Summary: 3 clean, 1 dirty, 1 error, 1 new
Run /update to check for remote changes, then /generate to extract.
```

4. Do NOT fetch any pages, clone any repos, or modify any files.
5. Status comes entirely from sync-state.yaml — reflects the last /update run.

## Notes on freshness display

- Only show `| Verified: <value>` for community sources where verification has been run
- Official, team, and reference sources omit the Verified line
- Fresh line always shown for all sources
