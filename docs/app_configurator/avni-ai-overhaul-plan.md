# avni-ai Overhaul: Remove OpenAI, Adopt Bundle-First + Playground Architecture

Overhaul avni-ai to remove the internal OpenAI LLM loop, replace entity-type CRUD with bundle upload, keep location/catchment/user tools as thin HTTP endpoints, and add the Python Playground — all orchestrated by Dify.

---

## 1. Current State (What Exists)

### LLM Orchestration Layer (TO BE REMOVED)
| File | Lines | What It Does |
|------|-------|-------------|
| `clients/openai_client.py` | 300 | `OpenAIResponsesClient` — async OpenAI function-calling loop |
| `services/config_processor.py` | 368 | `ConfigProcessor` — 15-iteration GPT-4o loop that decides tool order, resolves IDs, tracks state |
| `services/config_llm_helper.py` | 711 | Massive system prompt teaching GPT-4o CRUD sequencing, ID resolution, parent-child deps |
| `utils/env.py` | 32 | `OPENAI_API_KEY` dependency |
| `main.py:92-96` | 5 | Crashes on startup if no `OPENAI_API_KEY` |

### Existing Tools (registered via `ToolRegistry` for OpenAI function-calling)

**Entity Config Tools (OBSOLETED by bundle upload):**
| Tool | File | Replaced By |
|------|------|-------------|
| `create/update/delete_subject_type` | `tools/app_designer/subject_types.py` | `subjectTypes.json` + `operationalSubjectTypes.json` in bundle |
| `create/update/delete_program` | `tools/app_designer/programs.py` | `programs.json` + `operationalPrograms.json` in bundle |
| `create/update/delete_encounter_type` | `tools/app_designer/encounters.py` | `encounterTypes.json` + `operationalEncounterTypes.json` in bundle |

**Location/Admin Tools (KEEP as HTTP endpoints):**
| Tool | File | Why Keep |
|------|------|----------|
| `create/update/delete_location_type` | `tools/admin/addressleveltypes.py` | Also in bundle (`addressLevelTypes.json`) but needed for incremental changes |
| `get/create/update/delete_location` | `tools/admin/locations.py` | Actual data (geographic places), not just config templates |
| `get/create/update/delete_catchment` | `tools/admin/catchments.py` | Actual data (field worker assignments) |
| `find/update_user` | `tools/admin/users.py` | User management |
| `delete_implementation` | `tools/implementation/implementations.py` | App data deletion |

**Supporting Services (KEEP):**
| Service | File | Role |
|---------|------|------|
| `AvniClient` | `clients/avni_client.py` | HTTP client for Avni API — used by all tools |
| `ConfigFetcher` | `services/avni/config_fetcher.py` | Fetch existing config — useful for bundle generation too |
| `FormMappingProcessor` | `services/avni/form_mapping_processor.py` | Enrich config with form mappings |
| `TaskManager` | `services/task_manager.py` | Async task tracking — reuse for upload |
| `ToolRegistry` | `services/tool_registry.py` | Remove OpenAI tool format, repurpose or remove |

---

## 2. Target State

### Architecture
```
Dify (Single Orchestrator)
  │
  ├── LLM nodes: entity extraction, config enrichment, error handling
  ├── Code nodes: HTTP calls to avni-ai endpoints
  │
  ▼
avni-ai (Stateless Tool Service — NO LLM)
  │
  ├── Bundle endpoints:     /generate-bundle, /validate-bundle, /upload-bundle, /upload-status
  ├── Playground:           /execute-python (host subprocess, conversation silos)
  ├── Location/Admin APIs:  /api/location-types, /api/locations, /api/catchments, /api/users
  ├── Implementation:       /api/implementation/delete
  ├── Config Fetch:         /api/existing-config
  └── Health:               /health
```

