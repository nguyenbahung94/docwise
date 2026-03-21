---
name: generate
description: Force full extraction (Tier 2) for sources. Extracts best-practice rules and creates per-source knowledge files. Spawns source-verifier for community sources. Use before committing for team distribution.
arguments:
  - name: --all
    description: Re-extract ALL sources, ignoring cache
    required: false
  - name: --topic
    description: Extract only sources for a specific topic
    required: false
  - name: --dry-run
    description: Show what would be extracted without doing it
    required: false
---

You are running the `/generate` command for the buildSkillDocs plugin.

## Process

1. Read `sources.yaml` and `.cache/sync-state.yaml`

2. Determine which sources to extract:
   - No flags: sources where `extracted: false`
   - `--all`: all sources regardless of extraction state
   - `--topic <name>`: sources matching that topic where `extracted: false` (or all if combined with `--all`)

3. If `--dry-run`: list sources that would be extracted and stop:
   ```
   Dry run — would extract:
     1. [doc] developer.android.com/topic/architecture → topic: architecture
     2. [repo] google/nowinandroid → topic: architecture

   Estimated token cost: ~47K tokens
   Run /generate (without --dry-run) to proceed.
   ```

4. For each source to extract:

   a. Determine the `source_slug` for the output file:
      - For doc sources: derive a slug from the URL (e.g., `developer.android.com/topic/architecture` → `android-architecture`, `medium.com/@someone/my-article` → `my-article`)
      - For repo sources: use the repo name part (e.g., `google/nowinandroid` → `nowinandroid`)

   b. Ensure the topic directory exists: `knowledge/<topic>/`
      Create it if it doesn't exist.

   c. Spawn the `doc-extractor` agent with:
      - source_type, source_url, source_paths (if repo), source_priority, topic
      - source_slug: the derived slug
      - output_path: `knowledge/<topic>/<source-slug>.md`

   d. The agent writes the knowledge file directly to `knowledge/<topic>/<source-slug>.md`

5. After each community source is extracted, spawn the `source-verifier` agent with:
   - community_knowledge_file: `knowledge/<topic>/<source-slug>.md`
   - topic: the topic name
   - knowledge_dir: `knowledge/`

   Update the knowledge file's `<!-- Verified: ... -->` metadata header based on verifier results:
   - `overall_status: verified` → `<!-- Verified: trusted -->`
   - `overall_status: partial` → `<!-- Verified: partial -->`
   - `overall_status: rejected` → `<!-- Verified: rejected -->`

6. Update `.cache/sync-state.yaml` for each processed source:
   - Set `extracted: true`
   - Set `fetched_at: <today>`
   - Set `verified: <overall_status>` (for community sources)

7. Update `knowledge/index.md`: set Fresh column to `yes` for processed sources

8. Report results:
   ```
   Generated knowledge for N/M sources:
     - architecture/android-architecture.md (12 rules, 4 patterns)
     - architecture/nowinandroid.md (8 rules, 2 decision tables)
     - concurrency/coroutines-guide.md (6 rules) [verified: partial]

   Failed: K sources [list if any]

   Knowledge files ready. Commit and push to share with your team.
   ```

## Error handling

- If a source fetch fails (404, timeout): log warning, skip, continue with others
- HTTP 403/429 (rate limited): log "rate limited — try again later", skip
- If extraction produces empty or malformed output: keep previous knowledge file if one exists, report failure
- If source-verifier fails for a community source: keep `Verified: pending` in the knowledge file header, log warning
- Report partial results at the end
