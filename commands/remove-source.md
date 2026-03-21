---
name: remove-source
description: Remove a registered source, its index entry, its knowledge file, and cached state. Leaves the topic directory if other sources remain.
arguments:
  - name: source
    description: URL of the doc page or repo name (owner/name) to remove
    required: true
---

You are running the `/remove-source` command for the buildSkillDocs plugin.

## Process

1. Read `sources.yaml` and find the matching source by URL or repo name
2. If not found, report: "Source not found: [input]. Use /list-sources to see registered sources."

3. Determine the `source_slug` for this source (same derivation as /generate uses):
   - For doc sources: slug derived from URL (e.g., `developer.android.com/topic/architecture` → `android-architecture`)
   - For repo sources: repo name part (e.g., `google/nowinandroid` → `nowinandroid`)

4. Remove the source entry from `sources.yaml`

5. Remove only the row for this source from `knowledge/index.md`
   - Match by URL or repo identifier in the row
   - Do NOT remove rows for other sources in the same topic

6. Remove the matching entry from `.cache/sync-state.yaml`

7. Remove the specific knowledge file: `knowledge/<topic>/<source-slug>.md`
   - If the file does not exist, skip silently (no error)

8. Check if the topic directory `knowledge/<topic>/` is now empty:
   - If other source files remain → leave the directory as-is
   - If the directory is empty (no other .md files) → remove the directory

9. Report:
   ```
   Removed source: [url/repo]
   Topic: [topic] ([N] other sources remain for this topic)
   Knowledge file removed: knowledge/[topic]/[source-slug].md
   ```

   Or if topic directory was also removed:
   ```
   Removed source: [url/repo]
   Topic: [topic] (no sources remain — topic directory removed)
   Knowledge file removed: knowledge/[topic]/[source-slug].md
   Topic directory removed: knowledge/[topic]/
   ```
