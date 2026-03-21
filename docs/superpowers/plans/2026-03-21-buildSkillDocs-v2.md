# buildSkillDocs v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the buildSkillDocs plugin with per-source knowledge files, TTL freshness, source verification, priority-weighted loading, starter profiles, configurable triggers, and a best-practice linter mode.

**Architecture:** Two phases. Phase A updates existing files (knowledge structure, agents, skill, commands). Phase B adds new components (source-verifier agent, /setup, /check, profiles). Each task produces a working commit.

**Tech Stack:** Claude Code plugin system (markdown commands, skills, agents), YAML config, Markdown knowledge files.

**Spec:** `docs/superpowers/specs/2026-03-21-buildSkillDocs-design.md`

---

## File Structure (changes from v1)

```
buildSkillDocs/
  plugin.json                          # MODIFY — add new commands + source-verifier agent
  CLAUDE.md                            # MODIFY — configurable triggers, new dispatch rules
  README.md                            # MODIFY — document new features
  sources.yaml                         # MODIFY — add project section with file_patterns + versions

  commands/
    setup.md                           # CREATE — first-install profile picker
    add-source.md                      # MODIFY — TTL defaults, verified field, team priority
    list-sources.md                    # MODIFY — show freshness + verification status
    generate.md                        # MODIFY — per-source output, spawn verifier for community
    update.md                          # MODIFY — TTL-aware refresh, re-extract changed sources
    diff.md                            # MODIFY — show freshness column
    remove-source.md                   # MODIFY — remove per-source knowledge file
    check.md                           # CREATE — best-practice linter mode

  skills/
    best-practices/
      skill.md                         # MODIFY — priority-weighted loading, version filtering,
                                       #          stale notification, never block coding

  agents/
    doc-extractor/
      agent.md                         # MODIFY — why annotations, before/after, code snippets,
                                       #          per-source output, version requirements
    keyword-scanner/
      agent.md                         # MODIFY — add Priority + Fresh columns to output
    source-verifier/
      agent.md                         # CREATE — verifies community sources against official

  profiles/                            # CREATE — starter packs
    android/
      sources.yaml
      knowledge/                       # Pre-built knowledge files
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

  knowledge/
    index.md                           # MODIFY — add Priority + Fresh columns
    architecture/                      # NEW structure — per-source files in topic directories
      core.md
      nowinandroid.md
    ...
```

---

## Phase A: Core Enhancements

### Task 1: Update sources.yaml schema

Add `project` section with configurable file patterns and version info. Add `ttl_days` and `verified` fields to source entries.

**Files:**
- Modify: `sources.yaml`

- [ ] **Step 1: Update sources.yaml with project section**

Replace the current empty file with the new schema:

```yaml
project:
  name: ""
  file_patterns: []
  versions: {}

sources: []
```

- [ ] **Step 2: Commit**

```bash
git add sources.yaml
git commit -m "feat: add project config section to sources.yaml"
```

---

### Task 2: Update knowledge/index.md format

Add Priority and Fresh columns to support priority-weighted loading and freshness tracking.

**Files:**
- Modify: `knowledge/index.md`

- [ ] **Step 1: Update index.md with new columns**

```markdown
# Knowledge Index

| Keywords | Topic | Source | Priority | Extracted | Fresh |
|---|---|---|---|---|---|
```

- [ ] **Step 2: Commit**

```bash
git add knowledge/index.md
git commit -m "feat: add Priority and Fresh columns to knowledge index"
```

---

### Task 3: Update doc-extractor agent

Add "why" annotations, before/after examples, code snippet extraction for repos, version requirements, and per-source output format.

**Files:**
- Modify: `agents/doc-extractor/agent.md`

- [ ] **Step 1: Rewrite doc-extractor agent**

Replace the entire file with updated content. Key changes:
- Output schema now includes `why`, `exception`, `before_after`, and `requires` fields
- Repo extraction focuses on pattern-defining code snippets, not full files
- Output is per-source (one knowledge file per source, not merged)
- Knowledge file includes metadata header with Source, Priority, Fetched date, TTL, Verified status
- Token budget stays at ~800 tokens per file
- Extraction priority: rules with WHY > decision tables > pitfalls > before/after > patterns with code > versions

