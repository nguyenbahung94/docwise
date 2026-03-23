---
name: check
description: Audit current code against best-practice knowledge files. Acts as a linter — reads code and reports violations with sources and explanations.
---

You are running the `/check` command for the docwise plugin.

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
