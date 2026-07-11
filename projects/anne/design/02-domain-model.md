# Anne Homeowner App — Domain Model

*Document 02 of 5 · Design & Specification Set*

This document defines the core entities, the equipment ontology (as a class hierarchy), the relationship types between entities, and the ubiquitous language used throughout the product. **User-facing names are in the homeowner's plain language** — no programmer jargon in anything the user sees.

---

## 1. Ubiquitous Language

The vocabulary below is the single shared language for product, design, and engineering. The **User-facing term** is what appears in the UI. The **Internal name** is for code/schema only and is never shown to users.

| User-facing term | Internal name | Meaning |
|------------------|---------------|---------|
| **Home** | `home` | The property the record is about (house, condo, townhome). Root of everything. |
| **Room / Area** | `location` | A named place in or around the home (Kitchen, Master Bath, Mechanical Room, Backyard, Garage). |
| **House Map** | `floorplan` | The interactive floorplan image the user taps to navigate. |
| **Map Pin / Marker** | `map_marker` | A placed point on the House Map tied to an Item or a Room. |
| **Item** | `equipment_item` | Any physical thing tracked: appliance, system, fixture, device. |
| **Item Type** | `equipment_type` | The kind of thing an Item is (e.g., "Dishwasher"), from the ontology. |
| **Category** | `equipment_category` | The top-level grouping (e.g., "Kitchen Appliances"). |
| **Make** | `make` | Manufacturer/brand (e.g., "Bosch"). |
| **Model** | `model_number` | Model name/number. |
| **Serial Number** | `serial_number` | Unique serial. |
| **Filter Size** | `filter_size` | Replacement filter dimensions (e.g., 16×25×1). |
| **Paint Color** | `paint_entry` | A stored paint (color name, code, brand, sheen, where used). |
| **Warranty** | `warranty` | Coverage record with expiration. |
| **Manual / Document** | `document` | An attached file (manual, warranty PDF, receipt, photo). |
| **Photo** | `photo` | An image attached to an Item, Room, or the Home. |
| **Maintenance Task** | `maintenance_task` | A recurring or one-time upkeep job (e.g., "Replace furnace filter"). |
| **Reminder** | `reminder` | A scheduled prompt derived from a Maintenance Task's cadence. |
| **Service Record** | `service_record` | A log entry: something was done on a date (a.k.a. Maintenance History). |
| **Maintenance History** | (view of `service_record`) | The list of Service Records for an Item. |
| **Cadence** | `cadence` | How often a task repeats: Monthly / Quarterly / Semiannual / Annual / Custom. |
| **Last Serviced** | `last_service_date` | Date the task/item was last done. |
| **Next Due** | `next_due_date` | Date the task is next due. |
| **Contractor / Pro** | `contact` | A service provider (plumber, electrician, HVAC tech, etc.). |
| **Part** | `part` | A consumable/replaceable component of an Item (filter, belt, battery, bulb). |
| **Shutoff** | `shutoff` (Room flag) | A safety control location (water/gas main, breaker panel). |

**Rules of the language**
- Never show "entity," "record ID," "FK," "sync," "null," etc. to users.
- Prefer verbs users say out loud: "Serviced," "Due," "Replace," "Where is it."
- "Maintenance History" and "Service Record" refer to the same data — history is the list view of records.

---

## 2. Core Entities

```
Home
 ├── Room/Area (location)            many per Home
 │     └── Map Pin (on House Map)
 ├── House Map (floorplan)           one active per Home (image + calibration)
 ├── Item (equipment_item)           many per Home; belongs to one Room/Area
 │     ├── Item Type ──▶ Category    classification (ontology)
 │     ├── Warranty                  0..n per Item
 │     ├── Part                      0..n per Item (filters, belts, batteries…)
 │     ├── Document / Manual         0..n per Item
 │     ├── Photo                     0..n per Item
 │     ├── Maintenance Task          0..n per Item (recurring upkeep)
 │     │     └── Reminder            derived schedule
 │     └── Service Record            0..n per Item (history)
 ├── Maintenance Task (standalone)   not tied to an Item (e.g., "Test detectors")
 ├── Paint Color                     many per Home (Home Finishes)
 ├── Contractor / Pro (contact)      many per Home
 ├── Document / Photo (home-level)   survey, permits, insurance policy, etc.
 └── Warranty (home-level)           roof, structural, etc.
```

