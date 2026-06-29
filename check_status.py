#!/usr/bin/env python3
"""Quick status check for the Hermes Society."""
import json, os, glob, subprocess
from pathlib import Path

SOCIETY = Path.home() / '.hermes' / 'society'
ROSTER = SOCIETY / 'roster.json'
COMMONS = SOCIETY / 'commons.md'
SESSIONS = SOCIETY / 'sessions'

def fetch_cron_jobs():
    result = subprocess.run(
        ["sqlite3", 
         str(Path.home() / '.hermes' / 'profiles' / 'default' / 'cron.db'),
         "SELECT name, schedule, next_run_at, last_run_at FROM cron_jobs WHERE enabled=1 ORDER BY next_run_at"],
        capture_output=True, text=True, timeout=10
    )
    jobs = {}
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|')
        jobs[parts[0]] = {'schedule': parts[1], 'next': parts[2], 'last': parts[3] if len(parts) > 3 else None}
    return jobs

roster = json.loads(ROSTER.read_text())
jobs = fetch_cron_jobs()

print("=" * 60)
print("  HERMES SOCIETY STATUS")
print("=" * 60)
print()

for inst in roster:
    name = inst['id']
    print(f"  [{name}]")
    print(f"    Role: {inst['role'][:80]}")
    print(f"    Hours: {inst['active_start']} - {inst['active_end']} ({inst['tz']})")
    jname = f"society-{name}"
    if jname in jobs:
        j = jobs[jname]
        print(f"    Schedule: {j['schedule']}")
        print(f"    Next run: {j['next'] or 'soon'}")
        print(f"    Last run: {j['last'] or 'never'}")
    else:
        print(f"    No cron job found!")
    print()

# Session files
session_files = sorted(SESSIONS.glob("*.md"))
if session_files:
    print("  Session files:")
    for f in session_files[-8:]:  # last 8
        mtime = os.path.getmtime(f)
        size = f.stat().st_size
        print(f"    {f.name}  ({size}b)")
    print(f"    ({len(session_files)} total)")
else:
    print("  No session files yet.")

print()
print(f"  Commons: {COMMONS.stat().st_size}b")
print(f"  Status file: {(SOCIETY / 'status.md').stat().st_size}b")
print(f"  Prompts: {len(list((SOCIETY / 'prompts').glob('*.md')))}")

# Next events
print()
print("  Timeline:")
for name, j in sorted(jobs.items(), key=lambda x: x[1]['next'] or ''):
    print(f"    {name}: next at {j['next']}")
