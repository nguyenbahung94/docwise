# docwise — Design Spec

## Problem

AI coding assistants (Claude Code, Cursor, etc.) don't reliably follow the latest best practices from official documentation. They use outdated or generic patterns because their training data is frozen in time. Developers must manually provide doc links to get correct, modern code.

This affects every ecosystem — Android, React, Python, iOS, and more. Hundreds of doc pages, frequent updates, deprecated APIs, and evolving recommended patterns.

## Solution

**docwise** is a Claude Code plugin that:

1. Ingests official documentation pages, GitHub repos, blogs, and any web source
2. Builds a lightweight keyword index (cheap) — NOT full content extraction upfront
3. Extracts condensed knowledge **per-source** (not merged) — each source gets its own small file
4. Verifies community sources against official docs before trusting them
5. Tracks freshness via TTL — auto-detects stale knowledge, never blocks coding
6. Delivers knowledge through a single auto-triggering skill with priority-weighted loading
7. Ships with starter profiles for popular tech stacks (Android, React, Python, etc.)
8. Works for **any technology** — configurable file triggers, not hardcoded

## Core Design: Two-Tier Lazy Extraction

### Tier 1 — Keyword Index (built upfront, very cheap)

When a source is added, the system scans for **keywords, topic names, and key API names only**. No full content extraction. This creates a lightweight lookup table.

Cost: ~500-1K tokens per source (just scanning for keywords).

### Tier 2 — Full Extraction (via `/generate` or `/update`)

When the user runs `/generate` or `/update` detects changed content, the system fetches the full source and extracts detailed rules. The result is cached as a **per-source knowledge file**. Extraction never happens during coding — it's always an explicit user action.

Cost: ~12K per doc page, ~35K per repo — but only for sources the user chooses to extract.

### Why lazy?

- Adding 50 doc pages costs ~25K-50K tokens total (just indexing), not ~600K
- Adding 10 repos costs ~5K-10K tokens (just indexing), not ~350K
- Most sources may never need full extraction if you never work in that area
- Full extraction cost is spread across real coding tasks, not paid upfront

## Users

- Individual developers using AI tools (any tech stack)
- Development teams sharing a common knowledge base
- Open source community — install plugin, pick a starter profile, start coding

## Architecture

### Plugin structure

```
docwise/
  plugin.json                     # Plugin manifest
  CLAUDE.md                       # Plugin instructions

  commands/
    setup.md                      # /setup — first-install profile picker
    add-source.md                 # /add-source --doc <url> or --repo <repo>
    list-sources.md               # /list-sources
    generate.md                   # /generate (force full extraction)
    update.md                     # /update (check for changes, refresh stale)
    diff.md                       # /diff (show cached status)
    remove-source.md              # /remove-source <url>
    check.md                      # /check — audit current code against best practices

  skills/
    best-practices/
      skill.md                    # ONE skill — auto-triggers, reads index, loads knowledge

  agents/
    doc-extractor/
      agent.md                    # AI agent — Tier 2 extraction with verification
    keyword-scanner/
      agent.md                    # AI agent — Tier 1 keyword scanning
    source-verifier/
      agent.md                    # AI agent — verifies community sources against official

  profiles/                       # Starter packs for tech stacks
    android/
      sources.yaml
      knowledge/
    react/
      sources.yaml
      knowledge/
    python/
      sources.yaml
      knowledge/
    ios/
      sources.yaml
      knowledge/
    custom/
      sources.yaml
      knowledge/

  sources.yaml                    # Active source registry
  .cache/
    sync-state.yaml               # Content hashes, commit SHAs, TTL dates

  knowledge/                      # Per-source knowledge files, grouped by topic
    graph.yaml                    # Concept graph — rebuilt on every /generate
    index.md                      # Keyword-to-source mapping (fallback)
    architecture/
      core.md                     # From official docs
      nowinandroid.md             # From reference repo
      viewmodel-blog.md           # From community (verified)
    concurrency/
      core.md
      coroutines-repo.md
    ...
```

## Project Configuration

### Configurable file triggers

The skill trigger is **not hardcoded** to any language. It's configured per project:

