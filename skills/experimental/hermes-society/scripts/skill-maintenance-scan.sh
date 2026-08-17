#!/usr/bin/env bash
# Skill-maintenance candidate scan (HERMES-19, Part A — deterministic, no LLM).
#
# Narrows the reference corpus to a SMALL candidate list for the Archivist's
# maintenance cycle to classify. A file is a candidate only if it is BOTH:
#   (1) truly orphaned — not named in SKILL.md AND not referenced by any other
#       reference file (so archiving it can't break an inbound link), AND
#   (2) retired-concept-flavored — its name or body matches a retired-concept
#       keyword (commons.md-era / 400-line / builder / prime-mover / rolloff /
#       density) — the only signal a script can use to guess "probably dead".
# Protected operational playbooks are never candidates regardless.
#
# Output: a markdown candidate list on stdout (and to maintenance-queue.md).
# Empty list => nothing to do this cycle. Also refreshes 0-index.md.
#
#   bash scripts/skill-maintenance-scan.sh
#
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REF="$SKILL_DIR/references"
QUEUE="$SKILL_DIR/maintenance-queue.md"

# Keep the index fresh regardless of whether anything gets archived.
bash "$SKILL_DIR/scripts/build-reference-index.sh" >/dev/null 2>&1 || true

# Retired-concept signals (case-insensitive). A candidate must smell like one.
# Retired concepts. Matched against FILENAME + TITLE only (not the whole body):
# a file whose PURPOSE is a retired concept names it in the title; a live
# analysis file that merely mentions "line count" in passing does not — this is
# what keeps the candidate list precise (few, high-confidence) so the Archivist
# isn't handed dozens of false positives to wade through.
RETIRED_RE='commons\.md|400.?line|300.?line|prime.?mover|reactor|auto.?rolloff|rolloff|commons.?densit|line.?count|builder.?role|builder.?path|builder.?pattern'
# Protected: operational playbooks / live infra — never archive by scan.
PROTECT_RE='-cycle-|-routine|^0-index|^change-log|curator-infra|curator-run-workflow|shared-preamble'

candidates=()
for f in "$REF"/*.md; do
  b="$(basename "$f")"
  # skip protected operational files
  # `--` guards against PROTECT_RE starting with '-' (grep would parse it as a flag).
  echo "$b" | grep -qiE -- "$PROTECT_RE" && continue
  # (1) truly orphaned: no mention of the basename in SKILL.md or any OTHER ref.
  # Exclude 0-index.md — the complete auto-index lists EVERY file by design, so
  # it would make every file look "referenced" and mask all orphans.
  refs="$(grep -rlF "$b" "$SKILL_DIR/SKILL.md" "$REF" 2>/dev/null \
            | grep -v "/references/$b" | grep -v "/references/0-index.md" || true)"
  [ -n "$refs" ] && continue
  # (2) retired-concept flavored — FILENAME or TITLE (first heading), not body.
  title="$(awk 'NF && $0 !~ /^---$/ {print; exit}' "$f")"
  if echo "$b" | grep -qiE -- "$RETIRED_RE" || printf '%s' "$title" | grep -qiE -- "$RETIRED_RE"; then
    candidates+=("$b")
  fi
done

{
  echo "# Skill maintenance queue — $(date '+%Y-%m-%d %H:%M')"
  echo ""
  echo "Deterministic scan (scripts/skill-maintenance-scan.sh). Each entry is a"
  echo "reference file that is BOTH unreferenced anywhere AND matches a retired-"
  echo "concept keyword — i.e. a *candidate* for archiving. The Archivist still"
  echo "classifies each (ARCHIVE vs KEEP; when unsure → KEEP)."
  echo ""
  if [ "${#candidates[@]}" -eq 0 ]; then
    echo "**No candidates. Nothing to maintain this cycle.**"
  else
    echo "## Candidates (${#candidates[@]})"
    echo ""
    for b in "${candidates[@]}"; do
      title="$(awk 'NF && $0 !~ /^---$/ {gsub(/^#+ +/,""); print; exit}' "$REF/$b" | cut -c1-100)"
      echo "- \`$b\` — $title"
    done
  fi
} | tee "$QUEUE"
