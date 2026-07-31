# Anne Homeowner App — Feature Specification

*Document 04 of 5 · Design & Specification Set*

Build-ready specs for the four confirmed priority features, **in priority order**:
1. Reminders driven by a maintenance calendar
2. Home info storage
3. Clickable house map
4. Item marking

Each spec includes the user story, UX flow, data touchpoints (see Doc 02 & Doc 03), edge cases, and acceptance criteria. Field/label names use the ubiquitous language from Doc 02 §1.

---

## Feature 1 — Reminders (Maintenance Calendar) — *Priority 1*

### 1.1 Goal
Make sure homeowners never forget recurring upkeep. The app turns a **Maintenance Task** with a **Cadence** into scheduled **Reminders**, notifies the user at the right time, lets them mark it done (which writes a **Service Record**), and automatically computes the next due date.

### 1.2 User stories
- As a homeowner, I want to be reminded to replace my furnace filter every 3 months so my HVAC stays healthy.
- As a homeowner, I want to mark a task "Done" and have the next reminder scheduled automatically.
- As a homeowner, I want a calendar/list of what's coming due so I can plan.
- As a homeowner, I want reminders to fire even when I'm offline in the basement.

### 1.3 Cadence definitions
| Cadence | Interval | Example tasks |
|---------|----------|---------------|
| **Monthly** | every 1 month | Test smoke/CO detectors; check filter; inspect for leaks |
| **Quarterly** | every 3 months | Replace HVAC filter (typical); flush garbage disposal |
| **Semiannual** | every 6 months | Test detectors (battery); reverse ceiling fans; service reminder checks |
| **Annual** | every 12 months | HVAC pro service; water heater flush; dryer vent cleaning; gutter cleaning; chimney inspection; roof inspection |
| **Custom** | every N days | Anything not on the standard cadence (e.g., 45-day well filter) |

### 1.4 Reminder-scheduling logic (authoritative)

**Core computation — `computeNextDue(task)`:**

```
INPUT:  cadence, custom_interval_days, last_service_date (nullable),
        install_date (fallback), today

1. anchor = last_service_date
            ?? install_date
            ?? today                 # brand-new task with no history

2. interval_months = { monthly:1, quarterly:3, semiannual:6, annual:12 }[cadence]
   IF cadence == custom:
       next_due = anchor + custom_interval_days (days)
   ELSE:
       next_due = anchor + interval_months (calendar months)

3. # Never schedule in the past: roll forward whole intervals until >= today
   WHILE next_due < today:
       next_due += one interval   # month-based or day-based per cadence

4. RETURN next_due
```

**On task creation:** set `last_service_date` (if user knows it) → run `computeNextDue` → set `next_due_date` → schedule a **local notification** (Doc 03 §8) for `next_due_date` at the user's preferred reminder time (default 9:00 AM local).

**On "Mark Done":**
```
1. Create service_record { item/task, service_date = chosen date (default today),
                           contact?, cost?, notes? }
2. task.last_service_date = service_record.service_date
3. task.next_due_date = computeNextDue(task)   # anchored to the new last_service_date
4. Cancel the old local notification; schedule the new one for next_due_date.
```

**On "Snooze":** reschedule the reminder by the snooze interval (options: 1 day, 3 days, 1 week) **without** changing `last_service_date` or `next_due_date` — snooze only moves the notification, not the schedule.

**On cadence change:** recompute `next_due_date` from the existing `last_service_date` and reschedule.

**Overdue handling:** if `next_due_date < today` and not done, the task shows as **Overdue** (red), keeps nudging (daily local notification cap + a server catch-up push, Doc 03 §8), and stays overdue until marked done or snoozed.

**Month-end safety:** month math clamps to the last valid day (e.g., anchor Jan 31 + 1 month → Feb 28/29), so no invalid dates are produced.

### 1.5 Seed task templates (per Item Type)
Item Types carry `default_task_templates` (Doc 03 §3). When a user adds an Item, the app **offers** its standard tasks (user can accept/skip/edit). Defaults below are a starting point — **Anne to review/ratify (Doc 05 C4).**

| Item Type / class | Suggested task | Default cadence |
|-------------------|----------------|-----------------|
| Furnace / Central AC / Heat pump (FilteredDevice) | Replace air filter | Quarterly (adjust 1–3 mo) |
| Furnace / AC / Heat pump | Professional HVAC service | Annual |
| Water heater (tank) | Flush tank | Annual |
| Dryer | Clean dryer vent/duct | Annual |
| Refrigerator (with filter) | Replace water/ice filter | Semiannual |
| Range hood / Vent hood | Clean/replace grease filter | Quarterly |
| Smoke/CO detectors (SafetyDevice) | Test detectors | Monthly |
| Smoke/CO detectors | Replace batteries | Semiannual |
| Sump pump (Pump) | Test operation | Quarterly |
| Water softener | Refill salt / check | Monthly |
| Whole-house humidifier | Replace pad / clean | Annual (seasonal) |
| Gutters (Phase 2 exterior) | Clean gutters | Semiannual |
| Fireplace/chimney (CombustionDevice) | Inspection | Annual |
| Standby generator | Run test / service | Monthly test + Annual service |
| Irrigation controller (Outdoor) | Winterize / spring startup | Semiannual |

