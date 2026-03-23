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

## Step 2: Match concepts via graph

Read `knowledge/graph.yaml` from the plugin directory.

Look at the current task — what code is being written or modified? Match against concept nodes in the graph:
- If the user is writing a ViewModel → match "ViewModel" node
- If working with Room → match "Room" node
- If using coroutines → match "StateFlow", "Flow", "suspend" nodes

If `graph.yaml` doesn't exist or is empty, fall back to keyword matching via `knowledge/index.md`.

If no concepts match, this skill has nothing to contribute — exit silently.

## Step 3: Traverse graph and load knowledge files (max 3)

From each matched concept node, traverse up to 2 hops:
- 1st hop: directly connected concepts
- 2nd hop: concepts connected to 1st-hop concepts

Example: "ViewModel" matched →
  1st hop: StateFlow, UseCase, Hilt
  2nd hop: Repository (via UseCase), LiveData (via StateFlow)

Collect all knowledge files referenced by traversed nodes (from the `files` field in graph.yaml).

Sort collected files by priority: official > team > reference > community.

Load the top 3 files maximum.

If a file is from a community source, check its verification status in the metadata header.

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