```markdown
---
name: doc-extractor
description: Reads full content from a doc page or GitHub repo and extracts structured best-practice rules with "why" annotations, before/after examples, and code snippets. Outputs per-source knowledge files with metadata headers.
tools:
  - WebFetch
  - Bash
  - Read
  - Glob
  - Grep
  - Write
---

You are a best-practice extractor for the buildSkillDocs plugin. Your job is to read a source and extract actionable rules that help AI write correct, modern code.

## Input

You will receive:
- `source_type`: "doc" or "repo"
- `source_url`: URL of the doc page or GitHub repo
- `source_paths`: (repo only) glob patterns for files to read
- `source_priority`: "official", "team", "reference", or "community"
- `topic`: the topic this source belongs to
- `source_slug`: filename slug for the output (e.g., "core", "nowinandroid", "advanced-viewmodel")
- `project_versions`: (optional) project version config for version-aware extraction

## For doc pages

1. Use WebFetch to fetch the full page content
2. Read thoroughly and extract best practices
3. For each rule, capture WHY it matters and any EXCEPTIONS

## For GitHub repos

1. Use Bash to clone: `git clone --depth 1 https://github.com/<repo>.git /tmp/buildSkillDocs-extract/<repo-name>`
2. Read files matching `source_paths` patterns
3. Focus on extracting **pattern-defining code snippets** — not full files:
   - Find key classes (ViewModel, Repository, UseCase implementations)
   - Extract only the code that shows the pattern (constructor, state exposure, key method)
   - Include a one-line summary of what makes this snippet important
   - Include file path reference: `// From: path/to/File.kt`
4. Also extract: module structure, dependency versions from build.gradle*
5. Clean up after: `rm -rf /tmp/buildSkillDocs-extract/<repo-name>`

## Extraction rules

Extract ONLY actionable guidance. For every rule include:
- **WHY** it matters (root cause, not just "it's recommended")
- **EXCEPTION** if the rule doesn't always apply (optional)
- **Before/After** when showing a migration from old to new pattern (optional)

Skip:
- Explanatory prose
- History
- Setup instructions — UNLESS showing the current correct version

Focus on:
- **Rules**: DO/DON'T with WHY and optional EXCEPTION
- **Before/After**: Old way vs new way with WHY the change matters
- **Patterns**: Minimal code examples from repos showing the correct implementation
- **Decision tables**: When to use X vs Y
- **Pitfalls**: Common mistakes with WHY they're wrong
- **Versions**: Current recommended library versions
- **Version requirements**: Tag rules that only apply to specific SDK/language versions

## Output format

Return a YAML block:

```yaml
topic: "<topic>"
source: "<url>"
source_priority: "<official|team|reference|community>"
extracted:
  rules:
    - rule: "Description"
      type: do|dont
      confidence: high|medium|low
      why: "Root cause explanation"
      exception: "When this rule doesn't apply"   # optional
      requires:                                     # optional
        min_sdk: 29
  before_after:
    - name: "Pattern name"
      before: |
        // old code
      after: |
        // new code
      why: "Why the new way is better"
  patterns:
    - name: "Pattern name"
      code: |
        // From: path/to/File.kt
        // minimal code showing the pattern
      context: "One-line explanation of what matters"
  decision_tables:
    - question: "When to use X vs Y?"
      options:
        - use: "X"
          when: "condition"
        - use: "Y"
          when: "condition"
  pitfalls:
    - description: "What goes wrong"
      why: "Root cause"
  versions:
    - library: "library-name"
      version: "x.y.z"
```

## Knowledge file output

After extraction, write a markdown knowledge file to `knowledge/<topic>/<source_slug>.md` with this format:

```markdown
<!-- Source: <url> -->
<!-- Priority: <priority> -->
<!-- Fetched: <today's date> -->
<!-- TTL: <ttl_days> days — re-fetch after <date> -->
<!-- Verified: trusted|pending -->

# <Topic> — <Source Name>

## Rules
- DO: <rule>
  WHY: <reason>
  EXCEPTION: <exception if any>

- DON'T: <rule>
  WHY: <reason>

## Before/After
❌ Old way:
<code>

✅ New way:
<code>

## Patterns
```<language>
// From: path/to/File.kt
<code snippet>
```
> Key: <what matters about this snippet>

## Decision table
| Need | Use | Not |
|---|---|---|
| ... | ... | ... |

## Pitfalls
- <pitfall>
  WHY: <reason>

## Versions
- <library>: <version>
```

## Token budget

Max ~800 tokens per output knowledge file. Prioritize:
1. High-confidence rules with WHY
2. Decision tables
3. Pitfalls with WHY
4. Before/After examples
5. Code snippet patterns
6. Versions
```

- [ ] **Step 2: Commit**

```bash
git add agents/doc-extractor/agent.md
git commit -m "feat: update doc-extractor with why annotations, before/after, code snippets"
```

---

### Task 4: Update keyword-scanner agent

Add Priority and Fresh columns to output for the new index format.

**Files:**
- Modify: `agents/keyword-scanner/agent.md`

- [ ] **Step 1: Update keyword-scanner output format**

Read the existing file, then add to the output format section:

The agent's YAML output should now also include:
```yaml
keywords: ["keyword1", "keyword2", ...]
topic: "suggested-topic-name"
priority: "<source priority>"
sub_pages: [...]          # doc only
directories: [...]        # repo only
```

And the agent should include `priority` in its output so `/add-source` can populate the Priority column in index.md.

Update the index.md row format instruction to:
```
| <keywords csv> | <topic> | <url or repo> | <priority> | no | — |
```

- [ ] **Step 2: Commit**

```bash
git add agents/keyword-scanner/agent.md
git commit -m "feat: update keyword-scanner for new index format"
```

---

### Task 5: Update /add-source command

Add TTL defaults by priority, `verified` field for community sources, team priority support, and `file://` local path support.

**Files:**
- Modify: `commands/add-source.md`

- [ ] **Step 1: Rewrite add-source command**

Key changes from v1:
- Add `--priority team` option
- Support `file://` URLs for local files (team priority)
- Set `ttl_days` default based on priority: official=30, team=90, reference=14, community=90
- Add `verified: false` for community sources
- Update sources.yaml entry format with `ttl_days` and `verified` fields
- Update index.md row to include Priority and Fresh columns
- Update sync-state.yaml entry with `fetched_at`, `ttl_days`, `verified` fields
- Topic normalization: convert to kebab-case lowercase

The full command content should match the spec's sources.yaml schema and sync-state.yaml schema exactly.

- [ ] **Step 2: Commit**

```bash
git add commands/add-source.md
git commit -m "feat: update /add-source with TTL, verification, team priority"
```

---

### Task 6: Update /generate command

Output per-source knowledge files (in topic directories). Spawn source-verifier for community sources after extraction.

**Files:**
- Modify: `commands/generate.md`

- [ ] **Step 1: Rewrite generate command**

Key changes from v1:
- Knowledge output is now per-source: `knowledge/<topic>/<source-slug>.md`
- Create topic directory if it doesn't exist
- After extracting a community source, spawn `source-verifier` agent to verify rules against official sources
- Update the knowledge file's `Verified` metadata based on verifier results
- Update sync-state.yaml with `fetched_at` date and `verified` status
- Update index.md Fresh column based on fetched_at + ttl_days

- [ ] **Step 2: Commit**

```bash
git add commands/generate.md
git commit -m "feat: update /generate for per-source output and verification"
```

---

### Task 7: Update /update command

Add TTL-aware refresh — only re-fetch sources past their TTL. Re-extract if content changed.

**Files:**
- Modify: `commands/update.md`

- [ ] **Step 1: Rewrite update command**

