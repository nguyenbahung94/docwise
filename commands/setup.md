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