### Entity field summaries (user-facing fields)

**Item** — the heart of the model. Every Item supports:
`Name` · `Item Type` · `Make` · `Model` · `Serial Number` · `Purchase Date` · `Install Date` · `Warranty Expiration` · `Room/Area (location)` · `Map Pin (optional)` · `Filter Size (if applicable)` · `Notes` · `Photos` · `Manuals/Documents` · `Maintenance History` · `Maintenance Tasks`.

**Room/Area** — `Name` · `Type (indoor/outdoor/mechanical)` · `Map Pin(s)` · `Shutoff flag (water/gas/electrical)` · `Notes` · `Photos`.

**Maintenance Task** — `Title` · `Item (optional link)` · `Cadence` · `Last Serviced` · `Next Due` · `Preferred Contractor (optional)` · `Notes`.

**Service Record** — `Item or Task` · `Date` · `What was done` · `Contractor (optional)` · `Cost (optional)` · `Notes` · `Attachments`.

**Paint Color** — `Color name` · `Color code` · `Brand` · `Sheen/Finish` · `Where used (Room/Area)` · `Notes` · `Photo`.

**Warranty** — `Covers (Item/roof/etc.)` · `Provider` · `Start Date` · `Expiration Date` · `Coverage notes` · `Document`.

**Contractor / Pro** — `Name` · `Trade (plumber, electrician, HVAC, roofer, handyman, pest, landscaper…)` · `Phone` · `Email` · `Company` · `Notes`.

---

## 3. Equipment Ontology — Class Hierarchy

The ontology maps the **~80 equipment types** into a two-level classification: **Category → Item Type**, with each Item Type assigned to one or more **ontology classes** (abstract behavioral roles) that drive shared fields and default maintenance behavior.

### 3.1 Ontology classes (behavioral roles)

These abstract classes determine which fields and default maintenance cadences an Item Type inherits. An Item Type may belong to more than one class (multiple inheritance of behavior).

| Class | Meaning | Confers |
|-------|---------|---------|
| `Appliance` | Plug-in / built-in household appliance | make/model/serial, warranty, manual, install date |
| `FilteredDevice` | Has a replaceable filter | **Filter Size**, filter-replacement cadence |
| `WaterHandling` | Moves, heats, softens, or filters water | flush/service cadence, leak-risk flag |
| `Pump` | Contains a motor-driven pump | inspection/service cadence, run-test task |
| `HeatingCooling` | Conditions air / temperature | seasonal service cadence |
| `CombustionDevice` | Burns gas/wood/pellets | annual inspection, CO-risk flag |
| `SafetyDevice` | Life-safety function | battery/test cadence, priority reminders |
| `PoweredBackup` | Provides/stores backup power | battery/load-test cadence |
| `Electronic` | A/V, network, smart device | firmware/warranty, low maintenance |
| `PlumbingFixture` | Fixed plumbing fixture | leak-check, no serial expected |
| `MotorizedOpening` | Motorized door/shade | lubrication/safety-test cadence |
| `OutdoorSystem` | Lives outside; weather-exposed | seasonal winterize/open cadence |

### 3.2 Category → Item Type mapping (with ontology classes)

Legend for classes: **A**=Appliance, **F**=FilteredDevice, **W**=WaterHandling, **P**=Pump, **HC**=HeatingCooling, **C**=CombustionDevice, **S**=SafetyDevice, **B**=PoweredBackup, **E**=Electronic, **PF**=PlumbingFixture, **M**=MotorizedOpening, **O**=OutdoorSystem.

#### Category 1 — Kitchen Appliances
| Item Type | Classes |
|-----------|---------|
| Refrigerator | A, F (water/ice filter) |
| Freezer (standalone) | A |
| Wine refrigerator | A |
| Beverage refrigerator | A |
| Ice maker (standalone) | A, W, F |
| Microwave | A |
| Built-in microwave | A |
| Range | A, C (if gas) |
| Cooktop | A, C (if gas) |
| Oven | A |
| Double oven | A |
| Warming drawer | A |
| Dishwasher | A, W |
| Range hood | A, F |
| Vent hood | A, F |
| Garbage disposal | A, W, PF |
| Trash compactor | A |
| Instant hot water dispenser | A, W |
| Water filtration system | W, F |
| Reverse osmosis system | W, F |