### What Gets Deleted
| Item | Reason |
|------|--------|
| `clients/openai_client.py` | No more internal LLM calls |
| `services/config_processor.py` | Entire LLM orchestration loop → Dify |
| `services/config_llm_helper.py` | 711-line GPT prompt → becomes Dify LLM node system prompts |
| `tools/app_designer/subject_types.py` | → `subjectTypes.json` in bundle |
| `tools/app_designer/programs.py` | → `programs.json` in bundle |
| `tools/app_designer/encounters.py` | → `encounterTypes.json` in bundle |
| `schemas/subject_type_contract.py` | No longer needed (bundle JSON replaces contracts) |
| `schemas/program_contract.py` | Same |
| `schemas/encounter_type_contract.py` | Same |
| `schemas/crud_operations_schema.json` | LLM CRUD schema → deleted |
| `services/tool_registry.py` | OpenAI function-call registry → deleted (tools become HTTP endpoints) |
| `OPENAI_API_KEY` requirement | No longer needed — avni-ai has zero LLM dependencies |
| `handlers/request_handlers.py` | `/process-config-async` and `/process-config-status` → replaced by new endpoints |

### What Gets Kept (refactored to HTTP endpoints)
| Current Tool | New HTTP Endpoint | Notes |
|-------------|-------------------|-------|
| `create_location_type` | `POST /api/location-types` | Keep contract validation via Pydantic |
| `update_location_type` | `PUT /api/location-types/{id}` | |
| `delete_location_type` | `DELETE /api/location-types/{id}` | |
| `get_locations` | `GET /api/locations` | |
| `create_location` | `POST /api/locations` | |
| `update_location` | `PUT /api/locations/{id}` | |
| `delete_location` | `DELETE /api/locations/{id}` | |
| `get_catchments` | `GET /api/catchments` | |
| `create_catchment` | `POST /api/catchments` | |
| `update_catchment` | `PUT /api/catchments/{id}` | |
| `delete_catchment` | `DELETE /api/catchments/{id}` | |
| `find_user` | `GET /api/users?name={name}` | |
| `update_user` | `PUT /api/users/{id}` | |
| `delete_implementation` | `DELETE /api/implementation` | Query params: deleteMetadata, deleteAdminConfig |
| `ConfigFetcher.fetch_complete_config` | `GET /api/existing-config` | Returns all entity types, locations, etc. |

### What Gets Added (from v4 plan)
| New Endpoint | Purpose |
|-------------|---------|
| `POST /generate-bundle` | Deterministic bundle generation from enriched config |
| `POST /validate-bundle` | Bundle validation → structured errors |
| `POST /upload-bundle` | Async bundle upload to Avni server |
| `GET /upload-status/{task_id}` | Poll upload progress |
| `POST /execute-python` | Python Playground — host subprocess with conversation silos |

---

## 3. Key Insight: Bundle Upload Replaces Entity CRUD

The existing flow does this:
```
Dify → /process-config-async → ConfigProcessor (GPT-4o loop, 15 iterations)
  → GPT decides: call create_subject_type, wait, call create_program, wait...
  → Each tool = individual Avni API call
  → GPT resolves IDs between calls, handles parent-child sequencing
```

The new flow does this:
```
Dify LLM → enriched_config JSON → /generate-bundle
  → Deterministic Python generates subjectTypes.json, programs.json, encounterTypes.json, etc.
  → All UUID references resolved deterministically
  → Parent-child ordering handled by canonical ZIP order
  → Single upload via /upload-bundle
```

**Why this is better:**
- No LLM needed for ID resolution or sequencing — it's deterministic
- Bundle upload is atomic — all-or-nothing, no partial state
- Existing Avni server already handles bundle import with proper ordering
- Bundle format is the source of truth for all Avni implementations

**Locations/catchments/users stay as API calls** because:
- They involve actual data (geographic places, user assignments), not just config templates
- They may change incrementally during implementation (add new locations post-setup)
- The playground (`/execute-python`) handles ad-hoc corrections for these

---

## 4. Module Structure After Overhaul

