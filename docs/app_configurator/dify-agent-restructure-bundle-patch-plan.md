# Fix Dify YAML: UUIDs, Agent Restructure, Stale Removal + Bundle Patch Flow

Three workstreams: (A) fix all non-UUID IDs in Dify YAML, (B) restructure agent nodes & remove stale correction cluster, (C) redesign bundle flow to download→patch→rezip→upload instead of generating from scratch.

---

## Workstream A: Fix Non-UUID IDs (Dify YAML)

### A1. Node IDs → UUIDv4

| Current ID | Node Title | Type | Action |
|---|---|---|---|
| `spec-agent-node` | Spec Agent | agent | Replace |
| `review-agent-node` | Review Agent | agent | Replace |
| `error-agent-node` | Error Agent | agent | Replace |
| `fs-check-processed` | Already Processed? | if-else | Replace |
| `fs-save-jsonl` | Save entities_jsonl | assigner | Replace |
| `fs-ask-corrections` | Ask Corrections | answer | **Remove** (stale) |
| `fs-timeout` | Timeout | answer | Replace |
| `generate-bundle-req` | Generate Bundle | http-request | Replace |
| `upload-bundle-req` | Upload Bundle | http-request | Replace |
| `setup-guidance-answer` | Program Setup Guidance | answer | Replace |
| `break-upload-loop` | Break Upload Loop | assigner | Replace |
| `upload-done-answer-loop` | Upload Done | answer | Replace |
| `upload-progress-answer` | Upload Progress | answer | Replace |

Update all references: edges `source`/`target`, `parentId`, variable selectors, body templates.

### A2. Edge IDs → UUIDv4

| Current ID | Route |
|---|---|
| `spec-agent-to-generate-bundle` | Spec Agent → Generate Bundle |
| `review-agent-to-upload` | Review Agent → Upload Bundle |
| `save-task-to-error-agent` | Save Task ID → Error Agent |
| `error-agent-to-loop` | Error Agent → Polling Loop |

### A3. Inline IDs → UUIDv4

Prompt template IDs and body data IDs:
- `corrector-system`, `apply-corrections-body` (stale nodes — removed with node)
- `bundle-body`, `upload-body`, `correction-summary-system`, `summary-system`, `entity-extractor-system`

---

## Workstream B: Agent Restructure + Stale Removal

### B1. Restructure 3 agent nodes

Rewrite from current invalid schema to match reference `research agent process flow .yml`:

```yaml
# Current (invalid)              →  Target (valid)
agent_strategy: function_call    →  agent_strategy_name: function_calling
max_iterations: 5                →  agent_strategy_label: FunctionCalling
model: { ... }                   →  agent_strategy_provider_name: langgenius/agent/agent
prompt: "..."                    →  agent_parameters:
tools: [identity/parameters]     →    instruction/maximum_iterations/model/query/tools
                                 →  plugin_unique_identifier: langgenius/agent:0.0.14@...
                                 →  tool_node_version: '2'
```

**Auth cleanup:** Remove `avni-auth-token` references from all 3 agent prompts. Their tools are all deterministic no-auth endpoints:
- Spec Agent: `/validate-entities`, `/apply-entity-corrections`, `/generate-spec`, `/validate-spec`, `/bundle-to-spec`
- Review Agent: `/validate-bundle`, `/bundle-to-spec`
- Error Agent: `/upload-status/{task_id}`, `/validate-bundle`

Auth is only needed in HTTP-request nodes (`upload-bundle-req`, `generate-bundle-req`) which pass it via headers.

### B2. Remove stale correction cluster

**Nodes to remove** (replaced by Spec Agent):

| Node ID | Title |
|---|---|
| `fs-ask-corrections` | Ask Corrections |
| `1773981975918` | Entities Corrector LLM |
| `1773982043351` | Entities Corrector HTTP |
| `1773984373385` | Update entities_jsonl assigner |
| `17748473384490` | Correction Summary LLM |

**Keep** `1773909436902` (Summary Answer) + `17748474036620` (Summary LLM) — used in initial extraction path.

**Edges to remove:**
- `7e25197b` → fs-check-processed → Corrector LLM (rewire to Spec Agent)
- `9fee834f` → Corrector LLM → Corrector HTTP
- `50668f44` → Corrector HTTP → Update assigner
- `4cfba0f9` → Update assigner → Correction Summary LLM
- `fd7dec48` → Correction Summary LLM → Summary Answer

**Rewire:** `fs-check-processed` case-true → Spec Agent (new edge)

---

## Workstream C: Bundle Patch Flow (Download → Patch → Rezip → Upload)

### C1. New backend endpoint: `POST /patch-bundle`

**Current flow** (generate from scratch):
```
entities → /generate-bundle → brand-new ZIP → /upload-bundle → Avni
```

**New flow** (fractional changes to existing bundle):
```
/download-bundle-b64 (auth) → existing ZIP
spec_yaml + existing ZIP → /patch-bundle → patched ZIP → /upload-bundle (auth) → Avni
```

**`/patch-bundle` handler logic:**
1. Accept `{ "existing_bundle_b64": "...", "spec_yaml": "..." }` (no auth needed — deterministic)
2. Unzip existing bundle into memory (dict of filename → JSON content)
3. Parse spec YAML to determine what changed
4. For each changed entity type, merge/overwrite the relevant JSON file:
   - `subjectTypes.json`, `programs.json`, `encounterTypes.json`
   - `concepts.json`, `forms/*.json`, `formMappings.json`
   - `operationalSubjectTypes.json`, `operationalPrograms.json`, `operationalEncounterTypes.json`
   - `organisationConfig.json`, `groups.json`, `groupPrivilege.json`
   - `reportCard.json`, `reportDashboard.json`, `groupDashboards.json`
5. Re-zip using canonical order from `zip_bundle.js` (`CANONICAL_ORDER`)
6. Return `{ "patched_bundle_b64": "..." }`

### C2. Python port of canonical ZIP ordering

Port the `createOrderedZip()` logic from `srs-bundle-generator/scripts/zip_bundle.js` to Python:
- Same `CANONICAL_ORDER` array
- Same `__FORMS__` expansion for `forms/*.json`
- Use Python's `zlib` for deflate, manual ZIP construction to preserve insertion order (standard `zipfile` module may reorder)

### C3. Dify YAML flow changes

Add new nodes to the Dify workflow:

1. **Download Existing Bundle** (http-request, needs auth) — `GET /download-bundle-b64` with `avni-auth-token` header
2. **Patch Bundle** (http-request, no auth) — `POST /patch-bundle` with existing bundle + spec_yaml
3. Update `generate-bundle-req` → becomes `patch-bundle-req`
4. Add `existing_bundle_b64` conversation variable

### C4. TaskManager validation ✅

Already validated — the in-memory TaskManager is sound:
- 24-hour TTL for completed/failed tasks
- Periodic cleanup every 12 hours
- Cross-conversation safe (singleton, tasks keyed by UUID)
- `/upload-status/{task_id}` is local lookup, no auth needed
- `config_data` stores `zip_bytes` temporarily, cleaned up by TTL

---

## Execution Order

1. **A1-A3** — Mechanical UUID replacement (all at once)
2. **B2** — Remove stale nodes + edges
3. **B1** — Restructure 3 agent nodes
4. **C2** — Port canonical ZIP ordering to Python
5. **C1** — Implement `/patch-bundle` endpoint
6. **C3** — Update Dify YAML flow for download→patch→upload
7. **Verify** — Scan for dangling references, validate YAML
