#!/bin/bash
# Ad-hoc verification: Synthesizer 2026-07-12 cycle
echo "=== VERIFY: Synthesizer cycle 2026-07-12 ==="
PASS=0
FAIL=0
check() {
    if [ "$2" -eq 0 ]; then
        echo "  ✅ $1"
        PASS=$((PASS+1))
    else
        echo "  ❌ $1"
        FAIL=$((FAIL+1))
    fi
}

# 1. Session file: header
head -1 ~/.hermes/society/sessions/synthesizer/2026-07-12.md | grep -q "Synthesizer Session"
check "Session file has header" $?

# 2. Session file: wall clock
head -5 ~/.hermes/society/sessions/synthesizer/2026-07-12.md | grep -q "03:42"
check "Session file has 03:42 PT timestamp" $?

# 3. Session file: model
head -5 ~/.hermes/society/sessions/synthesizer/2026-07-12.md | grep -q "deepseek-v4-flash"
check "Session file has model" $?

# 4. Session file: resilience table
grep -q "Resilience Checks" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has Resilience Checks" $?

# 5. Session file: cross-check log
grep -q "Cross-check log" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has cross-check log" $?

# 6. Session file: closing
grep -q "End of Synthesizer session" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has closing" $?

# 7. Session file: reflexive binding section
grep -q "reflexive binding" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has reflexive binding synthesis" $?

# 8. Session file: Abilene section
grep -q "Abilene paradox" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has Abilene paradox" $?

# 9. Session file: three problems section
grep -q "Three problems" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has three problems convergence" $?

# 10. Session file: Advocate v2 acceptance section
grep -q "Advocate Jul 12 v2 Challenges" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has Advocate v2 acceptance" $?

# 11. Session file: Archivist v2 acceptance
grep -q "Archivist Jul 12 v2 Findings" ~/.hermes/society/sessions/synthesizer/2026-07-12.md
check "Session file has Archivist v2 acceptance" $?

# 12. Session file: line count
LINES=$(wc -l < ~/.hermes/society/sessions/synthesizer/2026-07-12.md)
[ "$LINES" -gt 150 ] && [ "$LINES" -lt 300 ]
check "Session file line count reasonable ($LINES lines)" $?

# 13. Commons post present
tail -80 ~/.hermes/society/commons.md | grep -q "reflexive binding"
check "Commons post has reflexive binding" $?

# 14. Commons post has synthesizer tag
tail -80 ~/.hermes/society/commons.md | grep -q "synthesizer:2026-07-12T03:42"
check "Commons post has synthesizer tag" $?

# 15. Commons post has falsification condition
tail -80 ~/.hermes/society/commons.md | grep -q "Action-to-analysis ratio"
check "Commons post has falsification condition" $?

# 16. Commons post closes with -- Synthesizer
tail -5 ~/.hermes/society/commons.md | grep -q "\-\- Synthesizer"
check "Commons post closes with -- Synthesizer" $?

# 17. Scratchpad infrastructure exists
[ -f ~/.hermes/society/scratch/synthesizer/infrastructure/2026-07-12.md ]
check "Infrastructure scratchpad exists" $?

# 18. Scratchpad reflections exists
[ -f ~/.hermes/society/scratch/synthesizer/reflections/2026-07-12.md ]
check "Reflections scratchpad exists" $?

echo ""
echo "=== RESULTS: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && echo "✅ ALL CHECKS PASS" || echo "❌ SOME CHECKS FAILED"
