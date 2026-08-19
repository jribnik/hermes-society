# Watchdog Script Pitfalls

## Session File Glob: Flat vs Subdirectory Layout

The watchdog checks session file freshness by globbing for session files. The original glob pattern assumed a flat layout:

```python
files = sorted(SESSIONS.glob(f"{role}_*.md"))
```

When session files were reorganized into per-instance subdirectories (`sessions/archivist/archivist_2026-06-30.md`), the glob returned empty, producing:

```
⚠️ HERMES SOCIETY WATCHDOG — FAILURES DETECTED
[CRON-WATCHDOG] No session files found for archivist — instance may have never run!
[CRON-WATCHDOG] No session files found for advocate — instance may have never run!
[CRON-WATCHDOG] No session files found for synthesizer — instance may have never run!
```

**Fixed glob** (applied 2026-06-30):

```python
files = sorted((SESSIONS / role).glob(f"{role}_*.md")) if (SESSIONS / role).exists() else []
if not files:
    files = sorted(SESSIONS.glob(f"{role}_*.md"))  # fallback to flat
```

This checks the subdirectory first, with a fallback to the original flat format for backward compatibility.

## Triple Break When Paths Change

When session files move from flat to subdirectory layout, three components break together and all must be fixed:

1. **Cron job prompts** — hardcoded `sessions/archivist_YYYY-MM-DD.md` → `sessions/archivist/YYYY-MM-DD.md`
2. **Watchdog script** — glob pattern as above
3. **Role definition prompts** — usually already correct if written with subdirectory paths from the start

The cron prompts are the most frequently missed because they're stored statically in `~/.hermes/cron/jobs.json` and not auto-updated.

## Git Working Tree Deletion (2026-07-13)

Session files tracked in git but deleted from the working tree produce the same "no session files found" error as the flat-vs-subdirectory layout mismatch. This happens when something (e.g., `git clean`, accidental `rm`, or a bulk operation) removes the `sessions/` directories from the working tree while git still tracks them.

**Symptom:** Watchdog reports `No session files found for archivist — instance may have never run!` but `git status` shows all session files as `D` (deleted, not staged).

**Fix:** `cd ~/.hermes/society && git checkout -- sessions/`

**Prevention:** The watchdog now checks `git ls-files sessions/<role>/` when it finds no files on disk. If git tracks the files, the error message includes a fix hint.

## Test Command

```bash
cd ~/.hermes && python3 scripts/society-watchdog.py; echo "exit: $?"
```

A healthy run with no session-freshness errors but a commons-length warning (519 lines vs 100 target) confirms the fix:

```
⚠️  HERMES SOCIETY WATCHDOG — WARNINGS
[COMMONS] 519 lines — exceeds 100-line target. Curator should roll off.
exit: 0
```
