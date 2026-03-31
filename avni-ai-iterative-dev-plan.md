# avni-ai Iterative Development Plan

## Context

**Strategic:** Approach A (Dify + avni-ai) is the chosen platform (79% score per TechApproachEvaluation.md). Bundle generation code from avni-ai-platform (Approach B, 12,280 LOC) is being ported into avni-ai. The goal is Phase 1: structured SRS → importable Avni app, targeting 30% effort reduction.

**Current state of the flow (`App Configurator [Staging] v2`):**
- `advanced-chat` Dify workflow, 42 explicit nodes
- Entity extractor produces `subject_types`, `programs`, `encounter_types`, `address_levels` — **no forms, no concepts**
- Bundle generator has `process_forms()` but it's never called (no `forms` key in input)
- Result: upload succeeds but Avni app shows nothing
- Validation split across Dify code nodes (business logic) and avni-ai (structural) — 5 code nodes that are pure overhead
- No intermediate spec representation; requirements gathering and generation are entangled
- No YAML spec, no spec validator

**What a real Avni bundle contains (from avni-impl-bundles/reference and avni-server):**

The server (`BundleZipFileImporter.java`) processes **36 file types** in strict order. Current `generator.py` only produces 8. Missing:

| Category | Missing from generator | Priority |
|----------|----------------------|----------|
| Core operational | operationalSubjectTypes, operationalPrograms, operationalEncounterTypes | **Critical** — server expects these |
| Location hierarchy | addressLevelTypes | **Critical** — foundational block |
| Dashboard/Reports | reportCard, reportDashboard, groupDashboards | High — needed for usable app |
| Org config | organisationConfig (languages, filters, search config) | High — app UX depends on it |
| Access control | groupPrivilege (150-300+ entries per impl) | High — security |
| Relationships | individualRelation, relationshipType | Medium |

Out of scope for now: identifierSource, ruleDependency/rules (deprecated), translations (separate story), media/extensions (not part of app configurator AI).

**Server processing order (critical for bundle correctness):**
1. organisationConfig → 2. addressLevelTypes → 3. locations → 4. catchments → 5. subjectTypes → 6. operationalSubjectTypes → 7. programs → 8. operationalPrograms → 9. encounterTypes → 10. operationalEncounterTypes → 11. concepts → 12. forms/ → 13. formMappings → 14. individualRelation → 15. relationshipType → 16. identifierSource → 17. groups → 18. groupRole → 19. groupPrivilege → 20. reportCard → 21. reportDashboard → 22. groupDashboards → ... → 36. customQueries

---

## Architecture: Hybrid Agent + Deterministic Sub-flows

```
advanced-chat (Dify workflow)
│
├── FIXED PIPELINE (explicit nodes — deterministic, always same order)
│   ├── File upload → Doc Extractor
│   ├── Entity Extractor LLM (structured output)
│   ├── HTTP: POST /validate-entities
│   ├── HTTP: POST /generate-bundle
│   ├── HTTP: POST /validate-bundle
│   ├── HTTP: POST /upload-bundle
│   └── Polling loop: GET /upload-status
│
└── AGENT NODES (LLM + tool calling — dynamic, open-ended)
    │
    ├── Spec Agent
    │   Task: iteratively define/refine YAML spec with user
    │   Tools: /validate-entities, /apply-entity-corrections, /generate-spec,
    │          /bundle-to-spec, /api/existing-config, /validate-spec
    │   Output: approved spec_yaml → stored in conversation
    │
    ├── Review Agent
    │   Task: inspect generated bundle before upload
    │   Tools: /validate-bundle, /bundle-to-spec (human-readable diff),
    │          /download-bundle-b64 (compare with existing), /execute-python
    │   Output: bundle_zip_b64 confirmed (or fixed) → proceed to upload
    │
    └── Error Agent
        Task: diagnose upload failures, analyze server errors
        Tools: /upload-status, /api/existing-config, /execute-python,
               /generate-bundle (retry), /validate-bundle
        Output: fixed bundle uploaded, or clear error report to user
```

avni-ai endpoints are registered as **Dify tools** (via OpenAPI spec or HTTP tool definitions). Agent nodes call them dynamically; explicit pipeline nodes also call them as HTTP-request nodes. Same endpoints, two invocation patterns.

