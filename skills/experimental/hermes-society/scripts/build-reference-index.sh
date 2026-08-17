#!/usr/bin/env bash
# Regenerate references/0-index.md — a complete map of every file in references/
# (and references/archive/) so nothing is unindexed. Each summary is the file's
# own title / first non-empty line. Run after adding, renaming, or archiving a
# reference file. Idempotent.
#
#   bash scripts/build-reference-index.sh
#
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REF="$SKILL_DIR/references"
OUT="$REF/0-index.md"

summ() { awk 'NF && $0 !~ /^---$/ {gsub(/^#+ +/,""); gsub(/\|/,"\\|"); print; exit}' "$1" | cut -c1-140; }

n_active=$(ls "$REF"/*.md 2>/dev/null | wc -l | tr -d ' ')
n_arch=$(ls "$REF"/archive/*.md 2>/dev/null | wc -l | tr -d ' ')

{
  echo "# Hermes Society — Reference Index (complete)"
  echo ""
  echo "Auto-generated map of **every** file in \`references/\` so any file can be found by name. Regenerate with \`scripts/build-reference-index.sh\` after adding/renaming/archiving a reference (last built $(date '+%Y-%m-%d'))."
  echo "Summaries are each file's own title / first line. For curated highlights of the most-loaded references, see \`SKILL.md\` § Skill Support Files."
  echo ""
  echo "## Active references ($n_active files)"
  echo ""
  echo "| File | Summary |"
  echo "|------|---------|"
  for f in $(ls "$REF"/*.md | sort); do
    echo "| \`$(basename "$f")\` | $(summ "$f") |"
  done
  if [ "$n_arch" -gt 0 ]; then
    echo ""
    echo "## Archived references ($n_arch files — retired concepts: Builder role, commons.md-era workflows, 400-Line Protocol)"
    echo ""
    echo "> These describe retired mechanisms and are kept only as historical record. Do NOT follow their procedures — see the retirement banners and \`SKILL.md\`."
    echo ""
    echo "| File | Summary |"
    echo "|------|---------|"
    for f in $(ls "$REF"/archive/*.md | sort); do
      echo "| \`archive/$(basename "$f")\` | $(summ "$f") |"
    done
  fi
} > "$OUT"

echo "Wrote $OUT — $n_active active + $n_arch archived references indexed."
