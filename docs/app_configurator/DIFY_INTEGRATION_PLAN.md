# Plan: SRS Bundle Generator Integration into Avni Prod Dify Assistant

## Context

The goal is to make the Avni Prod Dify assistant (`Avni [Prod] Assistant [Do Not Touch].yml`) capable of generating AVNI bundles directly from uploaded SRS Excel/CSV files.

**Flow**: User uploads SRS Excel/CSV in chat → Dify routes to `FILE_SETUP_BUNDLE` path → avni-ai Python tool invokes the Node.js srs-bundle-generator → full AVNI bundle JSON (concepts, forms, programs, encounterTypes, formMappings) is generated → returned to user.

All files in `srs-bundle-generator/` (docs, JS generators, training data) must be available inside the avni-ai service for execution.

---

## Scope

Two parallel tracks:

### Track 1: avni-ai Python service — new bundle tools

Port/wrap `srs-bundle-generator` logic as Python tools callable from Dify via the existing MCP/function-calling bridge.

### Track 2: Dify Prod YAML — new FILE_SETUP_BUNDLE workflow branch

Add file upload support + new intent routing + new workflow nodes to trigger bundle generation.

---

## Track 1: avni-ai Bundle Tools

### 1.1 Copy srs-bundle-generator into avni-ai

Copy the entire `srs-bundle-generator/` folder into avni-ai:

```
avni-ai/src/tools/bundle/srs_bundle_generator/
  generators/
    bundle.js
    concepts.js
    forms.js
  parsers/
    srs_parser.js
  training_data/
    uuid_registry.json
    concept_patterns.json
    form_patterns.json
    rule_templates.json
    summary.json
    CONSOLIDATED_PATTERNS.md
    SECTOR_KNOWLEDGE.md
    extracted/         ← all 5 org subdirectories
  scripts/
    generate_bundle_v2.js
    generate_pad_bundle.js
    generate_jk_laxmi_bundle.js
    generate_astitva_nourish_bundle.js
    inspect_excel.js
    inspect_excel_full.js
    extract_training_data.js
  validators/
    bundle_validator.js
  BUNDLE_CONFIG_GUIDE.md
  BUNDLE_QUESTIONNAIRE.md
  HOW_TO_GENERATE_BUNDLES.md
  HOW_TO_UNDERSTAND_SRS.md
  LEARNINGS.md
  VisitSchedulingGuidelines.md
  skill.md
  CHANGELOG.md
  package.json
  package-lock.json
```

**Approach**: The Python tool invokes the Node.js generators via `subprocess` (calling `node generate_bundle_v2.js <tempfile> <org_name>`). This reuses the already-tested JS generators without porting to Python.

### 1.2 New file: `avni-ai/src/tools/bundle/__init__.py`

Empty init to make it a package.

### 1.3 New file: `avni-ai/src/tools/bundle/bundle_generator.py`

```python
import asyncio
import base64
import json
import logging
import os
import tempfile
from pathlib import Path

from src.services import tool_registry

logger = logging.getLogger(__name__)

BUNDLE_DIR = Path(__file__).parent / "srs_bundle_generator"


async def generate_bundle_from_srs(
    auth_token: str,
    file_content_base64: str,
    file_name: str,
    org_name: str,
) -> str:
    """
    Generate an AVNI bundle (concepts, forms, programs, encounterTypes, formMappings)
    from an SRS Excel/CSV file. Returns consolidated bundle JSON as a string.

    Args:
        auth_token: Avni auth token (unused for generation, used if uploading)
        file_content_base64: Base64-encoded content of the SRS Excel/CSV file
        file_name: Original filename (e.g. "my_srs.xlsx") to detect format
        org_name: Organization name used for output folder naming
    """
    # 1. Decode base64 → temp file
    file_bytes = base64.b64decode(file_content_base64)
    suffix = Path(file_name).suffix.lower() or ".xlsx"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        with tempfile.TemporaryDirectory() as out_dir:
            # 2. Invoke Node.js generator
            script = str(BUNDLE_DIR / "scripts" / "generate_bundle_v2.js")
            cmd = ["node", script, tmp_path, org_name, out_dir]

            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(BUNDLE_DIR),
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)

            if proc.returncode != 0:
                error = stderr.decode()
                logger.error(f"Bundle generation failed: {error}")
                return f"Bundle generation failed: {error}"

            # 3. Read all output JSON files
            out_path = Path(out_dir)
            bundle = {}
            for json_file in out_path.glob("**/*.json"):
                key = json_file.stem
                with open(json_file) as f:
                    bundle[key] = json.load(f)

            logger.info(f"Bundle generated: {list(bundle.keys())}")
            return json.dumps(bundle, indent=2)

    finally:
        os.unlink(tmp_path)


def register_bundle_tools() -> None:
    tool_registry.register_tool(generate_bundle_from_srs)
```

### 1.4 New handler: `avni-ai/src/handlers/bundle_handler.py`

