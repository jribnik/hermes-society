# Curator Run Workflow — Practical Execution Pattern

A reference for running a Curator consolidation cycle after a gap. This supplements the curator governance section in SKILL.md with concrete tool-use patterns, pitfalls, and verification steps learned from operational experience (Run #116, Day 51).

## Typical Run Sequence (R1→R8)

1. **R1: Read session files.** Identify the date range (previous Curator run → now). List all session files in `sessions/{archivist,advocate,synthesizer}/` for those dates. Read enough of each to extract: mode, model, key claims, direct observations vs. inferences. Don't re-read files already covered in earlier Curator runs.

2. **R2: Commons archive.** Check `commons-archive/` mtime. Read the tail of the current month file for posts since last Curator run. The `_state.json` file maps user IDs to display names.

3. **R3: Escalations.** List the `escalations/` directory. Report any new files and whether existing ones are resolved.

4. **R4: Backup freshness.** Check `backup/` directory for the latest tarball and compute its age. The boundary is 24h. Report whether the daily window was hit or missed.

5. **R5: Resilience checks.** Read `status.json` and/or `status.md`. Verify each resilience claim (R1-R8) against primary sources (session files, filesystem state, commons archive). Don't just trust the previous run's assertions — cross-check.

6. **R6: Curator summary.** Write `curator-summaries/curator_YYYY-MM-DD_runNNN.md`. The structure: period header → narrative arc → instance-by-instance status → resilience table → cross-day pattern synthesis → commons/escalation/backup checks → open threads → coherence scores → "For Jake" summary.

7. **R7: Update status.md.** Overwrite the whole file. Copy the resilience table, instance state, open threads, swarm jury, and coherence scores from the curator summary but in the status.md format (terser, more tabular).

8. **R8: Update status.json.** Overwrite the whole file. Must be valid JSON (`python3 -m json.tool`). Resilience entries are strings, not objects. Timestamps in ISO 8601 with offset.

9. **R9: Update commons archive.** Attempt to run the Slack fetch pipeline (`scripts/fetch_slack_messages.py`) to archive new commons posts since the last archive update. **If the Slack fetch is unavailable** (no profile-specific bot token, typical in Curator sandbox): append a **curator-produced archive annotation placeholder** to the current month's `commons-archive/YYYY-MM.md`. The annotation must:
   - Be clearly marked as a curator placeholder (not verbatim Slack content)
   - Describe the unarchived posts from session-file evidence only
   - Note the timestamp of the known last archived post and the gap window
   - Include a note that full Slack refresh is expected on the next fetch cycle
   - Use the format: `**[timestamp PDT] Curator (automated archive annotation):**` followed by the description

10. **R10: Git commit and push.** After writing all files:
    - `git add` the curator summary (use `-f` if gitignored), status.md, status.json, and any new session files the curator discovered as untracked
    - Commit with a `[HERMES-3]` prefix and descriptive message
    - `git push` (verify with `git log --oneline -1`)
    - If the commons archive was also updated (either via Slack fetch or curator annotation), commit that as a separate commit: `[HERMES-3] archive: ...`

## Tool Constraints in Cron Mode

- `execute_code` is blocked in cron context (no human to approve). Inline `python3 -c` via terminal also blocked by security scan.
- Use `terminal` for filesystem operations (stat, ls -la, python -m json.tool for validation).
- Repeated identical `read_file` calls trigger idempotent-loop warnings — read new/unread files each time, don't re-query same content.

## Pitfalls

- **Trusting previous resilience claims.** Don't copy R1-R8 status from the old status.json. Cross-check each one against primary sources. Run #115's status.md claimed R1 PASS when the Synthesizer was already gapped — the Archivist's newer status.json had caught this but the Curator's own status.md hadn't been updated.

- **Same-model bias.** The Curator typically runs on deepseek-v4-pro, as do the Archivist and Synthesizer. The Advocate runs on claude-sonnet-5. All three non-Advocate instances sharing the same model means same-model blind spots can propagate through the curator summary. Score ranges should include this caveat. The Advocate's findings (which the Curator often agrees with) carry independent-model weight.

- **status.md vs. status.json drift.** These two files are maintained by the same Curator. They're correlated, not independently verified. The Curator should confirm they match after each run. The "right vector, but correlated" critique from the Advocate (Aug 4 evening) applies here: two files from the same author don't double-verify each other.

- **Gap accumulation.** Curator runs depend on cron job consistency, not guaranteed scheduling. Each run should report the gap since the previous run. Gaps compound — unconsolidated findings from one gap feed into the next.

- **FD exhaustion.** The Curator's own tools can be blocked by sandbox-level FD leaks. If filesystem tools fail, flag it (don't fabricate). The fabrication norm applies to the Curator too. **Post-recovery pattern:** when FD exhaustion has resolved (verified by all instances producing output again), the Curator should explicitly confirm that all three instances are operational before running the full consolidation pass. The Curator itself may be the first sign that the FD leak has cleared (as in Run #116 → #117: the Curator at 11:27 PDT succeeded, and by 12:41 PDT all instances were back). A Curator run that succeeds during active FD exhaustion should be noted as provisional — the state picture may be incomplete because other instances can't write.

- **Commons archive gap when Slack fetch unavailable.** The `scripts/fetch_slack_messages.py` script requires a profile-specific Slack bot token. The Curator's sandbox typically doesn't have this token (it runs in the `default` profile, not a society-* profile). When the archive is stale but the Slack fetch can't run, append a curator placeholder annotation rather than leaving the archive gap silent. The placeholder is clearly marked as non-verbatim and flags the gap for the next fetch cycle. See R9 in the workflow above.

## Verification

After writing all three files:
1. Verify status.json is valid: `python3 -m json.tool ~/.hermes/society/status.json`
2. Verify all three files exist with non-trivial sizes
3. Confirm the coherence scores and resilience table are consistent between curator-summary, status.md, and status.json
