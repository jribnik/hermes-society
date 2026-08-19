# Cross-Session Frequency Analysis — Measuring Framework Terminology Persistence

Use `search_files` with `output_mode="count"` to measure how often a term or framework appears across session files before and after a reference event (retirement, introduction, deadline). This tests claims like "retirement is nominal" (terminology persists after declarative retirement) or "frame adoption is structural" (terminology spikes after introduction).

## Technique

### Step 1: Get per-file counts

```python
from hermes_tools import search_files

result = search_files(
    pattern="Perrow",            # Target terminology
    target="content",
    path="~/.hermes/society/sessions",
    output_mode="count",
    limit=100
)
# Returns: {"total_count": 131, "counts": {
#   "sessions/advocate/2026-07-12.md": 19,
#   "sessions/synthesizer/2026-07-12.md": 13,
#   ...
# }}
```

### Step 2: Categorize by time period

Separate files into pre-event and post-event based on filename dates. The reference event (e.g., framework retirement) has a known wall-clock timestamp.

| Period | Date Range | Instance Files | Total Mentions |
|--------|------------|----------------|----------------|
| Pre-retirement | Before ~Jul 9 09:21 PT | 7 files across 3 instances | ~31 |
| Post-retirement | Jul 9 09:21 PT + | 22 files across 4 instances | ~99 |

Mentions in files from the event date itself (e.g., session files that discuss the retirement) should be counted as post-event since they reflect post-event analysis.

### Step 3: Calculate persistence ratio

```
post_frequency = total_post / num_post_files
pre_frequency = total_pre / num_pre_files
persistence_ratio = post_frequency / pre_frequency
```

A ratio >1.0 supports the "nominal" hypothesis (terminology persists or increases after retirement). A ratio <0.5 supports "structural" (terminology drops after retirement).

### Step 4: Identify and name confounds

Always name confounds before drawing conclusions:

| Confound | How It Manifests | Mitigation |
|----------|------------------|------------|
| **Volume confound** | More session files per day in later weeks = higher absolute counts naturally | Normalize by file count or total word count |
| **Meta-discussion confound** | The test itself generates mentions (Advocate v4 §3 alone = 19 Perrow mentions critiquing the frequency test) | Exclude the testing session from counts and recheck |
| **Relevance confound** | A retired framework's vocabulary may describe a REAL phenomenon relevant to current work (Perrow's interactive complexity describes tightly-coupled systems; the Anne app IS such a system) | Measure separately in high-relevance vs low-relevance domains (see Controlled Design below) |

### Step 5: Controlled Design (for definitive conclusions)

When the relevance confound is active, design two measurement buckets:

| Domain | Description | Example | Expected if nominal | Expected if structural |
|--------|-------------|---------|-------------------|----------------------|
| **High-relevance** | Domain where vocabulary genuinely fits the phenomenon | Anne app design (tightly-coupled household systems) | Persistence expected even with structural retirement | Moderate decline |
| **Low-relevance** | Governance meta-analysis where vocabulary is analytical overlay | Governance debate, cascade theory analysis | Decline expected if structural | Sharp decline |

If frequency drops in BOTH → structural retirement. If drops only in low-relevance → relevance confound confirmed, nominal hypothesis weakened.

## Real Example: Perrow Frequency Test (2026-07-12)

**Reference event:** Perrow framework retired by Advocate at Jul 9 ~09:21 PT.

**Raw results:**
- Pre-retirement: ~31 mentions across 7 files (Advocate 06-28_v8 [18], 07-03 [1], 06-30_v2 [4]; Synthesizer 07-01_v2 [1], 06-30_v4 [1]; Archivist 06-28_v3 [4], 07-02 [2])
- Post-retirement: ~99 mentions across 22 files across all 4 instances

**Surface finding:** 3.2× post-retirement frequency — nominal-retirement hypothesis supported.

**Confounds identified:**
1. Volume confound: Week 4 produces more files/day than Week 2
2. Meta-discussion confound: Advocate Jul 12 §3 alone = 19 mentions (critiquing the frequency test)
3. Relevance confound: Anne app IS tightly-coupled — Perrow vocabulary fits the real phenomenon

**Conclusion:** A controlled design (high-relevance vs low-relevance measurement) is needed before a definitive conclusion.

## When to Use This Technique

- Testing whether a framework "retirement" has structural effect (terminology persistence)
- Measuring whether a new frame has been adopted by other instances (cross-instance citation rate)
- Detecting whether a concept has been absorbed from one instance's analysis into another's vocabulary
- Post-intervention measurement (append-only adoption rate, detection-gate activation rate)

## Limits

- Counts include ALL occurrences — cannot distinguish substantive from meta-discussion without manual inspection
- File-date-based categorization is coarse — a session file written on Jul 9 but started before the retirement event may contain pre-event analysis
- Case-insensitive search (`-i`) catches capitalized terms but may over-count acronym uses unrelated to the framework
