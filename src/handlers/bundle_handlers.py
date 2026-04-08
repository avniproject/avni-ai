"""
HTTP handlers for bundle generation, validation, download, and patching.
Endpoints: POST /generate-bundle, POST /validate-bundle, GET /download-bundle,
           GET /download-bundle-b64, POST /patch-bundle
"""

from __future__ import annotations

import base64
import json
import logging
import time

import httpx
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ..bundle.canonical_zip import patch_bundle_zip, unzip_to_map
from ..bundle.generator import BundleGenerator
from ..bundle.spec_parser import spec_to_entities
from ..bundle.validators import BundleValidator
from ..utils.env import AVNI_BASE_URL

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory bundle store keyed by conversation_id (TTL = 6 hours)
# Allows agent tool calls to pass only conversation_id instead of bundle_zip_b64,
# keeping large binary payloads off the LLM context entirely.
# ---------------------------------------------------------------------------
_BUNDLE_STORE_TTL = 6 * 3600  # seconds


class _BundleStore:
    def __init__(self) -> None:
        self._store: dict[str, tuple[dict, float]] = {}  # id -> (data, expiry)

    def put(self, conversation_id: str, zip_b64: str, bundle_dict: dict) -> None:
        self._store[conversation_id] = (
            {"zip_b64": zip_b64, "bundle": bundle_dict},
            time.time() + _BUNDLE_STORE_TTL,
        )

    def get(self, conversation_id: str) -> dict | None:
        entry = self._store.get(conversation_id)
        if entry is None:
            return None
        data, expiry = entry
        if time.time() > expiry:
            del self._store[conversation_id]
            return None
        return data

    def cleanup(self) -> int:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)


_bundle_store = _BundleStore()


def get_bundle_store() -> _BundleStore:
    """Return the global bundle store (used by upload_handlers)."""
    return _bundle_store


