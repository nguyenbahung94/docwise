---
name: update
description: TTL-aware refresh — only re-fetches sources past their TTL. Re-extracts if content changed. Use --force to ignore TTL and check all sources.
arguments:
  - name: --force
    description: Ignore TTL and check all sources regardless of freshness
    required: false
  - name: --source
    description: Target a specific source URL (use with --force)
    required: false
  - name: --dry-run
    description: Show what would be refreshed without doing it
    required: false
---

You are running the `/update` command for the buildSkillDocs plugin.

## Process

1. Read `sources.yaml` and `.cache/sync-state.yaml`

2. If `--force` with `--source <url>`:
   - Find the matching source
   - Fetch it and check for content changes (proceed to smart update logic for just that source, ignoring TTL)
   - Report and stop

3. Determine which sources to check:
   - Without `--force`: only sources where `fetched_at + ttl_days < today` (past TTL) — skip sources within TTL
   - With `--force`: all sources, regardless of TTL

4. For each source to check:

   **Doc sources:**
   - Use WebFetch to fetch the page
   - Compute content hash (hash the text content)
   - Compare with stored `content_hash` in sync-state.yaml

   **Repo sources:**
   - Use Bash: `git ls-remote https://github.com/<repo>.git HEAD` to get latest commit SHA
   - Compare with stored `last_commit`

5. For each checked source, apply the appropriate action:

   **Content unchanged:**
   - Reset `fetched_at` to today (TTL clock restarts)
   - Keep `extracted: true` if already extracted
   - Log "[fresh] <source> — content unchanged, TTL reset"

   **Content changed:**
   - Update `content_hash` or `last_commit`
   - Set `fetched_at` to today
   - Set `extracted: false`
   - Re-run `keyword-scanner` agent for fresh keywords
   - Update `knowledge/index.md` with new keywords and Fresh column = "no"
   - Re-run `doc-extractor` agent to update the knowledge file
   - For community sources: re-run `source-verifier` agent after re-extraction
   - Update sync-state.yaml `verified` field if community
   - Log "[changed] <source> — re-extracted"

   After all changed sources are re-extracted, rebuild `knowledge/graph.yaml` using the same process as /generate step 8.
   Only rebuild if at least one source was re-extracted (skip if all unchanged).

   **Within TTL (skipped):**
   - Do not fetch, do not modify
   - Log "[skipped] <source> — fresh (Nd left)"

6. If `--dry-run`: show what would be refreshed without writing:
   ```
   Dry run — checking sources past TTL:
     [skipped]  developer.android.com/topic/architecture (12d left)
     [stale]    google/nowinandroid (expired 3d ago)
     [stale]    kotlinlang.org/docs/coroutines-guide.html (expired 1d ago)
     [ERROR]    square.github.io/retrofit/ (timeout)

   Would re-fetch: 2 sources
   Run /update (without --dry-run) to proceed.
   ```

7. Update `knowledge/index.md` Fresh column for all refreshed sources.

8. Report:
   ```
   Checked N sources (M skipped — within TTL):
     - K fresh (content unchanged, TTL reset)
     - J changed (re-extracted)
     - L errors

   Changed sources re-extracted. Run /list-sources to see current status.
   ```

## Error handling

- Network errors: mark source status = error, skip, continue
- Timeout: retry once, then mark error
- HTTP 403/429 (rate limited): mark error with "rate limited — try again later", skip
- Report all errors at end
