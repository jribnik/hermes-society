# Delegation Brief — Anne Homeowner App: Design & Spec Docs

**Written by:** Builder (2026-07-11)
**Delegated to:** Opus (Claude Opus 4.8) via `delegate_task`
**Trigger:** Jake's explicit Jul 9 directive ("This is enough to produce comprehensive design and spec docs. Start designing.") + diagnosis-action gap: 3 producing instances × multiple cycles × 0 design content. 12h design window (Jul 10) closed with zero technical output. Governance-tier ceramic deadline (spec due) Jul 12 06:00 PT.

## What Anne wants (confirmed via Ha, Jul 8)

The app is for Anne's **clients (homeowners)** — NOT for Anne's business operations. Anne is a handyperson; she wants to build/sell this app separate from her business. Homeowner-facing priorities, in order:

1. **Reminders** (maintenance schedules — monthly/quarterly/semiannual/annual)
2. **Home info storage** — filter sizes, serial numbers, paint colors, manuals, warranties
3. **Clickable house map** with marked items (floorplan-based navigation)
4. **Item marking** — mark specific items (e.g. "sink in master bath") on the map

## Reference: Homeowner Master Binder (docx)

The full requirements doc (`projects/anne/Homeowner_Master_Binder.docx`) defines 13 information categories (Property Info, Emergency & Safety, Home Systems, Appliances, Home Finishes, Building Envelope, Annual Maintenance Calendar, Maintenance Log, Repair & Improvement History, Warranties & Manuals, Contractor Directory, Insurance & Home Inventory, Vehicle Maintenance) plus an **~80-item equipment ontology** across 13 groups (Kitchen, Laundry, HVAC, Water Systems, Garage, Security, Entertainment, Outdoor, Fireplace, Backup Power, Smart Home, Bathroom, Commonly-Forgotten built-ins). Each equipment item carries: make/model/serial, purchase date, install date, warranty expiration, maintenance history, manual location.

## Society pre-work (already decided — honor these)

- **Platform:** iOS + Android (Jake). Society leaning React Native + Supabase (Advocate, unratified).
- **Pre-commit ontology thresholds:** ≥70 of 80 equipment types mapped to classes; ≥5 relation types (installation-location, manufacturer, part, maintenance-history, manual); ubiquitous-language preserved (no programmer-ese); ≤3 delegation rounds.
- **Design insights already captured** in `projects/anne/WORKSPACE.md` (FAE, Signal Detection Theory, Normalization of Deviance, Diffusion of Responsibility, Prospect Theory) — these were framed for a sub-management app; the confirmed scope is homeowner personal-inventory/floorplan, so treat them as optional UX seasoning, not core requirements.

## Deliverable

A comprehensive design + spec document set written to `projects/anne/design/`:
1. `01-product-overview.md` — vision, target user, core jobs-to-be-done, MVP scope vs later.
2. `02-domain-model.md` — entities, the ~80-item equipment ontology as a class hierarchy, relationships, ubiquitous language. Must meet the pre-commit thresholds above.
3. `03-architecture.md` — stack recommendation (evaluate React Native + Supabase vs alternatives), data model / schema sketch, auth, offline/sync, file/manual/photo storage, the clickable-floorplan approach.
4. `04-feature-spec.md` — the 4 priority features (reminders, info storage, clickable house map, item marking) specified to build-ready detail, plus reminder-scheduling logic from the maintenance calendar.
5. `05-open-questions.md` — decisions needing Jake/Anne input.

Output must be concrete enough that a developer (or a follow-up Opus code delegation) could start building from it.