```yaml
# sources.yaml — project section
project:
  name: "my-project"
  file_patterns: ["*.kt", "*.java", "*.xml", "*.gradle*"]   # what files trigger the skill
  versions:                                                    # optional, for version-aware rules
    min_sdk: 26
    kotlin: "2.0"
    compose_bom: "2024.12"
```

Examples for other stacks:

```yaml
# React project
project:
  file_patterns: ["*.tsx", "*.ts", "*.jsx", "*.css"]
  versions:
    node: "20"
    react: "19"

# Python project
project:
  file_patterns: ["*.py", "*.yaml"]
  versions:
    python: "3.12"
```

The CLAUDE.md dispatch rule reads `file_patterns` from `sources.yaml` instead of using hardcoded extensions.

## First-Install Experience: `/setup` Command

```
/setup

> Welcome to docwise!
>
> Pick your stack:
>   1. Android (Kotlin + Jetpack) — 15 sources pre-configured
>   2. React (TypeScript + Next.js) — 12 sources pre-configured
>   3. Python (Django + FastAPI) — 10 sources pre-configured
>   4. iOS (Swift + SwiftUI) — 11 sources pre-configured
>   5. Custom — start empty, add your own sources
>
> You can always add more sources later with /add-source.

User picks: 1

> Setting up Android profile...
> Copied sources.yaml and pre-built knowledge files.
> File triggers set to: *.kt, *.java, *.xml, *.gradle*
>
> Ready! Your AI now follows Android best practices.
> Run /list-sources to see what's included.
```

The `/setup` command:
1. Copies the selected profile's `sources.yaml` and `knowledge/` directory into the plugin root
2. Sets `project.file_patterns` based on the profile
3. Pre-built knowledge files are included — no `/generate` needed
4. User can add more sources later with `/add-source`

## Source Management

### Adding sources

Users register sources via slash commands:

```
/add-source --doc "https://developer.android.com/topic/architecture"
/add-source --repo "google/nowinandroid"
/add-source --doc "https://medium.com/@someone/advanced-viewmodel" --priority community
```

Optional topic grouping and priority:

```
/add-source --doc "https://developer.android.com/topic/architecture/ui-layer" --topic architecture --priority official
```

### Sub-page discovery

When a doc page has a sidebar with child pages, the system discovers them and lets the user choose:

```
/add-source --doc "https://developer.android.com/topic/architecture"

> Scanning page... Found 12 sub-pages:
>   1. Guide to app architecture
>   2. UI layer
>   ...
>
> Add all? Or pick specific ones? (all / 1,2,5,6 / none)
> [Default: all]
```

For repos, sub-page discovery is replaced by directory listing:

```
/add-source --repo "google/nowinandroid"

> Scanning repo structure... Key directories found:
>   1. app/src/main/kotlin (main app)
>   2. core/model (data models)
>   ...
>
> Include all? Or pick specific ones? (all / 1,2,3,4 / none)
> [Default: 1,2,3,4 — core modules]
```

### sources.yaml

```yaml
project:
  name: "my-android-app"
  file_patterns: ["*.kt", "*.java", "*.xml", "*.gradle*"]
  versions:
    min_sdk: 26
    kotlin: "2.0"
    compose_bom: "2024.12"

sources:
  - type: doc
    url: "https://developer.android.com/topic/architecture"
    topics: [architecture]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: repo
    repo: "google/nowinandroid"
    topics: [architecture, compose, navigation]
    paths: ["app/src/main", "core/*/src/main", "*.md"]
    priority: reference
    ttl_days: 14
    last_synced: null
    extracted: false

  - type: doc
    url: "https://medium.com/@someone/advanced-viewmodel-patterns"
    topics: [architecture]
    priority: community
    ttl_days: 90
    last_synced: null
    extracted: false
    verified: false          # community sources need verification
```

### Source priority levels

| Priority | Meaning | Default TTL | Trusted? | Example |
|---|---|---|---|---|
| `official` (highest) | Official documentation from the technology owner | 30 days | Yes | developer.android.com, kotlinlang.org |
| `team` | Your company's internal rules — can supplement or override for team-specific reasons | 90 days | Yes | internal wiki, team conventions |
| `reference` | Official reference/sample repos | 14 days | Yes | google/nowinandroid |
| `community` (lowest) | Blogs, Medium, third-party repos | 90 days | **No — requires verification** | medium.com articles, personal blogs |