```
src/
├── main.py                              # REWRITE — no OPENAI_API_KEY, new route registration
├── clients/
│   ├── __init__.py
│   └── avni_client.py                   # KEEP — HTTP client for Avni API
├── handlers/
│   ├── __init__.py
│   ├── bundle_handlers.py               # NEW — /generate-bundle, /validate-bundle
│   ├── upload_handlers.py               # NEW — /upload-bundle, /upload-status
│   ├── sandbox_handlers.py              # NEW — /execute-python
│   ├── admin_handlers.py                # NEW — /api/location-types, /api/locations, etc.
│   └── config_handlers.py               # NEW — /api/existing-config
├── bundle/                              # NEW — deterministic bundle generator
│   ├── __init__.py
│   ├── generator.py
│   ├── concepts.py
│   ├── forms.py
│   ├── report_cards.py
│   ├── validators.py
│   ├── uuid_utils.py
│   ├── zip_bundle.py
│   ├── models.py
│   └── defaults.py
├── playground/                           # NEW — Python Playground (lightweight)
│   ├── __init__.py
│   └── executor.py                     # subprocess runner + silo manager
├── services/
│   ├── __init__.py
│   ├── task_manager.py                  # KEEP — async task tracking
│   └── avni/
│       ├── config_fetcher.py            # KEEP — fetch existing config
│       └── form_mapping_processor.py    # KEEP — form mapping enrichment
├── schemas/
│   ├── __init__.py
│   ├── address_level_type_contract.py   # KEEP — used by admin endpoints
│   ├── location_contract.py             # KEEP
│   ├── catchment_contract.py            # KEEP
│   ├── user_contract.py                 # KEEP
│   ├── implementation_contract.py       # KEEP
│   ├── field_names.py                   # KEEP (trim entity type fields)
│   └── bundle_models.py                 # NEW — Pydantic models for bundle I/O
├── tools/
│   └── admin/                           # KEEP — refactor to be called by handlers
│       ├── addressleveltypes.py         # KEEP (remove register_*_tools, just export functions)
│       ├── locations.py                 # KEEP
│       ├── catchments.py                # KEEP
│       └── users.py                     # KEEP
├── utils/
│   ├── __init__.py
│   ├── env.py                           # SIMPLIFY — remove OPENAI_API_KEY
│   ├── result_utils.py                  # KEEP
│   └── session_context.py               # KEEP (may simplify)
└── training_data/                       # NEW — from srs-bundle-generator
    ├── uuid_registry.json
    ├── concept_patterns.json
    ├── form_patterns.json
    └── rule_templates.json
```

### Files DELETED
```
DELETED: clients/openai_client.py
DELETED: services/config_processor.py
DELETED: services/config_llm_helper.py
DELETED: services/tool_registry.py
DELETED: tools/app_designer/subject_types.py
DELETED: tools/app_designer/programs.py
DELETED: tools/app_designer/encounters.py
DELETED: tools/app_designer/ (entire directory)
DELETED: tools/implementation/implementations.py → move to admin_handlers
DELETED: schemas/subject_type_contract.py
DELETED: schemas/program_contract.py
DELETED: schemas/encounter_type_contract.py
DELETED: schemas/crud_operations_schema.json
DELETED: handlers/request_handlers.py
```

---

## 5. main.py Rewrite

Before:
```python
# Crashes without OPENAI_API_KEY
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is required")

# Registers tools for OpenAI function-calling
register_subject_type_tools()
register_program_tools()
register_encounter_tools()

# Routes through ConfigProcessor (LLM loop)
@server.custom_route("/process-config-async", methods=["POST"])
@server.custom_route("/process-config-status/{task_id}", methods=["GET"])
```

After:
```python
# No OPENAI_API_KEY needed — avni-ai is LLM-free

# Register HTTP routes directly (no ToolRegistry)
# Bundle endpoints
@server.custom_route("/generate-bundle", methods=["POST"])
@server.custom_route("/validate-bundle", methods=["POST"])
@server.custom_route("/upload-bundle", methods=["POST"])
@server.custom_route("/upload-status/{task_id}", methods=["GET"])

# Python Playground
@server.custom_route("/execute-python", methods=["POST"])

# Admin/Location endpoints (thin wrappers around existing tool functions)
@server.custom_route("/api/location-types", methods=["POST"])
@server.custom_route("/api/location-types/{id}", methods=["PUT", "DELETE"])
@server.custom_route("/api/locations", methods=["GET", "POST"])
@server.custom_route("/api/locations/{id}", methods=["PUT", "DELETE"])
@server.custom_route("/api/catchments", methods=["GET", "POST"])
@server.custom_route("/api/catchments/{id}", methods=["PUT", "DELETE"])
@server.custom_route("/api/users", methods=["GET"])
@server.custom_route("/api/users/{id}", methods=["PUT"])
@server.custom_route("/api/implementation", methods=["DELETE"])

# Config fetch (for Dify or playground to use)
@server.custom_route("/api/existing-config", methods=["GET"])

# Health
@server.custom_route("/health", methods=["GET"])
```

