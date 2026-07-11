# Anne Homeowner App — Architecture

*Document 03 of 5 · Design & Specification Set*

This document recommends the technology stack (with a critical evaluation of the society's leaning toward React Native + Supabase), sketches the data schema, and specifies auth, offline-first sync, file/photo/manual storage, and the interactive House Map.

---

## 1. Requirements the architecture must satisfy

1. **iOS + Android**, both first-class, from one team/codebase if possible.
2. **Offline-first**: fully usable in basements, garages, crawlspaces with no signal; syncs when back online.
3. **Local + push notifications** for reminders (the #1 feature).
4. **File-heavy**: manuals (PDF), photos, warranty docs, receipts — stored, cached offline, synced.
5. **Interactive floorplan** with tappable pins.
6. **System-of-record durability**: people rely on this for years; data loss is unacceptable.
7. **Small team, fast iteration**: minimize backend boilerplate and platform-specific code.

---

## 2. Stack Recommendation — Critical Evaluation

### 2.1 Cross-platform framework

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **React Native (Expo)** | One JS/TS codebase for iOS+Android; huge ecosystem; Expo simplifies builds, OTA updates, notifications, file system, image picker; strong offline libs. | Bridge/perf edge cases; native module friction (mitigated by Expo config plugins). | **Recommended.** |
| **Flutter** | Excellent rendering (great for the custom floorplan canvas); single codebase; strong perf. | Dart (smaller hiring pool for this team); fewer turnkey backend integrations; team's stated leaning is RN. | Strong runner-up; would be the pick if the floorplan were the dominant technical risk. |
| **Native (Swift + Kotlin)** | Best performance & platform fidelity. | Two codebases, ~2× effort — unjustifiable for a small team building a CRUD+notifications+map app. | Rejected. |
| **PWA / web-wrapped** | Cheapest reach. | Weak offline file caching, unreliable background notifications on iOS, no true app-store presence. Reminders would be unreliable — a dealbreaker. | Rejected. |

**Decision: React Native via Expo (managed workflow, with config plugins as needed).** The app is fundamentally forms + lists + notifications + attachments + one custom canvas view. RN handles all of it, gives us one codebase for both required platforms, and matches the team's leaning. The one area of concern — the interactive floorplan — is solvable in RN (see §7) and does not justify Flutter's added hiring/ecosystem cost.

### 2.2 Backend / data platform

| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| **Supabase** | Postgres (real relational DB — perfect for our entity/relation model); built-in Auth (email, magic link, Apple, Google); Storage for files; Row-Level Security; realtime; generous DX; open-source / self-host escape hatch. | Offline is **not** built in — we must add a local DB + sync layer; realtime≠offline. | **Recommended, with an added offline layer.** |
| **Firebase** | Firestore has mature offline persistence out of the box; excellent notifications (FCM). | Document DB is a poor fit for our richly relational ontology (joins across Item↔Room↔Task↔Record↔Contractor get awkward and costly); vendor lock-in; querying/relations weaker. | Rejected — data model fit is wrong. |
| **Custom (Node/Postgres self-built)** | Full control. | Reinvents auth, storage, RLS, APIs — slows a small team significantly. | Rejected for MVP. |
| **PowerSync / ElectricSQL + Postgres** | Purpose-built Postgres⇄local-SQLite sync. | More moving parts; can layer on Supabase. | **Adopt PowerSync (or ElectricSQL) *on top of* Supabase** to solve the offline gap. |

**Decision: Supabase (Postgres + Auth + Storage + RLS) as the backend, with a local SQLite database and a sync engine (PowerSync or WatermelonDB-based custom sync) for offline-first.** Supabase's relational Postgres is the right fit for our ontology and relations (Doc 02 §4). Its only weakness — no native offline — is closed by the local-DB + sync layer described in §5. Firebase's one advantage (built-in offline) doesn't outweigh its poor relational fit.

### 2.3 Final stack

- **App:** React Native + Expo + TypeScript.
- **Navigation/UI:** React Navigation; a component kit (e.g., Tamagui or React Native Paper) for consistent, accessible UI.
- **Local DB:** SQLite (via WatermelonDB or op-sqlite) — source of truth on device.
- **Sync engine:** PowerSync (preferred) or ElectricSQL, bridging local SQLite ⇄ Supabase Postgres. (Fallback: a custom pull/push sync via Supabase — see §5.4.)
- **Backend:** Supabase — Postgres, Auth, Storage, Row-Level Security, Edge Functions.
- **Notifications:** Expo Notifications for local scheduled reminders; Expo Push + Supabase Edge Function/cron for server-side pushes (warranty expirations, catch-up nudges).
- **File storage:** Supabase Storage + local file cache (expo-file-system).
- **Floorplan:** react-native-svg + react-native-gesture-handler + reanimated (see §7).

---

## 3. Data Schema Sketch (Postgres)

Column names below are internal; user-facing labels come from Doc 02 §1. All tables carry `id (uuid)`, `home_id`, `created_at`, `updated_at`, `deleted_at (soft delete)`, and a `sync_status` for the offline layer. RLS scopes every row to its owner via `home_id → owner_user_id`.

```
users                (managed by Supabase Auth)
  id, email, ...

homes
  id, owner_user_id, name, address, purchase_date, hoa_notes, created_at, ...

locations                         -- "Room/Area"
  id, home_id, name, kind(indoor|outdoor|mechanical),
  shutoff_flags(jsonb: water|gas|electrical), notes

floorplans                        -- "House Map"
  id, home_id, storage_path(image), width_px, height_px,
  is_active(bool), created_at

map_markers                       -- "Map Pin"
  id, home_id, floorplan_id,
  location_id (nullable), equipment_item_id (nullable),
  x_ratio(float 0..1), y_ratio(float 0..1), label

equipment_categories              -- seeded reference (Kitchen, HVAC, ...)
  id, name, sort_order

equipment_types                   -- seeded reference (~84 types)
  id, category_id, name,
  ontology_classes(text[]),       -- ['Appliance','FilteredDevice',...]
  is_commonly_forgotten(bool),
  default_task_templates(jsonb)   -- seed cadences (see Doc 04 §1.5)

equipment_items                   -- "Item"
  id, home_id, equipment_type_id, location_id (nullable),
  name, make, model_number, serial_number,
  purchase_date, install_date, warranty_expiration,
  filter_size, notes

parts                             -- "Part" (R3)
  id, home_id, equipment_item_id,
  name(filter|belt|battery|bulb|...), spec(text),
  reorder_url, part_number, notes

warranties                        -- (R8) covers Item OR home-level asset
  id, home_id, equipment_item_id (nullable),
  covers_label, provider, start_date, expiration_date,
  coverage_notes, document_id (nullable)

documents                         -- "Manual/Document" (R5) & photos
  id, home_id,
  equipment_item_id (nullable), location_id (nullable),
  kind(manual|warranty|receipt|photo|other),
  storage_path, filename, mime_type, size_bytes,
  local_cache_path (device-only), caption

maintenance_tasks                 -- "Maintenance Task"
  id, home_id, equipment_item_id (nullable),
  title, cadence(monthly|quarterly|semiannual|annual|custom),
  custom_interval_days (nullable),
  last_service_date, next_due_date,
  preferred_contact_id (nullable), is_active, notes

reminders                         -- generated from tasks (R7)
  id, home_id, maintenance_task_id,
  fire_at(timestamptz), status(pending|done|snoozed|dismissed),
  local_notification_id

service_records                   -- "Maintenance History" (R4)
  id, home_id,
  equipment_item_id (nullable), maintenance_task_id (nullable),
  service_date, description, contact_id (nullable),
  cost, notes  -- retained even if item deleted

contacts                          -- "Contractor/Pro" (R6)
  id, home_id, name, trade, company, phone, email, notes

paint_entries                     -- "Paint Color"
  id, home_id, color_name, color_code, brand, sheen,
  location_id (nullable), notes, document_id (nullable)
```

Key indexes: `equipment_items(home_id, location_id)`, `maintenance_tasks(home_id, next_due_date)`, `reminders(home_id, fire_at, status)`, `documents(home_id, equipment_item_id)`.

---

## 4. Authentication

- **Supabase Auth** with:
  - **Email magic link** (primary — low friction, no passwords).
  - **Sign in with Apple** (required by App Store since we offer social login).
  - **Sign in with Google**.
- **Row-Level Security** on every table: a user can read/write only rows whose `home_id` belongs to a home they own. Policy shape: `home_id IN (SELECT id FROM homes WHERE owner_user_id = auth.uid())`.
- **Session** persisted securely on device (expo-secure-store) so the app opens straight into offline data without a round-trip.
- **Account recovery**: server (Supabase) is the durable source of truth after sync; document a recovery flow (magic link re-auth restores full data). Multi-home and household sharing are deferred (Doc 05 B1/B2) but the schema is already home-scoped to support them.

---

## 5. Offline-First & Sync Strategy

Offline is a hard requirement, not a nice-to-have. The device is the primary read/write surface; the cloud is the durable backup and sync hub.

### 5.1 Model
- **Local SQLite is the app's working database.** All reads and writes hit local storage first — the UI never blocks on the network.
- A **sync engine** (PowerSync/ElectricSQL) continuously (when online) reconciles local SQLite with Supabase Postgres.

### 5.2 Write path
1. User edits → written to local SQLite immediately, row marked `sync_status = pending`.
2. Reminders schedule as **local notifications** on the device right away (so they fire even fully offline).
3. When connectivity returns, the sync engine pushes pending changes to Postgres and pulls remote changes.

### 5.3 Conflict resolution
- **Last-write-wins per record** using `updated_at` for MVP (single-owner homes rarely conflict — same user on one device typically).
- Soft deletes (`deleted_at`) sync as tombstones so a delete on one device propagates.
- When household sharing lands (Doc 05 B2), revisit toward field-level merge for high-contention tables (tasks, service records).

### 5.4 Fallback sync (if not adopting PowerSync)
A custom sync is viable: each table carries `updated_at` + `sync_status`; the client periodically `POST`s pending rows and `GET`s rows where `updated_at > last_pulled_at` via Supabase. This is more code but removes a dependency — kept as a documented fallback.

### 5.5 Files offline
- Documents/photos are cached to the device (`expo-file-system`) on first view or on demand; metadata syncs via the DB, binaries via Supabase Storage (see §6). A "make available offline" toggle lets users pin critical manuals for guaranteed offline access.

---

## 6. File / Manual / Photo Storage

- **Binaries** (PDF manuals, JPEG/PNG photos, receipts) live in **Supabase Storage**, in a per-home bucket path: `homes/{home_id}/documents/{document_id}.{ext}`.
- **Access** via signed URLs generated on demand; Storage RLS mirrors the DB (owner-only).
- **Upload flow:** capture/pick file → write to local cache immediately → create `documents` row (`sync_status=pending`) → upload binary to Storage when online → store `storage_path`.
- **Offline cache:** `local_cache_path` points to the on-device copy; the app prefers cache, falls back to signed URL. Users can pin files "available offline."
- **Image handling:** compress/resize photos on capture (keep an original + a thumbnail) to control storage and bandwidth; thumbnails power fast list/grid rendering.
- **Storage limits & cost** tie to monetization (Doc 05 A1/D7): soft cap (e.g., 1 GB) on free tier.

---

## 7. Interactive House Map — Concrete Approach

The House Map is the product's spatial spine (Doc 01 §1). We choose a **pragmatic, image-based, pin-overlay approach** rather than building a CAD-grade drawing tool.

### 7.1 What the user provides (see Doc 05 C3)
- **Primary path — upload an image**: a photo of a builder's floorplan, an appraisal drawing, or a hand sketch. Any raster image works; no scale calibration required.
- **Fallback path — room list**: if the user has no floorplan, they build a simple list of Rooms/Areas and navigate via list instead of map. This guarantees the feature is never a dead end.
- (Later phase: an optional simple room-shape drawing tool, or third-party floorplan-scan SDK.)

### 7.2 Rendering & interaction
- Render the floorplan image inside an **`react-native-svg`** canvas wrapped with **`react-native-gesture-handler`** + **`react-native-reanimated`** for **pan and pinch-zoom** (essential on phone screens).
- **Pins** are SVG markers positioned by **normalized coordinates** (`x_ratio`, `y_ratio` in 0..1 of the image), so pins stay correct across zoom levels and device sizes and don't depend on absolute pixels.
- **Tap a pin** → open the linked Room/Area or Item detail. **Tap empty space** in "place mode" → drop a new pin (Item Marking, Doc 04 §4).
- **Clustering:** when zoomed out and pins overlap, collapse into a count badge that expands on zoom/tap.
- **Shutoff highlighting:** Rooms/Areas flagged with shutoffs (water/gas/electrical) render a distinct high-visibility marker for emergency use.

### 7.3 Why this approach
- **No dependency on CAD data** most homeowners don't have.
- **Normalized coordinates** make the map resolution- and device-independent and trivial to store/sync (two floats per pin).
- **Pure RN libraries** (svg + gesture-handler + reanimated) — no native fork, keeps the Expo workflow.
- **Graceful degradation** to a room list means the feature ships even for users without a floorplan.

### 7.4 Data touchpoints
- `floorplans` holds the image + intrinsic pixel dimensions (to compute aspect ratio).
- `map_markers` holds `x_ratio/y_ratio` + a link to a `location_id` and/or `equipment_item_id`.
- This directly implements the **installation-location (R1)** relation from Doc 02.

---

## 8. Notifications Architecture

- **Local scheduled notifications** (Expo Notifications) are the backbone — reminders fire on-device, offline, at the task's Next Due time. This is why reminders work in a basement.
- **Server-side push** (Expo Push via a Supabase Edge Function on a daily cron) handles cross-device consistency, warranty-expiration alerts, and catch-up nudges for tasks that went unaddressed.
- On task completion, the client logs a Service Record, recomputes Next Due (Doc 04 §1), cancels the old local notification, and schedules the next.

---

## 9. Environments & Delivery

- **Expo EAS Build** for iOS + Android binaries; **EAS Update** for OTA JS updates (fast fixes without store review).
- Environments: `dev` / `staging` / `prod` Supabase projects.
- **Observability:** Sentry (crash/error), plus basic product analytics (privacy-respecting) for the metrics in Doc 01 §5.
- **Backups:** Supabase automated Postgres backups + Storage durability; document restore procedure (system-of-record requirement).