Default priority: `official` for doc sources, `reference` for repo sources. Overridable via `--priority` flag.

TTL is configurable per source via `ttl_days` field. Defaults shown above.

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

### index.md format (Tier 1 — always loaded by skill)

```markdown
# Knowledge Index

| Keywords | Topic | Source | Priority | Extracted | Fresh |
|---|---|---|---|---|---|
| ViewModel, UiState, StateFlow | architecture | developer.android.com/topic/architecture | official | yes | yes |
| sealed interface, TopicUiState | architecture | google/nowinandroid | reference | yes | yes |
| SharedFlow, SavedStateHandle | architecture | medium.com/@someone/... | community | yes | stale (25d) |
| WorkManager, CoroutineWorker | background-work | developer.android.com/... | official | no | — |
```

The `Fresh` column shows whether the knowledge file is within its TTL. Stale files are still usable but flagged.

## Extraction Pipeline (Tier 2 — on-demand)

### Per-source knowledge files

Each source gets its **own** knowledge file, organized under a topic directory:

```
knowledge/
  architecture/
    core.md                    ← from developer.android.com (official)
    nowinandroid.md            ← from google/nowinandroid (reference)
    advanced-viewmodel.md      ← from Medium article (community, verified)
  concurrency/
    core.md                    ← from kotlinlang.org (official)
    coroutines-repo.md         ← from Kotlin/kotlinx.coroutines (reference)
```

**Why per-source, not merged:**
- Each source stays independent — adding/removing a source doesn't affect others
- Each file tracks its own TTL and freshness
- Verification status is per-source
- No merging conflicts or growing files

### Knowledge file format

Each file contains condensed highlights with "why" annotations and before/after examples:

```markdown
<!-- Source: developer.android.com/topic/architecture -->
<!-- Priority: official -->
<!-- Fetched: 2026-03-21 -->
<!-- TTL: 30 days — re-fetch after 2026-04-20 -->
<!-- Verified: trusted (official source) -->

# Architecture — Core Rules

## Rules
- DO: Expose UI state via StateFlow, not LiveData
  WHY: Integrates with coroutines, survives config changes, null-safe by default
  EXCEPTION: Legacy Java modules that can't use coroutines

- DON'T: Pass Context into ViewModel
  WHY: Causes memory leaks — ViewModel outlives Activity/Fragment

## Before/After
❌ Old way:
val name = MutableLiveData<String>()
val loading = MutableLiveData<Boolean>()

✅ New way:
data class ProfileUiState(val name: String = "", val loading: Boolean = false)
val uiState: StateFlow<ProfileUiState> = ...

## Decision table
| Need | Use | Not |
|---|---|---|
| Expose UI state | StateFlow<UiState> | LiveData |
| Share logic across ViewModels | UseCase | Base ViewModel |

## Pitfalls
- Using LiveData in new Kotlin code
  WHY: Deprecated pattern — StateFlow integrates better with coroutines
```

### Repo extraction: code snippets, not full files

For repos, the extractor reads key files but saves **only the pattern-defining code**:

```markdown
<!-- Source: google/nowinandroid -->
<!-- Priority: reference -->
<!-- Fetched: 2026-03-21 -->
<!-- TTL: 14 days -->

# Architecture — nowinandroid patterns

## Structure
- Modules: core/data, core/domain, core/model, feature/*
- Each feature = standalone module with own ViewModel

## Pattern: ViewModel with UiState
```kotlin
// From: feature/topic/TopicViewModel.kt
class TopicViewModel @Inject constructor(
    private val getTopicsUseCase: GetTopicsUseCase
) : ViewModel() {

    val uiState: StateFlow<TopicUiState> = getTopicsUseCase()
        .map(TopicUiState::Success)
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = TopicUiState.Loading
        )
}

sealed interface TopicUiState {
    data object Loading : TopicUiState
    data class Success(val topics: List<Topic>) : TopicUiState
}
```
> Key: inject UseCase, expose StateFlow, use stateIn with WhileSubscribed, sealed interface

## Versions
- Kotlin: 2.0.x
- Compose BOM: 2024.12
- Hilt: 2.51
```

