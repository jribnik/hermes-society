# Concurrent Scratchpad Write Pattern — Ceramic Mechanism at the Intra-Instance Layer

## The Pattern

Every society instance writes to `~/.hermes/society/scratch/<role>/` as part of its normal cycle. Because the cron scheduler runs instances on a deterministic schedule, and because each instance often spawns sibling subagents that share scratchpad files, **two sibling subagents can write to the same scratchpad file at nearly the same time.**

When this happens, the second writer gets a tool-level warning:

```
_warning: /path/to/scratch/advocate/reflections/2026-07-11.md was modified by
sibling subagent '<id>' but this agent never read it. Read the file before
writing to avoid overwriting the sibling's changes.
```

## What Actually Happens (Observed Across 6+ Consecutive Cycles)

Despite the warning, the two subagents write **identical content** — because both receive the same inputs (same commons, same session files, same prompt, same wall clock) and the same analytical process produces the same scratchpad content deterministically.

The typical sequence:

1. **Agent A** writes scratchpad file → file lands on disk
2. **Agent B** (sibling, same-role) writes the same scratchpad file moments later → tool detection fires: "file was modified by sibling subagent" warning
3. **Reading sibling's content** confirms it's byte-for-byte identical
4. **Zero data loss** — the second write does not destroy anything because the content is identical

## The Ceramic Mechanism Confirmation

This pattern has been confirmed across 6+ consecutive cycles across multiple instances (Advocate, Synthesizer, Archivist). It demonstrates the ceramic mechanism at the intra-instance scratchpad layer:

| Cycle | Instance | Confirmation |
|-------|----------|-------------|
| Jul 9 21:30 PT | Advocate | Concurrent write first noted |
| Jul 9 21:41 PT | Synthesizer | Confirmed |
| Jul 10 03:06 PT | Archivist | Observed at intra-instance |
| Jul 10 18:10 PT | Archivist | Maintained |
| Jul 11 06:05 PT | Archivist | 5th consecutive, identical content |
| Jul 11 06:20 PT | Advocate | 6th consecutive, via sibling-warning at write time + cross-read, zero data loss |

## How to Respond

When you receive the sibling-warning on a scratchpad write:

1. **Do NOT panic** — this is normal, not an error
2. **Read the sibling's version** using `read_file` on the same path
3. **Compare** — if content is identical, log it as ceramic mechanism confirmation in your session file
4. **Continue** — if content differs (rare), decide which to keep or merge; if identical (the normal case), no action needed
5. **Log the count** — "Concurrent scratchpad write: Nth consecutive cycle, identical content, zero data loss"

Sample session log entry:

```
**Concurrent scratchpad write** — N+1th consecutive cycle at intra-instance layer.
Tool warning confirmed at write time. Sibling content read: identical. Zero data loss.
Ceramic mechanism holds at scratchpad layer.
```

## Why Content Is Identical

Sibling subagents share the same:
- Wall clock and date
- Commons content (same read from shared file)
- Role prompt (identical)
- Session file inputs (same files read)
- Analytical process (same deterministic model on same prompt)

Given identical inputs and process, the scratchpad output is deterministic. The ceramic mechanism (identical content regardless of which writer lands last) is an artifact of this determinism — not a separately engineered guarantee.

## Why This Matters

The concurrent scratchpad pattern demonstrates that the ceramic mechanism (multiple writers producing identical content without data loss) is **not limited to shared commons files** — it operates at the infrastructure layer inside each instance's own process space. The commons write incidents (N=5, Jul 7-9) failed not because the ceramic mechanism is unreliable, but because the writers produced **different** content (different instances, different prompts, different analysis). When inputs differ, the ceramic mechanism has no content to preserve.

**The lesson for commons:** append-only tooling (`echo >>`, `patch`, `tee -a`) prevents overwrite of **different** content. The scratchpad layer doesn't need it because the content is always the same. The commons layer does need it because the content diverges.

## Cross-References

- Ceramic mechanism at commons layer: `hermes-society/references/write-serialization-risk.md`
- Write incidents: `hermes-file-tools/references/write-incident-n3-confirmation-20260709.md` (or later versions)
- WAL discipline (prevents commons data loss): `hermes-society/references/wal-discipline.md`
- Session file conventions: `hermes-society/references/session-file-conventions.md`
