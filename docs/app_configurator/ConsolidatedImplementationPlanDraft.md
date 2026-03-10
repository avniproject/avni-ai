**1\.  Problem Statement**

**Last year around 40-50% of Avni's incoming revenue came from SaaS subscriptions. To grow this share and reach more NGOs — especially those with smaller budgets — Avni needs to reduce the cost of client onboarding and app configuration. The process today is manual, time-intensive, and dependent on skilled team members, making it difficult to scale.**

**2\.  Current Process & Pain Points**

**2.1  End-to-end current workflow**

| How it works today Step 1 — Requirement gathering:  Delivery Manager (DM) collects requirements from client calls, Excel sheets, and PDFs. Step 2 — Specification:  DM maps requirements to Avni domain model and produces Scoping, Forms & Modelling documents.  (1.5 – 2 days) Step 3 — Estimation & contract:  Mapped documents used to estimate cost with the implementation team; contract signed. Step 4 — App configuration:  Implementation team configures app; clarifies requirements with client as needed. Step 5 — UAT:  Client tests app, shares feedback; engineer incorporates changes within scope. Step 6 — Go live:  Field-user training begins; app used on the ground. |
| :---- |

**2.2  Pain points**

* Manual work of filling forms and the modelling document — time-consuming and error-prone.  
* Too many form fields to be filled in specification document with self-evident answers. Example: 'Number of children delivered' cannot be negative or a decimal — yet must be explicitly specified today.  
* Currently AI aided generation of forms is dependent on a team member since it requires setup and not integrated with Avni product. Post generation corrections are to be made to make it work as expected.  
* AI aided rule generation is not reliable.

**3\.  Proposed Solution**

**Two-phase implementation plan**

| Phase | What it delivers | Estimated Timelines |
| :---- | :---- | :---- |
| **Phase 1** | Scoping, Forms & Modelling documents  →   (AI assistance in Avni web app)  \-\> Avni app Automate app configuration from structured specification documents. | March end |
| **Phase 2** | Raw requirements (PDFs / Excels / call notes)  →  (AI assistance in Avni web app) \-\> Scoping, Forms & Modelling documents Automate mapping of unstructured inputs to Avni domain model and structured spec. | April end |

**Once both phases are complete, the feature will serve two distinct user types:**

| User Persona | Org Category | Behaviour / Flow | Notes |
| :---- | :---- | :---- | :---- |
| **Internal team / users with Avni domain knowledge** | UAT & Self-service org | Upload requirements (spreadsheet, PDF, plain text)  →  Review Specifications sheet  →  Download Avni app to try out with username and password | Specifications sheet shared with user to finalise scope and sign contract with client |
| **Users without Avni domain knowledge** | Trial org | Upload requirements (spreadsheet, PDF, plain text)  →  Directions to download Avni app to try out with username and password | Specification sheet generated internally; not shared with user |

**4\.  Success Measurement**

**Before vs. after targets**

| Task | Current State | Target State | Scope Note |
| :---- | :---- | :---- | :---- |
| **Requirements → Specification documents** | 1.5 – 2 days | \~0.5 day | Calls still needed; AI automates document creation |
| **Specification documents → Avni app** | 100% of current effort | 30% reduction in effort | Field visit, report cards (DB migration in progress) and PM work are out of scope for this reduction |

**5\.  Solution Design**

In addition to above we would like to explore AI solutions for requirements raised from clients like extraction of data from image and filling it.

### Solution Design (Technical)

#### Context & Design Decision

Two earlier plans exist — `ai_app_config_tech_solution.md` (individual REST API calls per entity) and `DIFY_INTEGRATION_PLAN.md` (Node.js subprocess bundle generation). This document **supersedes both** with a unified approach:

- **No individual avni-server APIs for config creation.** All configuration is generated as bundle JSON files and uploaded to avni-server via the existing **Metadata ZIP upload** mechanism (`Admin → Upload → Metadata Zip`).
- The `avni-ai` Python service is the only place where new code is added. It parses the spec, generates bundle assets, stores them, and uploads them.
- The existing Node.js `srs-bundle-generator` is ported to Python (not wrapped via subprocess) for maintainability and single-runtime simplicity.

---

#### Architecture

```
Avni Webapp (React)
  ↓ file upload + chat message
Dify Workflow (Advanced Chat)
  ↓ intent routing → FILE_SETUP path
avni-ai Python service (FastAPI)
  ↓ parse spec → generate bundle JSONs → store as assets
  ↓ assemble Metadata ZIP → upload to avni-server
avni-server (Spring Boot)
  ↓ existing /api/importMetaData (Metadata ZIP upload endpoint)
PostgreSQL
```

**Key components in avni-ai:**

