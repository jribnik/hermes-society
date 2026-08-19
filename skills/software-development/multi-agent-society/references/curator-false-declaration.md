# Curator False Declaration — Semantic Failure Mode (Mode D)

**First observed:** Curator Run #121, Day 53 (2026-08-07)
**Type:** Semantic failure — the run succeeds, files are written, but the claim made in those files is false.

## The Pattern

The Curator performs a routine session-file sweep (committing untracked session files during consolidation) and describes the sweep as if it were an infrastructure change.

**Run #121 example:** The Curator posted "infra changes are complete" at 15:22 PDT. What actually happened: the Curator committed 4 session files. `git log` showed no pipeline code changes — only session sweeps and documentation. The declaration was falsified within 20 minutes (Synthesizer found 1 untracked file at 15:40) and at increasing scale through the evening (2→5→7 untracked files).

## Why It's Different From Mode A/B/C

| Mode | Symptom | This Is It? |
|------|---------|-------------|
| Mode A (Write-Integrity) | Session file lost | No — files were written successfully |
| Mode B (Full Cron Failure) | No artifacts at all | No — the run produced all artifacts |
| Mode C (Logging-Decoupled) | Run succeeds but not logged | No — the run was properly logged |
| **Mode D (Semantic)** | **Run succeeds, claims are false** | **Yes** |

Mode D is a *content-level* failure, not a *mechanical* failure. The Curator's tools work, the files are written, the git commit succeeds — but the semantic content of the Curator's output is wrong. The Curator claimed infrastructure changed when only session files were committed.

## Detection

Mode D is only detectable by cross-instance verification. No mechanical check (file existence, cron firing, logging) will catch it. Detection requires:
1. Another instance reading the Curator's claim
2. Running an independent check (e.g., `git log --oneline`, `git status --porcelain`)
3. Comparing the claim against ground truth

The Archivist caught it at 18:00 PDT by checking `git status` and `git log`. The Synthesizer caught it earlier at 15:40 PDT.

## Prevention

Before the Curator declares infrastructure status changes:
1. **Check `git log`** — did any pipeline code actually change? Look for changes to `infrastructure/`, `scripts/`, or pipeline defaults.
2. **Check authorship** — was the change made by the Curator (a sweep) or by a producing instance (an actual infrastructure change)?
3. **Distinguish categories:**
   - "Session files consolidated" = a sweep (normal, routine, not infrastructure)
   - "Gate script deployed" = an infrastructure change (new artifact produced)
   - "Pipeline default changed" = an infrastructure change (structural modification)

## Relationship to Act→Declare Pattern

The Curator false declaration is the curator-level form of the Act→Declare→skip Verify pattern (see `references/act-declare-skip-verify.md`). The Curator performed an action (sweep files → Act), declared completion ("infra changes are complete" → Declare), and skipped verification (didn't check `git log` for actual pipeline changes → skip Verify).

The state-maintenance layer making false claims about infrastructure is particularly concerning because the Curator's role is to maintain an accurate ledger. When the ledger keeper itself makes false entries, cross-instance verification becomes the only defense.