---

## 6. Auth Token Handling (Unchanged)

All endpoints extract `avni-auth-token` from the HTTP request header:
```python
auth_token = request.headers.get("avni-auth-token")
```

- Dify Code nodes pass it as an HTTP header
- avni-ai forwards it to Avni API as `AUTH-TOKEN` header (via `AvniClient`)
- For `/execute-python`: injected as `AVNI_AUTH_TOKEN` env var in subprocess
- **LLM nodes in Dify never see the token**

---

## 7. Dify Flow Changes

### Current Dify Flow (ASSISTANT branch → `/process-config-async`)
```
User says "create subject types, programs..." 
  → Entities Corrector LLM → generates config JSON
  → Code node: POST /process-config-async {config}
  → Poll loop: GET /process-config-status/{task_id}
  → ConfigProcessor (GPT-4o, 15 iterations) decides tool calls
  → Return result
```

### New Dify Flow (ASSISTANT branch → bundle OR individual APIs)
```
User says "create subject types, programs..."
  → Config LLM → generates enriched_config JSON
  → Code node: POST /generate-bundle {enriched_config}
  → IF validation errors → Error Handler LLM → POST /execute-python {fix_script}
  → Code node: POST /upload-bundle {bundle_zip}
  → Poll: GET /upload-status/{task_id}

User says "add location Maharashtra under State"
  → Config LLM → generates API call params
  → Code node: POST /api/locations {name, level, type, parents}

User says "delete all app data"
  → Code node: DELETE /api/implementation?deleteMetadata=true&deleteAdminConfig=true
```

---

## 8. Playground Design (Lightweight — No Docker)

Instead of spinning up Docker containers per execution, the playground uses **host subprocesses with conversation-scoped temp directories** ("silos").

### Architecture
```
/execute-python request (conversation_id, code, input_files?, timeout?)
       │
       ▼
  playground/executor.py
       │
       ├── 1. Resolve or create silo dir: /tmp/avni-playground/{conversation_id}/
       ├── 2. Write script.py + input files into silo dir
       ├── 3. Run: subprocess.run(["python", "script.py"], cwd=silo_dir,
       │        env={AVNI_AUTH_TOKEN, AVNI_BASE_URL}, timeout=30s)
       ├── 4. Capture stdout, stderr, exit_code
       ├── 5. Collect output files from silo dir
       └── 6. Return {stdout, stderr, exit_code, output_files}
```

### Conversation Silos
- Each Dify conversation gets a directory: `/tmp/avni-playground/{conversation_id}/`
- Files from previous `/execute-python` calls in the same conversation **persist** — the LLM can build on previous outputs (e.g., generate a bundle, then fix it)
- Silo directory is reused across calls with the same `conversation_id`
- **Cleanup:** A periodic task (e.g., every 6 hours) deletes silos older than a configurable TTL (default: 24h)

### Endpoint Contract
```
POST /execute-python
Headers: avni-auth-token: <token>

Body:
{
  "conversation_id": "conv-abc-123",       // required — identifies the silo
  "code": "import json\nprint('hello')",   // required — Python script to execute
  "input_files": {                          // optional — files to write before execution
    "bundle.zip": "<base64>",
    "config.json": "{...}"
  },
  "timeout": 30                            // optional — seconds, default 30, max 120
}

Response:
{
  "success": true,
  "exit_code": 0,
  "stdout": "hello\n",
  "stderr": "",
  "output_files": {                        // files created/modified in silo dir
    "fixed_bundle.zip": "<base64>",
    "result.json": "{...}"
  },
  "silo_files": ["script.py", "bundle.zip", "fixed_bundle.zip", "result.json"]
}
```

### Security Model (Simplified)
- **Auth token:** Extracted from HTTP header, injected as `AVNI_AUTH_TOKEN` env var into subprocess. LLM writes `os.environ['AVNI_AUTH_TOKEN']` but never sees the value.
- **Env vars:** Only `AVNI_AUTH_TOKEN` and `AVNI_BASE_URL` are passed. No other host env vars leak.
- **Timeout:** Hard limit via `subprocess.run(timeout=...)`. Default 30s, max 120s.
- **Resource limits:** `ulimit` or `resource` module to cap memory (256MB) and prevent fork bombs.
- **No network filtering needed:** The subprocess runs on the host but only has Avni API credentials. No arbitrary network access concern since this is an internal tool service, not user-facing.
- **Filesystem:** Scripts can only write within their silo dir (`cwd` is set to silo dir).

