#!/usr/bin/env python3
"""
Hermes Society Watchdog — no-agent mode cron script.

Runs as a standalone watchdog using cronjob(no_agent=True).
On each tick:
  1. Checks that all three daily-instance session files exist and are < 8h old
  2. Checks backup is < 24h old
  3. Checks commons is < 300 lines
  4. Reports any failures

SILENT on success — only outputs when something is wrong.
"""

import os, json, glob, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

SOCIETY = Path.home() / '.hermes' / 'society'
SESSIONS = SOCIETY / 'sessions'
BACKUP   = SOCIETY / 'backup'
COMMONS  = SOCIETY / 'commons.md'

errors = []
warnings = []

now = datetime.now(timezone.utc)

# ── 1. Session file freshness ──────────────────────────────────
for role in ['archivist', 'advocate', 'synthesizer']:
    files = sorted(SESSIONS.glob(f"{role}_*.md"))
    if not files:
        errors.append(f"[CRON-WATCHDOG] No session files found for {role} — instance may have never run!")
        continue
    latest = max(f.stat().st_mtime for f in files)
    age_hours = (now.timestamp() - latest) / 3600
    if age_hours > 8:
        errors.append(f"[CRON-WATCHDOG] {role} last session is {age_hours:.1f}h old — stale!")

# ── 2. Backup freshness ────────────────────────────────────────
BACKUP_TARBALL = SOCIETY / 'backup'
if not BACKUP_TARBALL.exists():
    errors.append("[BACKUP] No backup directory exists at ~/.hermes/society/backup/ — run backup.py first!")
elif not any(BACKUP_TARBALL.iterdir()):
    errors.append("[BACKUP] Backup directory exists but is empty!")
else:
    latest_backup = max(BACKUP_TARBALL.glob("society-backup-*.tar.gz"), key=lambda f: f.stat().st_mtime, default=None)
    if latest_backup:
        backup_age = (now.timestamp() - latest_backup.stat().st_mtime) / 3600
        if backup_age > 24:
            errors.append(f"[BACKUP] Last backup ({latest_backup.name}) is {backup_age:.1f}h old!")
    else:
        errors.append("[BACKUP] No society-backup-*.tar.gz found in backup/ directory.")

# ── 3. Commons line count ──────────────────────────────────────
COMMONS_THRESHOLD = 300
if COMMONS.exists():
    line_count = len(COMMONS.read_text().splitlines())
    if line_count > COMMONS_THRESHOLD:
        warnings.append(f"[COMMONS] {line_count} lines — exceeds {COMMONS_THRESHOLD}-line target. Curator should roll off.")
else:
    errors.append("[COMMONS] commons.md not found!")

# ── 4. Model baseline ──────────────────────────────────────────
baseline_path = SOCIETY / 'baseline' / 'model-baseline.json'
if baseline_path.exists():
    baseline = json.loads(baseline_path.read_text())
    for role in ['archivist', 'advocate', 'synthesizer']:
        files = sorted(SESSIONS.glob(f"{role}_*.md"))
        if files:
            latest = max(f for f in files)
            content = latest.read_text()
            for line in content.splitlines()[:10]:
                line_stripped = line.strip()
                if line_stripped.startswith('Model:') or line_stripped.startswith('model:'):
                    current_model = line.split(':', 1)[1].strip()
                    # Strip markdown formatting like **bold** for comparison
                    clean_model = current_model.replace('**', '').strip()
                    if clean_model != baseline.get('model'):
                        warnings.append(f"[MODEL] {role} uses '{clean_model}' — baseline is '{baseline.get('model')}' (possible upgrade)")
                    break
else:
    warnings.append("[BASELINE] No model baseline file — run baseline.sh first.")

# ── 5. Report ──────────────────────────────────────────────────
if not errors and not warnings:
    sys.exit(0)  # silent on success (no_agent=True)

lines = []
if errors:
    lines.append("❌ HERMES SOCIETY WATCHDOG — FAILURES DETECTED")
    lines.extend(errors)
if warnings:
    if not errors:
        lines.append("⚠️  HERMES SOCIETY WATCHDOG — WARNINGS")
    lines.extend(warnings)

lines.append(f"\nChecked at: {now.isoformat()}")
print("\n".join(lines))
sys.exit(1 if errors else 0)
