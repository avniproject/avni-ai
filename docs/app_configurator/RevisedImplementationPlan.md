# AI App Configurator — Revised Implementation Plan

> **Supersedes**: `ai_app_config_tech_solution.md`, `ConsolidatedImplementationPlanDraft.md`, `DIFY_INTEGRATION_PLAN.md`
> **Inputs**: `AI cohort 2 concept note.md` + mentor feedback (March 2026)

---

## 1. Problem Statement

Avni's app configuration process (entity + form setup) consumes 30–32% of total implementation effort per client. The goal is to automate this from uploaded SRS Excel files via a conversational chat interface, reducing time-to-go-live by 30%.

---

## 2. Mentor Feedback Incorporated

Three key changes from the cohort mentor review:

| Mentor Input | Design Decision |
|---|---|
| Parse SRS into JSONL format first | Add JSONL as an intermediate representation between raw Excel and Avni bundle JSON |
| Use MongoDB for Asset Store | PyMongo async replaces filesystem storage — enables session resume, versioning, LLM context refresh |
| Iterative confirmation before applying | Story #1706: parse Modelling → confirm entities with user → apply. Story #1704: parse forms → confirm → apply |
| Ambiguity/missing-info checks before generation | `ambiguity_checker.py` validates JSONL before presenting to user |
| Resume workflows after a while | MongoDB session persistence with status tracking enables resuming across restarts |

---

## 3. Architecture

```
Avni Webapp (React)
  ↓ file upload + chat message
Dify Workflow (Advanced Chat)
  ↓ intent routing → FILE_SETUP path
  ↓ Doc Extractor → Extraction LLM → Ambiguity Checker → Summary → User Confirmation
  ↓ confirmed JSONL
avni-ai Python service (FastAPI)
  ↓ POST /generate-bundle → bundle JSON → MongoDB
  ↓ assemble Metadata ZIP → upload to avni-server
avni-server (Spring Boot)
  ↓ POST /api/importMetaData (Metadata ZIP bulk import)
PostgreSQL
```

### Where AI/LLM Is Used vs. Where It Isn't

| Step | AI? | Rationale |
|------|-----|-----------|
| Intent classification (file upload vs. Q&A vs. config change) | Yes — LLM | Natural language understanding |
| Entity extraction from spec document | Yes — LLM | Documents have varying formats, sheet names, column headers; LLM handles ambiguity |
| Ambiguity detection (missing values, orphan references) | No — deterministic | Known validation rules (runs as Dify code node) |
| User corrections (rename, add, delete entities) | Yes — LLM | Natural language interpretation of corrections |
| Bundle JSON generation | No — deterministic | Exact schemas required; template-based is reliable |
| Visit schedule rule generation | Hybrid | Pattern matching for common; LLM for ambiguous |
| Skip logic / conditional display rules | Hybrid | Simple: deterministic parse; complex: LLM |
| Conversational corrections ("rename X", "add field Y") | Yes — LLM | Natural language + structured output |

---

## 4. Data Flow

```
Upload SRS Excel
       │
       ▼
  ┌─────────────────┐
  │  Doc Extractor   │  ← Dify built-in node; converts Excel/CSV to markdown
  │  (Dify node)     │
  └────────┬────────┘
           │ markdown text
           ▼
  ┌─────────────────┐
  │  Extraction LLM  │  ← LLM reads markdown, extracts entities into JSONL format
  │  (Dify LLM node) │    Prompt: dify/extraction_llm_prompt.md
  └────────┬────────┘
           │ entities JSONL (array[object])
           ▼
  ┌─────────────────┐
  │  Ambiguity       │  ← Deterministic validation (Dify code node)
  │  Checker         │    Code: dify/ambiguity_checker_node.py
  └────────┬────────┘
           │ issues report
           ▼
  ┌─────────────────┐
  │  Summary LLM     │  ← Present summary + issues to user
  │  (Dify LLM node) │    Ask for confirmation
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Human Input     │  ← Yes: proceed | No: corrections needed
  │  (Dify node)     │
  └────────┬────────┘
           │
     ┌─────┴─────┐
     │ Yes       │ No → Correction LLM → Apply Corrections → back to Summary
     ▼
  ┌─────────────────┐
  │ /generate-bundle │  ← avni-ai endpoint: JSONL → bundle JSON → MongoDB → ZIP → upload
  │ (HTTP request)   │
  └─────────────────┘
```

### JSONL Format Examples