### Pre-installed Libraries
Scripts execute using the avni-ai virtualenv, which includes:
- `requests`, `httpx` — HTTP calls to Avni API
- `openpyxl`, `pandas` — spreadsheet/data manipulation
- `jsonschema` — JSON validation
- `pyyaml` — YAML parsing
- `uuid`, `hashlib`, `json`, `os`, `zipfile` — stdlib

### Module: `playground/executor.py`
```python
# ~80 lines total
class PlaygroundExecutor:
    def __init__(self, base_dir="/tmp/avni-playground", default_timeout=30, max_timeout=120, silo_ttl_hours=24):
        ...

    def get_or_create_silo(self, conversation_id: str) -> Path:
        """Return silo dir, create if missing."""

    def execute(self, conversation_id: str, code: str,
                input_files: dict = None, timeout: int = 30,
                auth_token: str = None, avni_base_url: str = None) -> dict:
        """Write files, run subprocess, collect output."""

    def cleanup_stale_silos(self):
        """Delete silos older than TTL. Called by periodic task."""

    def list_silo_files(self, conversation_id: str) -> list:
        """List files in a conversation's silo."""
```

### Why This Is Sufficient
- **No Docker overhead:** Subprocess starts in <50ms vs ~2s for Docker container
- **Conversation continuity:** Silo persistence lets the LLM iterate on files across multiple calls
- **Simple cleanup:** `shutil.rmtree` on stale dirs, no container lifecycle management
- **Same security as any internal microservice:** avni-ai is not exposed to end users, only Dify
- **Pre-installed libs:** No pip install at runtime, everything available in the venv

---

## 9. Implementation Phases

### Phase 1: Remove LLM Layer + Expose Admin Endpoints
1. Delete `openai_client.py`, `config_processor.py`, `config_llm_helper.py`, `tool_registry.py`
2. Delete `tools/app_designer/` (subject_types, programs, encounters)
3. Delete corresponding schemas (subject_type_contract, program_contract, encounter_type_contract, crud_operations_schema)
4. Delete `handlers/request_handlers.py` (process-config-async)
5. Remove `OPENAI_API_KEY` requirement from `main.py` and `env.py`
6. Create `handlers/admin_handlers.py` — thin HTTP wrappers around location/catchment/user/implementation tools
7. Create `handlers/config_handlers.py` — expose `GET /api/existing-config`
8. Rewrite `main.py` — register new routes, remove old registrations
9. Remove `register_*_tools()` calls from tool files, keep functions as importable utilities

### Phase 2: Python Playground
(Host subprocess with conversation silos — see Playground Design section below)

### Phase 3: Bundle Generator
(From v4 plan — `/generate-bundle`, `/validate-bundle` endpoints)

### Phase 4: Bundle Upload
(From v4 plan — `/upload-bundle`, `/upload-status` endpoints)

### Phase 5: Dify Flow Integration
- Update Dify flow to use new endpoints
- Remove `/process-config-async` code nodes
- Add bundle generation + validation + playground error correction loop

---

## 9. Migration Safety

### Backward Compatibility
- `/process-config-async` and `/process-config-status` are **deleted** (breaking change)
- The Dify flow that calls these must be updated simultaneously
- Admin endpoints are **new** — no backward compatibility concern

### Risk Mitigation
- Phase 1 can be tested independently (admin endpoints work without bundle/playground)
- `AvniClient`, `ConfigFetcher`, `TaskManager` are untouched — proven code stays
- Location/catchment/user tool functions are kept as-is, just wrapped in HTTP handlers

### OpenAI Dependency Removal Checklist
- [ ] `openai` package removed from `requirements.txt` / `pyproject.toml`
- [ ] `OPENAI_API_KEY` removed from env.py, main.py, .env files
- [ ] No import of `openai` anywhere in codebase
- [ ] Server starts without any LLM API keys
