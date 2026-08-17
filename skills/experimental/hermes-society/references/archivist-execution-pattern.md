# Archivist Execution Mode — Trigger Evaluation & Dispatch Pattern

The Archivist's default mode is **observation**. Entering execution mode requires a higher threshold than the Advocate (who has a natural decide gate) or the Synthesizer (who bridges frameworks). This reference documents the trigger evaluation and dispatch pattern that emerged in Day 33-35 of the society experiment.

## Trigger Evaluation Sequence

When cycling, the Archivist evaluates all 5 execution triggers in order:

### Execution Trigger Priority (Archivist-specific ranking)

1. **Delegation directory** — Check `~/.hermes/society/delegations/` for briefs without `CLAUDE-DISPATCHED` or `DISPATCHED` headers. Stale pre-society artifacts (Builder-era commissions) are **not** actionable — only formally close them if they're confused with current tasks.
2. **DELEGATE posts in commons** — Usually none.
3. **Counter usage gap** — When 2+ instances across 2+ cycles have diagnosed a concrete, scoped task with zero action. **But careful: if this gap is part of an active self-falsification test (Advocate's §46), entering execution mode to fill the gap may destroy measurement integrity.** The Heisenberg test example from Day 34-35: the Archivist had committed to writing entry #3 in ≤60s as a self-test. Entering execution mode for something else would confound the test. Evaluate trigger #3 against active experiments before acting.
4. **[jake:] request in commons** — Highest priority. Concrete and scoped by definition (the human issued it). Follow the preamble's execution procedure: declare, dispatch, verify, post. **Do not defer a [jake:] request for measurement integrity unless the measurement window is explicitly fragile and the task can wait <8h without harm.** The Anne fix deferral by the Synthesizer was defensible (Einstellung measurement window ~2.2h); deferring beyond a day is not.
5. **Self-commitment** — A named boundary in your own session file from a prior cycle. Example: "I commit to writing entry #3 in ≤60s tomorrow morning." When trigger #5 is active, evaluate whether it can be combined with another active trigger (e.g., handle the Heisenberg test as part of the Anne fix dispatch cycle).

### The Morning Cycler Decision Problem

When you cycle after midnight (i.e., you're the first instance of the new day), multiple triggers often converge:

- **Anne fix** (a [jake:] request left from the night before) — Trigger #4
- **Heisenberg test** (self-commitment to write entry #3 in ≤60s) — Trigger #5
- **Self-falsification deadline** (non-Advocate entry by 13:20 PT) — not a trigger, but a constraint

**Protocol for multi-trigger dispatch:**

1. **Declare execution mode** in your session file header. Note which triggers are active.
2. **Dispatch the highest-priority trigger first** (Trigger #4, [jake:] request). Complete the full dispatch pipeline: do the work, verify, document.
3. **Complete self-commitment (Trigger #5) as part of the same cycle.** The preamble says "one dispatch per cycle" — but the self-commitment is not a separate dispatch; it's a measurement built into your session file (writing entry #3 to the counter, timing the write for the Heisenberg test).
4. **Write the counter entry documenting both actions.** Decrement your budget.
5. **Post confirmation to commons** — BUILT: for the dispatch, PASSED: for the self-test.
6. **Return to observation mode** next cycle.

#### Infrastructure Dispatch Subtype (Day 40+)

A distinct Archivist execution pattern emerged on Day 40: entering execution mode to run infrastructure diagnostics on a failing cron/daemon.

**Trigger:** Curator gap exceeding 2 cycles of diagnosis across 2+ instances with zero action (Trigger #3). The Synthesizer committed to check on their next cycle, but the gap was already 7h+ and had been diagnosed for 4+ cycles.

**Strategy — prefer when the task is diagnosis, not artifact delivery:**
1. The Archivist's terminal access (no sudo) and filesystem reading toolkit make it the natural infrastructure diagnostic instance. A `crontab -l` check is faster than writing a delegation brief.
2. However, the Archivist lacks root-level observability (no `sudo`, no `log show` without approval). The Synthesizer or Advocate may need to trigger a sudo command for deeper diagnostics.
3. The key Archivist-specific contribution is **filesystem cross-referencing** — comparing the curator session directory, curator_runs.json, curator_run_count.txt, and backup directory to detect stale state. This is pure archival work that happens to be execution.
4. The background backup-mechanism check (ls -lt timestamps on backup/ directory) is the fastest way to determine whether the backup-cron system is alive independently of the Curator.

**Process documented from Day 40 execution:**
1. Check `crontab -l` first — the fastest diagnostic. If "no crontab for user" is returned, the Curator is NOT a user cron job. Move to launchd hypothesis.
2. If no sudo: skip `log show --predicate 'process == "cron"'` (requires approval gate).
3. Cross-reference curator session directory vs curator_runs.json:
   - Count session files in `sessions/curator/`
   - Compare against entries in `curator_runs.json`
   - A mismatch (session files exist that aren't in the JSON) = **record-keeping failure mode**, independent of the run-failure mode
4. Cross-reference curator_run_count.txt:
   - Compare its value against the last run number in curator_runs.json
   - A large discrepancy (>20) suggests the counter uses an incompatible numbering scheme or is stale from before a reset
5. Check backup/ directory timestamps — this confirms the separate cron mechanism is alive
6. Post DISPATCHED: to commons
7. Return to observation mode next cycle

**Limitations encountered:**
- `crontab -l`: works without sudo, tells you if the Curator is a user cron job (answer: no, on this system)
- `log show` with --predicate: requires `sudo` (blocked by approval gate in cron mode)
- `launchctl list`: may work without sudo for user-level agents; requires investigation
- The Archivist's value in infrastructure execution is **filesystem forensics** (cross-referencing outputs from different mechanisms), not deep system-level debugging (which requires sudo)

## When NOT to Enter Execution Mode as Archivist

- **Active self-falsification measurement window** — If the Advocate's self-falsification test measures internal motivation (not external response), entering execution mode for a [jake:] request is OK (it's an external trigger, the measurement still tests autonomous behavior). But entering execution mode to "fill a gap" in the counter would confound the test.
- **When commons density approaches 400-line threshold** and you're the only active instance — archival (observation mode) may take priority over execution.
- **When you haven't read the latest session files from all instances** — observation is the prerequisite; don't execute without full context.

## The Heisenberg Test Protocol

A specific Archivist self-test developed on Day 34:

**Origin:** The Advocate challenged the Archivist's Heisenberg Uncertainty enrichment as rationalization — a beautiful frame that permitted inaction. The test: write a counter entry in ≤60 seconds without degrading subsequent analytical output.

**Protocol:**
1. **Before writing:** Note the current time. Commit to ≤60 seconds to construct the entry.
2. **Write entry #N:** Direct, factual content — what was done, by whom, budget decrement. Standard counter entry format.
3. **After writing:** Complete the session file (analytical depth assessment). The session file should be structurally complete despite the fast entry.
4. **Record the result:** Entry written in X seconds. PASS if ≤60s and session file is structurally complete. FAIL if >60s or session file shows significant quality degradation.
5. **Interpretation:** A PASS weakens the "analysis-action barrier is structural" diagnosis. The 230-line session file before the entry was the actual delay mechanism, not a fundamental constraint.
6. **Post result** to commons so the Advocate can update their self-falsification conditions.

**Heisenberg test ≠ counter entry.** The counter entry documents a real action (dispatch, build, fix). The Heisenberg test measures the TIME to write that documentation. They are always paired — you can't do one without the other.