### Knowledge file size limit

Target: **max 800 tokens per file**. With max 3 files loaded per task, worst case is ~2400 tokens. The extractor must prioritize: high-confidence rules first, then decision tables, then pitfalls, then patterns with code, then versions.

### Extractor → Knowledge file pipeline

The extractor agent produces a structured YAML output (see schema below). The system then renders this YAML into a markdown knowledge file. The YAML is intermediate — only the markdown file is stored and loaded by the skill.

### Topic normalization

Topic names are always kebab-case lowercase: `architecture`, `background-work`, `data-persistence`. If a user provides `--topic "Background Work"`, it is normalized to `background-work`. This becomes the directory name under `knowledge/`.

### Extractor output schema

The doc-extractor agent produces structured output including "why" annotations and before/after:

```yaml
topic: "architecture"
source: "https://developer.android.com/topic/architecture"
source_priority: official
extracted:
  rules:
    - rule: "Expose UI state via StateFlow, not LiveData"
      type: do
      confidence: high
      why: "Integrates with coroutines, survives config changes, null-safe by default"
      exception: "Legacy Java modules that can't use coroutines"
    - rule: "Do NOT pass Context into ViewModel"
      type: dont
      confidence: high
      why: "Causes memory leaks — ViewModel outlives Activity/Fragment"
  before_after:
    - name: "UI State pattern"
      before: |
        val name = MutableLiveData<String>()
        val loading = MutableLiveData<Boolean>()
      after: |
        data class ProfileUiState(val name: String = "", val loading: Boolean = false)
        val uiState: StateFlow<ProfileUiState> = ...
      why: "Single state object is easier to test and reason about"
  patterns:
    - name: "UiState sealed interface"
      code: |
        sealed interface TopicUiState { ... }
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
  concepts:                              # NEW — graph data
    - name: "ViewModel"
      relates_to:
        - concept: "StateFlow"
          relation: "exposes state via"
        - concept: "UseCase"
          relation: "delegates logic to"
        - concept: "Hilt"
          relation: "injected by"
    - name: "StateFlow"
      relates_to:
        - concept: "LiveData"
          relation: "replaces"
```

The `concepts` section is used by `/generate` to build `knowledge/graph.yaml`. Each concept lists its relationships to other concepts found in the source.

## Source Verification

### Problem

Community sources (blogs, Medium articles) can contain wrong advice, outdated patterns, or opinions presented as facts. The plugin must verify before trusting.

### Verification flow

```
Community source added (/add-source --priority community)
        |
        v
   [ Extract rules from the source ]
        |
        v
   [ Spawn source-verifier agent ]
        |
        v
   For each extracted rule, compare against official sources:
        |
        +-- AGREES with official → ✅ verified
        |
        +-- CONTRADICTS official → ❌ rejected (warn user)
        |
        +-- NEW info, not in official → ⚠ unverified
        |
        +-- Can't determine → ⚠ unverified
```

### Verification statuses

| Status | Meaning | Skill behavior |
|---|---|---|
| ✅ `verified` | Matches official sources | Apply confidently |
| ⚠ `unverified` | Not covered by official — could be correct | Apply but note: "from community source, not officially verified" |
| ❌ `rejected` | Contradicts official recommendation | Never apply. Warn user if their code follows this pattern |

### What gets verified

- Only `community` priority sources are verified
- `team`, `official`, and `reference` sources are trusted by default
- Verification runs automatically during extraction — no user action needed
- Each rule in the knowledge file is tagged with its verification status

### Version-aware verification

If the project has `versions` configured in `sources.yaml`, the verifier can also check:
- "This rule requires minSdk 29+ but your project targets 26" → flag as incompatible
- "This library version is older than what you're using" → flag as outdated

## TTL and Freshness

### Smart TTL defaults

| Source priority | Default TTL | Reason |
|---|---|---|
| `team` | 90 days | Internal rules rarely change |
| `official` | 30 days | Official docs update moderately |
| `reference` | 14 days | Reference repos update frequently |
| `community` | 90 days | Blog posts almost never change |

User can override per source via `ttl_days` field in sources.yaml.

### Freshness check — never blocks coding

