# Anne Homeowner App — Open Questions & Decisions Needed

*Document 05 of 5 · Design & Specification Set*

These are decisions that require **Jake** (product/technical direction) or **Anne** (domain expert, business owner, and buyer of the vision) to resolve before or during the build. Each item notes who should own it, why it matters, and a recommended default so the team can proceed if no answer arrives.

---

## A. Product & Business

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| A1 | **Monetization model** — one-time purchase, subscription, freemium, or free (as a lead-gen tool for Anne's business)? | Anne + Jake | Drives whether we need billing infra, paywall gating, and cloud-cost budgeting in MVP. | ✅ **ANSWERED (Jul 12):** Freemium. Anne suggests exploring category-specific ads (home improvement/handyperson) as an additional revenue stream. |
| A2 | **Is the app truly separate from Anne's business**, or is there a "powered by Anne" / pro-assist tie-in later? | Anne | Affects branding, whether a "trusted pro" role exists, and data-sharing design. | ✅ **ANSWERED (Jul 12):** Fully separate, generalized consumer app for nationwide use — not tied to Anne's business. Anne wants homeowners anywhere to manage their home, document issues, and track replacement/maintenance. Design pro-assist role as optional Phase 4 add-on per original recommendation. |
| A3 | **Target launch platform priority** — iOS-first, Android-first, or true simultaneous? | Jake | Even with cross-platform stack, QA and store approval effort differ. | ✅ **ANSWERED (Jul 12):** Both iPhone and Android on launch. Simultaneous via React Native. |
| A4 | **Who seeds the initial home record** — the homeowner alone, or with Anne's help at a service visit? | Anne | Determines onboarding UX weight and whether a guided/pro-assisted flow is MVP or later. | ✅ **ANSWERED (Jul 12):** Both tiers — homeowner can self-serve for free, OR pay someone (pro-assist) to enter the data for them. Pro-assist is a paid option from day one, not deferred. |
| A5 | **Branding / name** — is "Anne Homeowner App" the product name or a placeholder? | Anne | Needed for store listing, splash, icon, and copy. | Treat as placeholder; needs a real consumer-facing name before beta. |

---

## B. Scope & Feature Boundaries

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| B1 | **Multi-home support** — needed in MVP, or single-home acceptable at launch? | Jake | Affects data model root and navigation. Model already supports it; UI is the question. | ✅ **ANSWERED (Jul 12):** Single-home free; adding additional properties is a paid feature. Keep multi-home in the data model but gate the UI behind the paid tier. |
| B2 | **Sharing** between household members (spouse/family) — MVP or later? | Anne + Jake | Common expectation; adds auth/permissions complexity. | ✅ **ANSWERED (Jul 12):** Paid feature. Keep out of free tier; design auth model to support sharing as a premium upgrade. |
| B3 | **Vehicle maintenance module** — include, or drop entirely? | Anne | Listed as "optional" in the source; adds a whole entity family. | Phase 3, off by default, opt-in module. |
| B4 | **Emergency & Safety fast-access screen** — is this important enough to pull into MVP? | Anne | It's high-value in a crisis (shutoffs, contacts) and cheap to build on existing data. | ✅ **ANSWERED (Jul 12):** Yes — promote into MVP. Anne specifically flagged whole-property water shutoff info and city utility contact numbers as key use cases. |
| B5 | **Document/manual auto-lookup** by model number — build vs. buy vs. skip? | Jake | Big UX win but depends on third-party data availability/licensing. | Skip in MVP; investigate for Phase 4. |
| B6 | **Insurance home-inventory export** format expectations — is there a target insurer format? | Anne | Determines export schema for Phase 3. | ✅ **ANSWERED (Jul 12):** No specific insurer format known. Stick with generic PDF + CSV per recommendation. |

---

## C. Domain & Ontology

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| C1 | **Custom equipment types** — can users add types not in the ~80-item ontology? | Anne | Homes have oddball equipment; rigid lists frustrate users. | ✅ **ANSWERED (Jul 12):** Yes — users can add their own equipment types. Implement as free-text custom types within each category, promotable to proper classes later. |
| C2 | **How granular should "location" be** — room-level, wall/zone within room, or exact pin coordinates? | Anne + Jake | Affects map data model and marking UX (Doc 04). | ✅ **ANSWERED (Jul 12):** Pin on floor plan is preferred, but needs investigation into how homeowners would map/place pins (UX challenge). Support both named room/area and optional pin coordinates — the pin placement UX needs design work. |
| C3 | **Do users draw their own floorplan, upload one, or pick a template?** | Anne + Jake | Biggest UX risk in the map feature; drawing tools are expensive to build. | ✅ **ANSWERED (Jul 12):** Start with a list of rooms to choose from. Photo upload and drawing tool deferred to later iterations. |
| C3a | If upload: acceptable sources? (builder PDF plan, hand sketch photo, appraisal drawing) | Anne | Sets expectations for image quality and calibration. | Deferred — room-list MVP first, revisit when photo upload is added. |
| C4 | **Maintenance cadence defaults** — are the standard cadences (e.g., 1–3 month filter, annual HVAC, semiannual detector test) authoritative from Anne? | Anne | Anne's expertise is the differentiator; defaults should be *her* recommendations. | ✅ **ANSWERED (Jul 12):** Follow industry standard. Anne is comfortable with standard cadences — no need for custom overrides. Proceed with the defaults in Doc 04. |
| C5 | **Filter size format** — free text, or structured (W×H×D)? | Anne | Structured enables validation and future reorder; free text is faster. | ✅ **ANSWERED (Jul 12):** Free text. Keep it simple — no structured fields needed. |

---

## D. Architecture & Technical

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| D1 | **Ratify the stack** — React Native + Supabase (recommended in Doc 03) vs. alternatives? | Jake | Foundational; the society leaned toward RN+Supabase but did not ratify. | ✅ **ANSWERED (Jul 12):** Ratified. React Native (Expo) + Supabase. Jake has signed off. |
| D2 | **Offline sync conflict policy** — last-write-wins vs. field-level merge vs. per-entity rules? | Jake | Single-owner homes rarely conflict, but sharing (B2) changes this. | Last-write-wins per record in MVP; revisit when sharing lands. See Doc 03 §5. |
| D3 | **Where do photos/manuals live** — Supabase Storage, or a dedicated CDN/object store? | Jake | Cost and offline caching strategy depend on this. | Supabase Storage in MVP with local device cache; re-evaluate at scale. See Doc 03 §6. |
| D4 | **Data residency / privacy posture** — any regulatory constraints (home data can be sensitive)? | Jake | Affects hosting region and privacy policy. | US region default; add privacy policy before store submission. |
| D5 | **Account model** — email/password, magic link, social sign-in, or Apple/Google required? | Jake | Apple requires "Sign in with Apple" if other social logins are offered. | Email magic link + Sign in with Apple + Google via Supabase Auth. |
| D6 | **Backup / account recovery** expectations for a "system of record" people rely on for years. | Jake | Losing a home record is catastrophic to trust. | Server-side is source of truth after sync; document recovery flow. |
| D7 | **Free-tier storage limits** — how much photo/document storage per home before it costs us? | Jake + Anne | Directly ties to A1 monetization. | Set a soft cap (e.g., 1 GB free) pending cost modeling. |

---

## E. Design & UX

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| E1 | **Onboarding depth** — quick-start (add a few items) vs. guided full-binder setup? | Anne + Jake | Too much upfront = abandonment; too little = empty app. | ✅ **ANSWERED (Jul 12):** Start with the most common and important home maintenance tasks pre-loaded as defaults. Let homeowners add additional fields/categories for a more comprehensive setup. Guided quick-start with essential tasks, then expandable. |
| E2 | **Notification permission timing** — ask at onboarding or at first reminder creation? | Jake | Premature prompts get denied and reminders are the #1 feature. | Ask contextually when the user creates their first reminder. |
| E3 | **Accessibility targets** — font scaling, contrast, screen-reader support level? | Jake | Broad age range (28–70) needs strong readability. | Meet WCAG AA basics + dynamic type in MVP. |
| E4 | **Visual identity** — does Anne have brand colors/logo, or does design start fresh? | Anne | Needed for UI kit. | ✅ **ANSWERED (Jul 12):** Brand colors: forest green + yellow. Anne has an existing logo she can provide. Use these as the design system foundation. |

---

## F. Immediate blockers (need answers to start building)

The following must be resolved (or the recommended default explicitly accepted) before Phase 1 development begins:

1. ~~**D1** — Ratify the stack (React Native + Supabase).~~ ✅ **Resolved (Jul 12):** Jake ratified RN + Supabase.
2. ~~**C3** — Floorplan input method (upload image vs. draw vs. room-list).~~ ✅ **Resolved (Jul 12):** Start with room list; photo upload and drawing deferred.
3. ~~**C4** — Anne's review of the seed maintenance cadence table.~~ ✅ **Resolved (Jul 12):** Follow industry standard.
4. ~~**A1** — Monetization direction.~~ ✅ **Resolved (Jul 12):** Freemium + category ads.
5. ~~**B4** — Whether Emergency & Safety is pulled into MVP.~~ ✅ **Resolved (Jul 12):** Yes, promote into MVP.

**Newly added (from Anne's answers):**
6. **Name** — Anne wants the app generalized for nationwide use. The placeholder "Anne Homeowner App" needs a real consumer-facing name.

Everything else can proceed on the recommended defaults and be revisited during the build.