Key changes from v1:
- Smart update now checks TTL: only re-fetch sources where `fetched_at + ttl_days < today`
- Sources within TTL are skipped (even if hash might have changed)
- `--force` ignores TTL and checks all sources
- When content changed on re-fetch: re-run doc-extractor, re-run source-verifier for community
- When content unchanged: just reset `fetched_at` to today
- Update index.md Fresh column after refresh
- Report format shows fresh/stale/changed/error breakdown

- [ ] **Step 2: Commit**

```bash
git add commands/update.md
git commit -m "feat: update /update with TTL-aware refresh"
```

---

### Task 8: Update /list-sources and /diff commands

Show freshness and verification status.

**Files:**
- Modify: `commands/list-sources.md`
- Modify: `commands/diff.md`

- [ ] **Step 1: Update list-sources**

Add Freshness and Verified columns to the output table:

```
| # | Type | Source | Topic | Priority | Status | Extracted | Fresh | Verified |
```

Fresh shows: "yes", "stale (Nd)", or "—"
Verified shows: "trusted", "verified", "partial", "unverified", or "—"

- [ ] **Step 2: Update diff**

Add freshness info to each source in the output:

```
[clean]     developer.android.com/topic/architecture
            Last checked: 2026-03-20 | Extracted: yes | Fresh: yes (28d left)
```

- [ ] **Step 3: Commit**

```bash
git add commands/list-sources.md commands/diff.md
git commit -m "feat: update /list-sources and /diff with freshness and verification"
```

---

### Task 9: Update /remove-source command

Remove per-source knowledge file (not entire topic directory).

**Files:**
- Modify: `commands/remove-source.md`

- [ ] **Step 1: Update remove-source**

Key changes:
- Remove the specific knowledge file: `knowledge/<topic>/<source-slug>.md`
- Do NOT remove the topic directory if other source files remain
- If topic directory is now empty, remove it
- Update index.md: remove only the row for this source

- [ ] **Step 2: Commit**

```bash
git add commands/remove-source.md
git commit -m "feat: update /remove-source for per-source knowledge files"
```

---

### Task 10: Update best-practices skill

Priority-weighted loading (max 3 files), version-aware filtering, stale notification, never block coding, conflict resolution.

**Files:**
- Modify: `skills/best-practices/skill.md`

- [ ] **Step 1: Rewrite best-practices skill**

```markdown
---
name: best-practices
description: Auto-triggers when writing or modifying code. Reads the knowledge index, matches keywords, loads up to 3 knowledge files sorted by priority, filters by project version, and provides best-practice guidance. Never fetches during coding — uses cached knowledge only, flags stale sources.
---

You are the best-practices skill for the buildSkillDocs plugin.

## When you trigger

- Automatically when writing, modifying, or reviewing code matching file patterns defined in `sources.yaml` under `project.file_patterns`
- Manually when the user says "check docs for X" or "what do the docs say about X"
- In audit mode when user says "check my code against best practices" (see /check command)

## Step 1: Read the index

Read `knowledge/index.md` from the plugin directory.

If `sources.yaml` has no `project.file_patterns` configured, check if the current file extension matches any known pattern. If not, exit silently.

## Step 2: Match keywords

Look at the current task — what code is being written or modified? Match against the Keywords column.

If no keywords match, exit silently.

## Step 3: Load knowledge files (priority-weighted, max 3)

For each matched topic:
1. Find all knowledge files in `knowledge/<topic>/` directory
2. Read each file's metadata header to get Priority
3. Sort by priority: official > team > reference > community
4. Load the top 3 files maximum

**Loading priority:**
1. Always load the `official` file first (highest authority)
2. Load `team` file if exists (company-specific supplements)
3. Load `reference` or verified `community` file if keywords strongly match

**Budget cap: max 3 files loaded per task.**

## Step 4: Check freshness (never block)

For each loaded file, read the `Fetched` and `TTL` metadata:
- If within TTL → use normally
- If past TTL → STILL use it, but collect stale sources for notification

**NEVER fetch or extract during coding.** Always use cached knowledge.

## Step 5: Version-aware filtering

If `sources.yaml` has `project.versions` configured:
- Skip rules tagged with `requires` that the project doesn't meet (e.g., `requires.min_sdk: 29` but project has `min_sdk: 26`)
- Flag library versions in knowledge that are older than project's configured versions

If no `project.versions` configured, skip this step — all rules apply.

## Step 6: Apply knowledge

When applying knowledge to the current task:
- Follow DO rules — use the recommended patterns
- Flag DON'T violations: "Note: official docs recommend X instead of Y (WHY: ...)"
- Reference decision tables when choosing between approaches
- Show Before/After when migrating old patterns
- Mention pitfalls if current code is at risk
- For unverified community rules: "This practice comes from [source], not officially verified"

**Conflict resolution:** If two loaded files give conflicting advice:
1. Higher priority source wins
2. Note: "[lower source] suggests [alternative], but [higher source] recommends [approach] because [WHY]"

Keep it concise — 2-3 relevant rules per task.

## Step 7: Stale notification

At the end of the response, if any loaded sources were past TTL:

"📋 buildSkillDocs: N source(s) for '[topic]' past TTL. Run /update to refresh."

## Important

- This skill adds context, it does not override user instructions
- If the user explicitly chooses a different approach, respect their choice
- The goal is to prevent common mistakes, not dictate every decision
- NEVER fetch pages or extract knowledge during coding
```

