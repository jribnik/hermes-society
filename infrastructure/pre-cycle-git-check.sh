#!/usr/bin/env bash
# pre-cycle-git-check.sh — Tier-1 ground-truth gate
# Surfaces untracked/modified files in the Society repo so every instance
# sees them in its cron input. Informational only — exits 0 always.
#
# Delegation: delegations/2026-08-07--tier1-git-status-gate.md
# Built: 2026-08-07 ~12:00 PDT by Archivist (execution mode)

set -euo pipefail

REPO_DIR="${HERMES_SOCIETY_REPO_DIR:-$HOME/.hermes/society}"

if ! cd "$REPO_DIR" 2>/dev/null; then
    echo "[pre-cycle-git-check] WARNING: could not cd to $REPO_DIR — skipping git status check"
    exit 0
fi

STATUS_OUTPUT="$(git status --porcelain 2>/dev/null)" || true

if [ -n "$STATUS_OUTPUT" ]; then
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║  TIER-1 GATE: Untracked or modified files in society repo  ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "$STATUS_OUTPUT" | while IFS= read -r line; do
        printf "║  %-56s ║\n" "$line"
    done
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "[pre-cycle-git-check] $(echo "$STATUS_OUTPUT" | wc -l | tr -d ' ') untracked/modified file(s) detected."
    echo "[pre-cycle-git-check] This is informational — cycle execution is NOT blocked."
fi

exit 0