**Entities JSONL (extracted by LLM):**
```json
{"type": "subject_type", "name": "Individual", "subjectTypeKind": "Person", "formLink": "Individual Registration"}
{"type": "program", "name": "Pregnancy", "subject": "Individual", "enrolmentForm": "Pregnancy Enrolment", "exitForm": "Pregnancy Exit"}
{"type": "encounter_type", "name": "ANC", "program": "Pregnancy", "subject": "", "encounterType": "Scheduled", "is_program_encounter": true, "frequency": "Monthly"}
{"type": "address_level", "name": "State", "level": 4, "parent": null}
{"type": "address_level", "name": "District", "level": 3, "parent": "State"}
```

**Form sheet → fields JSONL (for Story #1704):**
```json
{
  "type": "field",
  "form": "ANC Form",
  "page": "Vital Signs",
  "name": "BP Systolic",
  "data_type": "Numeric",
  "mandatory": true,
  "user_entered": true,
  "allow_negative": false,
  "allow_decimal": false,
  "min_value": null,
  "unit": "mmHg",
  "options": null,
  "unique_exclusive": false,
  "skip_logic": null,
  "frequency": "Monthly"
}
```

---

## 5. MongoDB Asset Store

### Document Schema (`bundle_sessions` collection)

```json
{
  "_id": "ObjectId",
  "session_id": "abc123",
  "org": "trial_org_name",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "version": 3,
  "status": "entities_confirmed | forms_pending | complete",
  "entities_jsonl": [...],
  "forms_jsonl": [...],
  "ambiguity_report": {
    "entities": { "issues": [], "warnings": [] },
    "forms": { "issues": [], "warnings": [] }
  },
  "assets": {
    "addressLevelTypes": {},
    "subjectTypes": {},
    "programs": {},
    "encounterTypes": {},
    "concepts": {},
    "forms": {},
    "formMappings": {}
  },
  "upload_history": [
    { "timestamp": "ISO8601", "status": "success", "files_uploaded": ["subjectTypes", "programs"] }
  ]
}
```

### Asset Store API (`asset_store.py`)

```python
async def create_session(org: str) -> str                              # returns session_id
async def find_or_create_session(org: str) -> str                     # resume if exists
async def store_jsonl(session_id: str, kind: str, rows: List[dict])   # "entities" or "forms"
async def get_jsonl(session_id: str, kind: str) -> List[dict]
async def store_asset(session_id: str, filename: str, content: dict)
async def get_asset(session_id: str, filename: str) -> dict
async def update_asset(session_id: str, filename: str, patch: dict)
async def list_assets(session_id: str) -> List[str]
async def assemble_zip(session_id: str) -> bytes
async def update_session_status(session_id: str, status: str)
async def add_upload_record(session_id: str, result: dict)
```

---

## 6. Files

### avni-ai server

```
src/tools/bundle/
  __init__.py
  models/                   # Typed dataclasses for parsed entities and bundle contracts
    parsed.py               # ParsedEntities, ParsedSubjectType, etc. (JSONL intermediate)
    subject_type.py         # SubjectTypeContract, SubjectTypeEnum (matches avni-server)
    program.py              # ProgramContract
    encounter_type.py       # EncounterTypeContract
    address_level_type.py   # AddressLevelTypeContract
    form_mapping.py         # FormMappingContract
    bundle.py               # Bundle container
    ambiguity.py            # AmbiguityIssue, AmbiguityReport
  bundle_generator.py       # JSONL → Avni bundle JSON (deterministic)
  asset_store.py            # MongoDB CRUD for sessions, JSONL, bundle assets (PyMongo async)
  bundle_uploader.py        # ZIP assembly + POST /api/importMetaData
  uuid_registry.py          # 143 standard UUIDs + deterministic UUID5

src/handlers/
  bundle_handler.py         # POST /generate-bundle, GET /bundle-status/{session_id}
  request/
    bundle_request.py       # GenerateBundleRequest
  response/
    bundle_response.py      # GenerateBundleResponse, BundleSummary
```

### Dify workflow nodes

```
dify/
  extraction_llm_prompt.md      # Prompt for LLM to extract entities from doc extractor markdown
  ambiguity_checker_node.py     # Deterministic validation code node (runs in Dify sandbox)
  apply_corrections_node.py     # Code node to apply LLM corrections to entities JSONL
  orchestrator_prompt.md        # Updated with FILE_SETUP routing
```

### Modified Files

| File | Change |
|------|--------|
| `src/main.py` | Add `/generate-bundle` + `/bundle-status/{session_id}` routes |
| `dify/orchestrator_prompt.md` | Add FILE_SETUP routing class |
| `dify/App Config [Staging] Assistant.yml` | FILE_SETUP intent routing, Doc Extractor → LLM → confirmation flow |

---

## 7. Story Execution Order

### Story #1706 — Entity Creation from Uploaded Spec

**Input**: Uploaded Excel/CSV file
**Output**: MongoDB assets: `subjectTypes`, `programs`, `encounterTypes`, `addressLevelTypes`, `formMappings` (skeleton)

**Dify chatflow steps:**
1. Doc Extractor converts uploaded file to markdown
2. Extraction LLM reads markdown → produces entities JSONL (subject types, programs, encounters, address levels with all available fields)
3. Ambiguity Checker code node validates JSONL → flags missing associations, duplicates, orphan references
4. Summary LLM presents summary + issues to user, asks for confirmation
5. User confirms or corrects via chat
6. If corrections: Correction LLM interprets → Apply Corrections code node patches JSONL → back to summary
7. On confirmation: Dify calls `POST /generate-bundle` with confirmed JSONL

**avni-ai server steps (`/generate-bundle`):**
1. Rebuild ParsedEntities from JSONL
2. `bundle_generator.generate_bundle(entities)` → produces:
   - Deterministic UUIDs (UUID5 on entity name)
   - Program eligibility rules (Gender=Female for Pregnancy)
   - Cancellation encounter types for each ProgramEncounter
   - Operational configs (operationalSubjectTypes, operationalPrograms, operationalEncounterTypes)
   - Individual relations and relationship types
   - Organisation config
3. `asset_store.store_jsonl()` + `asset_store.store_asset()` per entity type
4. `bundle_uploader.upload_bundle(session_id, auth_token)` — assembles ZIP, POSTs to `/api/importMetaData`
5. Returns bundle summary to Dify

**Dify changes:**
- Add FILE_SETUP intent to orchestrator routing
- Enable file upload (`.xlsx`, `.xls`, `.csv`)
- Add Doc Extractor → Extraction LLM → Ambiguity Checker → Summary → Human Input flow
- Conversation variables: `entities_jsonl` (array[object]), `uploaded_files` (array[object]), `session_status` (string)

### Story #1704 — Form & Concept Creation

**Input**: All non-Modelling form sheets (columns A–Q)
**Output**: Assets: `concepts`, `forms/*`, updated `formMappings`

**Steps:**
1. `spec_parser.parse_form_sheets(file_bytes)` → fields JSONL (one object per row per sheet)
2. `ambiguity_checker.check_forms(jsonl)` → flag unknown data types, coded fields with no options, skip logic referencing missing fields
3. LLM enrichment: infer `allowNegativeValue`, `allowDecimalValue`, `lowAbsolute/highAbsolute` from field names (e.g. "Number of children" → non-negative, non-decimal)
4. Dify presents per-form summary: _"ANC Form: 14 fields across 3 pages. Inferred: BP Systolic cannot be negative."_ → user confirms
5. `bundle_generator.generate_concepts(fields_jsonl)` — dedup, UUID registry, normal ranges
6. `bundle_generator.generate_forms(fields_jsonl, concepts)` — form element groups, elements, keyValues; auto-generate cancellation form for each ProgramEncounter
7. `bundle_generator.generate_form_mappings(entities_jsonl, forms)` — complete skeleton from #1706
8. Store assets in MongoDB → upload bundle (concepts first, then forms, then formMappings)

**Key logic in bundle_generator:**
- Standard UUID registry for answers (Yes/No/Male/Female etc.) — no duplication across orgs
- `unique: true` for exclusive options (None, NA, Not Applicable)
- `lowNormal/highNormal` for common vitals from NORMAL_RANGES config (BP, Hb, Weight, Height)
- Cancellation forms auto-generated for every ProgramEncounter form

### Story #1705 — Visit Schedule Rules

**Input**: Frequency column from JSONL
**Output**: Updated `forms/*` JSON with `visitScheduleRule` and `visitScheduleDeclarativeRule`

**Steps:**
1. `spec_parser.parse_visit_schedules(fields_jsonl)` — extract frequency per encounter type
2. `bundle_generator.generate_visit_rules(fields_jsonl)` — for each encounter form:
   - `visitScheduleRule`: JS string using `VisitScheduleBuilder` (Monthly → +30 days, Quarterly → +90 days)
   - `visitScheduleDeclarativeRule`: JSON with `scheduleVisit` action
   - Base date always from `programEncounter.encounterDateTime || earliestVisitDateTime` (per VisitSchedulingGuidelines.md)
3. `asset_store.update_asset()` — patch form JSONs in MongoDB
4. Re-upload bundle (incremental: only updated form files)

### Story #1707 — Conditional Display Rules

**Input**: Column Q ("When to show") + boolean columns (F, G, J–L)
**Output**: Updated `forms/*` with `declarativeRule` on form elements + groups

**Steps:**
1. `spec_parser.parse_skip_logic(fields_jsonl)` — extract conditions from column Q
2. `bundle_generator.generate_declarative_rules(fields_jsonl)`:
   - Simple conditions (FieldName = Value): deterministic parse → `containsAnswerConceptName` operator
   - Complex conditions: LLM interpretation
   - `actionType: "showFormElement"` / `"hideFormElement"`
   - Page-level group visibility rules
3. `bundle_generator.apply_key_values(fields_jsonl)`:
   - Column F → `allowNegativeValue`
   - Column G → `allowDecimalValue`
   - Column J-L → `allowFutureDate`
4. Update form assets in MongoDB → re-upload

---

## 8. Bundle Upload Mechanism

avni-server's `POST /api/importMetaData` processes JSON files in this order:
1. `addressLevelTypes.json`
2. `subjectTypes.json`, `programs.json`, `encounterTypes.json`
3. `concepts.json`
4. `forms/*.json`
5. `formMappings.json`
6. `groups.json`, `groupPrivilege.json`

`bundle_uploader.py` assembles the ZIP with the correct directory structure. UUID-based upsert in avni-server ensures re-upload updates entities (not duplicates).

**Two upload modes:**
| Mode | When | What |
|------|------|------|
| **Full bundle** | After all stories complete, or explicit request | All assets in single ZIP |
| **Incremental** | After each story | Only newly generated/updated files |

---

## 9. UUID Strategy

All UUIDs are **deterministic** — `uuid5(NAMESPACE_DNS, "avni:{entity_type}:{name}")`.
- Same name → same UUID on every run → idempotent re-upload
- Standard UUIDs from `uuid_registry.py` (143 answers: Yes/No/Male/Female/vaccine names etc.) take priority

Port `srs-bundle-generator/training_data/uuid_registry.json` → Python dict in `uuid_registry.py`.

---

## 10. Dependencies

| Package | Purpose | Add to |
|---------|---------|--------|
| `openpyxl` | Excel file parsing (kept for testing/local use) | `pyproject.toml` |
| `pymongo` | Async MongoDB driver (PyMongo 4.16+ AsyncMongoClient) | `pyproject.toml` |
| `python-multipart` | Multipart file upload to avni-server | `pyproject.toml` |

> **Note**: Motor (async MongoDB driver) is deprecated as of May 2026. Use PyMongo's built-in `AsyncMongoClient` instead.

---

## 11. Reference Code to Port/Reuse

### Reuse from existing avni-ai
- `src/services/task_manager.py` — `create_task()`, `start_background_task()` async pattern
- `src/clients/avni_client.py` — `AvniClient.call_avni_server(method, endpoint, auth_token, data)`
- `src/handlers/request_handlers.py` — `validate_config_request()`, `create_success_response()`

### Ported from srs-bundle-generator (JS → Python)
| JS Source | Python Target | What |
|-----------|--------------|------|
| `training_data/uuid_registry.json` | `uuid_registry.py` | 143 standard answer UUIDs (inlined as Python dict) |
| `scripts/generate_bundle_v2.js` | `bundle_generator.py` | Entity generation, operational configs, relations |

### Bundle contract models match avni-server
| Python model | Java contract |
|---|---|
| `SubjectTypeContract` | `SubjectTypeContract.java` |
| `ProgramContract` | `ProgramRequest.java` / `ProgramContract.java` |
| `EncounterTypeContract` | `EntityTypeContract.java` |
| `AddressLevelTypeContract` | `AddressLevelTypeContract.java` |
| `FormMappingContract` | `FormMappingContract.java` |

---

## 12. Verification

| Story | Test |
|-------|------|
| **#1706** | Upload SRS → entity summary shown in chat → user confirms → Subject Types/Programs/Encounter Types appear in App Designer |
| **#1706 re-upload** | Re-upload same SRS → no duplicates, UUIDs stable |
| **#1706 corrections** | User says "rename X to Y" → entities updated → re-confirm → bundle generated |
| **#1704** | Upload SRS with form sheets → forms + concepts in App Designer with correct fields, groups, data types |
| **#1705** | Upload SRS with Frequency column → visit schedule rules on forms |
| **#1707** | Upload SRS with "When to show" column → declarative rules on form elements; keyValues applied |
| **Resume** | Restart avni-ai service → continue session → assets still in MongoDB |
| **Incremental** | Upload only Modelling sheet → only entities created, no form errors |
| **Ambiguity** | Upload SRS with missing program association → AI asks to clarify before proceeding |
