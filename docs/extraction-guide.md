# Docwise Extraction Guide

## Lessons Learned

### What Python regex extraction CANNOT do
- Understand WHY an API exists
- Build mental models (when to use X vs Y)
- Detect relationships between APIs (X = Y + Z internally)
- Identify subtle behaviors (snapshotFlow only emits when State read INSIDE block changes)
- Explain cost/performance (WHY something is expensive — what gets allocated)
- Connect to architecture (how topic fits with ViewModel, Navigation, Hilt)
- Detect anti-patterns that LOOK correct but break in edge cases

### What Python regex extraction CAN do well
- Extract code blocks, headings, warnings, tables
- Filter language tabs (Kotlin > Java > Groovy)
- Detect DO/DON'T rules from text patterns
- Extract pitfalls from warning/caution boxes
- Build concepts list from headings

### Rule: Always use 2-pass LLM enhancement
- Pass 1: Generate semantic sections (Mental Model, Lifecycle, Decisions, etc.)
- Pass 2: Self-review with checklist to find gaps
- Never trust single-pass output — it's always shallow

---

## LLM Prompt Design Rules

### 1. Force self-questioning BEFORE writing
Bad: "Write a mental model for this topic"
Good: "Ask yourself these 8 questions, THEN write based on your answers"

Why: LLMs skip thinking if you let them. Forcing questions = forcing depth.

### 2. Be specific about output structure
Bad: "Add a decision framework"
Good: "Table with columns: I need to... | Use | NOT | Because"

Why: Vague instructions get vague output. Format = quality.

### 3. Name what's MISSING, not what to write
Bad: "Write about lifecycle timing"
Good: "For EVERY API mentioned, is the exact trigger/cancel/restart timing documented? If any API is missing timing info, add it."

Why: Review mindset > generation mindset. Finding gaps > filling space.

### 4. Require specificity constraints
Bad: "Be concise"
Good: "Every claim must name the API, the callback, and the dispatcher. No 'ensure proper handling'."

Why: LLMs default to vague corporate language. Ban it explicitly.

### 5. Use checklist for review pass
The review prompt should check:
1. Lifecycle timing — is every API's trigger/cancel/restart documented?
2. Direct comparisons — are confusable API pairs compared head-to-head?
3. Internal mechanics — is "expensive" explained with WHAT gets allocated?
4. Subtle behaviors — edge cases that only show up in production?
5. Architecture integration — ViewModel, Navigation, DI, Testing connections?
6. Missing APIs — any API in code but not analyzed?
7. Anti-pattern depth — exact failure mode, not just "can cause issues"?

### 6. Multi-pass > single-pass with bigger prompt
- Pass 1 with a focused prompt > 1 giant prompt trying to do everything
- Review pass catches things the first pass missed
- Diminishing returns after 2-3 passes

### 7. Local LLM (14B) is sufficient with good prompts
- Qwen 2.5 14B produces good output when prompted correctly
- 32B is too slow on 32GB RAM (swap kills performance)
- Quality comes from prompt design, not model size (within reason)

---

## Extraction Pipeline

```
Page URL
  │
  ├─ Step 1: Python script (0 tokens, 0 cost)
  │   keyword_scanner.py → keywords, sub-pages
  │   doc_extractor.py → rules, code, pitfalls, guidelines
  │
  ├─ Step 2: Local LLM Pass 1 (0 API tokens)
  │   llm_summarizer.py --passes 1
  │   → Mental Model, Lifecycle, Decisions, Composition,
  │     Cost, Anti-Patterns, Relationships
  │
  ├─ Step 3: Local LLM Pass 2 (0 API tokens)
  │   llm_summarizer.py --passes 2
  │   → Review checklist finds gaps
  │   → Deepens: comparisons, subtle behaviors, architecture
  │
  └─ Output: Complete knowledge file
      0 API tokens spent. All local.
```

## Token Cost Comparison

| Approach | Per page | 20 pages |
|----------|---------|----------|
| LLM agent (old) | ~25K tokens | ~500K tokens ($$$) |
| Python + Claude API | ~8K tokens | ~160K tokens ($$) |
| Python + Local LLM | 0 tokens | 0 tokens (free) |

---

## Quality Checklist for Knowledge Files

Before considering a knowledge file "done", verify:

- [ ] Mental Model explains WHY the topic exists (the problem it solves)
- [ ] Every API has lifecycle timing (trigger, cancel, restart)
- [ ] Confusable API pairs have direct comparison tables
- [ ] Internal composition documented (X = Y + Z)
- [ ] Performance costs explained (what gets allocated, why expensive)
- [ ] At least 3 anti-patterns with Looks like / Why breaks / Fix
- [ ] Architecture context (ViewModel, Navigation, DI, Testing)
- [ ] Subtle behaviors / edge cases documented
- [ ] No Java/Groovy code — Kotlin only
- [ ] No noise (Android Developers, Content License, SideEffectsSnippets.kt)