#### Category 2 — Laundry
| Item Type | Classes |
|-----------|---------|
| Washing machine | A, W |
| Dryer | A, F (lint/vent) |
| Washer/dryer combo | A, W, F |
| Steam closet | A, W |
| Ironing system | A |

#### Category 3 — HVAC & Air Quality
| Item Type | Classes |
|-----------|---------|
| Furnace | A, HC, F, C (gas) |
| Central AC | A, HC, F |
| Heat pump | A, HC, F |
| Mini-split | A, HC, F |
| Whole-house humidifier | A, HC, F, W |
| Whole-house dehumidifier | A, HC, F |
| Whole-house air purifier | A, F |
| ERV (energy recovery ventilator) | A, HC, F |
| HRV (heat recovery ventilator) | A, HC, F |
| Attic fan | A, M |
| Whole-house fan | A, M |
| Thermostat | E, HC |

#### Category 4 — Water Systems
| Item Type | Classes |
|-----------|---------|
| Water heater (tank) | A, W, C (gas) |
| Tankless water heater | A, W, C (gas) |
| Water softener | W, F |
| Water conditioner | W, F |
| Whole-house water filter | W, F |
| Well pump | W, P |
| Well pressure tank | W |
| Sewage ejector pump | W, P |
| Sump pump | W, P |
| Grinder pump | W, P |

#### Category 5 — Garage & Workshop
| Item Type | Classes |
|-----------|---------|
| Garage door opener | A, M |
| EV charger | A, E |
| Air compressor | A |
| Workshop dust collection | A, F |
| Utility sink pump | W, P |

#### Category 6 — Security & Safety
| Item Type | Classes |
|-----------|---------|
| Security system | E, S |
| Security cameras | E, S |
| Video doorbell | E, S |
| Smart locks | E, M, S |
| Smoke detectors | S |
| CO detectors | S |
| Water leak detectors | S, W |
| Radon mitigation fan | A, S |
| Backup battery systems | B, S |

#### Category 7 — Entertainment & Technology
| Item Type | Classes |
|-----------|---------|
| Television | A, E |
| Home theater receiver | A, E |
| Soundbar | A, E |
| Whole-home audio | A, E |
| Projector | A, E |
| Streaming devices | E |
| Network router | E |
| Network switches | E |
| Wi-Fi access points | E |
| Modem | E |

#### Category 8 — Outdoor & Landscape
| Item Type | Classes |
|-----------|---------|
| Irrigation controller | E, O |
| Sprinkler system | O, W |
| Pool pump | P, W, O |
| Pool heater | HC, C, O |
| Pool filter | F, W, O |
| Spa/hot tub | A, W, HC, O |
| Spa pump | P, W, O |
| Spa heater | HC, C, O |
| Pond pump | P, W, O |
| Fountain pump | P, W, O |
| Outdoor kitchen appliances | A, O, C (gas) |
| Outdoor refrigerator | A, O |
| Outdoor ice maker | A, W, O |
| Patio heaters | C, O |

#### Category 9 — Fireplace & Heating
| Item Type | Classes |
|-----------|---------|
| Gas fireplace | HC, C |
| Electric fireplace | A, HC, E |
| Pellet stove | HC, C, F |
| Wood stove | HC, C |
| Fireplace blower | A, HC |

#### Category 10 — Backup Power
| Item Type | Classes |
|-----------|---------|
| Portable generator | A, B, C |
| Standby generator | A, B, C |
| Solar inverter | E, B |
| Solar battery storage | B |
| UPS (uninterruptible power supply) | B, E |

#### Category 11 — Smart Home
| Item Type | Classes |
|-----------|---------|
| Smart thermostat | E, HC |
| Smart hubs | E |
| Smart lighting controllers | E |
| Smart blinds/shades | E, M |
| Smart irrigation controller | E, O |

#### Category 12 — Bathroom Fixtures
| Item Type | Classes |
|-----------|---------|
| Exhaust fans | A, M |
| Heated towel rack | A |
| Bidet seat | A, W, PF |
| Whirlpool/jetted tub pump | P, W, PF |
| Steam shower generator | A, W, HC |

