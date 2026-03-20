# buildSkillDocs — Design Spec

## Problem

AI coding assistants (Claude Code, Cursor, etc.) don't reliably follow the latest best practices from official documentation. They use outdated or generic patterns because their training data is frozen in time. Developers must manually provide doc links to get correct, modern code.

The Android + Kotlin ecosystem is especially affected — hundreds of doc pages, frequent updates, deprecated APIs, and evolving recommended patterns.

## Solution

**buildSkillDocs** is a Claude Code plugin that:

1. Ingests official documentation pages and GitHub repositories
2. Builds a lightweight keyword index (cheap) — NOT full content extraction upfront
3. When AI encounters matching keywords during coding, it fetches and extracts from the source on-demand
4. Caches extracted knowledge so the same source is never re-extracted twice
5. Tracks source changes over time — only invalidates cache when content actually changed
6. Delivers knowledge through a single auto-triggering skill

## Core Design: Two-Tier Lazy Extraction

### Tier 1 — Keyword Index (built upfront, very cheap)

When a source is added, the system scans for **keywords, topic names, and key API names only**. No full content extraction. This creates a lightweight lookup table.

Cost: ~500-1K tokens per source (just scanning for keywords).

### Tier 2 — Full Extraction (on-demand, only when needed)

When the AI hits matching keywords during an actual coding task, it fetches the full source and extracts detailed rules. The result is cached as a knowledge file for next time.

Cost: ~12K per doc page, ~35K per repo — but only when actually needed.

### Why lazy?

- Adding 50 doc pages costs ~25K-50K tokens total (just indexing), not ~600K
- Adding 10 repos costs ~5K-10K tokens (just indexing), not ~350K
- Most sources may never need full extraction if you never work in that area
- Full extraction cost is spread across real coding tasks, not paid upfront

## Users

- Individual Android/Kotlin developers using AI tools
- Development teams sharing a common knowledge base
- Source-agnostic — works with any documentation or GitHub repo, starting with Android + Kotlin

## Architecture

### Two parts

| Part | Role |
|---|---|
| **CLI commands** (slash commands in Claude Code) | Builder — adds sources, indexes keywords, manages cache |
| **best-practices skill** | Consumer — auto-triggers when AI writes code, looks up index, fetches on-demand |

### Plugin structure

```
buildSkillDocs/
  plugin.json                     # Plugin manifest
  CLAUDE.md                       # Plugin instructions

  commands/
    add-source.md                 # /add-source --doc <url> or --repo <repo>
    list-sources.md               # /list-sources
    generate.md                   # /generate (force full extraction for all/specific sources)
    update.md                     # /update (check for source changes, invalidate stale cache)
    diff.md                       # /diff (show what changed, zero tokens)
    remove-source.md              # /remove-source <url>

  skills/
    best-practices/
      skill.md                    # ONE skill — auto-triggers, reads index, fetches on-demand

  agents/
    doc-extractor/
      agent.md                    # AI agent that reads raw content and extracts rules
    keyword-scanner/
      agent.md                    # AI agent that scans sources for keywords (Tier 1)

  sources.yaml                    # Registered sources (user adds over time)

  .cache/
    sync-state.yaml               # Content hashes, commit SHAs, last checked dates

  knowledge/                      # Cached extraction output — AI reads these
    index.md                      # Keyword-to-source mapping (Tier 1 — always loaded)
    architecture.md               # Full extraction (Tier 2 — created on first need)
    concurrency.md
    ...
```

## Source Management

### Adding sources

Users register sources via slash commands:

```
/add-source --doc "https://developer.android.com/topic/architecture"
/add-source --repo "google/nowinandroid"
```

Optional topic grouping and priority:

```
/add-source --doc "https://developer.android.com/topic/architecture/ui-layer" --topic architecture --priority official
```

### Sub-page discovery

When a doc page has a sidebar with child pages (common on developer.android.com, kotlinlang.org), the system discovers them and lets the user choose:

