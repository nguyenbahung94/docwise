---
name: add-source
description: Register a documentation page or GitHub repo as a knowledge source. Scans for keywords (Tier 1), discovers sub-pages/directories, and lets user pick what to include.
arguments:
  - name: --doc
    description: URL of a documentation page (http/https) or local file path (file://)
    required: false
  - name: --repo
    description: GitHub repo in "owner/name" format
    required: false
  - name: --topic
    description: Topic to assign this source to (e.g., "architecture", "concurrency")
    required: false
  - name: --priority
    description: Source priority — official, team, reference, or community
    required: false
---

You are running the `/add-source` command for the docwise plugin.

## Validation

1. Exactly one of `--doc` or `--repo` must be provided. If neither or both, show usage and stop.
2. If `--doc` is provided:
   - It must be a valid URL starting with `http://`, `https://`, or `file://`
   - `file://` URLs are treated as local files (team priority by default)
3. If `--repo` is provided, it must be in `owner/name` format
4. Check `sources.yaml` for duplicates:
   - Read all existing source entries
   - For doc sources: normalize the URL before comparing (strip trailing slash, lowercase hostname, remove fragments like `#section`)
   - For repo sources: compare `owner/name` case-insensitively
   - If a match is found, inform user: "Source already exists: [url]. Use /remove-source first if you want to re-add it." and stop.

## Default priority

- `--doc` with `http://` or `https://` defaults to `official`
- `--doc` with `file://` defaults to `team`
- `--repo` defaults to `reference`
- User can override with `--priority`

## TTL defaults by priority

| Priority | ttl_days |
|----------|----------|
| official | 30 |
| team | 90 |
| reference | 14 |
| community | 90 |

## Topic normalization

Convert the topic to kebab-case lowercase. Examples:
- "Android Architecture" → "android-architecture"
- "Concurrency" → "concurrency"
- "ViewModels" → "viewmodels"

## Process

### For doc sources:

1. Spawn the `keyword-scanner` agent with:
   - source_type: "doc"
   - source_url: the provided URL
   - source_topic: the --topic value (if provided)

2. The agent returns keywords, suggested topic, and discovered sub-pages.

3. If sub-pages were found:

   a. **Check for duplicates first.** For each discovered sub-page, normalize the URL and compare against ALL existing sources in `sources.yaml`. Mark already-registered sub-pages with `[exists]`.

   b. Present them to the user:
   ```
   Scanning page... Found N sub-pages:
     1. [title] — [url]
     2. [title] — [url]
     3. [title] — [url] [exists — already registered]
     4. [title] — [url]
     ...

   Add all new? Or pick specific ones? (all / 1,2,4 / none)
   Already registered sub-pages (3) will be skipped.
   [Default: all new]
   ```
   Use AskUserQuestion to get the user's choice.

   c. Skip any sub-pages marked `[exists]` — never create duplicate entries.

4. For the parent page + each selected NEW sub-page:
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
Added [N] source(s) to docwise:
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
  priority: <official|team|reference|community>
  ttl_days: <30|90|14|90>
  verified: <false if community, omit otherwise>
  last_synced: null
  extracted: false
```

### sources.yaml entry (repo):
```yaml
- type: repo
  repo: "<owner/name>"
  topics: [<topic>]
  paths: [<selected paths>]
  priority: <official|team|reference|community>
  ttl_days: <30|90|14|90>
  verified: <false if community, omit otherwise>
  last_synced: null
  extracted: false
```

Note: `verified: false` is only added for `community` priority sources. Official, team, and reference sources omit the `verified` field.

### knowledge/index.md row:
```
| <keywords csv> | <topic> | <url or repo> | <priority> | no | — |
```

### .cache/sync-state.yaml entry (doc):
```yaml
- type: doc
  url: "<url>"
  content_hash: "<hash of fetched content>"
  fetched_at: "<today>"
  ttl_days: <ttl_days>
  verified: <false if community, omit otherwise>
  last_checked: "<today>"
  last_changed: "<today>"
  status: clean
  extracted: false
  error: null
```

### .cache/sync-state.yaml entry (repo):
```yaml
- type: repo
  repo: "<owner/name>"
  last_commit: "<HEAD commit SHA>"
  fetched_at: "<today>"
  ttl_days: <ttl_days>
  verified: <false if community, omit otherwise>
  last_checked: "<today>"
  last_changed: "<today>"
  status: clean
  extracted: false
  error: null
```