- [ ] **Step 2: Commit**

```bash
git add skills/best-practices/skill.md
git commit -m "feat: update skill with priority loading, version filtering, stale notifications"
```

---

## Phase B: New Features

### Task 11: Create source-verifier agent

Verifies community source rules against official knowledge files.

**Files:**
- Create: `agents/source-verifier/agent.md`

- [ ] **Step 1: Create source-verifier agent**

```markdown
---
name: source-verifier
description: Verifies rules extracted from community sources by comparing them against official knowledge files. Tags each rule as verified, unverified, or rejected.
tools:
  - Read
  - Glob
  - Grep
---

You are a source verifier for the buildSkillDocs plugin. Your job is to check whether rules from a community source are consistent with official documentation.

## Input

You will receive:
- `community_knowledge_file`: path to the community source's knowledge file
- `topic`: the topic to verify against
- `knowledge_dir`: path to the knowledge directory

## Process

1. Read the community knowledge file
2. Find all `official` and `team` priority knowledge files in `knowledge/<topic>/` by reading their metadata headers
3. For each rule in the community file, compare against official rules:

   **AGREES with official** → mark as ✅ verified
   The community rule says the same thing as an official rule (possibly different wording).

   **CONTRADICTS official** → mark as ❌ rejected
   The community rule recommends something that official docs explicitly advise against.

   **NEW — not covered by official** → mark as ⚠ unverified
   The community rule covers something official docs don't mention. Could be correct but can't confirm.

   **Can't determine** → mark as ⚠ unverified

4. Also check version compatibility if project versions are provided:
   - Rule requires a higher SDK/language version than the project → flag as incompatible

## Output format

Return a YAML block:

```yaml
verification:
  source: "<community source url>"
  overall_status: "verified" | "partial" | "rejected"
  rules:
    - rule: "Rule text"
      status: "verified" | "unverified" | "rejected"
      reason: "Matches official rule X" | "Contradicts official rule Y" | "Not covered by official docs"
    - ...
  summary:
    verified: 3
    unverified: 2
    rejected: 0
```

## Rules

- Only compare against `official` and `team` knowledge files — never against other `community` files
- A rule is "rejected" ONLY if it directly contradicts an official rule
- "Different approach" is NOT the same as "contradicts" — if official says "use X" and community says "also consider Y for special case", that's unverified, not rejected
- Be conservative: when in doubt, mark as unverified rather than rejected
```

- [ ] **Step 2: Commit**

```bash
git add agents/source-verifier/agent.md
git commit -m "feat: add source-verifier agent for community validation"
```

