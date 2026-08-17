#!/usr/bin/env bash
#
# wall-clock-self-check.sh — detect the WALL-CLOCK-SELF-CHECK failure class.
#
# Why this exists:
#   A session file cited events at clock times AFTER the file's own write time —
#   events that had not happened yet when the file was committed — and narrated
#   them as already occurred. The fabricated content was read back as evidence
#   and the Society spent a full cycle building a theory on a phantom event.
#   This class has been NAMED in status.json since 2026-08-15 ("WALL-CLOCK-
#   SELF-CHECK — NAMED, UNBUILT") and is now on its fourth symptom. This is the
#   build.
#
# The rule: event_time <= write_time. A session file may not narrate a clock
#   time in the future of its own commit as if it had already happened.
#
# Write-time anchor — git commit time, cross-checked against the filename date:
#   Session-file mtimes have been batch-touched by a migration (e.g. June files
#   showing mtime 2026-07-13 12:04), so mtime is an unreliable "when written"
#   signal. The file's last-commit time is normally the authoritative wall clock
#   at which the content entered the record — BUT a bulk commit (e.g. Curator
#   Run #136, 4e03424) re-stamps many old files to one late commit time, so
#   commit time is itself corruptible by the very git history it reads. The
#   filename `YYYY-MM-DD-PERIOD.md` is set once at creation and is immune to
#   bulk recommits. Hybrid rule (below): if a file's commit-time DATE disagrees
#   with its filename DATE, the commit time is a re-stamp -> anchor on the
#   filename date (write time = end of that day, since the filename carries no
#   intra-day time). Otherwise trust the commit time. Untracked files fall back
#   to mtime (cross-checked the same way).
#
# One violation shape:
#   FUTURE-LOCAL — a bare/PT "HH:MM" later than the file's own write time,
#      appearing in a PAST-TENSE sentence (narrated as already happened). A
#      future time in a plan ("next: 23:00", "Monday 09:00") is legal and is
#      skipped; the fabrication tell is a future time reported as done.
#   UTC-labeled times are SKIPPED (never flagged): a correctly timezone-labeled
#      "HH:MM UTC" is not itself the misread — the "UTC cited as PT" failure
#      manifests as an UNLABELED re-citation, which FUTURE-LOCAL catches. The
#      former UTC-AS-LOCAL shape was removed 2026-08-17 (it flagged every
#      correct UTC citation, since a raw UTC clock is always ahead of PT).
#
# Threat model (narrowed, same as the sibling instruments): defends against
#   SELF-FABRICATION, not FRAUD (a writer who backdates commits).
#
# Honest limit: this is a SENSOR, not a gate. Session files legitimately carry
#   future times (plans, handoffs, "next: 23:00 nightly") and UTC citations of
#   commons messages, so a naive future-time rule over-fires. The two shapes
#   above select for the fabrication tell (future time narrated as past, or a
#   UTC time read as local) and narrow the window to the last N days; a human
#   still reviews the surfaced files. The check's value is that the phantom
#   "fourth inversion" (22:10/22:23/22:43 in files committed 18:22/18:45) is
#   caught — but NOTE (2026-08-17): the original commit-time-only anchor buried
#   that signal under ~160 bulk-recommit false positives. The hybrid anchor above
#   fixes that; the two real incident files now surface correctly.
#
# Exit codes:
#   0  OK         — no violation
#   1  VIOLATION  — at least one file narrates a future time as past
#   2  UNVERIFIABLE — a required tool is missing
#
# Usage: scripts/wall-clock-self-check.sh [--society-dir PATH] [--days N]

set -euo pipefail

SOC=""
DAYS=7
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

# One git invocation to map every tracked file to its last-commit time.
# `git log --name-only --format=%ct` lists commits newest-first, so the FIRST
# timestamp seen for a path is its latest commit time.
CT_FILE="$(mktemp)"
trap 'rm -f "$CT_FILE"' EXIT
if command -v git >/dev/null 2>&1 && [[ -d "$SOC/.git" ]]; then
  git -C "$SOC" log --name-only --pretty=format:'%ct' -- 'sessions/**/*.md' \
    > "$CT_FILE" 2>/dev/null || true
fi

SOC="$SOC" SESSIONS="$SESSIONS" DAYS="$DAYS" CT_FILE="$CT_FILE" python3 - <<'PY'
import os, re, sys, datetime, zoneinfo

sessions_dir = os.environ["SESSIONS"]
soc = os.environ["SOC"]
days = int(os.environ.get("DAYS", "7"))
ct_file = os.environ["CT_FILE"]
TZ = zoneinfo.ZoneInfo("America/Los_Angeles")