---

## Two-Stage Flow

```
STAGE 1: Requirements Gathering + Spec (Spec Agent)
────────────────────────────────────────────────────
Input files (XLS/PDF/CSV/images)
  → Doc Extractor → Entity Extractor LLM → raw entities JSONL
  → POST /validate-entities → deterministic structural issues
  → Spec Agent loop:
      /bundle-to-spec    ← if org has existing config, start from that
      /generate-spec     ← entities → YAML spec
      /validate-spec     ← deterministic spec validation
      /apply-corrections ← user requests changes
      /api/existing-config  ← inspect current org
      LLM adequacy check ← semantic/completeness (within agent reasoning)
      → user reviews spec → corrections → re-validate → repeat
  → Approved spec_yaml stored in conversation

STAGE 2: Bundle Generation + Review + Upload
─────────────────────────────────────────────
  → POST /spec-to-entities → full entities JSON
  → POST /generate-bundle → deterministic ZIP
  → Review Agent: inspect, compare, confirm
  → POST /upload-bundle → async
  → Polling loop → if error → Error Agent → retry or report
  → Done
```

---

## YAML Spec Format

The spec must handle the **wide variety** of real Avni implementations (5+ production orgs in avni-impl-bundles/reference). It is human-readable (no UUIDs, no JSON technicalities), but complete enough that `/spec-to-entities` can produce a full bundle from it.

```yaml
org: "My Org"
settings:
  languages: [en, hi_IN]
  enableComments: true

addressLevels:
  - {name: State, level: 3}
  - {name: District, level: 2, parent: State}
  - {name: Village, level: 1, parent: District}

subjectTypes:
  - name: Individual
    type: Person
    allowProfilePicture: false
    uniqueName: false
    lastNameOptional: true
    registrationForm:
      sections:
        - name: Demographics
          fields:
            - {name: Age, dataType: Numeric, mandatory: true, min: 0, max: 120}
            - {name: Gender, dataType: Coded, mandatory: true, options: [Male, Female, Other]}
            - {name: Phone Number, dataType: PhoneNumber, validFormat: "^[0-9]{10}$"}

  - name: Household
    type: Household
    registrationForm:
      sections:
        - name: Household Info
          fields:
            - {name: Household Head, dataType: Text, mandatory: true}

programs:
  - name: Maternal Health
    targetSubjectType: Individual
    colour: "#E91E63"
    allowMultipleEnrolments: false
    enrolmentForm:
      sections:
        - name: Enrolment Details
          fields:
            - {name: LMP Date, dataType: Date, mandatory: true}
            - {name: High Risk, dataType: Coded, options: [Yes, No]}
    exitForm:
      sections:
        - name: Exit Details
          fields:
            - {name: Exit Reason, dataType: Coded, options: [Delivery, Transfer, Death]}

encounterTypes:
  - name: ANC Visit
    program: Maternal Health
    subjectType: Individual
    scheduled: true
    form:
      sections:
        - name: Vital Signs
          fields:
            - {name: Weight, dataType: Numeric, mandatory: true, unit: kg, min: 30, max: 200}
            - name: BP Systolic
              dataType: Numeric
              unit: mmHg
              min: 80
              max: 220
            - name: Haemoglobin
              dataType: Numeric
              unit: g/dL
              min: 2
              max: 16
        - name: Assessment
          fields:
            - name: Is High Risk
              dataType: Coded
              options: [Yes, No]
              skipLogic:
                dependsOn: High Risk
                condition: "="
                value: "Yes"
    cancellationForm:
      fields:
        - {name: Cancellation Reason, dataType: Coded, options: [Not Available, Refused, Migrated]}

  - name: General Visit
    subjectType: Individual
    scheduled: false
    form:
      sections:
        - name: Visit Details
          fields:
            - {name: Visit Type, dataType: Coded, options: [Follow-up, Emergency]}

groups:
  - {name: Everyone, hasAllPrivileges: false}
  - {name: Administrators, hasAllPrivileges: true}

reportCards:
  - {name: Scheduled Visits, type: standard, standardType: scheduledVisits}
  - {name: Overdue Visits, type: standard, standardType: overdueVisits, color: "#f44336"}
  - {name: Total Registrations, type: standard, standardType: total}
  - {name: Recent Registrations, type: standard, standardType: recentRegistrations, recentDuration: {value: 1, unit: days}}

dashboard:
  - name: Main Dashboard
    sections:
      - name: Overview
        cards: [Scheduled Visits, Overdue Visits, Total Registrations]
      - name: Recent Activity
        cards: [Recent Registrations]

relationships:
  - {a: father, aGender: Male, b: son, bGender: Male}
  - {a: mother, aGender: Female, b: daughter, bGender: Female}
  - {a: husband, aGender: Male, b: wife, bGender: Female}
```

