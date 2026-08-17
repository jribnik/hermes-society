#!/bin/bash
# Ad-hoc verification for Hermes Society markdown files (no canonical test suite).
# Run after editing any .md files under ~/.hermes/society/.
# Creates and self-cleans a temporary script under $TMPDIR with hermes-verify- prefix.
#
# Usage: bash ~/.hermes/skills/experimental/hermes-society/scripts/verify-society-files.sh
# Or copy the pattern inline for one-shot use.

set -euo pipefail

HERMES="${HOME:-/Users/jribnik}/.hermes/society"
TMPDIR="${TMPDIR:-/var/folders/zq/d8k0nmw12vbd6f5bjsw5pqr80000gn/T}"

PASS=0
FAIL=0
check() { local label="$1" result="$2"; [ "$result" = "PASS" ] && PASS=$((PASS+1)) || { FAIL=$((FAIL+1)); echo "  [FAIL] $label — $result"; }; }

echo "=== Hermes Society — Ad-Hoc Markdown Verification ==="
echo "(No canonical test suite — structural integrity checks)"
echo ""

# --- 1. File existence ---
echo "--- Expected Files ---"
for f in commons.md roster.json status.md; do
    [ -f "$HERMES/$f" ] && echo "  [PASS] $f exists" && PASS=$((PASS+1)) || check "$f" "MISSING"
done

# --- 2. All producing instances have a session file for today ---
echo ""
echo "--- Session Freshness (today = $(date +%F)) ---"
TODAY=$(date +%F)
for inst in archivist advocate synthesizer; do
    dir="$HERMES/sessions/$inst"
    if [ -d "$dir" ]; then
        latest=$(ls -t "$dir"/*.md 2>/dev/null | head -1)
        if [ -n "$latest" ]; then
            basename "$latest" | grep -q "$TODAY" && \
                echo "  [PASS] $inst: $latest" || \
                echo "  [WARN] $inst: latest is $(basename "$latest") (not today)"
            PASS=$((PASS+1))
        else
            check "$inst" "No session files found"
        fi
    else
        check "$inst sessions dir" "MISSING"
    fi
done

# --- 3. Commons structural integrity ---
echo ""
echo "--- Commons Structure ---"
C="$HERMES/commons.md"
[ -f "$C" ] || { check "commons.md" "MISSING"; exit 1; }
LINES=$(wc -l < "$C")
echo "  [INFO] commons.md: $LINES lines, $(stat -f%z "$C") bytes"

# Header should start with density warning
head -1 "$C" | grep -q '^⚠️.*Commons density' && echo "  [PASS] header starts with density warning" || check "header" "No density warning"
PASS=$((PASS+1))

# All session refs should resolve
echo ""
echo "--- Cross-Reference Health ---"
BROKEN=0
for ref in $(grep -oE 'sessions/[a-z-]+/[a-zA-Z0-9._-]+' "$C" | sort -u); do
    clean_ref=$(echo "$ref" | sed 's/§[0-9]*$//')
    fp="$HERMES/$clean_ref"
    [ -f "$fp" ] && continue
    [ -d "$fp" ] && continue
    # Try versioned variants
    base=$(dirname "$fp")
    name=$(basename "$fp" .md)
    found=$(ls "$base/${name}"*.md 2>/dev/null | head -1)
    [ -z "$found" ] && { echo "  BROKEN: \`$ref\`"; BROKEN=$((BROKEN+1)); }
done
[ "$BROKEN" -eq 0 ] && echo "  [PASS] all $(( $(grep -oE 'sessions/[a-z-]+/[a-zA-Z0-9._-]+' "$C" | sort -u | wc -l) )) session refs resolve" || check "cross-references" "$BROKEN broken refs"
PASS=$((PASS+1))

# --- 4. Anne project directory ---
echo ""
echo "--- Anne Project ---"
AP="$HERMES/projects/anne"
if [ -d "$AP" ]; then
    echo "  [PASS] projects/anne/ exists"
    for f in status.md tasks.md decisions.md WORKSPACE.md; do
        [ -f "$AP/$f" ] && echo "  [PASS]   $f" && PASS=$((PASS+1)) || check "  $f" "MISSING"
    done
else
    check "projects/anne/" "MISSING"
fi

# --- Summary ---
echo ""
echo "=== SUMMARY: $PASS checks passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && echo "OK" || echo "Some issues remain — review above"
