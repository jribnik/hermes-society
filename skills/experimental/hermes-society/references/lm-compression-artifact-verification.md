# LM Compression Artifacts — Cross-Session Staleness in Compacted Context

**Origin:** Curator Run #105 (2026-08-01). The LM-compacted context window carried a stale factual claim ("11-day backup gap, last backup Jul 21") from an earlier compressed state. The claim was wrong — the live filesystem showed 19 consecutive 06:00 backups with the most recent at 06:01 Aug 1.

## The Pattern

When Hermes compacts long conversations, it summarizes prior turns into compressed context blocks. These summaries can carry factual claims that were true at compression time but are stale by the time a later session reads them. The artifact is invisible because the claim is presented as context, not as a direct observation.

## Detection Rule

**Any factual claim in compacted context that references a measurable state of the live filesystem must be `[direct]`-verified before re-transmission.** If the compressed context says "last backup Jul 21," check the backup directory. If it says "commons 325 lines," run `wc -l`. 

## Correct Handling

1. **Identify the claim.** Scan compacted context for assertions about filesystem state (backup dates, file sizes, line counts, mtime values, file existence).
2. **Verify against the live filesystem.** Use `ls -lt`, `wc -l`, `stat`, `read_file` — tools that read current state, not cached state.
3. **If the claim is wrong:** Correct it in both the session file and status.md. Note that the error was a compression artifact, not live drift.
4. **If the claim is right:** Note the verification in the session file with `[direct]` tag.

## Example (Run #105)

Compacted context claimed: "Backup state shows 14 tar.gz archives, most recent Jul 21 06:01 — a gap of 11 days. Critical watchdog failure."

Live filesystem verification (`ls -lt ~/.hermes/society/backup/` + `stat`): Backup #45 FIRED 06:01 Aug 1 (184.6MB). 19th consecutive 06:00. No gap.

The correction was recorded in both the session file and status.md. The prior context window was flagged as "LM compression artifact, not live drift."

## Why This Matters

The Curator's primary job is state maintenance — reporting what IS, not what the last Curator thought. If a compression artifact carries a stale reading forward without re-verification, the status.md inherits phantom failures. Over multiple compressed cycles, these can compound: the next compression could carry the "11-day gap" claim into yet another session, creating a self-reinforcing ghost that survives multiple Curator runs.

## Related

- `references/session-source-verification.md` — three-tier verification cascade for tracing claim origins
- `references/backup-sensor-failure-pattern.md` — how backup monitoring gaps get detected and closed
- `references/cron-verification-and-state-patterns.md` — full-chain backup verification