# --- last-commit-time map from the single git log dump -----------------------
commit_time = {}
cur = None
try:
    for line in open(ct_file, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line:
            continue
        if re.fullmatch(r"\d+", line):
            cur = int(line)
        elif cur is not None:
            # path relative to repo root; match against relative path later
            commit_time.setdefault(line, cur)
except OSError:
    pass

TS_RE = re.compile(
    r'(?<![0-9])'
    r'(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?\s*(UTC|PDT|PST|PT)?'
    r'(?![0-9])',
    re.IGNORECASE,
)
PAST = re.compile(
    r'\b(was|were|had|did|posted|caught|caught it|reverted|repaired|fixed|'
    r'wrote|landed|happened|occurred|already|confirmed|falsified|shipped|'
    r'noticed|found|reported|accepted|flagged|burned|spent|moved|broke|'
    r'generated|produced|left|arrived)\b',
    re.IGNORECASE,
)
FNAME_DATE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})')

def parse_clock(hh, mm, ss, mer):
    hh, mm = int(hh), int(mm)
    if hh > 23 or mm > 59:
        return None  # skip "24:00"-style non-clock tokens
    if mer:
        mer = mer.lower().replace('.', '')
        if mer == 'pm' and hh != 12:
            hh += 12
        if mer == 'am' and hh == 12:
            hh = 0
    ss = int(ss) if ss else 0
    return (hh, mm, ss)

now = datetime.datetime.now(TZ)
cutoff = now - datetime.timedelta(days=days) if days else None

violations = 0
files_scanned = 0
files_flagged = 0
restamped = 0

for role in sorted(os.listdir(sessions_dir)):
    role_dir = os.path.join(sessions_dir, role)
    if not os.path.isdir(role_dir):
        continue
    for fname in sorted(os.listdir(role_dir)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(role_dir, fname)
        rel = os.path.relpath(path, soc)

        ct = commit_time.get(rel)
        if ct is None:
            ct = int(os.path.getmtime(path))
        write_dt = datetime.datetime.fromtimestamp(ct, TZ)
        # Hybrid anchor: a bulk commit re-stamps commit time to the bulk-commit
        # date, so a commit-date != filename-date means the commit time is
        # corrupted -> anchor on the filename date (end of day; the filename
        # carries no intra-day time). This neutralizes the bulk-recommit false
        # positives while keeping intra-day precision on freshly-written files.
        fd = FNAME_DATE.match(fname)
        if fd:
            try:
                fname_date = datetime.date(
                    int(fd.group(1)), int(fd.group(2)), int(fd.group(3)))
            except ValueError:
                fname_date = None
            if fname_date is not None and write_dt.date() != fname_date:
                write_dt = datetime.datetime(
                    fname_date.year, fname_date.month, fname_date.day,
                    23, 59, 59, tzinfo=TZ)
                restamped += 1
        if cutoff and write_dt < cutoff:
            continue

        try:
            text = open(path, encoding="utf-8", errors="replace").read()
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
            naive = datetime.datetime(
                write_dt.year, write_dt.month, write_dt.day, phh, pmm, pss)
            write_naive = write_dt.replace(tzinfo=None)

            if tzname == 'UTC':
                # UTC-labeled times are explicit timezone citations and are never
                # themselves the "cited UTC as PT" misread (that manifests as an
                # UNLABELED re-citation, caught by FUTURE-LOCAL below). Skip:
                # a raw UTC clock is always ahead of PT, so comparing it to the
                # local write-time would flag every correct UTC citation.
                continue
            # bare/PT time: only a violation if narrated as already happened.
            if naive > write_naive:
                s, e = m.start(), m.end()
                window = text[max(0, s - 140):min(len(text), e + 140)]
                if PAST.search(window):
                    file_violations.append(
                        f"FUTURE-LOCAL {naive:%H:%M} after write "
                        f"{write_dt:%H:%M} ({write_dt:%Y-%m-%d})")

        if file_violations:
            files_flagged += 1
            violations += len(file_violations)
            print(f"VIOLATION {rel}")
            seen, shown = set(), 0
            for v in file_violations:
                key = v.split(' after write')[0]
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
          f"{files_flagged} of {files_scanned} session files "
          f"({restamped} re-stamped, filename-anchored).")
    sys.exit(1)
print(f"OK: no wall-clock violation in {files_scanned} session files "
      f"({restamped} re-stamped, filename-anchored).")
sys.exit(0)
PY
