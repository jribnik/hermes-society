#!/usr/bin/env bash
# citation-check.sh — verify a claimed citation against the archive
#
# Usage: citation-check.sh "claimed citation text" path/to/source.md
#
# Exit codes: 0 = PASS (citation verified), 1 = FAIL (not found), 2 = ERROR
#
# Part of the pointer principle implementation: replace memory with pointer.
# Built by the Archivist, 2026-08-05 night cycle.

set -euo pipefail

if [ $# -ne 2 ]; then
    echo "ERROR: usage: $0 \"cited text\" <source-file>"
    exit 2
fi

CITATION="$1"
SOURCE="$2"

if [ ! -f "$SOURCE" ]; then
    echo "ERROR: source file not found: $SOURCE"
    exit 2
fi

if grep -qF -- "$CITATION" "$SOURCE"; then
    echo "PASS: citation verified in $SOURCE"
    exit 0
else
    echo "FAIL: citation not found in $SOURCE"
    exit 1
fi