### 1.6 UX flows
- **Add reminder:** from an Item (pre-fills linked tasks) or standalone → pick Title, Cadence, Last Serviced (optional), preferred time, optional Contractor → save.
- **Reminders home ("What's Due"):** grouped tabs — **Overdue** · **Due This Month** · **Upcoming** · **Done recently**. Each row: task title, item, room, next due, quick **Done / Snooze**.
- **Calendar view:** month grid with due-date dots; tapping a day lists that day's tasks.
- **Notification actions:** "Mark Done" and "Snooze" directly from the notification.

### 1.7 Data touchpoints
`maintenance_tasks`, `reminders`, `service_records`, `equipment_items`, `contacts` (Doc 03 §3). Relations R4 (maintenance-history), R6 (serviced-by), R7 (scheduled-by).

### 1.8 Edge cases
- Task with no `last_service_date` and no `install_date` → anchor = today; first reminder one interval out.
- Deleting an Item with tasks → cancel its reminders, retain Service Records (Doc 02 §6).
- Time-zone/DST → schedule against local wall-clock time; recompute on device tz change.
- Notification permission denied → in-app "What's Due" still works; prompt to enable at first reminder (Doc 05 E2).

### 1.9 Acceptance criteria
- [ ] Creating a Quarterly task with Last Serviced = today sets Next Due exactly 3 calendar months out.
- [ ] Marking done re-anchors Next Due to the completion date and reschedules the notification.
- [ ] Snooze moves the notification but not Next Due.
- [ ] Overdue tasks are visually distinct and keep nudging.
- [ ] Reminders fire while the device is offline.
- [ ] Month-end anchors never produce invalid dates.

---

## Feature 2 — Home Info Storage — *Priority 2*

### 2.1 Goal
A fast, searchable store of everything about the home's Items: make, model, serial, dates, warranty, filter size, paint colors, and attached manuals/warranties/photos — retrievable in seconds at the moment of need (store, phone call, claim).

### 2.2 User stories
- As a homeowner, I want to look up my furnace filter size while at the store.
- As a homeowner, I want the model & serial ready when I call for service.
- As a homeowner, I want to find the exact paint color for a touch-up.
- As a homeowner, I want the manual and warranty PDF attached to the appliance.

### 2.3 Item record (create/edit)
Fields (Doc 02 §2): **Name** · **Item Type** (from ontology picker) · **Make** · **Model** · **Serial Number** · **Purchase Date** · **Install Date** · **Warranty Expiration** · **Room/Area** · **Filter Size** (shown only for FilteredDevice types) · **Notes** · **Photos** · **Manuals/Documents** · **Parts** · **Maintenance History** (read-only list) · **Maintenance Tasks**.

- **Item Type picker** is organized by the 12 Categories (Doc 02 §3.2), with search, plus a "Commonly-forgotten" prompt (Doc 02 §3.3) during onboarding and an **"Other"** free-text option (Doc 05 C1).
- **Filter Size**: structured optional W×H×D + nominal string, with free-text fallback (Doc 05 C5).
- **Parts**: add filters/belts/batteries/bulbs with spec, part number, reorder link (relation R3).

### 2.4 Attachments
- Add **Photos** (camera or library) and **Documents** (PDF/image manuals, warranty, receipt) per Doc 03 §6.
- Each attachment: kind, caption, "available offline" toggle.

### 2.5 Paint colors (Home Finishes slice in MVP)
Dedicated **Paint Color** entries: color name, code, brand, sheen, where used (Room/Area), photo, notes. Surfaced both in a Paint list and within a Room/Area.

### 2.6 Search & recall (the payoff)
- Global search across Item name, make, model, serial, filter size, room, paint color.
- **Quick-recall chips** on Item detail: big, copyable Model / Serial / Filter Size (one-tap copy for phone calls / store).
- Filter/sort Items by Category, Room/Area, warranty status (expiring soon).

### 2.7 Data touchpoints
`equipment_items`, `equipment_types`, `parts`, `warranties`, `documents`, `paint_entries`, `locations` (Doc 03 §3). Relations R2 (manufacturer), R3 (part), R5 (manual), R8 (covered-by).