---

### Task 12: Create /setup command

First-install profile picker.

**Files:**
- Create: `commands/setup.md`

- [ ] **Step 1: Create setup command**

```markdown
---
name: setup
description: First-install setup — pick a tech stack profile to pre-configure sources and knowledge files.
---

You are running the `/setup` command for the buildSkillDocs plugin.

## Process

1. List available profiles by reading directories under `profiles/`:

```
Welcome to buildSkillDocs!

Pick your stack:
  1. Android (Kotlin + Jetpack)
  2. React (TypeScript + Next.js)
  3. Python (Django + FastAPI)
  4. iOS (Swift + SwiftUI)
  5. Custom — start empty, add your own sources

You can always add more sources later with /add-source.
```

2. Use AskUserQuestion to get the user's choice.

3. For the selected profile:
   - Read `profiles/<profile>/sources.yaml`
   - Copy its `project` section and `sources` list into the root `sources.yaml`
   - Copy `profiles/<profile>/knowledge/` contents into root `knowledge/`
   - Update `knowledge/index.md` with entries from the profile's knowledge files

4. Report:
```
Setting up <profile> profile...
Copied N sources and M pre-built knowledge files.
File triggers set to: <file_patterns>

Ready! Your AI now follows <profile> best practices.
Run /list-sources to see what's included.
```

## If sources.yaml already has sources

Ask: "You already have sources configured. Options:"
- "Merge — add profile sources alongside existing ones"
- "Replace — overwrite with profile sources"
- "Cancel"

## If custom is selected

Set up an empty project config:
```yaml
project:
  name: ""
  file_patterns: []
  versions: {}

sources: []
```

Ask: "What file extensions should trigger best-practice guidance? (e.g., *.kt, *.java)"
Set `file_patterns` based on answer.
```

- [ ] **Step 2: Commit**

```bash
git add commands/setup.md
git commit -m "feat: add /setup command for profile selection"
```

---

### Task 13: Create /check command

Best-practice linter mode — audit current code against knowledge files.

**Files:**
- Create: `commands/check.md`

- [ ] **Step 1: Create check command**

```markdown
---
name: check
description: Audit current code against best-practice knowledge files. Acts as a linter — reads code and reports violations with sources and explanations.
---

You are running the `/check` command for the buildSkillDocs plugin.

## Process

1. Determine what to check:
   - If a file is currently open/being discussed, check that file
   - If the user specified a file path, check that file
   - Otherwise, ask: "Which file should I check?"

2. Read the file content

3. Identify which topics are relevant based on the code (e.g., Kotlin file with ViewModel → architecture topic)

4. Load ALL knowledge files for matched topics (not limited to 3 — this is an audit, not inline guidance)

5. For each best-practice rule in the loaded knowledge:
   - Check if the code follows it → ✅
   - Check if the code violates it → ⚠ with line number, rule source, and WHY

6. Report:

```
Checking: <filename>

  ⚠ Line N: <violation description>
    Source: <topic>/<source-slug>.md (<priority>)
    WHY: <explanation>

  ⚠ Line N: <violation description>
    Source: <topic>/<source-slug>.md (<priority>)
    WHY: <explanation>

  ✅ Line N: <what's correct>
  ✅ Line N: <what's correct>

Score: X/Y practices followed
```

7. Only report violations for rules with `confidence: high`. Medium/low confidence rules are informational only.

## Rules

- This is read-only — do NOT modify any code
- Show both violations AND correct practices (positive feedback matters)
- For unverified community rules, note: "(unverified — from community source)"
- Skip rules that don't apply to this file/code
- Version-aware: skip rules the project doesn't meet version requirements for
```

- [ ] **Step 2: Commit**

```bash
git add commands/check.md
git commit -m "feat: add /check command for best-practice auditing"
```

---

### Task 14: Create starter profiles

Create the profile directory structure with sources.yaml for each stack. Knowledge files will be pre-built later via /generate.