---

## YAML Spec Validator (`/validate-spec`)

Deterministic validation of the YAML spec **before** bundle generation. Catches errors early, gives clear human-readable messages.

**Validation rules:**

Structural:
- All referenced subjectTypes in programs/encounterTypes/forms exist
- All referenced programs in encounterTypes exist
- No duplicate names within any category
- Address levels have valid parent references and consistent level numbering
- Forms have at least one section with at least one field
- Coded fields have non-empty options array

Cross-reference:
- Program `targetSubjectType` matches a defined subject type
- Encounter type `program` matches a defined program (if set)
- Encounter type `subjectType` matches a defined subject type
- Skip logic `dependsOn` references a field that exists in the same or earlier form
- Report cards reference valid standardType values
- Dashboard sections reference valid report card names

Completeness:
- Every encounter type has a form
- Every program has enrolment form
- At least one subject type, one group
- Address levels present (warning if empty)

Output: `{"valid": bool, "errors": [...], "warnings": [...], "suggestions": [...]}`

---

## Phases

### Phase 0 — Address level types + operational configs in bundle (foundational)

**Problem:** `address_levels` ignored; no operational configs generated. Server expects these.

**Changes in `src/bundle/generator.py`:**
- `process_address_levels()` → produces `addressLevelTypes` entries with deterministic UUIDs, parent hierarchy, level ordering
- `_generate_operational_subject_types()` → simple wrapper: `[{name, uuid, subjectTypeUUID}]` for each subject type
- `_generate_operational_programs()` → `[{name, uuid, programUUID, programSubjectLabel}]`
- `_generate_operational_encounter_types()` → `[{name, uuid, encounterTypeUUID}]`
- Add all 4 to `self.bundle` dict and `to_zip_bytes()` output

**Files:** `src/bundle/generator.py`

**Verify:** POST `/generate-bundle` → ZIP has `addressLevelTypes.json`, `operationalSubjectTypes.json`, `operationalPrograms.json`, `operationalEncounterTypes.json`

---

### Phase 1 — Auto-derive forms from encounter types (unblocks current flow)

**Problem:** No `forms` key → empty bundle → nothing in Avni.

**In `src/bundle/generator.py`:** `_auto_derive_forms(entities)` called from `generate()` when forms absent/empty:
- Each `subjectType` → registration form (`IndividualProfile`)
- Each `program` → enrolment (`ProgramEnrolment`) + exit (`ProgramExit`)
- Each `encounterType` → form (`ProgramEncounter` or `Encounter` based on `is_program_encounter`) + cancellation form
- Links `subjectType`, `program` from encounter type's extracted fields
- All forms have empty `fields` — produces valid structures + form mappings

**Files:** `src/bundle/generator.py`

**Verify:** POST `/generate-bundle` with typical Dify payload → non-empty `forms`, `formMappings`, `concepts`

---

### Phase 2 — Server-side entity validation and corrections

Two new endpoints replacing Dify code nodes.

**`POST /validate-entities`:**
- Deterministic structural validation (moved from Dify Ambiguity Checker code node)
- Duplicate names, missing cross-references, fuzzy subject type matching
- Returns `{issues, error_count, warning_count, issues_summary}`

**`POST /apply-entity-corrections`:**
- Entity merge/delete logic (moved from Dify Entities Corrector code node)
- Input: `{entities, corrections: [{entity_type, name, _delete?, ...fields}]}`
- Returns `{result: ...updated entities}`

**Files:**
- `src/handlers/entity_handlers.py` — new
- `src/main.py` — register routes
- Dify YAML — replace 2 code nodes with HTTP nodes

---

### Phase 3 — Spec endpoints: generate, validate, convert

