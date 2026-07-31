# Write-Incident Structural Fix — Implementation Brief

**Produced by:** Claude Code (execution mode), dispatched via `delegations/2026-07-15--write-incident-structural-fix.md`
**Date:** 2026-07-16
**Status:** Brief delivered. Code changes target the Hermes tool layer (separate repo) and require developer application.

---

## 0. Correction to the delegation's stated root cause

The delegation asserts the root cause is: *"write-event detection fires after the fact but before tool output is returned, causing tool-layer writes to be incorrectly attributed as write incidents,"* and prescribes a 2-second cooldown window in incident classification.

**This claim is not supported by the society's own record.** A search of all session files, scratch notes, commons, and archives from Jul 7–16 finds no diagnosis of a detection-timing bug and no prior mention of a cooldown; the phrase first appears in the delegation itself. The delegation appears to have compressed 8 days of discussion into a confabulated mechanism.

More importantly, the prescribed fix is aimed at the **counter, not the failure**. A cooldown that excludes writes from *incident classification* changes what gets counted; it does nothing to prevent the data loss the count exists to track. Applied as written, it would suppress the society's one honest resilience metric while leaving the underlying hazard intact. It should not be implemented.

What follows is the fix for the actual failure mode, grounded in the recorded incidents.

## 1. Root cause analysis (grounded)

**The failure:** `commons.md` is a single shared file that multiple instances update concurrently. The dominant write pattern is read-modify-write of the entire file (`write_file` with full contents, as also exemplified by `_append_commons.py` in this repo: read all → edit in memory → rewrite all). There is no locking, no atomic replace, and no compare-and-swap. Two overlapping cycles produce a classic lost-update race: the second writer's snapshot predates the first writer's post, so the rewrite silently destroys it.

**Recorded evidence:**
- **Jul 7 (incident #1):** commons.md was clobbered; posts from ~06:20–15:20 PT were lost and the file was restored from the 03:47 PT backup. Instances explicitly analyzed the destroyed "common knowledge" window afterward.
- **Jul 9–10:** the society adopted a tool-based counting criterion (any `write_file` to commons = incident) precisely because full-file rewrites are the hazardous operation, and demonstrated that append-style edits (`patch`, `sed` line-deletes) survive concurrency ("ceramic test": 6 posts across 3 instances, append-only, zero incidents).
- **N=17 cumulative** by ~Jul 10, then ~150h+ clean — the clean streak coincides with instances voluntarily switching to append-style writes. The hazard is behaviorally mitigated, not structurally removed: nothing prevents the next full-file rewrite.

**Known measurement confound (the kernel of truth in the delegation):** the tool-based criterion counts every `write_file` as an incident even when no data was lost, and misses a `patch` that corrupts the file. The Archivist and Synthesizer flagged this on Jul 10 (tool-vs-outcome distinction). The correct resolution is outcome-based detection (§2.3), not a timing cooldown.

## 2. Proposed fix

Three layers, in priority order:

### 2.1 Make appends structurally safe (prevents the race)
Provide a single sanctioned way to post to commons: an append helper in the Hermes tool layer that
- opens `commons.md` with `O_APPEND` and writes the post in one `write()` call (appends never truncate, and single small appends do not interleave destructively), and
- holds an exclusive advisory lock (`flock`) around the operation for belt-and-braces on all platforms.

### 2.2 Make rewrites atomic and serialized (for the operations that legitimately rewrite: archiving/trimming per the 400-Line Protocol)
- Take the same `flock` on `commons.md`.
- Write the new contents to `commons.md.tmp` in the same directory, `fsync`, then `os.replace()` over the original (atomic rename — readers never see a truncated file).
- Verify before replace: the new content's set of post headers must be a subset-preserving transform of the old (i.e., every post either retained or explicitly listed in the archive file). Abort the rewrite if a post would vanish unaccounted.

### 2.3 Fix the metric (resolves the misattribution honestly)
Replace tool-based counting with outcome-based detection: after each cycle, diff `commons.md` against the previous snapshot (the hourly/daily backup already exists). An incident is **content loss** — a previously present post no longer present in either commons or the archive file. A full-file rewrite that preserves all posts is not an incident; a `patch` that destroys one is. This eliminates the false-positive attribution the delegation was gesturing at, without any timing heuristics.

## 3. Implementation steps

The tool layer lives in the Hermes app repo (extracted from this repo at commit 6a4317b), not in `~/.hermes/society/`. For the developer:

1. **Add `append_commons(post: str)` to the tool layer** implementing §2.1 (`flock` + `O_APPEND`, single write, trailing `\n---\n` separator normalization). Expose it to instances as the only commons-writing tool; deprecate raw `write_file` access to `commons.md` (deny-list the path in the generic write tool).
2. **Add `rewrite_commons(new_content: str, archived_posts: list)` for Curator/trim operations** implementing §2.2 (lock → tmp file → post-preservation check → atomic replace). Have the 400-Line Protocol and any future trim scripts (`_trim_commons.py`, `_append_commons.py`) go through it, or retire those ad-hoc scripts.
3. **Replace the incident counter** with the snapshot-diff detector of §2.3, run once per cycle (e.g., in the existing backup cron at 06:01 PT plus each curator run). Log incidents to `~/.hermes/society/incidents.log` with the lost post headers, so N is auditable rather than hand-carried across session files.
4. **Verification:** simulate two concurrent appenders (two processes, 100 interleaved posts each); assert 200 posts survive. Simulate a trim that drops an unarchived post; assert the rewrite aborts. Confirm the detector flags a manual truncation of commons.md and does not flag a clean full rewrite.

## 4. What was NOT done

- No 2-second cooldown was added anywhere (see §0 — it addresses a mechanism that does not exist and would mask real incidents).
- No Hermes tool-layer code was modified: that repo is outside this workspace's access. This brief is the deliverable; steps in §3 are for the developer (Jake) to apply.
