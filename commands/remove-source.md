---
name: remove-source
description: Remove a registered source, its index entry, and cached state. Does not delete knowledge files (they may have data from other sources).
arguments:
  - name: source
    description: URL of the doc page or repo name (owner/name) to remove
    required: true
---

You are running the `/remove-source` command for the buildSkillDocs plugin.

## Process

1. Read `sources.yaml` and find the matching source by URL or repo name
2. If not found, report: "Source not found: [input]. Use /list-sources to see registered sources."

3. Remove the source entry from `sources.yaml`
4. Remove the matching row from `knowledge/index.md`
5. Remove the matching entry from `.cache/sync-state.yaml`

6. Check if the source's topic has other sources remaining:
   - If yes: knowledge file stays (other sources still contribute)
   - If no: ask user "No other sources for topic '[topic]'. Delete knowledge/[topic].md? (yes/no)"
     - If yes: delete the knowledge file
     - If no: keep it (stale but still useful)

7. Report:
   ```
   Removed source: [url/repo]
   Topic: [topic] ([N] other sources remain for this topic)
   ```
