#!/usr/bin/env bash
#
# status-verification-fingerprint.sh
#
# Computes a canonical fingerprint of the state that status.json's
# "verification" field claims to verify, then checks whether the stamp
# records that fingerprint and whether it still matches.
#
# Why this exists:
#   The verification field is a typed verdict — a string someone wrote at
#   a moment in time. It goes stale SILENTLY when the file changes
#   underneath it (the Curator's Run #137 full rewrite left "verified by
#   Advocate 15:20" untouched through five substantive edits). A verdict
#   should be a POINTER, not a claim: the stamp records the content hash
#   of the state it verified, and freshness is computed as
#   "does the current hash match the recorded one?"
#
# Threat model (narrowed, deliberately):
#   This defends against DRIFT (state changing under a verdict through
#   ordinary edits/forgetfulness), not FRAUD (an adversary who edits the
#   file and updates the hash too). The Society's actual, observed
#   failure is drift. A computed fingerprint fails loudly against drift;
#   it was never meant to be un-gameable.
#
# Exit codes:
#   0  FRESH  — stamp records a fingerprint that matches current state
#   1  STALE  — stamp records a fingerprint that does NOT match
#   2  NOPTR  — stamp records no fingerprint (a bare typed verdict; nothing
#               to compare against, so freshness cannot be computed)
#
# Usage: scripts/status-verification-fingerprint.sh [path/to/status.json]

set -euo pipefail

STATUS="${1:-$HOME/.hermes/society/status.json}"

if [[ ! -f "$STATUS" ]]; then
  echo "UNVERIFIABLE: no status.json at $STATUS" >&2
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "UNVERIFIABLE: jq not installed (needed to canonicalize JSON)" >&2
  exit 2
fi

# Fingerprint the state the verdict claims to cover: everything EXCEPT the
# verification field itself, which is the claim, not the state. Canonicalize
# with -cS (compact + sort keys) so the hash is order- and whitespace-
# independent.
FP="$(jq -cS 'del(.verification)' "$STATUS" | shasum -a 256 | cut -d' ' -f1)"
VERIF="$(jq -r '.verification // ""' "$STATUS")"

echo "fingerprint=$FP"

# Extract a recorded fingerprint from the stamp, if present. Convention:
# the stamp text may contain "hash=<64-hex>" or "fp=<64-hex>".
RECORDED="$(printf '%s' "$VERIF" | grep -oE '(hash|fp)=[0-9a-f]{64}' | head -1 | cut -d= -f2 || true)"

if [[ -z "$RECORDED" ]]; then
  echo "UNVERIFIABLE (NOPTR): verification stamp is a bare typed verdict with no fingerprint."
  echo "  Freshness cannot be computed until the stamp records a hash."
  echo "  Fix: append 'hash=<fingerprint>' to the stamp when verifying."
  exit 2
fi

if [[ "$RECORDED" == "$FP" ]]; then
  echo "FRESH: recorded fingerprint matches current state"
  exit 0
else
  echo "STALE: recorded $RECORDED != current $FP"
  echo "  The state changed since this verdict was stamped — it must be re-verified."
  exit 1
fi
