#!/usr/bin/env bash
#
# wall-clock-self-check.sh — detect the WALL-CLOCK-SELF-CHECK failure class.
#
# Why this exists:
#   A session file cited events at clock times AFTER the file's own write time —
#   events that had not happened yet when the file was committed. The fabricated
#   content was then read back as evidence, and the Society spent a full cycle
#   building a theory on a phantom event before it was caught. The class has been
#   NAMED in status.json since 2026-08-15 ("WALL-CLOCK-SELF-CHECK — NAMED,
#   UNBUILT") and is now on its fourth symptom. This instrument is the build.
#
# The rule (one line, as diagnosed): event_time <= write_time.
#
# Write-time anchor — git commit time, not mtime:
#   The Society's session files have had their mtimes batch-touched by a
#   migration (e.g. June files showing mtime 2026-07-13 12:04), so mtime is an
#   unreliable "when was this written" signal and produces mass false positives.
#   The commit time of the file's last git commit is the authoritative wall clock
#   at which the content actually entered the record. Untracked files fall back
#   to mtime.
#
# Threat model (narrowed, same as the sibling instruments): this defends against
#   SELF-FABRICATION (a writer narrating events that have not occurred, then the
#   record re-reading them as facts), not FRAUD (an adversary backdating commits).
#
# Two violation shapes, both reported:
#   1. FUTURE-LOCAL — a bare or PT-labeled "HH:MM" later than the file's own
#      write time on the same day (the primary fabrication tell).
#   2. UTC-AS-LOCAL — a UTC-labeled "HH:MM" whose raw clock time is later than
#      the write time's local clock (the recurring "cited UTC as if it were PT"
#      artifact — the phantom 22:10/22:23/22:43 that never happened locally).
#
# Exit codes:
#   0  OK        — no session file cites a future timestamp
#   1  VIOLATION — at least one file cites a time after its own write time
#   2  UNVERIFIABLE — a required tool is missing
#
# Usage: scripts/wall-clock-self-check.sh [--society-dir PATH] [--days N]

set -euo pipefail

SOC=""
DAYS=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --society-dir) SOC="$2"; shift 2 ;;
    --days) DAYS="$2"; shift 2 ;;
    *) shift ;;
  esac
done
SOC="${SOC:-$HOME/.hermes/society}"
SESSIONS="$SOC/sessions"

if ! command -v python3 >/dev/null 2>&1; then
  echo "UNVERIFIABLE: python3 not installed" >&2
  exit 2
fi
if [[ ! -d "$SESSIONS" ]]; then
  echo "UNVERIFIABLE: no sessions/ dir at $SESSIONS" >&2
  exit 2
fi

SOC="$SOC" SESSIONS="$SESSIONS" DAYS="$DAYS" python3 - <<'PY'
import os, re, sys, subprocess, datetime, zoneinfo

sessions_dir = os.environ["SESSIONS"]
soc = os.environ["SOC"]
days = int(os.environ.get("DAYS", "0"))
TZ = zoneinfo.ZoneInfo("America/Los_Angeles")

TS_RE = re.compile(
    r'(?<![0-9])'
    r'(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?\s*(UTC|PDT|PST|PT)?'
    r'(?![0-9])',
    re.IGNORECASE,
)

def parse_clock(hh, mm, ss, mer):
    hh, mm = int(hh), int(mm)
    if hh > 23 or mm > 59:
        return None  # skip "24:00"-style and other non-clock times
    if mer:
        mer = mer.lower().replace('.', '')
        if mer == 'pm' and hh != 12:
            hh += 12
        if mer == 'am' and hh == 12:
            hh = 0
    ss = int(ss) if ss else 0
    return (hh, mm, ss)

def commit_time(path):
    # Last-commit timestamp (unix seconds) for a git-tracked file; None if
    # untracked or git unavailable. This is the write-time anchor.
    try:
        out = subprocess.run(
            ["git", "-C", soc, "log", "-1", "--format=%ct", "--", path],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        return int(out) if out else None
    except (subprocess.SubprocessError, ValueError):
        return None

now = datetime.datetime.now(TZ)
cutoff = now - datetime.timedelta(days=days) if days else None

violations = 0
files_scanned = 0
files_flagged = 0

for role in sorted(os.listdir(sessions_dir)):
    role_dir = os.path.join(sessions_dir, role)
    if not os.path.isdir(role_dir):
        continue
    for fname in sorted(os.listdir(role_dir)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(role_dir, fname)
        rel = os.path.relpath(path, soc)

        ct = commit_time(rel)
        if ct is None:
            ct = int(os.path.getmtime(path))
        write_dt = datetime.datetime.fromtimestamp(ct, TZ)
        if cutoff and write_dt < cutoff:
            continue

        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        files_scanned += 1

        file_violations = []
        for m in TS_RE.finditer(text):
            hh, mm, ss, mer, tzword = m.groups()
            parsed = parse_clock(hh, mm, ss, mer)
            if parsed is None:
                continue
            phh, pmm, pss = parsed
            tzname = (tzword or '').upper()

            # Anchor the cited clock to the file's own write-day for a same-day
            # wall-clock comparison.
            naive = datetime.datetime(
                write_dt.year, write_dt.month, write_dt.day, phh, pmm, pss)

            if tzname == 'UTC':
                # UTC-labeled: the raw clock is later than the writer's own
                # local clock -> the "cited UTC as if it were PT" misread.
                if naive > write_dt.replace(tzinfo=None):
                    file_violations.append(
                        f"UTC-AS-LOCAL {phh:02d}:{pmm:02d} UTC "
                        f"(cited as {naive:%H:%M}, wrote at {write_dt:%H:%M} local)")
                continue
            # Bare or PT-labeled: treat as local wall time.
            if naive > write_dt.replace(tzinfo=None):
                file_violations.append(
                    f"FUTURE-LOCAL {naive:%H:%M} after write "
                    f"{write_dt:%H:%M} ({write_dt:%Y-%m-%d})")

        if file_violations:
            files_flagged += 1
            violations += len(file_violations)
            print(f"VIOLATION {rel}")
            # collapse duplicates, cap at 5 lines
            seen, shown = set(), 0
            for v in file_violations:
                key = v.split('after write')[0]
                if key in seen:
                    continue
                seen.add(key)
                print(f"  {v}")
                shown += 1
                if shown >= 5:
                    print(f"  ... ({len(file_violations)} total)")
                    break

if violations:
    print(f"RESULT: {violations} wall-clock violation(s) across "
          f"{files_flagged} of {files_scanned} session files.")
    sys.exit(1)
print(f"OK: no wall-clock violation in {files_scanned} session files.")
sys.exit(0)
PY
