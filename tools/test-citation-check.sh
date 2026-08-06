#!/usr/bin/env bash
# test-citation-check.sh — permanent test suite for citation-check.sh
#
# Tests three modes:
#   1. Genuine citation (exit 0)
#   2. Fabricated/drifted citation (exit 1)
#   3. Missing source file (exit 2)
#
# Run: ./test-citation-check.sh

set -euo pipefail

PASS=0
FAIL=0
TOOL="./tools/citation-check.sh"

# Create a temp source file with known content
SOURCE=$(mktemp)
trap 'rm -f "$SOURCE"' EXIT

cat > "$SOURCE" << 'EOF'
## Compliance audit — 2026-08-05 afternoon

| Check | Status |
|-------|--------|
| File naming | 10/10 PASS |
| Epistemic tier labels | 10/10 PASS |

All checks passed. The 10/10 count is verified against the source archive.
EOF

echo "=== citation-check.sh test suite ==="
echo ""

# Test 1: Genuine citation — should PASS
echo "Test 1: Genuine citation"
if "$TOOL" "10/10 PASS" "$SOURCE" > /dev/null 2>&1; then
    echo "  PASS (exit 0 as expected)"
    ((PASS++))
else
    echo "  FAIL — expected exit 0, got exit $?"
    ((FAIL++))
fi

# Test 2: Fabricated/drifted citation — should FAIL
echo "Test 2: Fabricated citation (drift: 10→11)"
if "$TOOL" "11/11 PASS" "$SOURCE" > /dev/null 2>&1; then
    echo "  FAIL — expected exit 1, got exit 0 (false positive!)"
    ((FAIL++))
else
    exit_code=$?
    if [ "$exit_code" -eq 1 ]; then
        echo "  PASS (exit 1 as expected)"
        ((PASS++))
    else
        echo "  FAIL — expected exit 1, got exit $exit_code"
        ((FAIL++))
    fi
fi

# Test 3: Missing source file — should ERROR
echo "Test 3: Missing source file"
if "$TOOL" "anything" "/nonexistent/path.md" > /dev/null 2>&1; then
    echo "  FAIL — expected exit 2, got exit 0"
    ((FAIL++))
else
    exit_code=$?
    if [ "$exit_code" -eq 2 ]; then
        echo "  PASS (exit 2 as expected)"
        ((PASS++))
    else
        echo "  FAIL — expected exit 2, got exit $exit_code"
        ((FAIL++))
    fi
fi

echo ""
echo "=== Results: $PASS/$((PASS + FAIL)) PASS ==="

if [ "$FAIL" -gt 0 ]; then
    echo "FAILURES DETECTED"
    exit 1
fi

echo "All tests passed."
exit 0
