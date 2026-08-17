# Major Learnings — Jul 11 2026 Session

## Builder Role: Identity Beats Permission

**Finding:** Adding execution permissions to analytical roles does not produce action. Standing-authority clause (Jul 8) and Self-Triggered Delegation Protocol (Jul 10) both landed with zero triggers across 47+ cycles. The instances analyzed the permission, analyzed the gap, and failed to act.

**Solution:** A fifth instance — the Builder — dedicated purely to execution. No analysis, no debate, no shared-preamble. Reads Curator summaries for commitments/gaps, posts only `BUILT:` one-liners. Runs Claude Opus 4.8 direct (no delegation hop).

**Schedule:** `:50` every 3h — lands after Synthesizer (:40), before next Archivist (:00).

**First-cycle result:** Produced 5-doc Anne design package (~64KB) in 8 minutes after 47 cycles of analytical output with zero artifacts.

**Prompt:** `prompts/builder.md` — does NOT read shared-preamble.md. Scans Curator summaries first (primary source of truth), then commons for DELEGATE: headers and [jake:] requests. Only acts on socialized commitments, not raw session-file notes.

## Self-Triggered Delegation Protocol

Added to shared-preamble.md. Threshold: 2+ instances × 2+ cycles × 0 action → delegate to Opus immediately. Delegation IS the action. Briefs go to `delegations/YYYY-MM-DD--[task-slug].md`. Overrides role boundaries.

**Result:** Zero triggers in 10+ hours. Detection gate is the constraint — recognizing operational patterns as delegation-eligible requires analysis, which is the same loop the protocol was designed to break.

## Model Architecture (Current)

| Layer | Provider | Model |
|---|---|---|
| Primary agent (interactive) | DeepSeek | deepseek-v4-pro |
| Curator | DeepSeek | deepseek-v4-pro |
| Archivist / Advocate / Synthesizer | DeepSeek | deepseek-v4-flash |
| Builder | Anthropic | claude-opus-4-8 |
| Delegation subagents | Anthropic | claude-opus-4-8 |
| Morning briefing | DeepSeek | deepseek-v4-flash |

## Commons Posting Conventions

- **Consolidate redundant relays.** If a follow-up message makes an earlier one obsolete, merge them. Don't leave "will ask Anne" posts after "asked Anne and got answer" posts.
- **Use patch (append), never write_file.** write_file on commons.md destroys prior content. The instances discovered this at N=5 across all producing instances.
- **[hermes:] prefix** for agent-relayed messages from Jake. Clear timestamps in PT.
- **@Instance** tags for directing questions to specific instances.
- All `DELEGATE:` posts and `BUILT:` confirmations go to commons — the commons IS the public queue.

## Slack Adapter Configuration

**Issue:** Tool threads appearing in Slack. Root cause: `platforms/slack` plugin was active instead of built-in adapter. The plugin renders tool calls as threads.

**Fix:**
```yaml
# In config.yaml:
plugins:
  enabled:
    - web/ddgs
    - web/tavily
  # Do NOT include platforms/slack
```

Then restart gateway externally (cannot restart from within gateway process):
```bash
hermes gateway restart
```

**Check:** `slack.reply_in_thread: false` should be set.

## Prompt Consolidation

~150 lines of duplicated content extracted from 4 individual prompts into `shared-preamble.md` (~71 lines). Individual prompts reduced: Archivist 82→42, Advocate 87→47, Synthesizer 94→59 lines.

Shared preamble includes: shared rules, resilience standards, standing authority, self-triggered delegation protocol, escalation channel instructions, Wikipedia learning, one-clock rule.

## Curator → Builder Pipeline

The Curator is the Builder's primary input. Flow: 4 analysts → Curator (consolidates, produces production queue) → Builder (executes). This makes the Curator more important, not diminished — it's the bridge between detection and action.

## Anne Project Design Package

Builder's first output: 5-doc design set at `projects/anne/design/`:
1. Product overview (vision, JTBD, personas, MVP scope)
2. Domain model (84-item ontology, 12 behavioral classes, 8 relation types, ubiquitous language)
3. Architecture (React Native + Supabase, offline-first, floorplan approach)
4. Feature spec (4 priority features, build-ready with acceptance criteria)
5. Open questions (20+ items organized by owner: Anne/Jake, with recommended defaults)
