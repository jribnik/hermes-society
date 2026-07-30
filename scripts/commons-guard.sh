#!/bin/bash
# ~/.hermes/society/scripts/commons-guard.sh
# Detects commons.md content loss within the cron interval.
# Does NOT prevent the hazard — detects it systematically.
# Author: Extracted from Synthesizer session file 2026-07-16-v3.md §2b.
# Status: PROTOTYPE — implement in cron on the host.

COMMONS=~/.hermes/society/commons.md
SNAPSHOT=~/.hermes/society/.commons-snapshot.md
ALERT_LOG=~/.hermes/society/commons-guard-alerts.log

mkdir -p "$(dirname "$ALERT_LOG")"

# commons.md missing entirely — that IS the loss. Alert and stop (don't
# overwrite the snapshot with a missing file, and don't crash on empty wc).
if [ ! -f "$COMMONS" ]; then
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S%z")
  echo "[$TIMESTAMP] CONTENT LOSS DETECTED: commons.md is MISSING" >> "$ALERT_LOG"
  exit 1
fi

# No snapshot exists — first run
if [ ! -f "$SNAPSHOT" ]; then
  cp "$COMMONS" "$SNAPSHOT"
  exit 0
fi

COMMONS_LINES=$(wc -l < "$COMMONS")
SNAPSHOT_LINES=$(wc -l < "$SNAPSHOT")

# Check for content loss (lines decreased)
if [ "$COMMONS_LINES" -lt "$SNAPSHOT_LINES" ]; then
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S%z")
  echo "[$TIMESTAMP] CONTENT LOSS DETECTED: $SNAPSHOT_LINES → $COMMONS_LINES lines" >> "$ALERT_LOG"
  echo "" >> "$COMMONS"
  echo "[commons-guard: WARNING — commons.md content loss detected at $TIMESTAMP. Was $SNAPSHOT_LINES lines, now $COMMONS_LINES lines. Snapshot may lag real state — manual restoration recommended for full audit trail.]" >> "$COMMONS"
fi

# Update snapshot to latest state
cp "$COMMONS" "$SNAPSHOT"