**`POST /generate-spec`:** entities dict → YAML spec (format above)
- Uses standard UUID knowledge from `avni-skills/srs-bundle-generator/scripts/generate_bundle_v2.js` (STANDARD_UUIDS, NORMAL_RANGES) to enrich numeric field bounds
- Draws on CONSOLIDATED_PATTERNS.md for sector-specific defaults

**`POST /validate-spec`:** YAML spec → validation result
- All structural, cross-reference, and completeness checks defined above
- Returns `{valid, errors, warnings, suggestions}`

**`POST /bundle-to-spec`:** existing bundle JSON → YAML spec
- Inverts bundle: strips UUIDs, reconstructs hierarchy, converts formElementGroups → field lists
- Used by Spec Agent to start enhancement flow from current org state

**`POST /spec-to-entities`:** YAML spec → full entities dict with forms+fields
- Parses YAML; produces entities with fully populated `forms` array
- Feeds into `/generate-bundle`

**Files:**
- `src/handlers/spec_handlers.py` — new, all 4 handlers
- `src/bundle/spec_generator.py` — entities → YAML
- `src/bundle/spec_parser.py` — YAML → entities
- `src/bundle/spec_validator.py` — YAML validation rules
- `src/main.py` — register 4 routes

---

### Phase 4 — Dify Agent nodes: Spec Agent, Review Agent, Error Agent

Replace explicit correction/review/error node clusters with 3 Agent nodes.

**Spec Agent** (replaces ~10 correction/confirmation nodes):
- Tools: `/validate-entities`, `/apply-entity-corrections`, `/generate-spec`, `/validate-spec`, `/bundle-to-spec`, `/api/existing-config`
- System prompt: scoped to requirements gathering and spec definition
- Max iterations: 5
- Output: approved `spec_yaml`

**Review Agent** (new — between generate-bundle and upload):
- Tools: `/validate-bundle`, `/bundle-to-spec`, `/download-bundle-b64`, `/execute-python`
- Task: inspect bundle, compare with existing, confirm or fix
- Max iterations: 3

**Error Agent** (new — on upload failure):
- Tools: `/upload-status`, `/api/existing-config`, `/execute-python`, `/generate-bundle`
- Task: diagnose error, attempt fix, retry or report
- Max iterations: 3

**Dify implementation:**
- Register avni-ai endpoints as Dify tools (via OpenAPI spec from `/openapi.json` or explicit HTTP tool defs)
- Each Agent node configured with tool subset + system prompt + iteration cap
- Fixed pipeline nodes (generate-bundle, upload-bundle, polling) remain as explicit HTTP-request nodes

**Files:**
- Dify YAML — 3 agent nodes; tool registration
- `src/main.py` — optionally expose `/openapi.json` for Dify tool discovery

---

### Phase 5 — Extend Dify entity extractor to include forms+fields

Extend Entity Extractor LLM structured output schema:
```json
"forms": [{
  "name": str, "formType": str, "subjectType": str,
  "program": str, "encounterType": str,
  "fields": [{
    "name": str, "dataType": str, "group": str,
    "mandatory": bool, "options": [str],
    "skipLogic": {"dependsOn": str, "condition": str, "value": str}
  }]
}]
```

Phase 1 auto-derive becomes fallback when forms array is empty.
`/validate-entities` extended with forms cross-ref checks.
`/validate-spec` already handles forms validation from Phase 3.

**Files:**
- Dify YAML — Entity Extractor: extend prompt + schema
- `src/handlers/entity_handlers.py` — extend validation

---

### Phase 6 — Pydantic request schemas

`src/schemas/bundle_models.py`:
```python
class FieldSpec(BaseModel): name: str; dataType: str; mandatory: bool = False; ...
class FormSpec(BaseModel): name: str; formType: str; fields: list[FieldSpec] = []
class EntitySpec(BaseModel):
    subject_types: list[SubjectTypeSpec] = []
    programs: list[ProgramSpec] = []
    encounter_types: list[EncounterTypeSpec] = []
    forms: list[FormSpec] = []
    address_levels: list[AddressLevelSpec] = []
class GenerateBundleRequest(BaseModel): entities: EntitySpec; org_name: str
```

Wire into `/generate-bundle`, `/validate-entities`, `/generate-spec`, `/spec-to-entities` — return structured 422 on schema failure.

