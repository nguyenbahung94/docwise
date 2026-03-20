---
name: add-source
description: Register a documentation page or GitHub repo as a knowledge source. Scans for keywords (Tier 1), discovers sub-pages/directories, and lets user pick what to include.
arguments:
  - name: --doc
    description: URL of a documentation page
    required: false
  - name: --repo
    description: GitHub repo in "owner/name" format
    required: false
  - name: --topic
    description: Topic to assign this source to (e.g., "architecture", "concurrency")
    required: false
  - name: --priority
    description: Source priority — official, reference, or community
    required: false
---

You are running the `/add-source` command for the buildSkillDocs plugin.

## Validation

1. Exactly one of `--doc` or `--repo` must be provided. If neither or both, show usage and stop.
2. If `--doc` is provided, it must be a valid URL starting with `http://` or `https://`
3. If `--repo` is provided, it must be in `owner/name` format
4. Check `sources.yaml` for duplicates. If the source already exists, inform user and stop.

## Default priority

- `--doc` defaults to `official`
- `--repo` defaults to `reference`
- User can override with `--priority`

## Process

### For doc sources:

1. Spawn the `keyword-scanner` agent with:
   - source_type: "doc"
   - source_url: the provided URL
   - source_topic: the --topic value (if provided)

2. The agent returns keywords, suggested topic, and discovered sub-pages.

3. If sub-pages were found, present them to the user:
   ```
   Scanning page... Found N sub-pages:
     1. [title] — [url]
     2. [title] — [url]
     ...

   Add all? Or pick specific ones? (all / 1,3,5 / none)
   [Default: all]
   ```
   Use AskUserQuestion to get the user's choice.

4. For the parent page + each selected sub-page:
   - Add entry to `sources.yaml`
   - Add keyword row to `knowledge/index.md`
   - Add entry to `.cache/sync-state.yaml` with `extracted: false`

### For repo sources:

1. Spawn the `keyword-scanner` agent with:
   - source_type: "repo"
   - source_url: the provided repo
   - source_paths: default ["**/*.md", "**/*.kt", "**/build.gradle*"]
   - source_topic: the --topic value (if provided)

2. The agent returns keywords, suggested topic, and discovered directories.

3. Present directories to the user:
   ```
   Scanning repo structure... Key directories found:
     1. [path] — [description]
     2. [path] — [description]
     ...

   Include all? Or pick specific ones? (all / 1,2,3 / none)
   [Default: all]
   ```
   Use AskUserQuestion to get the user's choice.

4. Add single entry to `sources.yaml` with selected paths in the `paths` field.
5. Add keyword row to `knowledge/index.md`
6. Add entry to `.cache/sync-state.yaml` with `extracted: false`

## After adding

Report:
```
Added [N] source(s) to buildSkillDocs:
  - [url/repo] → topic: [topic] (keywords: [count])

Index updated. Knowledge will be extracted on-demand when you code in this area.
To force extraction now: /generate --topic [topic]
```

## File updates

### sources.yaml entry (doc):
```yaml
- type: doc
  url: "<url>"
  topics: [<topic>]
  priority: <official|reference|community>
  last_synced: null
  extracted: false
```

### sources.yaml entry (repo):
```yaml
- type: repo
  repo: "<owner/name>"
  topics: [<topic>]
  paths: [<selected paths>]
  priority: <official|reference|community>
  last_synced: null
  extracted: false
```

### knowledge/index.md row:
```
| <keywords csv> | <topic> | <url or repo> | no |
```

### .cache/sync-state.yaml entry:
```yaml
- type: <doc|repo>
  url: "<url>"        # or repo: "<owner/name>"
  content_hash: "<hash of fetched content>"
  last_checked: "<today>"
  last_changed: "<today>"
  status: clean
  extracted: false
  error: null
```
