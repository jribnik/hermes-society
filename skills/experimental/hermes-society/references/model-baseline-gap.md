# Model Baseline Gap — Missing Verification Anchor

## The Gap

Resilience check #3 (Model stability) across all instances references `~/.hermes/society/baseline/model-baseline.json` as the canonical source for comparing current model assignments against a known-good state.

**This file does not exist.** As of 2026-07-09, no `model-baseline.json` exists at the expected path.

## Impact

The check passes by **social consensus** ("all instances agree we're on deepseek-v4-flash") rather than by **reference to a canonical document**. This creates a structural vulnerability:

| Scenario | Risk | Detection Latency |
|----------|------|-------------------|
| A model change happens simultaneously for all instances | No instance notices because all agree on the new model — no social disagreement to trigger alarm | Indefinite — only Jake would notice |
| An instance's model changes but others don't | Social consensus breaks → alarm fires within 1 cycle | ~3h (one cron cycle) |
| A model baseline is needed for a new instance to calibrate against | No canonical reference exists | Documentation gap — must ask Jake |

The most dangerous scenario is the first one: a coordinated model change across all instances, where every instance reports "deepseek-v4-flash" and social consensus passes the check, but the model is actually something different. Without a baseline file, there is no independent verification path.

## Resolution Path

**Option A (minimal — recommended):** Create the baseline file with the current known-good state:

```json
{
  "baseline_date": "2026-07-09T00:00-0700",
  "baseline_source": "instance consensus verified against Hermes Agent relay (Jul 8 11:00 PT)",
  "models": {
    "archivist": "deepseek-v4-flash",
    "advocate": "deepseek-v4-flash",
    "synthesizer": "deepseek-v4-flash",
    "curator": "deepseek-v4-pro"
  },
  "delegation_model": "claude-opus-4.8"
}
```

Once created, resilience check #3 asserts: `current_model_assignments == model-baseline.json.models`. Any deviation triggers a real alarm.

**Option B (stronger):** Include model checksum or provider fingerprint — a hash of `hermes config get provider.model` output per instance, so a model-name change (v4-flash → v5-flash) is distinguishable from a provider change (DeepSeek → Anthropic).

## Discovery

Discovered by the Archivist during the Jul 9 afternoon cycle while verifying resilience check #3 against the file system. The check had been passing as "✅ All deepseek-v4-flash" for 23 days without a baseline file existing. The social-consensus mechanism was never wrong during this period, but the documentation implied a verification path that didn't exist.

## Relationship to Other Checks

- The model-baseline gap is structurally similar to the TIMESTAMP_AT_WRITE temporal anomaly — both are verification-chain gaps where the system's stated verification method relies on a non-existent or unreliable anchor.
- Unlike the temporal anomaly (which had a root cause and fix), the model baseline gap is purely a missing file — trivially fixable once created.
