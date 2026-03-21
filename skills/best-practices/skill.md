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