### 2.8 Edge cases
- No serial (many fixtures) → allowed; encouraged for Appliance class.
- Large manual PDF offline → respect storage cap + "available offline" pinning.
- Warranty Expiration set → auto-create an expiration alert (server push).

### 2.9 Acceptance criteria
- [ ] An Item can be created with only Name + Item Type; all else optional.
- [ ] Filter Size appears only for FilteredDevice-class types.
- [ ] Model/Serial/Filter Size are one-tap copyable.
- [ ] A PDF manual attaches, syncs, and opens offline when pinned.
- [ ] Global search finds an Item by serial number substring.

---

## Feature 3 — Clickable House Map — *Priority 3*

### 3.1 Goal
Let users navigate their home spatially: tap the House Map to reach a Room/Area and its Items — the fastest answer to "where is that thing?"

### 3.2 User stories
- As a homeowner, I want to tap the mechanical room and see the furnace, water heater, and sump pump.
- As a homeowner in an emergency, I want to quickly find the water shutoff on the map.
- As a homeowner without a floorplan, I still want to browse rooms.

### 3.3 Setup
- **Upload a floorplan image** (builder plan, appraisal, or hand-sketch photo) — primary path (Doc 03 §7.1).
- **Room-list fallback** if no image (Doc 05 C3): the map screen becomes a tappable list of Rooms/Areas.

### 3.4 Interaction (per Doc 03 §7.2)
- Pan + pinch-zoom the floorplan.
- **Pins** (SVG, normalized `x_ratio/y_ratio`) mark Rooms/Areas and Items.
- **Tap a Room/Area pin** → Room detail: its Items, photos, shutoff flags, paint colors.
- **Tap an Item pin** → Item detail (Feature 2).
- **Pin clustering** when zoomed out; count badge expands on zoom.
- **Shutoff pins** (water/gas/electrical) render with distinct high-visibility styling for emergencies.

### 3.5 Data touchpoints
`floorplans`, `map_markers`, `locations`, `equipment_items` (Doc 03 §3). Relation R1 (installation-location).

### 3.6 Edge cases
- Very large/high-res image → downscale for display, keep original.
- Multiple floors → support multiple floorplan images per home with a floor switcher (MVP: at least "add another floor"; confirm scope Doc 05).
- No pins yet → prompt "Place your first item on the map."

### 3.7 Acceptance criteria
- [ ] User can upload a floorplan image and see it pan/zoom smoothly.
- [ ] Pins stay correctly positioned across zoom levels and device sizes (normalized coords).
- [ ] Tapping a Room/Area pin opens its Items list.
- [ ] Room-list fallback works with no image uploaded.
- [ ] Shutoff-flagged locations are visually highlighted.

---

## Feature 4 — Item Marking — *Priority 4*

### 4.1 Goal
Let users pin specific Items to precise spots on the House Map (e.g., "sink in master bath," "furnace in mechanical room"), tying the physical thing to its place.

### 4.2 User stories
- As a homeowner, I want to drop a pin for the master-bath sink so I can find it and its details later.
- As a homeowner, I want an Item's pin to jump straight to its record.

### 4.3 Flow
1. From an **Item** → "Place on map" → enter **place mode** on the House Map.
2. Pan/zoom, then **tap the location** → a pin drops at that point → save `x_ratio/y_ratio` + `equipment_item_id` (+ inferred/selected `location_id`).
3. Alternatively, from the map in place mode, tap empty space → choose "Mark an Item" → pick existing Item or create a new one inline.
4. Pins are **draggable** to reposition; long-press → remove or reassign.

### 4.4 Relationship to Room/Area
- Placing a pin can auto-assign the Item's **Room/Area** (if the tapped spot falls within a known Room/Area) or prompt the user to confirm the Room/Area (Doc 05 C2 supports both named location + exact pin).
- An Item may rely on its Room/Area's pin (no own pin) or have its own precise pin.

### 4.5 Data touchpoints
`map_markers` (with `equipment_item_id`), `equipment_items.location_id`, `locations` (Doc 03 §3). Relation R1 (installation-location).

### 4.6 Edge cases
- Item marked before a floorplan exists → allow assigning a Room/Area now; prompt to place a pin once a floorplan is added.
- Deleting an Item → its pin is removed (Doc 02 §6).
- Reassigning a pin to a different Room/Area updates the Item's location.

### 4.7 Acceptance criteria
- [ ] User can drop, drag, and delete an Item pin on the House Map.
- [ ] Tapping an Item pin opens that Item's record.
- [ ] Placing a pin sets/confirms the Item's Room/Area.
- [ ] Pin coordinates persist and sync (offline-first).
- [ ] Items can be marked with only a Room/Area when no floorplan exists.

---

## Feature 5 — Client Task Intake Links — *Priority 5*

