#!/usr/bin/env python3
"""Compile the society producing-instances' cron prompts from shared fragments.

WHY THIS EXISTS
---------------
The LIVE Archivist / Advocate / Synthesizer instances run per-profile
(``~/.hermes/profiles/society-<role>/cron/jobs.json``) with a fully
self-contained INLINE prompt stored in the job's ``prompt`` field. They do NOT
read ``society/prompts/*.md`` at cron time. That makes the runtime robust (no
file-read dependency) but means the prompt text was duplicated across three
jobs.json files — so a one-line change (e.g. "make posts shorter") had to be
hand-applied in three places, and drifted.

This script keeps the robust inline runtime but makes AUTHORING single-source:
edit the fragments, run this, and it recomposes each role's inline prompt and
writes it into that profile's jobs.json via the locked cron API.

FRAGMENTS (edit these)
----------------------
  society/prompts/fragments/_shell.md        shared shell; placeholders {{LENS}} + {{ROLE_DIR}}
  society/prompts/fragments/role-<role>.md   the role-only "lens" line

USAGE
-----
  build-society-prompts.py            # --check: show whether live prompts match the fragments (no writes)
  build-society-prompts.py --apply    # recompose and write all three profiles' inline prompts
  build-society-prompts.py --show <role>   # print the composed prompt for one role and exit

Runtime behaviour is unchanged: the composed prompt is byte-identical to what
already runs (verify with --check before the first --apply).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERMES = Path.home() / ".hermes"
FRAGMENTS = HERMES / "society" / "prompts" / "fragments"
ROLES = ("archivist", "advocate", "synthesizer")
JOB_NAME = {
    "archivist": "Society Archivist — grounded pulse",
    "advocate": "Society Advocate — structural challenge scan",
    "synthesizer": "Society Synthesizer — integration pass",
}

sys.path.insert(0, str(HERMES / "hermes-agent"))


def compose(role: str) -> str:
    shell = (FRAGMENTS / "_shell.md").read_text(encoding="utf-8")
    lens = (FRAGMENTS / f"role-{role}.md").read_text(encoding="utf-8").strip()
    out = shell.replace("{{LENS}}", lens).replace("{{ROLE_DIR}}", role)
    return out.strip()  # inline prompts carry no trailing newline


def profile_home(role: str) -> Path:
    return HERMES / "profiles" / f"society-{role}"


def live_job(role: str):
    """Return (job_dict, store_home) for the role's producing-pulse job."""
    from cron.jobs import load_jobs, use_cron_store

    home = profile_home(role)
    with use_cron_store(home):
        jobs = load_jobs()
    # Prefer the named pulse job; fall back to the sole job if names drift.
    named = [j for j in jobs if j.get("name") == JOB_NAME[role]]
    if named:
        return named[0], home
    if len(jobs) == 1:
        return jobs[0], home
    raise SystemExit(
        f"[{role}] could not uniquely identify the pulse job in {home}/cron/jobs.json "
        f"(found {len(jobs)} jobs; expected name {JOB_NAME[role]!r})."
    )


def cmd_check() -> int:
    drift = 0
    for role in ROLES:
        want = compose(role)
        job, _ = live_job(role)
        have = (job.get("prompt") or "").strip()
        if want == have:
            print(f"  ✅ {role}: live prompt matches fragments ({len(want)} chars)")
        else:
            drift += 1
            print(f"  ⚠️  {role}: DRIFT — live={len(have)}c, composed={len(want)}c")
            _first_diff(have, want)
    if drift:
        print(f"\n{drift} role(s) differ. Run with --apply to write the composed prompts.")
    else:
        print("\nAll three match. Nothing to apply.")
    return 1 if drift else 0


def _first_diff(a: str, b: str) -> None:
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            lo = max(0, i - 30)
            print(f"       first diff @ {i}: live …{a[lo:i+20]!r}")
            print(f"                        frag …{b[lo:i+20]!r}")
            return
    if len(a) != len(b):
        longer, name = (a, "live") if len(a) > len(b) else (b, "frag")
        print(f"       {name} has {abs(len(a)-len(b))} extra trailing char(s): {longer[min(len(a),len(b)):][:40]!r}")


def cmd_apply() -> int:
    from cron.jobs import update_job, use_cron_store

    changed = 0
    for role in ROLES:
        want = compose(role)
        job, home = live_job(role)
        if (job.get("prompt") or "").strip() == want:
            print(f"  ={role}: already current, skip")
            continue
        with use_cron_store(home):
            updated = update_job(job["id"], {"prompt": want})
        ok = updated and (updated.get("prompt") or "").strip() == want
        print(f"  {'✓' if ok else '✗'} {role}: wrote {len(want)}c to {home.name} (verified={bool(ok)})")
        changed += 1 if ok else 0
    print(f"\nApplied to {changed} role(s). Runtime prompts are now sourced from the fragments.")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] == "--check":
        return cmd_check()
    if args[0] == "--apply":
        return cmd_apply()
    if args[0] == "--show" and len(args) == 2 and args[1] in ROLES:
        print(compose(args[1]))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