```
Skill triggers during coding
        |
        v
   Load knowledge files for matched topic
        |
        v
   For each file, check Fetched date vs TTL:
        |
        +-- Fresh (within TTL) → use as-is
        |
        +-- Stale (past TTL) → STILL use it, don't block
                                 Flag at end of response:
                                 "📋 1 source for 'architecture' is stale. Run /update to refresh."
```

**Key rule: NEVER fetch during coding.** Always use cached knowledge, even if stale. Refreshing happens via `/update` only.

### `/update` with TTL awareness

```
/update

> Checking 12 sources...
>   - 8 fresh (within TTL, unchanged) — skipped
>   - 2 stale (past TTL) → re-fetched → content unchanged → reset timer
>   - 1 stale (past TTL) → re-fetched → content CHANGED → re-extracted
>   - 1 error (timeout)
>
> Updated 1 knowledge file: architecture/core.md
> All sources now fresh.
```

### .cache/sync-state.yaml

```yaml
sources:
  - type: doc
    url: "https://developer.android.com/topic/architecture"
    content_hash: "abc123"
    last_checked: 2026-03-21
    last_changed: 2026-03-21
    fetched_at: 2026-03-21
    ttl_days: 30
    status: clean
    extracted: true
    verified: trusted
    error: null

  - type: repo
    repo: "google/nowinandroid"
    last_commit: "f7a2b3c"
    last_checked: 2026-03-21
    last_changed: 2026-03-15
    fetched_at: 2026-03-21
    ttl_days: 14
    status: clean
    extracted: true
    verified: trusted
    error: null

  - type: doc
    url: "https://medium.com/@someone/advanced-viewmodel"
    content_hash: "def456"
    last_checked: 2026-03-21
    last_changed: 2026-03-21
    fetched_at: 2026-03-21
    ttl_days: 90
    status: clean
    extracted: true
    verified: partial            # some rules verified, some unverified
    error: null
```

## The Skill — How AI Uses Knowledge

### Single skill: `best-practices`

Auto-triggers based on `project.file_patterns` from sources.yaml.

### Trigger rule (CLAUDE.md dispatch entry)

```markdown
| Writing, modifying, or reviewing code matching project.file_patterns | Invoke docwise:best-practices |
| User says "check docs for X" or "what do the docs say about X" | Invoke docwise:best-practices |
| User says "check my code against best practices" | Invoke docwise:best-practices in audit mode |
```

### Knowledge Graph — concept-based retrieval

Instead of flat keyword matching, docwise uses a **concept graph** to find related knowledge across topics.

#### graph.yaml

```yaml
# knowledge/graph.yaml — rebuilt on every /generate and /update

nodes:
  ViewModel:
    files: ["architecture/core.md", "architecture/nowinandroid.md"]
  StateFlow:
    files: ["concurrency/core.md", "architecture/core.md"]
  UseCase:
    files: ["architecture/core.md"]
  Repository:
    files: ["architecture/core.md", "data-persistence/core.md"]
  Room:
    files: ["data-persistence/core.md"]
  Hilt:
    files: ["dependency-injection/core.md"]
  WorkManager:
    files: ["background-work/core.md"]

edges:
  - from: ViewModel
    to: StateFlow
    relation: "exposes state via"
  - from: ViewModel
    to: UseCase
    relation: "delegates logic to"
  - from: ViewModel
    to: Hilt
    relation: "injected by"
  - from: UseCase
    to: Repository
    relation: "accesses data through"
  - from: Repository
    to: Room
    relation: "persists with"
  - from: Repository
    to: WorkManager
    relation: "syncs via"
  - from: StateFlow
    to: LiveData
    relation: "replaces"
```

#### How the skill uses the graph

```
1. Read knowledge/graph.yaml (~200-500 tokens)
2. Match current task to concept nodes (e.g., "ViewModel")
3. Traverse 2 hops from matched nodes:
   ViewModel → StateFlow, UseCase, Hilt (1st hop)
   UseCase → Repository (2nd hop)
4. Collect all knowledge files referenced by traversed nodes
5. Sort by priority: official > team > reference > community
6. Load top 3 files maximum
7. If a file is from community source, check its verification status
8. Apply rules to the current task
```

