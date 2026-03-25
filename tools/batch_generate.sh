#!/bin/bash
# Batch generate all pending topics
# Usage: bash tools/batch_generate.sh [--no-enhance]
#
# With --no-enhance: Python-only extraction (fast, ~2 min total)
# Without flag: Python + Ollama 4-pass (slow, ~80 min total)

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KNOWLEDGE_DIR="${1:-/Users/bahung/knowledge}"
MODEL="qwen2.5:14b"
ENHANCE="--enhance --model $MODEL"

if [[ "$1" == "--no-enhance" || "$2" == "--no-enhance" ]]; then
  ENHANCE=""
  echo "[batch] Mode: Python-only (no LLM)"
else
  echo "[batch] Mode: Python + Ollama 4-pass ($MODEL)"
fi

# Track results
PASS=0
FAIL=0
SKIP=0

run_topic() {
  local name="$1"
  local output="$2"
  shift 2
  local urls="$@"

  # Skip if already has enhanced file (contains "## Core Concepts" or "## Mental Model")
  local outfile="$output/${name}.md"
  if [[ -f "$outfile" ]] && grep -q "## Core Concepts\|## Mental Model" "$outfile" 2>/dev/null; then
    echo "[batch] SKIP $name (already enhanced)"
    SKIP=$((SKIP + 1))
    return
  fi

  echo ""
  echo "================================================================"
  echo "[batch] Generating: $name"
  echo "================================================================"

  if python3 "$SCRIPT_DIR/topic_extractor.py" \
    --urls "$urls" \
    --topic "$name" \
    --output "$output" \
    $ENHANCE 2>&1; then
    echo "[batch] OK: $name"
    PASS=$((PASS + 1))
  else
    echo "[batch] FAIL: $name"
    FAIL=$((FAIL + 1))
  fi
}

# ── Group 1: Kotlin Core ──────────────────────────────────────────
run_topic "kotlin-flow" "$KNOWLEDGE_DIR/kotlin-flow" \
  "https://kotlinlang.org/docs/flow.html"

# ── Group 2: Android Architecture ─────────────────────────────────
run_topic "android-lifecycle" "$KNOWLEDGE_DIR/android-lifecycle" \
  "https://developer.android.com/topic/libraries/architecture/lifecycle"

run_topic "hilt" "$KNOWLEDGE_DIR/hilt" \
  "https://developer.android.com/training/dependency-injection/hilt-android"

run_topic "android-architecture" "$KNOWLEDGE_DIR/android-architecture" \
  "https://developer.android.com/topic/architecture"

# ── Group 3: Compose Core (merged) ────────────────────────────────
run_topic "compose-state" "$KNOWLEDGE_DIR/compose-state" \
  "https://developer.android.com/develop/ui/compose/state,https://developer.android.com/develop/ui/compose/state-hoisting,https://developer.android.com/develop/ui/compose/state-saving,https://developer.android.com/develop/ui/compose/state-lifespans,https://developer.android.com/develop/ui/compose/state-callbacks"

run_topic "compose-lifecycle" "$KNOWLEDGE_DIR/compose-lifecycle" \
  "https://developer.android.com/develop/ui/compose/lifecycle"

run_topic "compose-side-effects" "$KNOWLEDGE_DIR/compose-side-effects" \
  "https://developer.android.com/develop/ui/compose/side-effects"

run_topic "compose-phases" "$KNOWLEDGE_DIR/compose-phases" \
  "https://developer.android.com/develop/ui/compose/phases"

run_topic "compose-compositionlocal" "$KNOWLEDGE_DIR/compose-compositionlocal" \
  "https://developer.android.com/develop/ui/compose/compositionlocal"

run_topic "compose-navigation" "$KNOWLEDGE_DIR/compose-navigation" \
  "https://developer.android.com/develop/ui/compose/navigation"

# ── Group 4: Compose Setup ────────────────────────────────────────
run_topic "jetpack-compose" "$KNOWLEDGE_DIR/jetpack-compose" \
  "https://developer.android.com/develop/ui/compose"

run_topic "material-design-3" "$KNOWLEDGE_DIR/material-design-3" \
  "https://developer.android.com/develop/ui/compose/designsystems/material3"

run_topic "kotlin-ksp" "$KNOWLEDGE_DIR/kotlin-ksp" \
  "https://kotlinlang.org/docs/ksp-overview.html"

# ── Group 5: Room (merged) ────────────────────────────────────────
run_topic "room" "$KNOWLEDGE_DIR/room" \
  "https://developer.android.com/training/data-storage/room,https://developer.android.com/training/data-storage/room/defining-data,https://developer.android.com/training/data-storage/room/accessing-data,https://developer.android.com/training/data-storage/room/relationships/one-to-one,https://developer.android.com/training/data-storage/room/relationships/one-to-many,https://developer.android.com/training/data-storage/room/relationships/many-to-many,https://developer.android.com/training/data-storage/room/relationships/nested,https://developer.android.com/training/data-storage/room/async-queries,https://developer.android.com/training/data-storage/room/creating-views,https://developer.android.com/training/data-storage/room/prepopulate,https://developer.android.com/training/data-storage/room/migrating-db-versions,https://developer.android.com/training/data-storage/room/testing-db,https://developer.android.com/training/data-storage/room/referencing-data,https://developer.android.com/training/data-storage/room/sqlite-room-migration"

# ── Group 6: Data Storage (merged) ────────────────────────────────
run_topic "data-storage" "$KNOWLEDGE_DIR/data-storage" \
  "https://developer.android.com/training/data-storage,https://developer.android.com/training/data-storage/app-specific,https://developer.android.com/training/data-storage/shared,https://developer.android.com/training/data-storage/shared/media,https://developer.android.com/training/data-storage/shared/photo-picker,https://developer.android.com/training/data-storage/shared/documents-files,https://developer.android.com/training/data-storage/manage-all-files,https://developer.android.com/training/data-storage/shared-preferences,https://developer.android.com/training/data-storage/sqlite,https://developer.android.com/training/data-storage/use-cases"

# ── Group 7: Background Work (merged) ─────────────────────────────
run_topic "background-work" "$KNOWLEDGE_DIR/background-work" \
  "https://developer.android.com/develop/background-work/background-tasks,https://developer.android.com/develop/background-work/services"

# ── Group 8: Navigation (merged) ──────────────────────────────────
run_topic "navigation" "$KNOWLEDGE_DIR/navigation" \
  "https://developer.android.com/guide/navigation,https://developer.android.com/guide/navigation/use-graph/navigate"

# ── Group 9: Other ────────────────────────────────────────────────
run_topic "permissions" "$KNOWLEDGE_DIR/permissions" \
  "https://developer.android.com/guide/topics/permissions/overview"

run_topic "location" "$KNOWLEDGE_DIR/location" \
  "https://developer.android.com/develop/sensors-and-location/location"

run_topic "app-compatibility" "$KNOWLEDGE_DIR/app-compatibility" \
  "https://developer.android.com/guide/app-compatibility"

# ── Summary ───────────────────────────────────────────────────────
echo ""
echo "================================================================"
echo "[batch] DONE: $PASS passed, $FAIL failed, $SKIP skipped"
echo "================================================================"
