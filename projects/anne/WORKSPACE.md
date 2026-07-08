# Anne Project — Workspace / Design Notes

**Created:** 2026-07-01T15:40-0700

## Background

Anne is a handyperson who wants an app for tracking, managing, and delegating households, tasks, and information. She wants to be able to sell the app separate from her business. Jake is acting as product manager and will have a conversation with Anne to identify requirements in "a matter of wall days."

## Initial Domain Observations

The core entities seem to be:
- **Household** — The organizing unit (Anne's clients' homes)
- **Task** — Work to be done (repairs, maintenance, inspections)
- **Delegation** — Who does what (Anne manages subs or employees)
- **Information** — Client contact, notes, history, photos, before/after

## Open Questions

1. Does the app need to support multiple users per household (client + Anne + subs)?
2. Is there a scheduling dimension (calendar, availability)?
3. Payment/invoicing — in scope or separate?
4. How "separate from business" works — white-label? multi-tenant?

## Design Insight: Fundamental Attribution Error (FAE) — Added 2026-07-01T21:11-0700

**Observation:** Handypersons who manage subcontractors (subs) are subject to the FAE — the tendency to overemphasize personality factors and underemphasize situational factors when explaining others' behavior. When a sub shows up late or does poor work, the natural attribution is "they're unreliable" (disposition), not "the scheduling was poor." This leads to conflict and churn.

**Design implications for the app:**

1. **Task context capture.** Before marking a task as "failed" or "late," prompt for situational factors: scheduling conflict, clarification needed, client delay, etc. Make situational attribution the default, not dispositional.

2. **Before/after photo logging.** Photos with timestamps and location create a situational record that reduces dispositional attributions.

3. **Feedback templates.** Default communication templates should surface situational factors: "The job at [location] was scheduled at [time] but the client wasn't ready." Normalize situational explanations.

4. **Status history over scores.** Instead of 5-star ratings for subs (which reinforce FAE — bad rating → dispositional attribution), show a timeline of completed jobs with context notes. "3 late arrivals in 15 jobs — context: traffic zone, morning rush" is more actionable than "★★★☆☆."

**Source:** Fundamental Attribution Error (Wikipedia). Applied by Archivist (2026-07-01T21:11-0700).

---

## Design Insight: Signal Detection Theory — Added 2026-07-06T09:41-0700

**Observation:** A household task management app is a continuous signal detection problem — distinguishing signal (truly complete, truly competent) from noise (prematurely marked complete, one good job outlier).

**Design implications:**

1. **Role-dependent decision criteria.** Different users need different bias levels:
   - Task owners (subs) → liberal bias on completion (prefer false alarms over misses)
   - Task verifiers (homeowner) → conservative bias on completion (prefer misses over false alarms)
   - Fairness trackers → balanced criterion with explicit cost structure

2. **The 2×2 completion matrix** should be surfaced:
   - Hit (correct payment) / Miss (stress, unpaid work)
   - False Alarm (pay for bad work) / Correct Rejection (protect quality)

3. **Cost visibility.** The app should show households what they're optimizing for — speed (liberal criterion) or quality (conservative) — so they can calibrate consciously.

**Source:** Signal Detection Theory (Green & Swets, 1966). Applied by Synthesizer (2026-07-06T09:41-0700).

---

## Design Insight: Normalization of Deviance — Added 2026-07-06T14:30-0600

**Observation:** Households managing multiple subcontractors are at high risk for normalization of deviance — early warning signs misinterpreted, missed completely, normalized by system trust.

**Design implications:**

1. **Trend analysis over threshold detection.** Slow degradation (sub burnout, quality drift) is invisible to threshold-based alerts. Show trends, not just crossing points.
2. **Warning signal persistence.** Task deferred >2x stays flagged until explicitly resolved — no automatic reset across cycles.
3. **Sensor independence.** If a sub self-reports completion, require independent verification (photo, timestamp) before automatic acceptance.
4. **Pre-mortem protocol.** Before assigning high-risk tasks (tight deadline, high-value materials), surface last 3 similar jobs' performance data as baseline.

**Source:** Normalization of Deviance (Vaughan, 1996). Applied by Advocate (2026-07-06T14:30-0700).

---

## Design Insight: Diffusion of Responsibility & Named Accountability — Added 2026-07-06T12:41-0700

**Observation:** In multi-member households, responsibility for tasks diffuses across members — each assumes another will act. This is the bystander effect in domestic form. The app must design against it structurally.

**Design implications:**

1. **Named accountability at every task.** Every recurring task has exactly one owner and one verifier. No shared assignments. If the owner doesn't act, the gap is visible.
2. **Verification tokens.** For high-stakes tasks, a designated verifier must confirm before payment/task-closure. The token transfers responsibility to a named individual.
3. **Anonymous escalation trigger.** Any member can flag a "task tension" without attribution. The system surfaces it at the next household meeting. Anonymity circumvents diffusion — no individual has to take visible responsibility.
4. **Rotating default reviewer.** If no one has updated a sub's performance entry for >2 weeks, the system assigns a default reviewer (rotating). Prevents "someone else is tracking that."
5. **Personalized requests.** Darley & Latané found that naming a specific person restores helping behavior to near-baseline. The app should default to "@Alice, please confirm the kitchen tiles" not "someone confirm the kitchen tiles."

**Source:** Diffusion of Responsibility (Darley & Latané, 1968). Applied by Synthesizer (2026-07-06T12:41-0700).

---

## Design Insight: Prospect Theory — Added 2026-07-06T12:03-0700

**Observation:** Household task management feels harder than the objective burden suggests because the evaluation function is asymmetric, not the workload itself.

**Design implications:**

1. **Reference management.** Show individual task load relative to personal average, not absolute count. Same 12 tasks feels like "reducing" vs "increasing" depending on last week's baseline.
2. **Base-rate anchoring.** Surface objective probabilities against overweighted small risks (sub will cancel: "they show up 90% of the time").
3. **Surprise gains.** Rare positive events (sub finished early, saved $200) should be made maximally salient — the overweighting of small probabilities works FOR the app here.
4. **Default to credit frame.** Completed tasks add visible credit from a positive baseline rather than deducting from zero.
5. **Fourfold pattern — certain losses.** Task bundling (swap dishes for garbage — both certain losses, bundling changes the reference point) for risk-seeking on certain-bad outcomes.

**Source:** Prospect Theory (Kahneman & Tversky, 1979). Applied by Archivist (2026-07-06T12:03-0700).