#### Graph rebuild rules

The graph is **always rebuilt from scratch** during `/generate` and `/update` (when sources are re-extracted). It is never patched incrementally.

```
After ALL sources extracted:
  1. Read ALL knowledge files in knowledge/*/
  2. Collect ALL concept relationships from extraction output
  3. Merge: same edge from multiple sources → keep, note both sources
  4. Conflict: contradicting edges → higher priority source wins
  5. Validate:
     - Orphan nodes (no edges) → warn, keep them
     - Nodes referencing missing files → remove those nodes
  6. Write knowledge/graph.yaml
```

This ensures the graph is always consistent with the current knowledge files. Deleting a source removes its nodes on next rebuild.

#### Fallback

If `graph.yaml` doesn't exist yet (no `/generate` run), the skill falls back to keyword matching via `knowledge/index.md`. The index still exists and is maintained.

**Loading priority (after graph traversal):**
1. Always load the `official` file first (highest authority)
2. Load `team` file if exists (company-specific supplements/overrides)
3. Load `reference` or verified `community` file if keywords strongly match

**Budget cap: max 3 files, max ~2400 tokens total per task.**

### Conflict resolution between loaded files

When 2-3 loaded files give conflicting advice on the same point:
1. Higher priority source wins (`official` > `team` > `reference` > `community`)
2. The skill applies the winning rule and notes: "Note: [lower source] suggests [alternative], but [higher source] recommends [winning approach]."
3. If both are the same priority, the more recently fetched source wins.

### Version-aware rule filtering

When the skill loads a knowledge file, it checks rules against `project.versions` from sources.yaml:

- If a rule is tagged with a version requirement (e.g., "requires minSdk 29+") and the project doesn't meet it → **skip the rule silently**
- If a library version in the knowledge file is older than the project's configured version → **flag as potentially outdated**
- If no `project.versions` is configured → no filtering, all rules apply

The extractor captures version requirements when present in the source:
```yaml
rules:
  - rule: "Use Foreground Service types in manifest"
    type: do
    confidence: high
    requires:
      min_sdk: 29          # rule only applies if project minSdk >= 29
```

### Team priority sources

`team` priority sources can be:
- A URL to an internal wiki/docs page (if accessible)
- A public or private GitHub repo (private repos require `gh auth` to be configured)
- A local file path (e.g., `/path/to/team-conventions.md`) — for rules not hosted anywhere

Adding a team source:
```
/add-source --doc "https://internal-wiki.company.com/android-conventions" --priority team
/add-source --repo "company/android-style-guide" --priority team
/add-source --doc "file:///path/to/local-conventions.md" --priority team
```

Team sources are always trusted (no verification). They can supplement official docs or override reference/community sources for team-specific reasons. Official docs remain the highest authority.

### Skill behavior during coding

```
Normal mode (auto-trigger):
  - Load relevant knowledge files (max 3)
  - Apply DO rules silently — AI just writes better code
  - Flag DON'T violations: "Note: official docs recommend X instead of Y"
  - Mention pitfalls if current code is at risk
  - For unverified community rules: "This practice comes from [source], not officially verified"
  - At end of response (if any stale sources):
    "📋 docwise: 1 source for 'architecture' is older than 30 days. Run /update to refresh."
```

### Conflict detection mode (`/check` command)

```
/check

> Scanning current file: ProfileViewModel.kt
>
>   ⚠ Line 15: Uses LiveData — recommended: StateFlow
>     Source: architecture/core.md (official)
>     WHY: Integrates with coroutines, survives config changes
>
>   ⚠ Line 23: Business logic in ViewModel
>     Source: architecture/core.md (official)
>     WHY: Move to UseCase — ViewModel should only map UI state
>
>   ✅ Line 8: Correct Hilt injection pattern
>   ✅ Line 30: StateFlow with WhileSubscribed — matches best practice
>
> Score: 2/4 practices followed
```

The `/check` command turns the plugin into a **best-practice linter** — reads current code and compares against knowledge files.

## Error Handling

### Fetch failures

