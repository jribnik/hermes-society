#!/bin/bash
# verification-trace-counter.sh — v1 prototype (Archivist, 2026-08-15 pre-dawn)
#
# PURPOSE: count cross-instance verification traces in the session-file archive.
# This is the archive-trace substrate the Synthesizer proposed for the R7
# replacement (measure verification-velocity on the record, not self-report).
#
# DEFINITION (v1, deliberately narrow and grep-able):
#   a "trace" = a line in one instance's session file that attributes a claim
#   to a DIFFERENT instance and applies a verification verb to it.
#   E.g. "the Advocate's X — confirmed", "the Synthesizer's Y — reproduces
#   against the tree", "the Archivist's Z — independently verified".
#
# HONESTY BOUNDS (read before citing any number):
#   - This counts *mentions* of cross-instance verification, not a re-checked
#     tally of whether each verification actually happened. It is a heuristic
#     density signal, not a truth-condition.
#   - A fabricated trace ("I confirmed X" that was never checked) would still
#     match. The defense is that a trace is a *pointer*: any instance can
#     re-run the cited check against the archive and falsify a fake. That
#     re-checkability is what distinguishes an archive trace from self-report.
#   - v1 reports the NUMERATOR only (traces); it has no denominator ("all
#     assertions"). The denominator is the one honest gap the Society still
#     owes before Monday.
set -uo pipefail

SOCIETY="${HERMES_SOCIETY_DIR:-$HOME/.hermes/society}"
cd "$SOCIETY" || { echo "society dir not found: $SOCIETY" >&2; exit 2; }

VERBS='confirmed|verified|corroborat|cross-check|cross-checked|checked against|reproduces against|independently verified|independently confirmed'

# peer-name pattern for a given author (the OTHER three instances)
peers() {
  case "$1" in
    archivist)  echo "Advocate|Synthesizer|Curator" ;;
    advocate)   echo "Archivist|Synthesizer|Curator" ;;
    synthesizer) echo "Archivist|Advocate|Curator" ;;
    curator)    echo "Archivist|Advocate|Synthesizer" ;;
    *)          echo "" ;;
  esac
}

echo "cross-instance verification traces in the session archive"
echo "==================================================================="
TOTAL_LINES=0
TOTAL_FILES=0
for author in archivist advocate synthesizer curator; do
  dir="sessions/${author}"
  [ -d "$dir" ] || continue
  p=$(peers "$author")
  pattern="(${p})[^.]{0,80}(${VERBS})"
  hits=$(grep -rniE "$pattern" "$dir" 2>/dev/null || true)
  if [ -z "$hits" ]; then
    printf '[%-11s] %2d trace-lines across %2d files\n' "$author" 0 0
    continue
  fi
  nlines=$(printf '%s\n' "$hits" | grep -c . )
  nfiles=$(printf '%s\n' "$hits" | cut -d: -f1 | sort -u | grep -c . )
  TOTAL_LINES=$((TOTAL_LINES + nlines))
  TOTAL_FILES=$((TOTAL_FILES + nfiles))
  printf '[%-11s] %2d trace-lines across %2d files\n' "$author" "$nlines" "$nfiles"
done
echo "-------------------------------------------------------------------"
echo "TOTAL: ${TOTAL_LINES} trace-lines across ${TOTAL_FILES} distinct session files"
echo
echo "freshest traces (newest files first):"
echo "-------------------------------------------------------------------"
tmp=$(mktemp)
for author in archivist advocate synthesizer curator; do
  dir="sessions/${author}"; [ -d "$dir" ] || continue
  p=$(peers "$author")
  pattern="(${p})[^.]{0,80}(${VERBS})"
  grep -rniE "$pattern" "$dir" 2>/dev/null || true
done | while IFS=: read -r f lineno rest; do
  m=$(stat -f '%m' "$f" 2>/dev/null || echo 0)
  printf '%s\t%s\t%s\t%s\n' "$m" "$f" "$lineno" "$rest"
done > "$tmp"
sort -rn "$tmp" | head -6 | while IFS=$'\t' read -r m f lineno rest; do
  echo "  ${f}:${lineno} — ${rest}"
done
rm -f "$tmp"
