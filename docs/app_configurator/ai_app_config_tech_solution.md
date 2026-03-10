# AI App Configurator - Tech Solutioning Plan

## Context

Avni implementation costs are high — form creation, rule configuration, and entity setup consume 30–32% of total implementation effort per client. The goal is to reduce time-to-go-live by 30% by automating app configuration from "field workflow specification" spreadsheets (Excel/CSV).

Epic [#1702](https://github.com/avniproject/avni-webapp/issues/1702) has 4 linked stories:
- **#1706** (In Progress): Create entities (location types, subjects, programs, encounters) from spec
- **#1704**: Create forms and concepts from spec
- **#1705**: Create visit schedule rules from spec
- **#1707**: Create conditional field/page display rules from spec

---

## Scope & Constraints

- **Trial orgs only** (same restriction as current AI assistant)
- File-based spec upload is the primary input mechanism
- The existing `avni-ai` Python service (at `/Users/himeshr/IdeaProjects/avni-ai/`) is the function-calling bridge between Dify and avni-server — **new capabilities must be added here**
- avni-server already has individual REST endpoints for each entity type (`/web/encounterType`, `/web/program`, etc.) — use these, with shared processing logic for both ZIP bundle upload and AI-driven import

---

## Architecture Overview

```
Avni Webapp (React)
  ↓ file upload + chat message
Dify Workflow (YAML, Advanced Chat mode)
  ↓ intent routing → FILE_SETUP path
avni-ai Python service (FastAPI, tool-calling bridge)
  ↓ parse spec → generate bundle JSON → call avni-server APIs
avni-server (Spring Boot)
  ↓ existing /web/* endpoints (encounterType, program, subjectType, form, concept...)
PostgreSQL
```

### Key Insight: avni-ai is the right place for bundle generation logic

The `avni-ai` service already:
- Has the tool-calling framework (`tool_registry.py`, `task_manager.py`)
- Handles async processing (task_id pattern)
- Calls avni-server APIs via `AvniClient`
- Is already invoked by Dify as an HTTP tool

New bundle processing tools (parse spec → generate entities/forms/rules → upload) belong in `avni-ai/src/tools/` as new tool modules.

---

## Implementation Plan by Story

### Story #1706 — Entity Creation from Spec (In Progress)

**What needs to happen:**
1. User uploads Excel/CSV field workflow spec in Avni Webapp chat UI
2. Dify routes to new `FILE_SETUP_ENTITIES` path
3. `avni-ai` service: new `parse_spec_and_create_entities` tool
   - Receives file content (or file URL) + auth_token
   - Parses "Modelling" sheet to extract: location hierarchy, subject types, programs, encounter types
   - Calls existing tools: `create_address_level_type`, `create_subject_type`, `create_program`, `create_encounter_type` (already exist in avni-ai)
   - On re-upload: calls update variants instead of create
4. Dify streams blocking progress messages back to webapp

**avni-ai changes (primary work):**

New file: `avni-ai/src/tools/bundle/spec_parser.py`
- `parse_modelling_sheet(file_content: bytes, file_type: str) -> ModellingSheetData`
- Uses `openpyxl` library (pure Python, no file system needed)
- Extracts: location hierarchy levels, subject type names, program names, encounter type names with their program association

New file: `avni-ai/src/tools/bundle/entity_setup.py`
- `setup_entities_from_spec(auth_token: str, file_content: str, file_name: str) -> str`
  - Calls spec_parser, then orchestrates create/update calls to existing tool functions
  - Returns structured result message
- `register_entity_setup_tools()` - registers with tool_registry

Update: `avni-ai/src/tools/__init__.py` to register new tools

**Dify changes:**
- Add new `FILE_SETUP` intent class to orchestrator routing
- Add new workflow branch: receives Dify file input → base64 encode → pass to avni-ai tool call
- Enable file upload in Dify workflow config (images+xlsx/csv)
- Add progress streaming nodes

**Avni Webapp changes:**
- Enable file upload button in chat UI (currently configured but disabled)
- Accept `.xlsx`, `.xls`, `.csv` file types
- Add blocking progress overlay component (reuse pattern from mobile app sync/Windsurf)

---

### Story #1704 — Form & Concept Creation from Spec

**avni-ai changes:**

New file: `avni-ai/src/tools/bundle/form_parser.py`
- `parse_form_sheets(file_content: bytes, file_type: str) -> List[FormSheetData]`
- Reads each non-Modelling sheet; maps columns A–Q:
  - A: Page/Group name, B: Field name, C: Data type, D: Mandatory
  - E: User/System, F: Allow negative, G: Allow decimal
  - H: Min value, I: Unit, J-L: Date constraints
  - M: Single/Multi select, N: Options, O: Unique exclusive, P: Validation, Q: When to show

New file: `avni-ai/src/tools/bundle/concept_generator.py`
- Reuse UUID registry from `srs-bundle-generator/training_data/uuid_registry.json` (143 standard UUIDs)
- Deterministic UUID generation: `hash("concept:{name}")` → stable UUID for re-uploads
- Concept deduplication: same name across forms → same UUID

New file: `avni-ai/src/tools/bundle/form_setup.py`
- `setup_forms_from_spec(auth_token: str, file_content: str, file_name: str) -> str`
- Phase 1: Upload all concepts (avni-server `/web/concept` bulk endpoint or individual)
- Phase 2: Upload forms with form element groups and form elements
- Phase 3: Upload form mappings (`/web/formMappings`)
- Also generates cancellation forms for each ProgramEncounter form (gap from LEARNINGS.md)

**avni-server API usage (existing endpoints):**
- Concepts: `POST /web/concept` (create) / `PUT /web/concept/{id}` (update)
- Forms: `POST /web/form` / `PUT /web/form/{uuid}`
- Form element groups: `POST /web/formElementGroup`
- Form elements: `POST /web/formElement`
- Form mappings: `POST /web/formMappings`

The critical constraint: concepts must be uploaded **before** forms that reference them.

---

### Story #1705 — Visit Schedule Rules

**avni-ai changes:**

New file: `avni-ai/src/tools/bundle/rule_generator.py`
- `generate_visit_schedule_rules(form_sheets: List[FormSheetData], encounter_types: List[str]) -> List[VisitScheduleRule]`
- Reads "Frequency" column from spec sheets
- Maps frequency patterns to JS rule templates:
  - "Monthly" → add 30 days from encounterDateTime
  - "Every N weeks" → add N*7 days
  - "Quarterly" → add 90 days
  - "N times: Day X, Day Y..." → multiple scheduled visits
- Generates both `visitScheduleRule` (JS string) and `visitScheduleDeclarativeRule` (JSON)
- **Constraint (VisitSchedulingGuidelines.md)**: Base date always from `programEncounter.encounterDateTime || earliestVisitDateTime`, never real-world date

Rule upload: `PUT /web/form/{uuid}` with rule fields populated

---

### Story #1707 — Conditional Display Rules

**avni-ai changes (in `rule_generator.py`):**
- `generate_declarative_rules(form_elements: List[FormElement]) -> List[DeclarativeRule]`
- Reads column Q "When to show" → `actionType: "showFormElement"`
- Negated form "When NOT to show" → `actionType: "hideFormElement"`
- Boolean columns (Allow negative, Allow decimal, Allow future date) → `keyValues` on form elements:
  - `allowNegativeValue: false`
  - `allowDecimalValue: false`
  - `allowFutureDate: false`
- Page-level rules: form element group visibility based on coded answer conditions

---

## Critical Files

### avni-ai repo (primary implementation target)
- `/Users/himeshr/IdeaProjects/avni-ai/src/tools/admin/` — existing entity tools to reuse
- `/Users/himeshr/IdeaProjects/avni-ai/src/services/tool_registry.py` — tool registration pattern
- `/Users/himeshr/IdeaProjects/avni-ai/src/handlers/request_handlers.py` — async task handler pattern
- `/Users/himeshr/IdeaProjects/avni-ai/src/clients/__init__.py` — AvniClient for API calls
- `/Users/himeshr/IdeaProjects/avni-ai/src/schemas/` — contract/schema pattern to follow

### SRS Bundle Generator (reference/port)
- `/Users/himeshr/IdeaProjects/siddharthr29/avni-skills/srs-bundle-generator/generators/bundle.js` — orchestration logic
- `/Users/himeshr/IdeaProjects/siddharthr29/avni-skills/srs-bundle-generator/generators/forms.js` — form generation + declarative rule logic
- `/Users/himeshr/IdeaProjects/siddharthr29/avni-skills/srs-bundle-generator/generators/concepts.js` — concept dedup + UUID registry
- `/Users/himeshr/IdeaProjects/siddharthr29/avni-skills/srs-bundle-generator/training_data/uuid_registry.json` — 143 standard UUIDs to port to Python
- `/Users/himeshr/IdeaProjects/siddharthr29/avni-skills/srs-bundle-generator/LEARNINGS.md` — gaps list (cancellation forms, keyValues, lowNormal/highNormal)

### Dify
- `/Users/himeshr/IdeaProjects/avni-ai/dify/Avni [Staging] Assistant.yml` — workflow to extend
- `/Users/himeshr/IdeaProjects/avni-ai/dify/orchestrator_prompt.md` — add FILE_SETUP routing
- `/Users/himeshr/IdeaProjects/avni-ai/dify/assistant_prompt.md` — update capabilities list

---

## New Files to Create in avni-ai

```
avni-ai/src/tools/bundle/
  __init__.py
  spec_parser.py          # Excel/CSV parsing (openpyxl), Modelling + form sheets
  entity_setup.py         # Tool: setup_entities_from_spec
  concept_generator.py    # UUID dedup, standard UUID registry, concept JSON generation
  form_setup.py           # Tool: setup_forms_from_spec (concepts + forms + mappings)
  rule_generator.py       # Visit schedule rules + declarative skip logic rules
  rule_setup.py           # Tool: setup_rules_from_spec
```

---

## Reuse from Existing Code

- **Entity creation**: reuse `create_encounter_type`, `create_program`, `create_subject_type` from `avni-ai/src/tools/app_designer/` — call them internally in the new setup tools
- **Async task pattern**: reuse `task_manager.create_task` + `task_manager.start_background_task` from `request_handlers.py`
- **AvniClient pattern**: reuse for all avni-server API calls
- **UUID registry**: port `srs-bundle-generator/training_data/uuid_registry.json` to Python dict
- **Standard UUIDs**: reuse the 143 standard answer UUIDs (Yes/No/Male/Female etc.) for concept dedup
- **Column mapping constants**: port `COLUMN_MAP` from `generate_bundle_v2.js` to Python

---

## Phased Rollout Order

1. **Phase 1 — Story #1706**: Entity creation from Modelling sheet (in progress)
   - Modelling sheet parser (Python/openpyxl)
   - `entity_setup.py` tool
   - Dify FILE_SETUP routing branch
   - Webapp file upload UI enablement + progress overlay

2. **Phase 2 — Story #1704**: Form + concept creation
   - Full column A–Q parser
   - `concept_generator.py` + `form_setup.py`
   - Concepts-first, then forms upload sequence
   - Cancellation form generation

3. **Phase 3 — Story #1705**: Visit schedule rules
   - `rule_generator.py` frequency parsing
   - JS rule + declarative rule generation
   - Rule upload via PUT /web/form/{uuid}

4. **Phase 4 — Story #1707**: Conditional display rules
   - Skip logic from column Q
   - keyValues for boolean constraints
   - Page-level group visibility rules

---

## avni-server API Endpoints to Use (Existing)

| Entity | Create | Update |
|--------|--------|--------|
| Address Level Type | `POST /web/addressLevelType` | `PUT /web/addressLevelType/{id}` |
| Subject Type | `POST /web/subjectType` | `PUT /web/subjectType/{id}` |
| Program | `POST /web/program` | `PUT /web/program/{id}` |
| Encounter Type | `POST /web/encounterType` | `PUT /web/encounterType/{id}` |
| Concept | `POST /web/concept` | `PUT /web/concept/{id}` |
| Form | `POST /web/form` | `PUT /web/form/{uuid}` |
| Form Element Group | `POST /web/formElementGroup` | `PUT /web/formElementGroup/{id}` |
| Form Element | `POST /web/formElement` | `PUT /web/formElement/{id}` |
| Form Mapping | `POST /web/formMappings` | — |

For upsert semantics on re-upload: first GET by UUID to check existence, then POST or PUT accordingly.

---

## Verification

1. Upload a sample SRS Excel file (e.g., PAD Adolescent or JK Laxmi SRS) via Avni Webapp chat
2. Verify entities created in Trial org via App Designer UI
3. Re-upload the same file → verify entities updated, not duplicated (check UUIDs stable)
4. Upload form sheet → verify forms appear in App Designer with correct fields, groups, data types
5. Upload spec with Frequency column → verify visit schedule rules on forms
6. Upload spec with "When to show" column → verify declarative rules on form elements
7. Run `node validators/bundle_validator.js <output>` (srs-bundle-generator) to validate generated bundle JSON before upload
