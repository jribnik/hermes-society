# Anne Homeowner App — Product Overview

*Document 01 of 5 · Design & Specification Set*

---

## 1. Product Vision

**The Anne Homeowner App is the "owner's manual for your entire house."** It gives everyday homeowners a single, trustworthy place to record what they own, where it lives in their home, and when it needs attention — so nothing important gets forgotten, lost, or discovered too late.

Today, the knowledge of how a house works is scattered: filter sizes scribbled on a garage wall, paint cans with faded labels, manuals in a junk drawer, warranty cards in a shoebox, and a mental note to flush the water heater "sometime this year." When the person who knows the house moves out, sells, or simply forgets, that knowledge disappears. The app captures it once and keeps it usable forever.

**One-sentence pitch:** *Know your home — every appliance, filter, paint color, warranty, and maintenance task — with a tap on an interactive map of your own house.*

### Guiding principles

1. **Homeowner-first, not pro-first.** This is a consumer reference and reminder tool. It is **not** a job-scheduling, invoicing, client-management, or subcontractor app. Anne's *business* operations are explicitly out of scope.
2. **Low-effort capture, high-value recall.** People will only maintain records if entry is fast. The payoff is effortless recall at the exact moment of need (standing in the basement, at the hardware store, filing an insurance claim).
3. **Works where houses are.** Basements, garages, crawlspaces, and mechanical rooms have poor connectivity. The app must be fully usable offline and sync later.
4. **Speak the homeowner's language.** Labels, categories, and prompts use plain household terms ("Filter size," "Paint color," "Last serviced"), never database or engineering jargon.
5. **The house map is the spine.** The floorplan is not a gimmick — it's the primary spatial index. "Where is that thing?" is answered by tapping the room it's in.

---

## 2. Target User

### Primary persona — "The Responsible Homeowner"