### 5.1 Goal
Let a homeowner (or a contractor acting on their behalf) generate a shareable web link. Anyone with the link — a client, tenant, family member — can submit task requests with photos and descriptions, **without installing the app or creating an account**. The homeowner sees the submissions in the app and can convert them into tracked Maintenance Tasks.

### 5.2 User stories
- As a contractor, I want to text a client a link where they can upload photos of the broken fan, the gap that needs caulking, and the cracked grout — so I know what supplies to bring before I show up.
- As a homeowner, I want to send my tenant a link to report maintenance issues with photos.
- As a homeowner, I want to review incoming task submissions, convert the real ones into tracked tasks, and dismiss the rest.
- As a homeowner, I want to add "after" photos to a completed task so the client (or my future self) can see the work that was done behind the drywall.

### 5.3 How it works

**For the homeowner/contractor (app side):**
1. From the Home screen, tap **"Request Tasks"** → generates a unique shareable link.
2. The link can be copied, texted, emailed, or embedded on a website.
3. Each home has **one active intake link** at a time (can regenerate to invalidate the old one).
4. Incoming submissions appear in an **Inbox** view: photo thumbnail, description, submitter name (optional), date submitted.
5. On each submission: **"Create Task"** (converts to a Maintenance Task, carries over photos) or **"Dismiss"** (archives it).
6. When creating a task from a submission, the homeowner can assign it to an existing Item/Room/Area or leave it standalone.

**For the client (web link side):**
1. Opens the link on any device — phone, tablet, desktop. No app store, no login.
2. Sees a simple form: **"What needs to be done?"** (text) + **"Add a photo"** (camera or gallery upload per task).
3. Can add **multiple tasks** in one session — each with its own photo and description.
4. Optional: enter their name so the contractor knows who submitted it.
5. Taps **"Send"** → confirmation screen. That's it.

**After the work is done:**
- The contractor/homeowner can add **"after" photos** to the Maintenance Task or Service Record (closing the loop — client sees the finished work if they have access, or the record is preserved for future reference).

### 5.4 UX flows

**Generate link:**
Home screen → "Request Tasks" button → "Share Link" sheet (copy, messages, email, etc.) → link is `yourapp.com/h/abc123/submit`

**Client experience (no auth):**
Open link → "Tell us what needs work" → [+ Add Task] × N → (per task: description + photo) → Name (optional) → "Send" → "Thanks! Your tasks have been submitted."

**Inbox (app):**
Home screen → inbox badge with unread count → list of submissions (newest first) → tap a submission → full-screen view: photo expandable, description, date, submitter name → [Create Task] [Dismiss]

**Create Task from submission:**
Tap "Create Task" → pre-filled title from description, pre-attached photo → optionally link to existing Item/Room → set cadence (or leave as one-time) → Save → submission moves to "converted" state.

### 5.5 Data touchpoints
New entities: `intake_links`, `task_submissions`. Existing: `maintenance_tasks`, `documents` (for photos).

### 5.6 Edge cases
- **Link expires or is regenerated:** old links show a friendly "This link is no longer active. Please ask the homeowner for a new link."
- **No photo submitted:** allowed — sometimes a text description is enough.
- **Duplicate submissions:** the homeowner can dismiss duplicates; no automatic dedup.
- **Large photos:** compress/resize on upload (client side, in the web form) to keep the experience fast even on slow connections.
- **Spam/abuse:** rate-limit submissions per link (e.g., 20 tasks per hour). If a link is being abused, homeowner regenerates it.
- **Offline behavior:** the intake web page requires internet (it's a hosted form). The homeowner's Inbox works offline once synced.

### 5.7 Acceptance criteria
- [ ] Homeowner can generate a shareable intake link from the app.
- [ ] Opening the link on any device shows a task-submission form (no auth required).
- [ ] Client can submit multiple tasks, each with an optional photo and description.
- [ ] Submissions appear in the homeowner's Inbox.
- [ ] Homeowner can convert a submission into a Maintenance Task (photos carry over).
- [ ] Homeowner can dismiss a submission.
- [ ] Regenerating the link invalidates the previous one.
- [ ] "After" photos can be attached to a Maintenance Task or Service Record.

---

## Cross-feature notes
- All features write to **local SQLite first** and sync (Doc 03 §5) — everything works offline **except the client intake web form, which requires internet to submit.**
- All user-facing strings use the ubiquitous language (Doc 02 §1); no programmer jargon.
- Onboarding threads these together: add an Item → place it on the map → accept its suggested maintenance tasks → get reminded (the core loop, Doc 01 §4).
- Feature 5 introduces the app's first **no-auth, guest-facing surface** — a lightweight hosted web form outside the React Native app. This is the only part of MVP that is not offline-first by nature.
