#!/usr/bin/env bash
#
# wall-clock-self-check.sh — detect the WALL-CLOCK-SELF-CHECK failure class.
#
# Why this exists:
#   A session file cited events at times AFTER the file's own write time —
#   timestamps that had not happened yet when the file was committed. The
#   fabricated content then got read back as evidence, and the Society spent
#   a full cycle building a theory on a phantom event before it was caught.
#   The failure class has been NAMED in status.json since 2026-08-15
#   ("WALL-CLOCK-SELF-CHECK — NAMED, UNBUILT") and is now on its fourth
#   symptom. This instrument is the build.
#
# The rule (one line, as diagnosed): event_time <= write_time.
#   A session file may not cite a clock time that postdates its own mtime.
#
# Threat model (narrowed, same as the sibling instruments):
#   This defends against SELF-FABRICATION (a writer narrating events that have
#   not occurred, then the record re-reading them as facts), not FRAUD (an
#   adversary who backdates mtimes). The Society's observed failure is the
#   former.
#
# Two violation shapes, both reported:
#   1. FUTURE-LOCAL — a bare or PT-labeled "HH:MM" that is later than the
#      file's own write time (the primary fabrication tell).
#   2. UTC-AS-LOCAL — a UTC-labeled "HH:MM" that is later than the file's
#      write time when the UTC instant is misread as local wall time. This is
#      the recurring "cited UTC as if it were PT" artifact.
#
# Exit codes:
#   0  OK      — no session file cites a future timestamp
#   1  VIOLATION — at least one file cites a time after its own write time
#   2  UNVERIFIABLE — a required tool is missing
#
# Usage: scripts/wall-clock-self-check.sh [--society-dir PATH]

set -euo pipefail

SOC="${1:-$HOME/.hermes/society}"
SESSIONS="$SOC/sessions"

if ! command -v python3 >/dev/null 2>&1; then
  echo "UNVERIFIABLE: python3 not installed" >&2
  exit 2
fi

if [[ ! -d "$SESSIONS" ]]; then
  echo "UNVERIFIABLE: no sessions/ dir at $SESSIONS" >&2
  exit 2
fi

python3 - "$SESSIONS" <<'PY'
import os, re, sys, datetime, zoneinfo

sessions_dir = sys.argv[1]
TZ = zoneinfo.ZoneInfo("America/Los_Angeles")

# Timestamps: HH:MM, optional :SS, optional AM/PM, optional trailing TZ word.
TS_RE = re.compile(
    r'(?<![0-9])'
    r'(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?\s*(UTC|PDT|PST|PT)?'
    r'(?![0-9])',
    re.IGNORECASE,
)

# Ignore time ranges that are clearly durations or ratios (e.g. "3:2", "2:1").
def looks_like_clock(hh, mm):
    return 0 <= hh <= 23 and 0 <= mm <= 59

def parse_clock(hh, mm, ss, mer, tzword):
    hh, mm = int(hh), int(mm)
    if not looks_like_clock(hh, mm):
        return None
    if mer:
        mer = mer.lower().replace('.', '')
        if mer == 'pm' and hh != 12:
            hh += 12
        if mer == 'am' and hh == 12:
            hh = 0
    ss = int(ss) if ss else 0
    tzname = (tzword or '').upper()
    return (hh, mm, ss, tzname)

def resolve_local(dt_naive):
    # Interpret a bare/PT timestamp in the Society's single timezone.
    return dt_naive.replace(tzinfo=TZ)

violations = 0
files_scanned = 0
for role in sorted(os.listdir(sessions_dir)):
    role_dir = os.path.join(sessions_dir, role)
    if not os.path.isdir(role_dir):
        continue
    for fname in sorted(os.listdir(role_dir)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(role_dir, fname)
        mtime = os.path.getmtime(path)
        write_dt = datetime.datetime.fromtimestamp(mtime, TZ)
        try:
            text = open(path, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        files_scanned += 1
        file_violations = []
        for m in TS_RE.finditer(text):
            hh, mm, ss, mer, tzword = m.groups()
            parsed = parse_clock(hh, mm, ss, mer, tzword)
            if parsed is None:
                continue
            phh, pmm, pss, tzname = parsed
            # Attach a candidate date: the file's own date, then adjust.
            naive = datetime.datetime(
                write_dt.year, write_dt.month, write_dt.day,
                phh, pmm, pss,
            )
            # Resolve against the file's write instant.
            if tzname == 'UTC':
                # UTC-labeled instant, converted to local for comparison.
                utc_dt = naive.replace(tzinfo=datetime.timezone.utc)
                resolved = utc_dt.astimezone(TZ)
                # Flag UTC-as-local only when the raw clock time is clearly in
                # the future on the local wall clock (the misread shape).
                if naive > write_dt.replace(tzinfo=None):
                    file_violations.append(
                        f"UTC-AS-LOCAL {hh}:{mm} (cited as {naive:%H:%M}, "
                        f"wrote at {write_dt:%H:%M} local)"
                    )
                continue
            # Bare or PT-labeled: treat as local wall time.
            if tzname in ('PDT', 'PST', 'PT'):
                resolved = naive.replace(tzinfo=TZ)
            else:
                resolved = resolve_local(naive)
            if resolved > write_dt:
                file_violations.append(
                    f"FUTURE-LOCAL {resolved:%H:%M} after write "
                    f"{write_dt:%H:%M} ({write_dt:%Y-%m-%d})"
                )
        if file_violations:
            violations += len(file_violations)
            print(f"VIOLATION {path}")
            for v in file_violations:
                print(f"  {v}")

if violations:
    print(f"RESULT: {violations} wall-clock violation(s) across {files_scanned} session files.")
    sys.exit(1)
print(f"OK: no wall-clock violation in {files_scanned} session files.")
sys.exit(0)
PY