| Component | Purpose |
|-----------|---------|
| `src/tools/bundle/spec_parser.py` | Parse Modelling + form sheets from Excel/CSV |
| `src/tools/bundle/bundle_generator.py` | Generate all bundle JSON files (concepts, forms, entities, rules) |
| `src/tools/bundle/asset_store.py` | Store, retrieve, update generated JSON assets per org/session |
| `src/tools/bundle/bundle_uploader.py` | Assemble ZIP from assets → upload via Metadata ZIP endpoint |
| `src/tools/bundle/uuid_registry.py` | Standard UUIDs (Yes/No/Male/Female) + deterministic UUID generation |

---

#### Asset Store

A central design element missing from both earlier plans. Every generated JSON file is an **asset** that can be stored, retrieved, inspected, updated, and re-uploaded.

```
Storage layout (filesystem, under configurable ASSET_ROOT):
  assets/
    {org_name}_{session_id}/
      concepts.json
      subjectTypes.json
      programs.json
      encounterTypes.json
      formMappings.json
      forms/
        Individual Registration.json
        ANC Form.json
        ANC Encounter Cancellation.json
        ...
      groups.json
      groupPrivilege.json
      individualRelation.json
      relationshipType.json
      organisationConfig.json
      validation_report.json       ← generated after each step
```

**Asset Store API (internal Python, exposed as tools):**

| Operation | Function | Description |
|-----------|----------|-------------|
| **Store** | `store_asset(org, session, filename, content)` | Write/overwrite a JSON asset |
| **Retrieve** | `get_asset(org, session, filename) → dict` | Read a stored asset |
| **List** | `list_assets(org, session) → List[str]` | List all assets for a session |
| **Update** | `update_asset(org, session, filename, patch)` | Merge-patch an existing asset |
| **Bundle** | `assemble_zip(org, session) → bytes` | ZIP all assets into Metadata ZIP |
| **Upload** | `upload_bundle(org, session, auth_token)` | Assemble ZIP + POST to avni-server |

Sessions are reusable — re-uploading the same spec overwrites assets (deterministic UUIDs ensure idempotency).

---

#### Story Execution Order

##### Story #1706 — Entity Creation from Spec

**Input:** Modelling sheet from uploaded Excel
**Output:** Asset files: `subjectTypes.json`, `programs.json`, `encounterTypes.json`, `addressLevelTypes.json`, `formMappings.json` (skeleton)

Steps in `avni-ai`:
1. `spec_parser.parse_modelling_sheet()` — extract location hierarchy, subject types, programs, encounter types with program associations
2. `bundle_generator.generate_entities()` — produce JSON for each entity type using deterministic UUIDs, including:
   - Program eligibility rules (e.g. Gender=Female for Pregnancy)
   - Cancellation encounter types for each ProgramEncounter
   - Operational configs (`operationalSubjectTypes.json`, `operationalPrograms.json`, `operationalEncounterTypes.json`)
3. `asset_store.store_asset()` — persist each JSON
4. `bundle_uploader.upload_bundle()` — assemble ZIP, upload to avni-server via Metadata ZIP

**Single-file upload mode:** For quick iteration, also support uploading a single entity JSON (e.g. just `programs.json`) via the same Metadata ZIP mechanism with only that file in the ZIP.

**Dify changes:** Add `FILE_SETUP` intent routing + file upload enablement (`.xlsx`, `.csv`).
**Webapp changes:** Enable file upload button in chat UI.

##### Story #1704 — Form & Concept Creation from Spec

**Input:** All non-Modelling sheets (columns A–Q)
**Output:** Asset files: `concepts.json`, `forms/*.json`, updated `formMappings.json`

Steps:
1. `spec_parser.parse_form_sheets()` — read each sheet, map columns A–Q to structured form data
2. `bundle_generator.generate_concepts()` — produce deduplicated concepts with:
   - Standard UUID registry (143 answers: Yes/No/Male/Female etc.)
   - Deterministic UUIDs: `md5("concept:{name}")` for stability on re-upload
   - `lowNormal`/`highNormal` for common vitals (BP, Hb, Weight, Height, Temperature)
   - `unique: true` for exclusive multi-select options (None, NA)
3. `bundle_generator.generate_forms()` — produce form JSONs with form element groups and elements
   - Auto-generate cancellation forms for each ProgramEncounter form
   - `keyValues` on form elements (editable, allowNegativeValue, allowDecimalValue, allowFutureDate)
4. `bundle_generator.generate_form_mappings()` — complete skeleton from #1706 with form UUIDs
5. Store all assets → upload bundle

**Critical constraint:** `concepts.json` must appear before form files in the ZIP processing order. The Metadata ZIP upload handles this ordering internally.

##### Story #1705 — Visit Schedule Rules from Spec

**Input:** Frequency column from form sheets
**Output:** Updated `forms/*.json` with `visitScheduleRule` and `visitScheduleDeclarativeRule`

