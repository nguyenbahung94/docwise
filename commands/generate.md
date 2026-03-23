---
name: generate
description: Force full extraction (Tier 2) for sources. Extracts best-practice rules and creates per-source knowledge files. Spawns source-verifier for community sources. Use before committing for team distribution.
arguments:
  - name: --all
    description: Re-extract ALL sources, ignoring hash check
    required: false
  - name: --topic
    description: Extract only sources for a specific topic
    required: false
  - name: --source
    description: Force re-extract one specific source URL or repo
    required: false
  - name: --dry-run
    description: Show what would be extracted without doing it
    required: false
---

You are running the `/generate` command for the docwise plugin.

## Process

1. Read `sources.yaml` and `.cache/sync-state.yaml`

2. Determine which sources to extract:
   - No flags: sources where `extracted: false` or content changed
   - `--all`: all sources, ignoring hash check — always re-extract
   - `--topic <name>`: sources matching that topic (respects hash check unless combined with `--all`)
   - `--source <url>`: force re-extract this one specific source, ignoring hash check
   - `--source` + `--topic` can be combined but `--source` takes priority

3. If `--dry-run`: list sources that would be extracted and stop:
   ```
   Dry run — would extract:
     1. [doc] developer.android.com/topic/architecture → topic: architecture
     2. [repo] google/nowinandroid → topic: architecture

   Uses Python script — zero LLM tokens.
   Run /generate (without --dry-run) to proceed.
   ```

4. For each source to extract:

   a. Determine the `source_slug` for the output file:
      - For doc sources: derive a slug from the URL (e.g., `developer.android.com/topic/architecture` → `android-architecture`, `medium.com/@someone/my-article` → `my-article`)
      - For repo sources: use the repo name part (e.g., `google/nowinandroid` → `nowinandroid`)
      - **Check for slug collision:** if two sources in the same topic would produce the same slug, append a suffix (e.g., `state.md`, `state-2.md`). Log a warning: "Slug collision for [topic]/[slug] — sources: [url1], [url2]"

   b. **Check if content changed before extracting (save tokens):**
      - Fetch the page / check repo HEAD commit
      - Compute content hash (for docs) or get latest SHA (for repos)
      - Compare with stored hash/SHA in `.cache/sync-state.yaml`
      - **If unchanged AND knowledge file already exists:** skip extraction, just update `fetched_at`. Log "[unchanged] <source> — skipped extraction"
      - **If changed OR no knowledge file exists:** proceed with extraction
      - Note: `--all` flag bypasses this check and always extracts

   c. Ensure the topic directory exists: `knowledge/<topic>/`
      Create it if it doesn't exist.

   d. Run the doc extractor Python script (zero tokens, no LLM agent):
      ```bash
      python3 ${CLAUDE_PLUGIN_ROOT}/tools/doc_extractor.py --url "<url>" --topic "<topic>" --priority "<priority>" --output "knowledge/<topic>/<source-slug>.md"
      ```
      For batch extraction of multiple URLs into one knowledge file:
      ```bash
      python3 ${CLAUDE_PLUGIN_ROOT}/tools/doc_extractor.py --urls "<url1>,<url2>" --topic "<topic>" --priority "<priority>" --output "knowledge/<topic>/<source-slug>.md"
      ```

   e. The script writes the knowledge file directly to `knowledge/<topic>/<source-slug>.md`

   f. **Enhance with local LLM** (optional, requires Ollama):
      ```bash
      python3 ${CLAUDE_PLUGIN_ROOT}/tools/llm_summarizer.py --input "knowledge/<topic>/<source-slug>.md" --model qwen2.5:32b
      ```
      This adds Mental Model, Decision Framework, Anti-Patterns, and Key Relationships sections.
      Skip this step if Ollama is not available — the raw knowledge file is still usable.

   g. Update `.cache/sync-state.yaml`: store new `content_hash` or `last_commit`

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

8. **Rebuild knowledge graph** (after all extractions complete):

   Rebuild `knowledge/graph.yaml` from scratch:

   a. Read ALL knowledge files in `knowledge/*/` directories
   b. Parse the `## Concepts (for graph)` section from each file
   c. Build nodes: each unique concept becomes a node, with `files` listing all knowledge files that mention it
   d. Build edges: each relationship becomes an edge with `from`, `to`, `relation`
   e. Merge: if multiple sources define the same edge, keep it (note both sources)
   f. Conflict: if sources contradict (A→B "uses" vs A→B "replaces"), higher priority source wins
   g. Validate:
      - Remove nodes that reference knowledge files that don't exist
      - Warn about orphan nodes (no edges) but keep them
   h. Write the rebuilt `knowledge/graph.yaml`

   The graph is ALWAYS rebuilt from scratch — never patched. This ensures deleted sources have their nodes removed.

9. Report results:
   ```
   Generated knowledge for N sources:
     - [extracted] architecture/android-architecture.md (12 rules, 4 patterns)
     - [extracted] architecture/nowinandroid.md (8 rules, 2 code snippets)
     - [extracted] concurrency/coroutines-guide.md (6 rules) [verified: partial]
     - [unchanged] navigation/android-navigation.md — content same, skipped

   Extracted: X | Unchanged (skipped): Y | Failed: Z

   Knowledge files ready. Commit and push to share with your team.
   ```

## Error handling

- If a source fetch fails (404, timeout): log warning, skip, continue with others
- HTTP 403/429 (rate limited): log "rate limited — try again later", skip
- If extraction produces empty or malformed output: keep previous knowledge file if one exists, report failure
- If source-verifier fails for a community source: keep `Verified: pending` in the knowledge file header, log warning
- Report partial results at the end