async def handle_generate_bundle(request: Request) -> JSONResponse:
    """
    POST /generate-bundle
    Body: { "entities": {...}, "org_name": "MyOrg", "conversation_id": "..." }

    When conversation_id is provided: stores bundle server-side in _bundle_store
    and returns summary ONLY (no bundle_zip_b64 in response — keeps LLM context small).

    Without conversation_id: legacy behaviour, returns full bundle_zip_b64.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    entities = body.get("entities")
    if not entities:
        return JSONResponse(
            {"error": "Missing 'entities' in request body"}, status_code=400
        )

    # Normalise snake_case keys (sent by Dify) to camelCase (used internally)
    _key_map = {
        "subject_types": "subjectTypes",
        "encounter_types": "encounterTypes",
        "address_levels": "addressLevels",
    }
    entities = {_key_map.get(k, k): v for k, v in entities.items()}

    org_name = body.get("org_name", "Unknown Organization")
    conversation_id = body.get("conversation_id")

    try:
        generator = BundleGenerator(org_name)
        result = generator.generate(entities)

        # Generate ZIP bytes
        zip_bytes = generator.to_zip_bytes()
        zip_b64 = base64.b64encode(zip_bytes).decode("ascii")

        summary = {
            "concepts": len(result["bundle"]["concepts"]),
            "forms": len(result["bundle"]["forms"]),
            "subjectTypes": len(result["bundle"]["subjectTypes"]),
            "programs": len(result["bundle"]["programs"]),
            "encounterTypes": len(result["bundle"]["encounterTypes"]),
            "formMappings": len(result["bundle"]["formMappings"]),
            "groups": len(result["bundle"]["groups"]),
        }

        if conversation_id:
            # Store bundle server-side; do NOT return bundle_zip_b64 to LLM
            _bundle_store.put(conversation_id, zip_b64, result["bundle"])
            logger.info(
                "generate-bundle: stored bundle for conversation_id=%s zip_b64_len=%d",
                conversation_id,
                len(zip_b64),
            )
            return JSONResponse(
                {
                    "success": True,
                    "stored": True,
                    "validation": result["validation"],
                    "confidence": result["confidence"],
                    "summary": summary,
                }
            )

        # Legacy: return full bundle_zip_b64 when no conversation_id
        return JSONResponse(
            {
                "success": True,
                "bundle": result["bundle"],
                "validation": result["validation"],
                "confidence": result["confidence"],
                "bundle_zip_b64": zip_b64,
                "summary": summary,
            }
        )
    except Exception as e:
        logger.exception("Bundle generation failed")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


async def handle_validate_bundle(request: Request) -> JSONResponse:
    """
    POST /validate-bundle
    Body: { "bundle": {...} } OR { "bundle_zip_b64": "..." } OR { "conversation_id": "..." }
    Returns: { "valid": bool, "errors": [...], "warnings": [...] }

    When conversation_id is provided: fetches bundle from _bundle_store (no LLM payload).
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    bundle = body.get("bundle")

    # Prefer conversation_id lookup (server-side store, nothing large on LLM)
    if not bundle:
        conversation_id = body.get("conversation_id")
        if conversation_id:
            stored = _bundle_store.get(conversation_id)
            if stored:
                bundle = stored["bundle"]
                logger.info(
                    "validate-bundle: resolved bundle from store for conversation_id=%s",
                    conversation_id,
                )
            else:
                return JSONResponse(
                    {
                        "error": f"No stored bundle for conversation_id={conversation_id!r}. Call generate_bundle first."
                    },
                    status_code=404,
                )

    if not bundle:
        b64 = body.get("bundle_zip_b64", "")
        if b64:
            try:
                zip_bytes = base64.b64decode(b64)
                file_map = unzip_to_map(zip_bytes)
                bundle = {}
                forms = []
                for fname, fbytes in file_map.items():
                    try:
                        parsed = json.loads(fbytes)
                    except Exception:
                        continue
                    if fname.startswith("forms/"):
                        forms.append(parsed)
                    else:
                        key = fname.replace(".json", "")
                        bundle[key] = parsed
                if forms:
                    bundle["forms"] = forms
            except Exception as e:
                return JSONResponse(
                    {"error": f"Failed to decode bundle_zip_b64: {e}"}, status_code=400
                )
    if not bundle:
        return JSONResponse(
            {"error": "Missing 'bundle' or 'bundle_zip_b64' in request body"},
            status_code=400,
        )

    try:
        validator = BundleValidator(bundle)
        result = validator.validate()
        return JSONResponse(result)
    except Exception as e:
        logger.exception("Bundle validation failed")
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_download_bundle(request: Request) -> Response:
    """
    GET /download-bundle?includeLocations=true|false
    Headers: avni-auth-token (or conversation_id query param)
    Proxies Avni server's /implementation/export/{includeLocations} endpoint.
    Returns the raw ZIP bytes with appropriate content-type.
    """
    from ..auth_store import resolve_auth_token

    auth_token = resolve_auth_token(request)
    if not auth_token:
        return JSONResponse(
            {
                "error": "Missing auth: provide avni-auth-token header or conversation_id"
            },
            status_code=401,
        )

    include_locations = (
        request.query_params.get("includeLocations", "false").lower() == "true"
    )
    base_url = request.query_params.get("baseUrl", AVNI_BASE_URL)

    url = (
        f"{base_url.rstrip('/')}/implementation/export/{str(include_locations).lower()}"
    )

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.get(
                url,
                headers={
                    "AUTH-TOKEN": auth_token,
                    "Accept": "application/octet-stream",
                },
            )
            response.raise_for_status()

        # Return raw ZIP bytes
        return Response(
            content=response.content,
            status_code=200,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename=bundle_{'with' if include_locations else 'without'}_locations.zip",
                "Content-Length": str(len(response.content)),
            },
        )
    except httpx.HTTPStatusError as e:
        logger.error(
            f"Avni server returned {e.response.status_code}: {e.response.text}"
        )
        return JSONResponse(
            {
                "error": f"Avni server error: HTTP {e.response.status_code}",
                "detail": e.response.text[:500],
            },
            status_code=e.response.status_code,
        )
    except Exception as e:
        logger.exception("Bundle download failed")
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_download_bundle_b64(request: Request) -> JSONResponse:
    """
    GET /download-bundle-b64?includeLocations=true|false&conversation_id=...
    Headers: avni-auth-token (or conversation_id query param)
    Same as /download-bundle but returns base64-encoded ZIP in JSON.

    When conversation_id is provided: stores downloaded bundle server-side under
    '{conversation_id}:existing' key and returns summary only (no bundle_zip_b64).
    Without conversation_id: legacy behaviour, returns full bundle_zip_b64.
    """
    from ..auth_store import resolve_auth_token

    auth_token = resolve_auth_token(request)
    if not auth_token:
        return JSONResponse(
            {
                "error": "Missing auth: provide avni-auth-token header or conversation_id"
            },
            status_code=401,
        )

    include_locations = (
        request.query_params.get("includeLocations", "false").lower() == "true"
    )
    base_url = request.query_params.get("baseUrl", AVNI_BASE_URL)
    conversation_id = request.query_params.get("conversation_id")

    url = (
        f"{base_url.rstrip('/')}/implementation/export/{str(include_locations).lower()}"
    )

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.get(
                url,
                headers={
                    "AUTH-TOKEN": auth_token,
                    "Accept": "application/octet-stream",
                },
            )
            response.raise_for_status()

        zip_b64 = base64.b64encode(response.content).decode("ascii")

        if conversation_id:
            # Store under '{cid}:existing' — keeps large b64 off the LLM
            _bundle_store.put(f"{conversation_id}:existing", zip_b64, {})
            logger.info(
                "download-bundle-b64: stored existing bundle for conversation_id=%s size_bytes=%d",
                conversation_id,
                len(response.content),
            )
            return JSONResponse(
                {
                    "success": True,
                    "stored": True,
                    "bundle_type": "existing",
                    "size_bytes": len(response.content),
                    "include_locations": include_locations,
                }
            )

        # Legacy: return full b64 when no conversation_id
        return JSONResponse(
            {
                "success": True,
                "bundle_zip_b64": zip_b64,
                "size_bytes": len(response.content),
                "include_locations": include_locations,
            }
        )
    except httpx.HTTPStatusError as e:
        logger.error(
            f"Avni server returned {e.response.status_code}: {e.response.text}"
        )
        return JSONResponse(
            {"error": f"Avni server error: HTTP {e.response.status_code}"},
            status_code=e.response.status_code,
        )
    except Exception as e:
        logger.exception("Bundle b64 download failed")
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_patch_bundle(request: Request) -> JSONResponse:
    """
    POST /patch-bundle
    Body: JSON { "conversation_id": "...", "spec_yaml": "..." }
       OR multipart/form-data { existing_bundle_b64, spec_yaml }  (legacy)
    No auth needed — deterministic local processing.

    When conversation_id is provided: fetches existing bundle from
    _bundle_store['{cid}:existing'] and stores patched result under conversation_id.

    Flow:
      1. Decode existing bundle ZIP from base64
      2. Unzip into memory (dict of filename → bytes)
      3. Parse spec_yaml into entities via spec_parser
      4. Generate a fresh bundle from those entities
      5. Merge: overwrite only the files that the spec touches
      6. Re-zip using canonical order
      7. Return patched bundle summary (stored server-side) or full b64 (legacy)
    """
    content_type = request.headers.get("content-type", "")
    logger.info("patch-bundle: content-type=%r", content_type)

    existing_b64: str | None = None
    spec_yaml: str | None = None
    conversation_id: str | None = None

    if "application/json" in content_type:
        try:
            body = await request.json()
        except Exception as e:
            return JSONResponse({"error": f"JSON parse failed: {e}"}, status_code=400)
        conversation_id = body.get("conversation_id")
        spec_yaml = body.get("spec_yaml")
        if conversation_id:
            stored = _bundle_store.get(f"{conversation_id}:existing")
            if stored:
                existing_b64 = stored["zip_b64"]
                logger.info(
                    "patch-bundle: resolved existing bundle from store for conversation_id=%s",
                    conversation_id,
                )
            else:
                return JSONResponse(
                    {
                        "error": f"No stored existing bundle for conversation_id={conversation_id!r}. Call download_bundle_b64 first."
                    },
                    status_code=404,
                )
        else:
            existing_b64 = body.get("existing_bundle_b64")
    else:
        try:
            form = await request.form()
        except Exception as e:
            logger.error("patch-bundle: form parse failed: %s", e)
            return JSONResponse({"error": f"Form parse failed: {e}"}, status_code=400)
        existing_b64 = form.get("existing_bundle_b64")
        spec_yaml = form.get("spec_yaml")

    logger.info(
        "patch-bundle: existing_b64 len=%s spec_yaml len=%s conversation_id=%s",
        len(existing_b64) if existing_b64 else "MISSING",
        len(spec_yaml) if spec_yaml else "MISSING",
        conversation_id,
    )

    if not existing_b64:
        return JSONResponse(
            {
                "error": "Missing 'existing_bundle_b64': pass it directly or provide conversation_id after calling download_bundle_b64"
            },
            status_code=400,
        )
    if not spec_yaml:
        return JSONResponse(
            {"error": "Missing 'spec_yaml' in request body"}, status_code=400
        )

    try:
        # 1. Decode existing bundle
        existing_zip_bytes = base64.b64decode(existing_b64)

        # 2. Parse spec into entities
        entities = spec_to_entities(spec_yaml)
        org_name = entities.get("org_name", "Unknown Organization")

        # Normalise keys for BundleGenerator
        _key_map = {
            "subject_types": "subjectTypes",
            "encounter_types": "encounterTypes",
            "address_levels": "addressLevels",
        }
        gen_entities = {_key_map.get(k, k): v for k, v in entities.items()}

        # 3. Generate fresh bundle from spec entities
        generator = BundleGenerator(org_name)
        result = generator.generate(gen_entities)
        fresh_bundle = result["bundle"]

        # 4. Build patches dict: only files that the spec produces
        patches: dict[str, bytes] = {}

        # Core entity files
        _file_mapping = {
            "subjectTypes": "subjectTypes.json",
            "operationalSubjectTypes": "operationalSubjectTypes.json",
            "programs": "programs.json",
            "operationalPrograms": "operationalPrograms.json",
            "encounterTypes": "encounterTypes.json",
            "operationalEncounterTypes": "operationalEncounterTypes.json",
            "concepts": "concepts.json",
            "formMappings": "formMappings.json",
            "addressLevelTypes": "addressLevelTypes.json",
            "organisationConfig": "organisationConfig.json",
            "groups": "groups.json",
            "groupPrivileges": "groupPrivilege.json",
            "reportCards": "reportCard.json",
            "reportDashboards": "reportDashboard.json",
            "groupDashboards": "groupDashboards.json",
        }

        for bundle_key, zip_name in _file_mapping.items():
            if bundle_key in fresh_bundle and fresh_bundle[bundle_key]:
                patches[zip_name] = json.dumps(
                    fresh_bundle[bundle_key], indent=2
                ).encode("utf-8")

        # Forms (in forms/ subdirectory)
        for form in fresh_bundle.get("forms", []):
            form_name = form.get("name", "UnknownForm")
            patches[f"forms/{form_name}.json"] = json.dumps(form, indent=2).encode(
                "utf-8"
            )

        # 5. Void stale forms and formMappings from the existing bundle.
        # "Stale" = present in the existing bundle but NOT in the new spec (by UUID).
        # Entries present in both are replaced by the new spec's version (Avni upserts by UUID),
        # so we must NOT void those — that would create ghost-voided duplicates on re-runs.
        existing_file_map = unzip_to_map(existing_zip_bytes)

        # Build the set of UUIDs produced by the new spec's formMappings
        new_fm_bytes = patches.get("formMappings.json", b"[]")
        new_fm: list = json.loads(new_fm_bytes) if new_fm_bytes else []
        new_fm_uuids = {m.get("uuid") for m in new_fm if m.get("uuid")}

        # Void only formMappings whose UUID is absent from the new spec
        if "formMappings.json" in existing_file_map:
            try:
                existing_fm = json.loads(existing_file_map["formMappings.json"])
                if isinstance(existing_fm, list):
                    stale_fm = [
                        {**m, "isVoided": True}
                        for m in existing_fm
                        if m.get("uuid") not in new_fm_uuids
                    ]
                    if stale_fm:
                        # Merge: voided-stale first so Avni deactivates them, then fresh entries
                        patches["formMappings.json"] = json.dumps(
                            stale_fm + new_fm, indent=2
                        ).encode("utf-8")
                        logger.info(
                            "patch-bundle: voided %d stale formMappings, kept %d new",
                            len(stale_fm),
                            len(new_fm),
                        )
                    # else: no stale mappings — new spec's formMappings.json patch is already correct
            except Exception as exc:
                logger.warning(
                    "patch-bundle: could not process existing formMappings: %s", exc
                )

        # Void only forms whose name is absent from the new spec (stale forms like old MCH forms)
        new_form_names = {
            form.get("name", "") for form in fresh_bundle.get("forms", [])
        }
        for zip_entry, content_bytes in existing_file_map.items():
            if not zip_entry.startswith("forms/") or zip_entry in patches:
                continue
            form_name = zip_entry[len("forms/") :]
            if form_name.endswith(".json"):
                form_name = form_name[:-5]
            if form_name not in new_form_names:
                try:
                    existing_form = json.loads(content_bytes)
                    if isinstance(existing_form, dict):
                        patches[zip_entry] = json.dumps(
                            {**existing_form, "isVoided": True}, indent=2
                        ).encode("utf-8")
                        logger.info("patch-bundle: voided stale form '%s'", zip_entry)
                except Exception:
                    pass

        # 6. Apply patches to existing ZIP
        patched_zip = patch_bundle_zip(existing_zip_bytes, patches)

        # 7. Return result
        patched_b64 = base64.b64encode(patched_zip).decode("ascii")

        if conversation_id:
            # Store patched bundle under conversation_id (overwrites generated bundle)
            _bundle_store.put(conversation_id, patched_b64, fresh_bundle)
            logger.info(
                "patch-bundle: stored patched bundle for conversation_id=%s size_bytes=%d files_patched=%d",
                conversation_id,
                len(patched_zip),
                len(patches),
            )
            return JSONResponse(
                {
                    "success": True,
                    "stored": True,
                    "size_bytes": len(patched_zip),
                    "files_patched": len(patches),
                    "validation": result.get("validation"),
                    "confidence": result.get("confidence"),
                }
            )

        # Legacy: return full b64 when no conversation_id
        return JSONResponse(
            {
                "success": True,
                "patched_bundle_b64": patched_b64,
                "size_bytes": len(patched_zip),
                "files_patched": len(patches),
                "validation": result.get("validation"),
                "confidence": result.get("confidence"),
            }
        )
    except ValueError as e:
        logger.warning(f"Patch bundle validation error: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        logger.exception("Bundle patching failed")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


def _resolve_bundle_zip(
    conversation_id: str, bundle_type: str
) -> tuple[bytes | None, str | None]:
    """Fetch ZIP bytes from store. Returns (zip_bytes, error_message)."""
    store_key = (
        f"{conversation_id}:{bundle_type}"
        if bundle_type == "existing"
        else conversation_id
    )
    stored = _bundle_store.get(store_key)
    if not stored:
        label = (
            "existing bundle (call download_bundle_b64 first)"
            if bundle_type == "existing"
            else "generated bundle (call generate_bundle first)"
        )
        return None, f"No stored {label} for conversation_id={conversation_id!r}."
    try:
        zip_bytes = base64.b64decode(stored["zip_b64"])
        return zip_bytes, None
    except Exception as e:
        return None, f"Failed to decode stored bundle: {e}"


async def handle_get_bundle_files(request: Request) -> JSONResponse:
    """
    GET /bundle-files?conversation_id=<id>&bundle_type=generated|existing
    Lists all files in a stored bundle with their sizes.
    Returns: { "files": [{"name": "...", "size_bytes": N}, ...], "total_files": N, "bundle_type": "..." }
    """
    conversation_id = request.query_params.get("conversation_id")
    bundle_type = request.query_params.get("bundle_type", "generated")

    if not conversation_id:
        return JSONResponse(
            {"error": "Missing 'conversation_id' query param"}, status_code=400
        )
    if bundle_type not in ("generated", "existing"):
        return JSONResponse(
            {"error": "bundle_type must be 'generated' or 'existing'"}, status_code=400
        )

    zip_bytes, err = _resolve_bundle_zip(conversation_id, bundle_type)
    if err:
        return JSONResponse({"error": err}, status_code=404)

    try:
        file_map = unzip_to_map(zip_bytes)
        files = [
            {"name": name, "size_bytes": len(content)}
            for name, content in sorted(file_map.items())
        ]
        return JSONResponse(
            {
                "files": files,
                "total_files": len(files),
                "bundle_type": bundle_type,
                "conversation_id": conversation_id,
            }
        )
    except Exception as e:
        logger.exception("get-bundle-files failed")
        return JSONResponse({"error": str(e)}, status_code=500)


async def handle_get_bundle_file(request: Request) -> JSONResponse:
    """
    GET /bundle-file?conversation_id=<id>&filename=<path>&bundle_type=generated|existing
    Returns the content of a specific file in a stored bundle.
    Returns: { "filename": "...", "bundle_type": "...", "size_bytes": N, "content": {...} }
    """
    conversation_id = request.query_params.get("conversation_id")
    filename = request.query_params.get("filename")
    bundle_type = request.query_params.get("bundle_type", "generated")

    if not conversation_id:
        return JSONResponse(
            {"error": "Missing 'conversation_id' query param"}, status_code=400
        )
    if not filename:
        return JSONResponse(
            {"error": "Missing 'filename' query param"}, status_code=400
        )
    if bundle_type not in ("generated", "existing"):
        return JSONResponse(
            {"error": "bundle_type must be 'generated' or 'existing'"}, status_code=400
        )

    zip_bytes, err = _resolve_bundle_zip(conversation_id, bundle_type)
    if err:
        return JSONResponse({"error": err}, status_code=404)

    try:
        file_map = unzip_to_map(zip_bytes)
        content_bytes = file_map.get(filename)
        if content_bytes is None:
            available = sorted(file_map.keys())
            return JSONResponse(
                {
                    "error": f"File '{filename}' not found in bundle.",
                    "available_files": available,
                },
                status_code=404,
            )

        # Try to parse as JSON; fall back to raw string
        try:
            content = json.loads(content_bytes)
        except Exception:
            content = content_bytes.decode("utf-8", errors="replace")

        return JSONResponse(
            {
                "filename": filename,
                "bundle_type": bundle_type,
                "size_bytes": len(content_bytes),
                "content": content,
            }
        )
    except Exception as e:
        logger.exception("get-bundle-file failed")
        return JSONResponse({"error": str(e)}, status_code=500)