**Files:**
- Create: `profiles/android/sources.yaml`
- Create: `profiles/react/sources.yaml`
- Create: `profiles/python/sources.yaml`
- Create: `profiles/ios/sources.yaml`
- Create: `profiles/custom/sources.yaml`
- Create: empty `profiles/*/knowledge/` directories (with .gitkeep)

- [ ] **Step 1: Create Android profile**

```yaml
project:
  name: "android"
  file_patterns: ["*.kt", "*.java", "*.xml", "*.gradle*"]
  versions: {}

sources:
  - type: doc
    url: "https://developer.android.com/topic/architecture"
    topics: [architecture]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://developer.android.com/kotlin/coroutines"
    topics: [concurrency]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://developer.android.com/topic/libraries/architecture/workmanager"
    topics: [background-work]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://developer.android.com/training/data-storage/room"
    topics: [data-persistence]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://developer.android.com/guide/navigation"
    topics: [navigation]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://dagger.dev/hilt/quick-start"
    topics: [dependency-injection]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: repo
    repo: "google/nowinandroid"
    topics: [architecture, compose]
    paths: ["app/src/main", "core/*/src/main", "*.md"]
    priority: reference
    ttl_days: 14
    last_synced: null
    extracted: false
```

- [ ] **Step 2: Create React profile**

```yaml
project:
  name: "react"
  file_patterns: ["*.tsx", "*.ts", "*.jsx", "*.js", "*.css"]
  versions: {}

sources:
  - type: doc
    url: "https://react.dev/learn"
    topics: [react-fundamentals]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://react.dev/reference/react/hooks"
    topics: [hooks]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://nextjs.org/docs/app"
    topics: [nextjs]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false
```

- [ ] **Step 3: Create Python profile**

```yaml
project:
  name: "python"
  file_patterns: ["*.py", "*.yaml", "*.toml"]
  versions: {}

sources:
  - type: doc
    url: "https://docs.python.org/3/library/typing.html"
    topics: [typing]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://fastapi.tiangolo.com/tutorial/"
    topics: [fastapi]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://docs.djangoproject.com/en/5.0/"
    topics: [django]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false
```

- [ ] **Step 4: Create iOS profile**

```yaml
project:
  name: "ios"
  file_patterns: ["*.swift", "*.storyboard", "*.xib"]
  versions: {}

sources:
  - type: doc
    url: "https://developer.apple.com/documentation/swiftui"
    topics: [swiftui]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false

  - type: doc
    url: "https://developer.apple.com/documentation/combine"
    topics: [concurrency]
    priority: official
    ttl_days: 30
    last_synced: null
    extracted: false
```

- [ ] **Step 5: Create Custom profile (empty)**

```yaml
project:
  name: ""
  file_patterns: []
  versions: {}

sources: []
```

- [ ] **Step 6: Create .gitkeep files for empty knowledge directories**

```bash
mkdir -p profiles/android/knowledge profiles/react/knowledge profiles/python/knowledge profiles/ios/knowledge profiles/custom/knowledge
touch profiles/android/knowledge/.gitkeep profiles/react/knowledge/.gitkeep profiles/python/knowledge/.gitkeep profiles/ios/knowledge/.gitkeep profiles/custom/knowledge/.gitkeep
```

- [ ] **Step 7: Commit**

```bash
git add profiles/
git commit -m "feat: add starter profiles for Android, React, Python, iOS, Custom"
```

---

### Task 15: Update plugin.json and CLAUDE.md

Register new commands, agent, and configurable triggers.

**Files:**
- Modify: `plugin.json`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update plugin.json**

```json
{
  "name": "buildSkillDocs",
  "version": "0.2.0",
  "description": "Indexes official docs and GitHub repos, extracts best-practice knowledge on-demand to guide AI coding. Supports any tech stack with starter profiles.",
  "commands": [
    "commands/setup.md",
    "commands/add-source.md",
    "commands/list-sources.md",
    "commands/generate.md",
    "commands/update.md",
    "commands/diff.md",
    "commands/remove-source.md",
    "commands/check.md"
  ],
  "skills": [
    "skills/best-practices/skill.md"
  ],
  "agents": [
    "agents/doc-extractor/agent.md",
    "agents/keyword-scanner/agent.md",
    "agents/source-verifier/agent.md"
  ]
}
```

