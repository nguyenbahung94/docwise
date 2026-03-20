---
name: diff
description: Show the current status of all sources from the cache. Zero cost — reads only local state files, no network calls.
---

You are running the `/diff` command for the buildSkillDocs plugin.

## Process

This command is purely local — it reads cached state only. No network calls, no fetching.

1. Read `.cache/sync-state.yaml` and `sources.yaml`

2. Display the current cached status of each source:

```
buildSkillDocs Source Status:

  [clean]     developer.android.com/topic/architecture
              Last checked: 2026-03-20 | Extracted: yes

  [dirty]     google/nowinandroid
              Changed since: 2026-03-15 | Extracted: no (cache invalidated)

  [clean]     kotlinlang.org/docs/coroutines-guide.html
              Last checked: 2026-03-18 | Extracted: yes

  [error]     developer.android.com/topic/libraries/architecture/workmanager
              Error: timeout on last check | Extracted: no

  [new]       square.github.io/retrofit/
              Never checked | Extracted: no

Summary: 2 clean, 1 dirty, 1 error, 1 new
Run /update to check for remote changes, then /generate to extract.
```

3. Do NOT fetch any pages, clone any repos, or modify any files.
4. Status comes entirely from sync-state.yaml — reflects the last /update run.
