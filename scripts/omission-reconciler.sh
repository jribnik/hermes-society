#!/usr/bin/env bash
#
# omission-reconciler.sh
#
# Cross-file reconciliation for omission-class failures: a record that
# SHOULD have been written was never written. Unlike drift (state changing
# under a verdict) or durability-leak (work written but not persisted),
# omission is invisible to a single-file hash or a git status — it only
# shows up as a MISMATCH between two ledgers that are supposed to refer
# to the same underlying events.
#
# Background — where this comes from (Curator Run #138, three-disease split):
#   - Drift            -> fingerprinted by status-verification-fingerprint.sh
#   - Durability leak  -> fixed by the auto-commit watcher + post-commit hook
#   - Omission         -> THIS INSTRUMENT (was "STILL MISSING" for 5 runs)
#   Live specimens: Run #137 wrote its summary + updated status.json but
#   never appended itself to curator_runs.json; Debates 38 and 39 were logged
#   as opened/closed in curator_runs.json but never written to swarm-jury.md
#   until Run #138 recovered them.
#
# Threat model (narrowed, same as the fingerprint script): this defends
# against FORGETFULNESS (a writer that updates one surface and skips the
# sibling), not FRAUD (a writer who updates neither or updates both to
# hide the omission). The Society's observed failure is the former.
#
# Check 1 — run-ledger vs summary-files:
#   The maximum run_number recorded in curator_runs.json must equal the
#   maximum run number in the curator-summaries/ filenames. A gap in either
#   direction is an omission: a summary without a ledger entry (Run #137),
#   or a ledger entry whose summary was never written (several "summary file
#   not found" entries in the ledger).
#
# Check 2 — run-ledger vs curator_run_count.txt:
#   The single-scope counter file must match max(run_number). It is cheap,
#   redundant, and drifts silently — currently a stale "140" while the
#   ledger tops out at 142+.
#
# Check 3 — swarm-jury vs run-ledger:
#   The highest debate number in topics/swarm-jury.md must be >= the debate
#   numbers referenced as opened/closed in curator_runs.json. Debates 38/39
#   were the specimen: referenced in the ledger, absent from the file.
#
# Exit codes:
#   0  OK        — every cross-file surface is reconciled
#   1  MISMATCH  — at least one omission detected (details on stdout/stderr)
#   2  UNVERIFIABLE — a required input file or tool is missing
#
# Usage: scripts/omission-reconciler.sh [--society-dir PATH]

set -euo pipefail

SOC="${1:-$HOME/.hermes/society}"
ledger="$SOC/curator_runs.json"
summaries="$SOC/curator-summaries"
run_count_file="$SOC/curator_run_count.txt"
jury="$SOC/topics/swarm-jury.md"

rc=0
note() { printf '  %s\n' "$*"; }

if ! command -v jq >/dev/null 2>&1; then
  echo "UNVERIFIABLE: jq not installed" >&2
  exit 2
fi
if [[ ! -f "$ledger" ]]; then
  echo "UNVERIFIABLE: no curator_runs.json at $ledger" >&2
  exit 2
fi

# ---- Check 1: ledger max run vs summaries max run -------------------------
max_run="$(jq -r '[.runs[].run_number] | max' "$ledger")"
echo "check1_ledger_max_run=$max_run"

max_summary_run=""
if [[ -d "$summaries" ]]; then
  max_summary_run="$(find "$summaries" -type f -name '*.md' -print0 \
    | xargs -0 -n1 basename \
    | grep -oE 'run[0-9]+' \
    | grep -oE '[0-9]+' \
    | sort -n | tail -1)"
else
  echo "WARN: no curator-summaries/ dir at $summaries (may be unarchived)"
fi
echo "check1_summaries_max_run=${max_summary_run:-<none>}"

if [[ -n "$max_summary_run" && "$max_summary_run" != "$max_run" ]]; then
  if (( max_summary_run > max_run )); then
    echo "MISMATCH: summaries top out at run $max_summary_run but the ledger tops out at $max_run"
    note "a summary file was written with no matching ledger entry (the Run #137 omission class)"
  else
    echo "MISMATCH: ledger tops out at run $max_run but summaries top out at $max_summary_run"
    note "a ledger entry exists whose summary file was never written (the 'summary file not found' class)"
  fi
  rc=1
fi

# ---- Check 2: ledger max run vs curator_run_count.txt ---------------------
if [[ -f "$run_count_file" ]]; then
  run_count="$(tr -d '[:space:]' < "$run_count_file")"
  echo "check2_run_count_file=$run_count"
  if [[ "$run_count" =~ ^[0-9]+$ ]] && (( run_count != max_run )); then
    echo "MISMATCH: curator_run_count.txt=$run_count but ledger max run=$max_run"
    note "the standalone counter drifted from the ledger (stale count)"
    rc=1
  fi
else
  echo "WARN: no curator_run_count.txt at $run_count_file"
fi

# ---- Check 3: swarm-jury highest debate vs ledger debate refs ------------
if [[ -f "$jury" ]]; then
  max_jury_debate="$(grep -oE '^### Debate [0-9]+:' "$jury" | grep -oE '[0-9]+' | sort -n | tail -1)"
  echo "check3_jury_max_debate=${max_jury_debate:-<none>}"

  # Any debate number referenced in ledger notes higher than the jury file's max?
  max_ledger_debate="$(jq -r '.runs[].notes // ""' "$ledger" | grep -oE 'Debate [0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1)"
  echo "check3_ledger_max_debate=${max_ledger_debate:-<none>}"

  if [[ -n "$max_ledger_debate" && -n "$max_jury_debate" ]] \
     && (( max_ledger_debate > max_jury_debate )); then
    echo "MISMATCH: ledger references Debate $max_ledger_debate but swarm-jury.md tops out at Debate $max_jury_debate"
    note "a debate was opened/closed in the ledger but never written to swarm-jury.md (the Debates 38/39 omission class)"
    rc=1
  fi
else
  echo "WARN: no topics/swarm-jury.md at $jury"
fi

# ---- Summary ---------------------------------------------------------------
if (( rc == 0 )); then
  echo "OK: all cross-file surfaces reconciled (no omission detected)"
else
  echo "RESULT: omission(s) detected — see MISMATCH lines above"
fi
exit $rc