```
/add-source --doc "https://developer.android.com/topic/architecture"

> Scanning page... Found 12 sub-pages:
>   1. Guide to app architecture
>   2. UI layer
>   3. State holders and UI state
>   4. UI events
>   5. Domain layer
>   6. Data layer
>   7. Data layer - Repositories
>   8. Data layer - Build an offline-first app
>   ...
>
> Add all? Or pick specific ones? (all / 1,2,5,6 / none)
> [Default: all]
```

Rules:
- The parent page is always added
- Sub-pages are listed for selection
- User picks which sub-pages to include
- Each selected sub-page becomes its own source entry (inherits parent's topic and priority)
- `none` = only the parent page

For repos, sub-page discovery is replaced by directory listing:

```
/add-source --repo "google/nowinandroid"

> Scanning repo structure... Key directories found:
>   1. app/src/main/kotlin (main app)
>   2. core/model (data models)
>   3. core/data (repositories)
>   4. core/domain (use cases)
>   5. core/ui (shared UI)
>   6. feature/* (feature modules)
>   ...
>
> Include all? Or pick specific ones? (all / 1,2,3,4 / none)
> [Default: 1,2,3,4 — core modules]
```

### sources.yaml

```yaml
sources:
  - type: doc
    url: "https://developer.android.com/topic/architecture"
    topics: [architecture]
    priority: official       # official > reference > community
    last_synced: null
    extracted: false         # true once Tier 2 extraction has been done

  - type: repo
    repo: "google/nowinandroid"
    topics: [architecture, compose, navigation]
    paths: ["app/src/main", "core/*/src/main", "*.md"]
    priority: reference
    last_synced: null
    extracted: false
```

### Source priority levels

| Priority | Meaning | Example |
|---|---|---|
| `official` (highest) | Official documentation from the technology owner | developer.android.com, kotlinlang.org |
| `reference` | Official reference/sample repos | google/nowinandroid, android/architecture-samples |
| `community` (lowest) | Community resources, blog posts, third-party repos | jakewharton/*, medium articles |

Default priority: `official` for doc sources, `reference` for repo sources. Overridable via `--priority` flag.

### Source-agnostic design

The system is not hardcoded to Android. Any doc URL or GitHub repo can be added. The knowledge base grows as more sources are registered. Multiple sources that relate to the same topic merge into one knowledge file.

## Indexing Pipeline (Tier 1 — cheap)

When `/add-source` is run:

```
Source (URL or repo)
        |
        v
   [ Quick scan ]    Fetch page / scan repo file list
        |             Extract: headings, API names, class names, key terms
        |             NO full content reading
        v
   [ Index ]          Add keywords + source link to index.md
        |
        v
   [ Done ]           Source registered, ready for on-demand extraction
```

### What gets indexed (keywords only)

| Source type | What is scanned | What is extracted |
|---|---|---|
| Doc page | Page title, headings (h1-h3), code block class/function names | Keywords, API names, topic label |
| Repo | File names, class names from key files, README headings | Keywords, pattern names, library versions |

### index.md format (Tier 1 — always loaded by skill)

```markdown
# Knowledge Index

| Keywords | Topic | Source | Extracted |
|---|---|---|---|
| ViewModel, UiState, StateFlow, UI layer, screen state | architecture | developer.android.com/topic/architecture | yes |
| WorkManager, CoroutineWorker, Constraints, OneTimeWorkRequest | background-work | developer.android.com/topic/libraries/architecture/workmanager | no |
| suspend, Flow, StateFlow, Channel, coroutineScope, launch | concurrency | kotlinlang.org/docs/coroutines-guide.html | no |
| sealed interface, TopicUiState, NiaAppState, OfflineFirstRepository | architecture | google/nowinandroid | yes |
| Room, Dao, Entity, Database, TypeConverter, Migration | data-persistence | developer.android.com/training/data-storage/room | no |
```

The `Extracted` column tells the skill whether a cached knowledge file exists or if it needs to fetch on-demand.

## Extraction Pipeline (Tier 2 — on-demand)

When the skill matches keywords but no cached knowledge file exists:

```
Matched source (from index)
        |
        v
   [ Fetch ]       Fetch full doc page via WebFetch / read repo files matching paths
        |
        v
   [ Extract ]     AI reads raw content, produces structured output
        |
        v
   [ Cache ]       Write to knowledge/<topic>.md, mark source as extracted
        |
        v
   [ Apply ]       Skill uses the freshly extracted knowledge for the current task
```

### Fetch strategy

| Source type | Method | Details |
|---|---|---|
| Doc page | `WebFetch` tool | Handles JavaScript-rendered pages (e.g., developer.android.com) |
| GitHub repo | `git clone --depth 1` or cached clone | Shallow clone. Only reads files matching `paths` in sources.yaml |

### Repo file selection (paths filter)

```yaml
# Default if paths is not specified:
paths: ["**/*.md", "**/*.kt", "**/build.gradle*"]

# User can customize per repo:
paths: ["app/src/main", "core/*/src/main", "*.md"]
```

The `paths` field is repo-only. Doc sources always fetch the single URL.

### Extractor output schema

The doc-extractor agent produces structured output:

```yaml
topic: "architecture"
source: "https://developer.android.com/topic/architecture"
source_priority: official
extracted:
  rules:
    - rule: "Expose UI state via StateFlow, not LiveData"
      type: do
      confidence: high
    - rule: "Do NOT pass Context into ViewModel"
      type: dont
      confidence: high
  patterns:
    - name: "UiState sealed interface"
      code: |
        sealed interface TopicUiState {
          data class Success(val topics: List<Topic>) : TopicUiState
          data object Loading : TopicUiState
          data object Error : TopicUiState
        }
      context: "From nowinandroid — preferred over data class for multi-state"
  decision_tables:
    - question: "How to expose UI state?"
      options:
        - use: "StateFlow<UiState>"
          when: "New code, Kotlin-first"
        - use: "LiveData"
          when: "Legacy Java codebase only"
  pitfalls:
    - description: "Using LiveData in new Kotlin code"
      why: "Deprecated pattern — StateFlow integrates better with coroutines"
  versions:
    - library: "lifecycle-viewmodel-compose"
      version: "2.8.x"
```

### Conflict resolution

When multiple sources provide guidance on the same topic:

1. **Same advice, different wording** — merge into the clearest version
2. **Contradictory advice** — higher priority source wins. The losing source's advice is noted as "Alternative (from [source]): ..." only if the contradiction is meaningful
3. **Complementary advice** — both are included (e.g., docs explain the rule, repo shows the implementation)

Priority order: `official` > `reference` > `community`. Within the same priority, more recently synced source wins.

### Output format (knowledge files)

Each knowledge file is organized by concept, not by source page. Every file includes a metadata header:

```markdown
<!-- Generated: 2026-03-21 | Sources: 3 docs, 1 repo | Max token budget: 800 -->

# Architecture — Best Practices

## Rules (from official docs)
- UI layer: ViewModel + UiState pattern
- Data layer: Repository pattern, single source of truth
- Domain layer: UseCases for reusable business logic

## Patterns (from nowinandroid repo)
- UiState: sealed interface, not data class
- ViewModel exposes: StateFlow<UiState>, not multiple flows
- Repository uses: Offline-first with Room + Network sync

## Decision table
| Need | Use | Not |
|---|---|---|
| Expose UI state | StateFlow<UiState> | LiveData |
| Share logic across ViewModels | UseCase | Base ViewModel |
| Cache network data | Repository + Room | ViewModel |

## Common pitfalls
- Do NOT pass Context into ViewModel
- Do NOT put business rules in ViewModel — use UseCase
- Do NOT use LiveData for new code — use StateFlow
```

### Knowledge file size limit

Target: **max 800 tokens per file**. If a topic exceeds this after merging sources, split by sub-topic:

```
knowledge/
  architecture.md            -> too large after adding 8 sources
  architecture-ui-layer.md   -> split into sub-topics
  architecture-data-layer.md
  architecture-domain.md
```

The index.md is updated to reflect the split. The skill handles this transparently.

## Smart Caching & Change Detection

### The rule: only invalidate cache when the source actually changed

### `/update` flow (cheap)

```
Step 1: Check each source for changes (NO AI cost)
  - Doc page: fetch page, compare content hash with stored hash
    - Same hash -> SKIP (zero tokens)
    - Different -> mark dirty, set extracted = false (invalidate cache)
  - Repo: git fetch, check latest commit SHA
    - Same SHA -> SKIP (zero tokens)
    - Different -> check which files changed (git diff), mark relevant ones dirty

Step 2: Dirty sources have their cache invalidated
  - Existing knowledge file is NOT deleted (kept as fallback)
  - Source is marked extracted = false in index
  - Next time skill needs this topic, it re-extracts fresh

Step 3: Re-index keywords for dirty sources (cheap — Tier 1 only)
```

Note: `/update` does NOT trigger full re-extraction. It only invalidates stale caches. Re-extraction happens lazily when the skill next needs the topic.

### `/update` flags

| Flag | Effect |
|---|---|
| (none) | Smart update — check for changes, invalidate stale caches |
| `--force` | Invalidate all caches regardless of hash/SHA |
| `--force --source <url>` | Invalidate one specific source's cache |
| `--dry-run` | Show what would be invalidated without doing it |

### `/generate` — force full extraction

Unlike the normal lazy flow, `/generate` forces Tier 2 extraction immediately:

| Flag | Effect | Token cost |
|---|---|---|
| `/generate` | Extract all sources that haven't been extracted yet | Medium-High |
| `/generate --all` | Re-extract ALL sources (ignore cache) | High |
| `/generate --topic <name>` | Extract all sources for one topic | Low-Medium |
| `/generate --dry-run` | Show what would be extracted | Zero |

Use `/generate` when you want to pre-build the knowledge base (e.g., before committing for your team).

### `/diff` — show what changed (zero tokens)

Reports which sources changed since last sync without extracting or invalidating.

### .cache/sync-state.yaml

```yaml
sources:
  - type: doc
    url: "https://developer.android.com/topic/architecture"
    content_hash: "abc123"
    last_checked: 2026-03-21
    last_changed: 2026-03-21
    status: clean                  # clean | dirty | error
    extracted: true

  - type: repo
    repo: "google/nowinandroid"
    last_commit: "f7a2b3c"
    last_checked: 2026-03-21
    last_changed: 2026-03-15
    status: clean
    extracted: true
    error: null                    # error message if status = error
```

## Error Handling

### Fetch failures

| Failure | Behavior |
|---|---|
| Doc URL returns 404 | Mark source status `error`, log warning, skip — continue with other sources |
| Doc URL times out | Retry once after 5s. If still fails, mark `error`, skip |
| HTTP 403/429 (rate limit) | Mark `error`, log "rate limited", skip |
| Repo clone fails (private/missing) | Mark `error`, log warning, skip |
| Network offline | Abort entirely — cannot proceed without network |

### Partial failure policy

- All commands are **best-effort** — process reachable sources, skip failed ones
- After completion, report: "Processed N/M sources. K sources failed: [list with reasons]"
- Failed sources retain their previous knowledge (not deleted)
- User can retry failed sources with `/generate --topic <name>` or `/update --force --source <url>`

### Extraction quality failures

- If the doc-extractor agent produces empty or malformed output, treat as error — keep previous knowledge file, report the failure
- `/generate --dry-run` shows proposed extractions so user can review before committing

### On-demand extraction failures (during coding)

- If the skill triggers on-demand extraction and it fails (network error, timeout), the skill reports: "Could not fetch latest docs for [topic]. Using cached version / No cached version available."
- The coding task is not blocked — skill proceeds with whatever knowledge is available

## The Skill — How AI Uses Knowledge

### Single skill: `best-practices`

Auto-triggers via CLAUDE.md dispatch when writing or modifying code.

### Trigger rule (CLAUDE.md dispatch entry)

```markdown
| Writing, modifying, or reviewing code in *.kt, *.java, *.xml, *.gradle* files | Invoke buildSkillDocs:best-practices |
| User says "check docs for X" or "what do the docs say about X" | Invoke buildSkillDocs:best-practices |
```

The first rule auto-triggers — no user action needed. The second allows manual lookup.

### Skill behavior

```
1. Read knowledge/index.md (~200 tokens, keyword index)
2. Match current task keywords against index
3. Check: is there a cached knowledge file for the matched topic?
   |
   +-- YES (extracted = true) --> Load cached file (~300-500 tokens). Apply rules.
   |
   +-- NO (extracted = false) --> Fetch source on-demand, extract, cache.
                                  Apply freshly extracted rules.
                                  (First time only — cached for next time)
```

### Token cost per coding task

| Scenario | Cost |
|---|---|
| Topic already cached | ~500-1500 tokens (index + cached file) |
| Topic not yet cached (first time) | ~12K-35K tokens (index + fetch + extract + cache) |
| Subsequent tasks on same topic | ~500-1500 tokens (uses cache) |

## Distribution

### Recommended: commit knowledge files to the plugin repo

Two workflows:

**Option A — Pre-built (recommended for teams):**
```
You:
  /add-source --doc <url>
  /add-source --repo <repo>
  /generate                    # Force extract everything upfront
  git commit + push            # Commit index + knowledge files

Team:
  claude plugin add buildSkillDocs
  # Works immediately — all knowledge pre-cached
```

**Option B — Lazy (for individual use):**
```
You:
  /add-source --doc <url>
  /add-source --repo <repo>
  # Done — just the index is built
  # Knowledge extracted on-demand as you code
```

## CLI Commands Summary

| Command | What it does | Token cost |
|---|---|---|
| `/add-source` | Register source, scan for keywords, discover sub-pages | Very low (~1K) |
| `/list-sources` | Show all sources with status and extraction state | Zero |
| `/generate` | Force Tier 2 extraction for un-extracted sources | Medium-High |
| `/generate --all` | Force re-extract ALL sources | High |
| `/generate --topic <name>` | Force extract for one topic | Low-Medium |
| `/generate --dry-run` | Show what would be extracted | Zero |
| `/update` | Check for source changes, invalidate stale caches | Very low |
| `/update --force` | Invalidate all caches | Zero |
| `/update --force --source <url>` | Invalidate one source's cache | Zero |
| `/update --dry-run` | Show what would be invalidated | Zero |
| `/diff` | Show what changed since last sync | Zero |
| `/remove-source` | Remove source, its index entry, and cached knowledge | Zero |

## Token Cost Summary

| Action | Token cost |
|---|---|
| `/add-source` (index only) | Very low — ~500-1K per source |
| `/generate` (force extract) | ~12K per doc page, ~35K per repo |
| `/update` (nothing changed) | Zero — only hash/SHA checks |
| `/update` (sources changed) | Zero — just invalidates cache |
| `/diff` | Zero |
| Daily coding (topic cached) | ~500-1500 tokens |
| Daily coding (topic not cached, first time) | ~12-35K tokens (one-time per topic) |

### Cost comparison: old approach vs lazy approach

| Scenario: 50 doc pages + 10 repos | Upfront extraction | Lazy extraction |
|---|---|---|
| Initial setup cost | ~950K tokens | ~50K tokens |
| First coding task (1 topic) | 0 (already done) | ~12-35K (extracts that topic) |
| After 5 different topics used | 0 | ~100K total (only what you needed) |
| Topics never used | Wasted ~800K tokens | 0 tokens (never extracted) |

## Success Criteria

1. AI produces code following latest official best practices without manual doc links
2. Adding new sources is trivial and cheap (one command, just indexes keywords)
3. Full extraction cost is deferred until actually needed
4. Updates only invalidate stale caches — no wasted re-extraction
5. Team onboarding is one command (plugin install with pre-built knowledge)
6. Knowledge files are small (~800 tokens max), focused, and grouped by concept
7. System works for any technology, not just Android
8. Sub-pages and repo directories are discoverable — user picks what to include
9. Partial failures are handled gracefully — never lose existing knowledge
10. Conflicting sources are resolved by priority, not randomly