| Failure | Behavior |
|---|---|
| Doc URL returns 404 | Mark source status `error`, log warning, skip |
| Doc URL times out | Retry once after 5s. If still fails, mark `error`, skip |
| HTTP 403/429 (rate limit) | Mark `error`, log "rate limited", skip |
| Repo clone fails (private/missing) | Mark `error`, log warning, skip |
| Network offline | Abort entirely — cannot proceed without network |

### Partial failure policy

- All commands are **best-effort** — process reachable sources, skip failed ones
- After completion, report: "Processed N/M sources. K sources failed: [list with reasons]"
- Failed sources retain their previous knowledge (not deleted)
- User can retry failed sources with `/update --force --source <url>`

### On-demand extraction: clarification

The skill **never fetches or extracts during coding**. Tier 2 extraction happens ONLY via:
- `/generate` — explicit user command
- `/update` — when a stale source is re-fetched and content changed

If the skill triggers and no cached knowledge file exists for a matched topic, it notes: "No knowledge cached for [topic]. Run `/generate --topic [topic]` to extract." The coding task is not blocked.

## Distribution

### Publishing to GitHub

```bash
# Push to GitHub as a public repo
git remote add origin https://github.com/your-username/docwise.git
git push -u origin main

# Anyone can install:
claude plugin add your-username/docwise
```

### Community contribution

- Anyone can submit a PR to add a new starter profile (e.g., "Flutter", "Rust", "Go")
- Each profile is a directory under `profiles/` with `sources.yaml` + `knowledge/`
- Maintainer reviews and merges — quality controlled
- Pre-built knowledge files are included so users don't need to `/generate`

### Distribution workflows

**For teams (Option A — pre-built):**
```
You:
  /setup → pick Android
  /add-source --doc <extra url>
  /generate
  git commit + push

Team:
  claude plugin add your-username/docwise
  /setup → pick Android
  # Works immediately — all knowledge pre-cached
```

**For individuals (Option B — lazy):**
```
You:
  claude plugin add your-username/docwise
  /setup → pick Android (or Custom)
  # Pre-built knowledge from profile works immediately
  # Additional sources extracted on-demand as you code
```

## CLI Commands Summary

| Command | What it does | Token cost |
|---|---|---|
| `/setup` | First-install profile picker — sets up sources + knowledge | Zero (copies files) |
| `/add-source` | Register source, scan for keywords, discover sub-pages | Very low (~1K) |
| `/list-sources` | Show all sources with status, extraction, and freshness | Zero |
| `/generate` | Force Tier 2 extraction for un-extracted sources | Medium-High |
| `/generate --all` | Force re-extract ALL sources | High |
| `/generate --topic <name>` | Force extract for one topic | Low-Medium |
| `/generate --dry-run` | Show what would be extracted | Zero |
| `/update` | Check for changes, refresh stale sources (past TTL) | Low (fetch + hash compare) |
| `/update --force` | Invalidate all caches | Zero |
| `/update --force --source <url>` | Invalidate one source's cache | Zero |
| `/update --dry-run` | Show what would be refreshed | Zero |
| `/diff` | Show cached status of all sources | Zero |
| `/remove-source` | Remove source, its index entry, and knowledge file | Zero |
| `/check` | Audit current code against best practices (linter mode) | Low (~1500 tokens) |

## Success Criteria

1. AI produces code following latest official best practices without manual doc links
2. Adding new sources is trivial and cheap (one command, just indexes keywords)
3. Full extraction cost is deferred until actually needed
4. Knowledge is per-source — adding/removing one source doesn't affect others
5. Community sources are verified against official docs before being trusted
6. Stale knowledge is flagged but never blocks coding
7. TTL is smart — different source types have appropriate refresh intervals
8. Extracted rules include "why" annotations and before/after examples
9. AI can explain why it's following a particular practice
10. `/check` command acts as a best-practice linter for existing code
11. `team` priority allows company-specific rules that override everything
12. Version-aware — rules can be filtered by project's SDK/language version
13. Works for any technology — configurable file triggers, starter profiles
14. Team onboarding is two commands (install plugin + /setup)
15. Community can contribute new profiles via PR
16. Partial failures are handled gracefully — never lose existing knowledge
17. Knowledge graph connects concepts across topics — AI finds related knowledge via traversal, not just keyword matching
18. Graph is always rebuilt from scratch on /generate and /update — never stale
