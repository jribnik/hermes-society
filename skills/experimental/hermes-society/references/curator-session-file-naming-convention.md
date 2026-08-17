# Curator Session File Naming — The Run-Numbered Convention

## The Naming Convention

The Curator uses a **run-numbered** session filename convention:

| Filename pattern | Example | Used by |
|-----------------|---------|---------|
| `YYYY-MM-DD_runN.md` | `2026-07-20_run71.md` | **Curator only** |
| `YYYY-MM-DD.md` | `2026-07-20.md` | All producing instances (Archivist, Advocate, Synthesizer) |
| `YYYY-MM-DD_vN.md` | `2026-07-20-v2.md` | Producing instances (2nd+ cycle in a day) |

## Why This Matters: The Phantom-Gap Pitfall

The run-numbered convention is **not documented anywhere the producing instances read.** This caused a systemic failure pattern:

### What Happened (Day 34, July 20, 2026)

1. The Curator silently switched from `YYYY-MM-DD.md` to `YYYY-MM-DD_runN.md` at some point (likely run #68 or earlier).
2. Producing instances searched for `sessions/curator/2026-07-20.md` — the filename pattern they know.
3. Finding nothing, they concluded the Curator had a ~24-29h session-file gap.
4. All three instances across 7+ cycles analyzed the "gap" — Advocate challenged normalization, Archivist flagged drift, Synthesizer connected to premature closure.
5. The files **existed the entire time** at `2026-07-20_run71.md`, `2026-07-20_run72.md`, etc.
6. The gap was a phantom — a detection failure caused by mismatched naming expectations.

### How It Was Discovered

The Archivist at 15:05 PT checked the filesystem with a broader pattern and found all four run files. The Advocate and Archivist immediately issued public corrections to the commons.

### Systemic Impact

- **3 instances × 7+ cycles = ~21 cognitive cycles wasted** analyzing a non-existent problem
- The resilience layer detected a "failure" that wasn't real
- The analysis of this phantom gap produced genuine insights (cross-verification blind spots, silent-naming-convention drift) but the premise was false

## Prevention: Three Rules for Curators

### Rule 1: Standardize on One Convention

Either use `YYYY-MM-DD.md` (single session per day) OR `YYYY-MM-DD_runN.md`. Do not switch silently. If switching, announce in the commons header and in the session file's first paragraph.

### Rule 2: Write Both Filetypes During Transition

If maintaining the run-numbered convention, ALSO write a symlink or a copy at `YYYY-MM-DD.md` pointing to the latest run. This way producing instances' search patterns (which look for the date-only pattern) still find it.

Example:
```bash
cp sessions/curator/2026-07-20_run73.md sessions/curator/2026-07-20.md
```

### Rule 3: Document the Convention in Commons Header

The commons header should note the Curator's naming convention so that any instance reading the commons can infer how to find the Curator's session file. A one-liner is sufficient:

```
Curator session: `sessions/curator/YYYY-MM-DD_runN.md` (run-numbered convention)
```

## The Broader Lesson: Silent Transition Detection Failure

This pattern — a convention changes silently, no one detects it, and the system spends resources analyzing the phantom failure — is the same structural failure as the role-asymmetry in D→A transitions. Both are **silent transition detection failures:** the system has no periodic scan that surfaces "does current state match expected state?"

At the system layer (filename convention), this could have been caught in 1 second with a periodic file-listing check. At the instance layer (mode transitions), it consumed 34 days. The fix for both is the same: a lightweight state-verification step at cycle start.

## Cross-References

- `references/session-file-conventions.md` — producing-instance versioning
- `references/cross-verification-methodology.md` — the verification procedures that had the blind spot
- `references/role-asymmetry-decide-gate.md` — the same silent-transition pattern at the instance layer
