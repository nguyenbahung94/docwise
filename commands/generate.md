---
name: generate
description: Force full extraction (Tier 2) for sources. Extracts best-practice rules and creates knowledge files. Use before committing for team distribution.
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

4. For each source to extract, spawn the `doc-extractor` agent with:
   - source_type, source_url, source_paths (if repo), source_priority, topic
   - existing_knowledge: path to existing knowledge file for this topic (if one exists from another source)

5. After extraction, the agent returns structured YAML. Convert it to a knowledge markdown file:
   - Write to `knowledge/<topic>.md`
   - Include metadata header: `<!-- Generated: <date> | Sources: N docs, N repos | Max token budget: 800 -->`
   - Format rules, patterns, decision tables, pitfalls, versions as markdown sections

6. If the knowledge file exceeds ~800 tokens, split by sub-topic:
   - `knowledge/<topic>-<subtopic>.md`
   - Update `knowledge/index.md` to reflect the split

7. Update `.cache/sync-state.yaml`: set `extracted: true` for processed sources

8. Update `knowledge/index.md`: set Extracted column to `yes` for processed sources

9. Report results:
   ```
   Generated knowledge for N/M sources:
     - architecture.md (3 sources → 12 rules, 4 patterns)
     - concurrency.md (2 sources → 8 rules, 2 decision tables)

   Failed: K sources [list if any]

   Knowledge files ready. Commit and push to share with your team.
   ```

## Error handling

- If a source fetch fails (404, timeout): log warning, skip, continue with others
- HTTP 403/429 (rate limited): log "rate limited — try again later", skip
- If extraction produces empty or malformed output: keep previous knowledge file, report failure
- Report partial results at the end