Steps:
1. `spec_parser.parse_visit_schedules()` — extract frequency patterns per encounter type
2. `bundle_generator.generate_visit_rules()` — for each form, generate:
   - `visitScheduleRule`: JavaScript string using `VisitScheduleBuilder` pattern
   - `visitScheduleDeclarativeRule`: JSON declarative rule with `scheduleVisit` action
   - Base date always from `programEncounter.encounterDateTime || earliestVisitDateTime` (per VisitSchedulingGuidelines.md)
3. `asset_store.update_asset()` — patch existing form JSONs with rule fields
4. Re-upload bundle

##### Story #1707 — Conditional Display Rules from Spec

**Input:** Column Q ("When to show") + boolean columns (F, G, J-L)
**Output:** Updated `forms/*.json` with `declarativeRule` on form elements and groups

Steps:
1. `spec_parser.parse_skip_logic()` — extract conditions from column Q per form element
2. `bundle_generator.generate_declarative_rules()` — for each condition:
   - `actionType: "showFormElement"` / `"hideFormElement"`
   - Compound rules with `containsAnswerConceptName` operator
   - Page-level group visibility rules
3. `bundle_generator.apply_key_values()` — boolean constraints as `keyValues`:
   - `allowNegativeValue`, `allowDecimalValue`, `allowFutureDate`
4. Update form assets → re-upload bundle

---

#### Upload Mechanism

avni-server's existing Metadata ZIP upload (`POST /api/importMetaData`, multipart file) processes JSON files in a defined order:
1. `addressLevelTypes.json`
2. `subjectTypes.json`, `programs.json`, `encounterTypes.json`
3. `concepts.json`
4. `forms/*.json`
5. `formMappings.json`
6. `groups.json`, `groupPrivilege.json`

The `bundle_uploader` assembles the ZIP with the correct directory structure. On re-upload, avni-server uses UUID-based upsert — existing entities are updated, new ones created.

**Two upload modes supported:**

| Mode | When | What gets uploaded |
|------|------|--------------------|
| **Full bundle** | After all stories complete or on explicit request | All assets as single Metadata ZIP |
| **Incremental** | After each story step | Only the newly generated/updated asset files in a ZIP |

---

#### Port from Node.js to Python

The `srs-bundle-generator` JS code is **ported to Python**, not wrapped via subprocess. Key mappings:

| JS Module | Python Module | What it does |
|-----------|--------------|--------------|
| `generators/bundle.js` | `bundle_generator.py` | Orchestrates all generation |
| `generators/concepts.js` | `bundle_generator.py` (concept methods) | Concept dedup + UUID registry |
| `generators/forms.js` | `bundle_generator.py` (form methods) | Form structure + declarative rules |
| `parsers/srs_parser.js` | `spec_parser.py` | Excel/CSV parsing (openpyxl) |
| `training_data/uuid_registry.json` | `uuid_registry.py` | Standard UUIDs as Python dict |
| `validators/bundle_validator.js` | `bundle_generator.py` (validate method) | Validation before upload |

---

#### New Files in avni-ai

```
avni-ai/src/tools/bundle/
  __init__.py
  spec_parser.py           # Excel/CSV parsing (Modelling + form sheets)
  bundle_generator.py      # All JSON generation (entities, concepts, forms, rules)
  asset_store.py           # Store/retrieve/update/list/ZIP assets
  bundle_uploader.py       # Assemble ZIP + upload to avni-server
  uuid_registry.py         # 143 standard UUIDs + deterministic UUID generation
```

#### Modified Files

| File | Change |
|------|--------|
| `src/tools/__init__.py` | Register bundle tools |
| `src/main.py` | Register bundle tools + new `/generate-bundle-async` route |
| `src/handlers/request_handlers.py` | Add bundle generation request handler |
| `dify/Avni [Staging] Assistant.yml` | FILE_SETUP intent routing + file upload config |
| `dify/orchestrator_prompt.md` | Add FILE_SETUP routing rules |

#### Dependencies

| Package | Purpose |
|---------|---------|
| `openpyxl` | Excel file parsing |
| `python-multipart` | Multipart file upload to avni-server |

---

#### Verification per Story

| Story | Verification |
|-------|-------------|
| **#1706** | Upload SRS → entities appear in App Designer (Subject Types, Programs, Encounter Types) |
| **#1704** | Upload SRS → forms appear in App Designer with correct fields, data types, groups; concepts deduplicated |
| **#1705** | Upload SRS with frequency column → visit schedule rules visible on forms |
| **#1707** | Upload SRS with "When to show" column → declarative rules on form elements; keyValues applied |
| **Re-upload** | Same SRS re-uploaded → entities updated (not duplicated), UUIDs stable |
| **Incremental** | After entity creation, upload only forms → no entity duplication |