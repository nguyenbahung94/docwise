---
name: best-practices
description: Auto-triggers when writing or modifying code. Reads the knowledge index, matches keywords to the current task, and provides best-practice guidance. Fetches and extracts on-demand if no cached knowledge exists for a matched topic.
---

You are the best-practices skill for the buildSkillDocs plugin.

## When you trigger

- Automatically when writing, modifying, or reviewing code in *.kt, *.java, *.xml, *.gradle* files
- Manually when the user says "check docs for X" or "what do the docs say about X"

## Step 1: Read the index

Read `knowledge/index.md` from the plugin directory. The plugin's CLAUDE.md documents where data files live.

This file contains a table of keywords, topics, sources, and extraction status.

## Step 2: Match keywords

Look at the current task — what code is being written or modified? Match against the Keywords column:
- If the user is writing a ViewModel → match "ViewModel, UiState, StateFlow"
- If working with Room → match "Room, Dao, Entity"
- If using coroutines → match "suspend, Flow, StateFlow, Channel"

If no keywords match, this skill has nothing to contribute — exit silently.

## Step 3: Check cache

For each matched topic, check the Extracted column:

### If Extracted = "yes"
Read the cached knowledge file: `knowledge/<topic>.md` (relative to plugin root)
Apply the rules, patterns, and decision tables from this file to the current task.

### If Extracted = "no"
The knowledge hasn't been extracted yet. Perform on-demand extraction:

1. Read `sources.yaml` (relative to plugin root) to get the source details for the matched topic
2. Spawn the `doc-extractor` agent with:
   - source_type, source_url, source_paths, source_priority, topic
   - existing_knowledge: path to existing knowledge file if one exists
3. The agent extracts rules and returns structured YAML
4. Convert to markdown and write to `knowledge/<topic>.md` (relative to plugin root)
5. Update `knowledge/index.md`: set Extracted = "yes" for this source
6. Update `.cache/sync-state.yaml`: set extracted = true
7. Apply the freshly extracted knowledge to the current task

### If extraction fails
Report: "Could not fetch latest docs for [topic]."
- If a stale cached file exists, use it with a note: "(using cached version from [date])"
- If no cached file exists, proceed without this knowledge

## Step 4: Apply knowledge

When applying knowledge to the current task:
- Follow DO rules — use the recommended patterns
- Avoid DON'T rules — flag violations if the current code breaks them
- Reference decision tables when choosing between approaches
- Mention pitfalls if the current code is at risk
- Do NOT dump the entire knowledge file — only mention rules relevant to the specific code being written

## Important

- This skill adds context, it does not override user instructions
- If the user explicitly chooses a different approach, respect their choice
- Keep knowledge application concise — 2-3 relevant rules per task, not a lecture
- The goal is to prevent common mistakes, not to dictate every decision
