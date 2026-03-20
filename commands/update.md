---
name: update
description: Check registered sources for changes. Invalidates stale caches so next on-demand extraction fetches fresh content. Does NOT re-extract — use /generate for that.
arguments:
  - name: --force
    description: Invalidate all caches regardless of changes
    required: false
  - name: --source
    description: Target a specific source URL (use with --force)
    required: false
  - name: --dry-run
    description: Show what would be invalidated without doing it
    required: false
---

You are running the `/update` command for the buildSkillDocs plugin.

## Process

1. Read `sources.yaml` and `.cache/sync-state.yaml`

2. If `--force` with `--source <url>`:
   - Find the matching source, set extracted = false, status = dirty
   - Update index.md Extracted column to "no"
   - Report and stop

3. If `--force` without `--source`:
   - Set ALL sources to extracted = false, status = dirty
   - Update all index.md Extracted columns to "no"
   - Report and stop

4. Otherwise (smart update): For each source, check for changes:

   **Doc sources:**
   - Use WebFetch to fetch the page
   - Compute content hash (hash the text content)
   - Compare with stored `content_hash` in sync-state.yaml
   - Same hash → skip (log "unchanged")
   - Different hash → mark dirty:
     - Update content_hash
     - Set status = dirty, extracted = false
     - Re-run keyword-scanner agent for fresh keywords
     - Update index.md with new keywords and Extracted = "no"

   **Repo sources:**
   - Use Bash: `git ls-remote https://github.com/<repo>.git HEAD` to get latest commit SHA
   - Compare with stored `last_commit`
   - Same SHA → skip
   - Different SHA → mark dirty (same process as docs)

5. If `--dry-run`: show what would be invalidated without writing:
   ```
   Dry run — checking N sources:
     - [unchanged] developer.android.com/topic/architecture
     - [CHANGED] google/nowinandroid (new commit: abc1234)
     - [ERROR] kotlinlang.org/docs/... (timeout)

   Would invalidate: 1 source
   Run /update (without --dry-run) to proceed.
   ```

6. Report:
   ```
   Checked N sources:
     - M unchanged
     - K changed (caches invalidated)
     - J errors

   Changed sources will be re-extracted on next use, or run /generate to extract now.
   ```

## Error handling

- Network errors: mark source status = error, skip, continue
- Timeout: retry once, then mark error
- HTTP 403/429 (rate limited): mark error with "rate limited", skip
- Report all errors at end