```python
async def generate_bundle_async_request(request: Request) -> JSONResponse:
    """
    POST /generate-bundle-async
    Body: { file_content: "<base64>", file_name: "srs.xlsx", org_name: "My Org" }
    Header: avni-auth-token
    Returns: { task_id: "..." }
    """
    body = await request.json()
    auth_token = request.headers.get("avni-auth-token", "")
    file_content = body.get("file_content", "")
    file_name = body.get("file_name", "srs.xlsx")
    org_name = body.get("org_name", "org")

    task = task_manager.create_task(
        config_data={"file_content": file_content, "file_name": file_name, "org_name": org_name},
        auth_token=auth_token,
    )

    async def process():
        return await generate_bundle_from_srs(auth_token, file_content, file_name, org_name)

    task_manager.start_background_task(task.task_id, process)
    return JSONResponse({"task_id": task.task_id, "status": "processing"})
```

Status polling reuses the existing `/process-config-status/{task_id}` endpoint — no new endpoint needed.

### 1.5 Update `avni-ai/src/main.py`

```python
from .tools.bundle.bundle_generator import register_bundle_tools
from .handlers.bundle_handler import generate_bundle_async_request

# inside create_server():
register_bundle_tools()

@server.custom_route("/generate-bundle-async", methods=["POST"])
async def generate_bundle_async_endpoint(request: Request):
    return await generate_bundle_async_request(request)
```

---

## Track 2: Dify Prod YAML Changes

File: `/Users/himeshr/IdeaProjects/avni-ai/dify/Avni [Prod] Assistant [Do Not Touch].yml`

### 2.1 Enable file upload (features section, lines ~57–89)

```yaml
features:
  file_upload:
    enabled: true
    allowed_file_extensions:
      - .XLSX
      - .XLS
      - .CSV
    allowed_file_types:
      - document
    allowed_file_upload_methods:
      - local_file
      - remote_url
    number_limits: 1
```

### 2.2 Add `FILE_SETUP_BUNDLE` intent to Orchestrator system prompt (node `1757492907627`)

Add to routing section:

```
**FILE_SETUP_BUNDLE** (SRS-to-Bundle Generation):
- User uploads an Excel/CSV file with an SRS specification
- Message contains phrases like: "generate bundle", "create config from file",
  "upload my SRS", "create forms from this file", "process my spec"
- Any message with a file attachment where intent is Avni bundle/config generation
```

Update output schema to include new value:
```json
{ "service": "RAG|ASSISTANT|FILE_SETUP_BUNDLE|OUT_OF_SCOPE" }
```

### 2.3 Add new case in IF/ELSE routing node (`1757493270484`)

New case: `service = FILE_SETUP_BUNDLE` → routes to new Bundle Code Node (skip LLM, go straight to generation)

### 2.4 New nodes

| Node | Type | Purpose |
|------|------|---------|
| Bundle Code Node | code (Python 3) | Reads `sys.files[0]`, base64-encodes it, POSTs to `/generate-bundle-async`, returns task_id |
| Bundle Loop | loop (max 20 iterations) | Wait 5s → poll `/process-config-status/{task_id}` → check if done |
| Bundle Answer | answer | Presents bundle JSON result (or download instructions) to user |
| Bundle Error Answer | answer | Error message if generation fails |

**Bundle Code Node** (Python 3):

```python
import base64, httpx, json

file = sys.files[0]
file_content_b64 = base64.b64encode(file.read()).decode()

resp = httpx.post(
    f"{avni_ai_server_url}/generate-bundle-async",
    json={"file_content": file_content_b64, "file_name": file.filename, "org_name": org_name},
    headers={"avni-auth-token": avni_auth_token},
    timeout=30,
)
result = resp.json()
return {"task_id": result.get("task_id", ""), "status": result.get("status", "")}
```

### 2.5 Update RAG LLM system prompt (node `1757495664531`)

Add to capabilities list:
```
3. Generating AVNI configuration bundles (concepts, forms, programs, rules) from SRS Excel/CSV files
```

---

## Critical Files

| File | Change |
|------|--------|
| `avni-ai/src/tools/bundle/srs_bundle_generator/` | **New** — copy of full srs-bundle-generator folder |
| `avni-ai/src/tools/bundle/__init__.py` | **New** — empty package init |
| `avni-ai/src/tools/bundle/bundle_generator.py` | **New** — Python wrapper tool |
| `avni-ai/src/handlers/bundle_handler.py` | **New** — async bundle request handler |
| `avni-ai/src/main.py` | **Modified** — register bundle tools + new route |
| `avni-ai/dify/Avni [Prod] Assistant [Do Not Touch].yml` | **Modified** — file upload, routing, new nodes |

---

## Implementation Order

1. `cp -r srs-bundle-generator/ avni-ai/src/tools/bundle/srs_bundle_generator/`
2. Create `avni-ai/src/tools/bundle/__init__.py`
3. Create `avni-ai/src/tools/bundle/bundle_generator.py`
4. Create `avni-ai/src/handlers/bundle_handler.py`
5. Update `avni-ai/src/main.py`
6. Update `avni-ai/dify/Avni [Prod] Assistant [Do Not Touch].yml`

---

## Verification

1. `cd avni-ai && python -m src.main` → confirm `/generate-bundle-async` endpoint appears
2. `curl -X POST .../generate-bundle-async -F file=@test_srs.xlsx ...` → verify task_id returned
3. Poll `/process-config-status/{task_id}` → verify bundle JSON in result
4. Import updated Dify YAML into **Staging** first, test full file-upload chat flow
5. Verify orchestrator routes file+bundle-intent to `FILE_SETUP_BUNDLE`
6. Once verified on Staging, apply same changes to Prod YAML