- [ ] **Step 2: Update CLAUDE.md**

```markdown
# buildSkillDocs Plugin

## Auto-trigger dispatch

The skill triggers based on `project.file_patterns` configured in `sources.yaml`.

| Condition | Action |
|---|---|
| Writing, modifying, or reviewing code matching project.file_patterns | Invoke buildSkillDocs:best-practices skill |
| User says "check docs for X" or "what do the docs say about X" | Invoke buildSkillDocs:best-practices skill |
| User says "check my code" or "audit best practices" | Run /check command |

If `project.file_patterns` is empty or not configured, the skill does not auto-trigger. Run /setup to configure.

## Data files

- `sources.yaml` — project config + registered sources. Edit project section manually or via /setup. Sources managed via /add-source and /remove-source.
- `knowledge/index.md` — keyword index. Auto-generated by /add-source.
- `knowledge/<topic>/<source>.md` — per-source knowledge files. Auto-generated by /generate.
- `.cache/sync-state.yaml` — content hashes, TTL dates, verification status. Auto-managed.
- `profiles/` — starter packs for different tech stacks. Used by /setup.
```

- [ ] **Step 3: Commit**

```bash
git add plugin.json CLAUDE.md
git commit -m "feat: update manifest and dispatch for v0.2"
```

---

### Task 16: Update README

Document all new features.

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite README**

```markdown
# buildSkillDocs

A Claude Code plugin that gives AI up-to-date best-practice knowledge from official docs, GitHub repos, and trusted sources — for any tech stack.

## Problem

AI coding assistants use outdated patterns because their training data is frozen in time. You have to manually provide doc links to get correct code.

## Solution

buildSkillDocs indexes your documentation sources and delivers best-practice guidance while you code:

- **Per-source knowledge** — each source gets its own condensed file with rules, WHY annotations, and code examples
- **Priority-weighted** — official docs first, then team rules, then reference repos, then verified community
- **Smart freshness** — TTL-based staleness tracking, never blocks coding
- **Source verification** — community sources checked against official docs
- **Any tech stack** — configurable file triggers with starter profiles

## Quick Start

```bash
# Install
claude plugin add your-username/buildSkillDocs

# Pick your stack
/setup

# Start coding — AI automatically follows best practices
```

## Add More Sources

```bash
/add-source --doc "https://developer.android.com/topic/architecture"
/add-source --repo "google/nowinandroid"
/add-source --doc "https://medium.com/@someone/article" --priority community
/add-source --doc "file:///path/to/team-rules.md" --priority team
```

## Commands

| Command | Description |
|---|---|
| `/setup` | Pick a tech stack profile |
| `/add-source` | Register a doc URL or GitHub repo |
| `/list-sources` | Show all sources with freshness and verification |
| `/generate` | Force extract best practices from sources |
| `/update` | Refresh stale sources (past TTL) |
| `/diff` | Show cached source status |
| `/remove-source` | Remove a source |
| `/check` | Audit current code against best practices |

## How It Works

1. **Add sources** — official docs, repos, blogs
2. **Extract** — AI reads sources, saves condensed rules with WHY annotations
3. **Verify** — community sources checked against official docs
4. **Code** — AI auto-loads relevant rules while you work (max 3 files, ~2400 tokens)
5. **Stay fresh** — TTL tracks staleness, /update refreshes

See [Design Spec](docs/superpowers/specs/2026-03-21-buildSkillDocs-design.md) for full architecture.

## Contributing

Add a starter profile for your tech stack! Create a PR with:
- `profiles/<stack>/sources.yaml` — sources for the stack
- `profiles/<stack>/knowledge/` — pre-built knowledge files (optional)
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README for v0.2 features"
```