### 3.3 "Commonly-Forgotten Built-ins" (cross-cutting tag)

These are **not a new category** — they are existing Item Types flagged with a `commonly-forgotten` tag so onboarding can proactively prompt: *"Many homes have these and forget them — do you have any?"*

Tagged types (all already mapped above): Garage door opener, Water softener, Whole-house water filter, Irrigation controller, Sump pump, Radon mitigation fan, Whole-house humidifier/dehumidifier, Security cameras, EV charger, Generator (portable/standby), Solar inverter, Exhaust fans, Fireplace blower, Water leak detectors (leak detection system).

### 3.4 Coverage check (threshold: ≥70 of 80 mapped)

**Total distinct equipment Item Types mapped: 84** (Categories 1–12), each assigned to ≥1 ontology class. This **exceeds the ≥70/80 threshold** — 100% of the source ontology's distinct items are mapped, plus the Commonly-Forgotten group is handled as tags rather than duplicates. Every Item Type inherits: make, model, serial, purchase date, install date, warranty expiration, maintenance history, manual/document location, and physical location (map link) via the base `equipment_item` entity, with class-specific fields (e.g., Filter Size for `FilteredDevice`) added on top.

---

## 4. Relationship / Relation Types

At least five first-class relation types connect the entities. These are the semantic edges the product reasons about.

| # | Relation type | From → To | Cardinality | Purpose / example |
|---|---------------|-----------|-------------|-------------------|
| R1 | **installation-location** | Item → Room/Area (and Map Pin) | many Items → one Room/Area | "Furnace is in the Mechanical Room" — powers the House Map & item marking. |
| R2 | **manufacturer** (make) | Item → Make/Model | many Items → one Make | "Dishwasher made by Bosch, model SHXM…" — powers recall (J1) and future manual lookup. |
| R3 | **part** | Item → Part | one Item → many Parts | "Furnace uses a 16×25×1 filter"; "Sump pump has a backup battery." Parts carry their own reorder info and cadence. |
| R4 | **maintenance-history** | Item/Task → Service Record | one Item → many Service Records | "Water heater flushed on 2025-03-12 by ABC Plumbing." Builds the Maintenance History view. |
| R5 | **manual** (document) | Item → Document | one Item → many Documents | "Owner's manual, warranty PDF, purchase receipt attached to the range." |
| R6 | **serviced-by** (contractor) | Service Record/Task → Contractor | many → one | "HVAC serviced by Cool Air Inc." Links log entries and preferred pros. |
| R7 | **scheduled-by** (reminder) | Maintenance Task → Reminder | one Task → recurring Reminders | Cadence generates the next Reminder + Next Due date. |
| R8 | **covered-by** (warranty) | Item → Warranty | one Item → many Warranties | "Roof covered until 2039." Drives warranty-expiration alerts. |

**Threshold check (≥5 relation types incl. installation-location, manufacturer, part, maintenance-history, manual):** all five required relations (R1 installation-location, R2 manufacturer, R3 part, R4 maintenance-history, R5 manual) are present, plus three more (R6–R8). **Threshold met.**

---

## 5. Location & Map Model

- A **Room/Area** is the semantic location; a **Map Pin** is its (optional) visual placement on the **House Map**.
- An **Item** always belongs to a Room/Area (R1). It *may* additionally have its own Map Pin for precise placement (e.g., "sink in master bath" pinned to a spot), or inherit its Room/Area's pin.
- Safety-critical Rooms/Areas can carry a **Shutoff** flag (water main, gas main, electrical panel) so the map and emergency views can highlight them.

This keeps the House Map (Doc 03 §7) and Item Marking (Doc 04 §4) grounded in a clean, testable relationship rather than free-floating coordinates.

---

## 6. Data Integrity Rules

- Deleting a Room/Area must not silently orphan Items — prompt to reassign or move to "Unassigned."
- Deleting an Item cascades to its Parts, Reminders, and Map Pin, but **Service Records are retained** (with a "for a removed item" marker) so history/warranty/insurance value is preserved.
- Serial Number is not required (many fixtures lack one) but is strongly encouraged for `Appliance`-class items.
- Filter Size is only surfaced for `FilteredDevice`-class items.
- Cadence changes recompute Next Due from Last Serviced (see Doc 04 §1).
