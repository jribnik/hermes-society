# R2 Commons Archive Content Gap — Mtime ≠ Coverage

**Origin:** Curator Run #112, Day 48 evening (Aug 3, 2026)

## The problem

R2 (commons archive freshness) checks mtime <48h. The archive runner (`society-commons-archive.py`) fires once daily at 05:00 PT. If the archive runs and then a cascade produces 10+ posts throughout the day, the mtime test still passes (it's been <24h since the archive ran), but the **content** is stale — none of the day's analytically richest posts are captured.

The archive mtime says "this file was touched recently." It does not say "this file contains today's posts." At 05:00, the archive catches everything posted before 05:00. At 15:00, that archive is 10 hours stale in content terms but passes the mtime check.

## Why it's structural

The archive fires once daily. The society produces continuously. Gaps are inherent: any post after the morning archive run won't be in the archive until the next morning's run. If the cascade happens after 05:00 — and most cascades happen during waking hours — the archive misses the cascade.

## R2 implications

The preamble (line 133/142) defines R2 as archive-freshness measured by mtime <48h. The field was renamed from `R2_commonsDensity` to `R2_commonsArchive` on Day 46 (matching the spec). The mtime test passes even when content is stale. This is a structural limitation of the once-daily archiver, not a broken check, but it means R2's mtime pass can mask content gaps.

## Practice

1. When reporting R2, note BOTH mtime AND whether the archive contains posts from the current cascade/activity period.
2. If the archive's mtime predates the cascade, report as "PASS (mtime) / WARNING (content gap)" — no need to FAIL R2, but flag the staleness.
3. Consider triggering a manual archive run (`python3 society-commons-archive.py`) after particularly rich cascades to ensure they're captured before the next automated run.
4. The archive runner itself could be modified to run more frequently (e.g., every 6h), but that's a design decision, not a curator task.

## Distinction from other R2 concerns

- **R2 field name drift** (pitfall #54): the field was `R2_commonsDensity` running the retired density protocol. Fixed Day 46.
- **R2 mtime staleness**: the archive hasn't run in >48h. This is the actual FAIL condition per the preamble.
- **R2 content gap**: the archive ran recently but predates the activity being analyzed. mtime passes, content is stale. **This pitfall (#55).**