**Files:** `src/schemas/bundle_models.py`, all handler files

---

### Phase 7 — Expand generator for dashboard, reports, privileges, org config

Extend `generator.py` to produce remaining high-priority bundle files:

- `reportCard.json` — standard report cards (Scheduled, Overdue, Total, Recent) using known standard UUIDs from reference bundles
- `reportDashboard.json` — default dashboard with sections
- `groupDashboards.json` — map groups to dashboards
- `groupPrivilege.json` — auto-generate full privilege matrix from subject types × programs × encounter types × privilege types
- `organisationConfig.json` — default settings (languages, filters)

These are derivable deterministically from the spec without LLM involvement.

**Files:** `src/bundle/generator.py` (or split into `src/bundle/reports.py`, `src/bundle/privileges.py`, `src/bundle/org_config.py`)

---

## Summary

| Phase | What | avni-ai Changes | Dify Changes | Impact |
|-------|------|-----------------|--------------|--------|
| **0** | Address levels + operational configs | `generator.py` | None | **Foundational — server expects these** |
| **1** | Auto-derive forms | `generator.py` | None | **Unblocks: upload now reflects config** |
| **2** | `/validate-entities` + `/apply-corrections` | `entity_handlers.py`, `main.py` | Replace 2 code nodes | Business logic in server |
| **3** | `/generate-spec` + `/validate-spec` + `/bundle-to-spec` + `/spec-to-entities` | `spec_handlers.py`, `spec_*.py` | Add spec stage | **Two-stage flow; spec as source of truth** |
| **4** | Spec/Review/Error Agent nodes | Tool registration | Replace ~15 nodes with 3 agents | **Dynamic sub-tasks; simpler workflow** |
| **5** | Forms+fields in entity extractor | `entity_handlers.py` | Extend Entity Extractor | Real field data in bundles |
| **6** | Pydantic schemas | `bundle_models.py`, handlers | None | Fail-fast validation |
| **7** | Reports, privileges, org config | `generator.py` + new modules | None | Production-complete bundles |

## Key Files

| File | Phases |
|------|--------|
| `src/bundle/generator.py` | 0, 1, 7 |
| `src/handlers/entity_handlers.py` | 2, 5 |
| `src/handlers/spec_handlers.py` | 3 |
| `src/bundle/spec_generator.py` | 3 |
| `src/bundle/spec_parser.py` | 3 |
| `src/bundle/spec_validator.py` | 3 |
| `src/schemas/bundle_models.py` | 6 |
| `src/main.py` | 2, 3 |
| `dify/App Configurator [Staging] v2.yml` | 2, 3, 4, 5 |

## Reference

| Source | Used In |
|--------|---------|
| `avni-server/.../BundleZipFileImporter.java` lines 107-144 | All phases: canonical processing order |
| `avni-server/.../SubjectTypeContract.java`, `FormatContract.java` | Phase 0: field structures |
| `avni-skills/srs-bundle-generator/scripts/generate_bundle_v2.js` | Phase 0, 3: STANDARD_UUIDS, NORMAL_RANGES |
| `avni-impl-bundles/reference/` (5 production bundles) | Phase 3, 7: real config variety |
| `avni-impl-bundles/reference/BUNDLE_CONFIG_GUIDE.md` | Phase 3: spec format + bundle docs |

## End-to-end Verification

**New org:**
1. Upload SRS → Entity Extractor → entities JSON
2. `/validate-entities` → structural issues
3. Spec Agent loop: `/generate-spec` → user reviews YAML → corrections → `/validate-spec` → approved
4. `/spec-to-entities` → `/generate-bundle` → ZIP with all config files
5. Review Agent: `/validate-bundle`, `/bundle-to-spec` diff → approved
6. `/upload-bundle` → polling → Avni app shows forms, subject types, programs, address hierarchy, dashboard

**Enhancement flow:**
1. `/api/existing-config` → `/bundle-to-spec` → current YAML spec
2. Spec Agent: user requests change → corrections → re-validate → updated spec
3. `/spec-to-entities` → `/generate-bundle` → Review Agent → upload

**Error recovery:**
1. Upload fails → Error Agent: `/upload-status` error detail → diagnose → `/execute-python` fix → retry
