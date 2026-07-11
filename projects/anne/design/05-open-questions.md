# Anne Homeowner App — Open Questions & Decisions Needed

*Document 05 of 5 · Design & Specification Set*

These are decisions that require **Jake** (product/technical direction) or **Anne** (domain expert, business owner, and buyer of the vision) to resolve before or during the build. Each item notes who should own it, why it matters, and a recommended default so the team can proceed if no answer arrives.

---

## A. Product & Business

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| A1 | **Monetization model** — one-time purchase, subscription, freemium, or free (as a lead-gen tool for Anne's business)? | Anne + Jake | Drives whether we need billing infra, paywall gating, and cloud-cost budgeting in MVP. | Freemium: free core (reminders + info + map), paid tier for unlimited documents/photos + export/handoff. Defer billing to Phase 2. |
| A2 | **Is the app truly separate from Anne's business**, or is there a "powered by Anne" / pro-assist tie-in later? | Anne | Affects branding, whether a "trusted pro" role exists, and data-sharing design. | Fully separate consumer app in MVP; design the data model to *allow* an optional pro-assist role in Phase 4 without building it now. |
| A3 | **Target launch platform priority** — iOS-first, Android-first, or true simultaneous? | Jake | Even with cross-platform stack, QA and store approval effort differ. | Simultaneous via React Native (see Doc 03), but designate iOS as the primary QA target for the first beta. |
| A4 | **Who seeds the initial home record** — the homeowner alone, or with Anne's help at a service visit? | Anne | Determines onboarding UX weight and whether a guided/pro-assisted flow is MVP or later. | Homeowner self-serve onboarding in MVP with strong templates; pro-assist deferred. |
| A5 | **Branding / name** — is "Anne Homeowner App" the product name or a placeholder? | Anne | Needed for store listing, splash, icon, and copy. | Treat as placeholder; needs a real consumer-facing name before beta. |

---

## B. Scope & Feature Boundaries

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| B1 | **Multi-home support** — needed in MVP, or single-home acceptable at launch? | Jake | Affects data model root and navigation. Model already supports it; UI is the question. | Single active home in MVP UI; schema is multi-home ready (see Doc 02/03). |
| B2 | **Sharing** between household members (spouse/family) — MVP or later? | Anne + Jake | Common expectation; adds auth/permissions complexity. | Defer to Phase 3; single-owner account in MVP. |
| B3 | **Vehicle maintenance module** — include, or drop entirely? | Anne | Listed as "optional" in the source; adds a whole entity family. | Phase 3, off by default, opt-in module. |
| B4 | **Emergency & Safety fast-access screen** — is this important enough to pull into MVP? | Anne | It's high-value in a crisis (shutoffs, contacts) and cheap to build on existing data. | Consider promoting a lightweight version into MVP; confirm with Anne. |
| B5 | **Document/manual auto-lookup** by model number — build vs. buy vs. skip? | Jake | Big UX win but depends on third-party data availability/licensing. | Skip in MVP; investigate for Phase 4. |
| B6 | **Insurance home-inventory export** format expectations — is there a target insurer format? | Anne | Determines export schema for Phase 3. | Generic PDF + CSV; revisit if a specific insurer partnership emerges. |

---

## C. Domain & Ontology

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| C1 | **Custom equipment types** — can users add types not in the ~80-item ontology? | Anne | Homes have oddball equipment; rigid lists frustrate users. | Yes — allow a free-text "Other" type within each category, promotable to a proper class later. |
| C2 | **How granular should "location" be** — room-level, wall/zone within room, or exact pin coordinates? | Anne + Jake | Affects map data model and marking UX (Doc 04). | Support both a named location (room/area) and an optional exact pin (x,y) on the floorplan. |
| C3 | **Do users draw their own floorplan, upload one, or pick a template?** | Anne + Jake | Biggest UX risk in the map feature; drawing tools are expensive to build. | MVP: upload an image (photo of a plan / sketch) OR pick a simple room-list fallback. Native drawing tool deferred. See Doc 03 §7. |
| C3a | If upload: acceptable sources? (builder PDF plan, hand sketch photo, appraisal drawing) | Anne | Sets expectations for image quality and calibration. | Accept any image; pins are placed by the user, no auto-registration needed. |
| C4 | **Maintenance cadence defaults** — are the standard cadences (e.g., 1–3 month filter, annual HVAC, semiannual detector test) authoritative from Anne? | Anne | Anne's expertise is the differentiator; defaults should be *her* recommendations. | Use industry-standard defaults in Doc 04 as a starting point; **Anne should review and adjust the seed cadence table.** |
| C5 | **Filter size format** — free text, or structured (W×H×D)? | Anne | Structured enables validation and future reorder; free text is faster. | Structured optional fields (W, H, D, nominal size string) with free-text fallback. |

---

## D. Architecture & Technical

| # | Question | Owner | Why it matters | Recommended default |
|---|----------|-------|----------------|---------------------|
| D1 | **Ratify the stack** — React Native + Supabase (recommended in Doc 03) vs. alternatives? | Jake | Foundational; the society leaned toward RN+Supabase but did not ratify. | Adopt **React Native (Expo) + Supabase** per Doc 03 recommendation. Needs Jake's sign-off. |
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
| E1 | **Onboarding depth** — quick-start (add a few items) vs. guided full-binder setup? | Anne + Jake | Too much upfront = abandonment; too little = empty app. | Quick-start with a "keep going" checklist; guided setup optional. |
| E2 | **Notification permission timing** — ask at onboarding or at first reminder creation? | Jake | Premature prompts get denied and reminders are the #1 feature. | Ask contextually when the user creates their first reminder. |
| E3 | **Accessibility targets** — font scaling, contrast, screen-reader support level? | Jake | Broad age range (28–70) needs strong readability. | Meet WCAG AA basics + dynamic type in MVP. |
| E4 | **Visual identity** — does Anne have brand colors/logo, or does design start fresh? | Anne | Needed for UI kit. | Assume fresh design system pending Anne's input. |

---

## F. Immediate blockers (need answers to start building)

The following must be resolved (or the recommended default explicitly accepted) before Phase 1 development begins:

1. **D1** — Ratify the stack (React Native + Supabase).
2. **C3** — Floorplan input method (upload image vs. draw vs. room-list). This is the highest-risk UX decision.
3. **C4** — Anne's review of the seed maintenance cadence table (her domain expertise is the product's differentiator).
4. **A1** — Monetization direction (affects whether billing/paywall infra is in scope).
5. **B4** — Whether Emergency & Safety is pulled into MVP.

Everything else can proceed on the recommended defaults and be revisited during the build.