- **Who:** Owns (or is buying) a single-family home, townhome, or condo. Age range broad (28–70). Not a technical expert, not a tradesperson.
- **Mindset:** Wants to take good care of their biggest asset, avoid expensive surprises, and not feel overwhelmed. Feels a low-grade anxiety about "am I forgetting some maintenance thing?"
- **Pain points:**
  - Can never find the model/serial number when calling for service or ordering parts.
  - Buys the wrong furnace filter size (again).
  - Forgets seasonal maintenance until something breaks.
  - Can't remember the exact paint color for a touch-up.
  - Loses warranty info and pays for a repair that was covered.
  - Panics during an emergency (where's the water shutoff?).
- **Tech comfort:** Uses a smartphone daily; comfortable with photos, notifications, and simple apps. Will not tolerate a steep learning curve or heavy data entry.

### Secondary personas

- **The New Buyer** — just closed on a house, wants to build the record from scratch (or receive it from the seller). High motivation window.
- **The Seller / Handoff** — wants to hand a complete, credible home record to a buyer (a differentiator and a viral loop).
- **The Landlord / Second-home owner** — manages a property they don't live in daily; reminders and remote recall matter even more.

### Explicitly NOT the user

- Anne's handyperson **business** (scheduling, dispatch, invoicing, client CRM, crew management). Anne sells the app to homeowners; she does not run her jobs through it.

### Anne's relationship to the product

Anne is the **creator/seller and domain expert**, not an operational user. She may optionally act as a "trusted pro" who helps set up a client's home record, but the app's design center is the homeowner using it themselves. Any "pro-assist" capability is a **later-phase** consideration, not MVP.

---

## 3. Core Jobs-To-Be-Done (JTBD)

Framed as the situations that cause a homeowner to reach for the app.

| # | When I… | I want to… | So that… |
|---|---------|-----------|----------|
| J1 | am standing at the store / on the phone with a tech | instantly find a model, serial, or filter size | I buy the right part or get faster service |
| J2 | face a recurring maintenance chore (filter, gutters, water heater) | be reminded at the right time and log that I did it | nothing important slips and I extend equipment life |
| J3 | can't remember where something is or how to reach it | tap my house map and see what's in each room/area | I find the shutoff, panel, or appliance fast |
| J4 | need a specific detail (paint color, warranty date, manual) | pull up the stored fact or document in seconds | I avoid re-buying, re-measuring, or paying for covered repairs |
| J5 | have an emergency (leak, gas smell, outage) | find shutoff locations and emergency contacts immediately | I act fast and reduce damage |
| J6 | file an insurance claim or update coverage | produce a photo/asset inventory and purchase details | I'm reimbursed fairly and quickly |
| J7 | buy or sell a home | build or hand off a complete home record | the value and knowledge transfer with the property |
| J8 | just moved in | capture everything once, guided | I start organized instead of digging for years |

**JTBD priority for MVP:** J2 (reminders), J1/J4 (info recall), J3 (map find), then J5/J6/J7/J8 layered in.

---

## 4. MVP Scope vs. Later Phases

The four **confirmed priority features** define the MVP. Everything else from the 13-category Master Binder is sequenced into later phases.

### MVP (Phase 1) — "The Core Loop"

The core loop: **record an item → place it on the map → set its maintenance cadence → get reminded → log the service.**

1. **Reminders driven by a maintenance calendar** *(priority 1)*
   - Monthly / quarterly / semiannual / annual cadences.
   - Per-item and standalone tasks.
   - Local + push notifications; complete/snooze; auto-reschedule next due date.
2. **Home info storage** *(priority 2)*
   - Equipment/appliance records with: make, model, serial, purchase date, install date, warranty expiration, maintenance history, manual/document location, physical location.
   - Filter sizes, paint colors, serial numbers as first-class quick-recall fields.
   - Attach photos and documents (manuals, warranties, receipts).
3. **Clickable house map** *(priority 3)*
   - An interactive floorplan the user can tap to navigate to a room/area and see its items.
4. **Item marking** *(priority 4)*
   - Pin specific items to a location on the map (e.g., "sink in master bath," "furnace in mechanical room").

Supporting MVP essentials (thin but required to make the above usable):
- Account + auth, single home per account.
- Offline-first data with background sync.
- Basic photo/document attachment + storage.
- Onboarding that seeds common equipment types and default cadences.

### Phase 2 — "The Full Binder"

Round out the 13 Master Binder categories:
- **Emergency & Safety** as a dedicated fast-access screen (shutoff locations, panel/breaker directory, detector battery dates).
- **Property Information** (address, purchase date, survey, permits/inspections, HOA).
- **Building Envelope & Exterior** (roof, gutters, windows, doors, weather stripping, drainage).
- **Home Finishes** full inventory (paint, flooring, lighting, cabinets/countertops).
- **Warranties & Manuals** as a browsable, expiration-aware library.
- **Contractor Directory** (plumber, electrician, HVAC, roofer, etc.) linked to items and log entries.
- **Repair & Improvement History** ledger (date, contractor, cost, description, warranty).
- **Maintenance Log** rich history views and export.

### Phase 3 — "Value & Handoff"

- **Insurance & Home Inventory** (policy info, annual photo/video walkthrough, major asset valuation, claim history).
- **Home record export / handoff** (PDF binder, buyer transfer at sale).
- **Vehicle Maintenance** (optional module: oil type, filter part numbers, tire info, records).
- **Multi-home** support.
- **Sharing / collaboration** (spouse, family, or a trusted pro like Anne).

### Phase 4+ — "Ecosystem"

- Pro-assist mode (Anne or another tradesperson sets up/services a client's record).
- Manufacturer manual auto-lookup by model number.
- Part reordering integrations.
- Smart-home device import to auto-populate equipment.
- Reminder intelligence (weather/season-aware nudges).

### Out of scope (all phases, by design)

- Business operations for the handyperson: job scheduling, dispatch, invoicing, payments, CRM, crew/subcontractor management, marketing. The app is sold **to** homeowners and is **about** their homes.

---

## 5. Success Metrics (directional)

- **Activation:** % of new users who add ≥5 items and place ≥3 on the map within 7 days.
- **Retention driver:** reminder completion rate (proxy for delivered value).
- **Recall value:** searches/lookups per active user per month (J1/J4 usage).
- **Depth:** average items per home; % of homes with ≥1 document attached.
- **North-star candidate:** *reminders completed per home per quarter* — the clearest signal the core loop is working.
