"""
HTTP handlers for bundle generation, validation, download, and patching.
Endpoints: POST /generate-bundle, POST /validate-bundle, GET /download-bundle,
           GET /download-bundle-b64, POST /patch-bundle
"""

from __future__ import annotations

import base64
import json
import logging

import httpx
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ..bundle.canonical_zip import patch_bundle_zip, unzip_to_map
from ..bundle.generator import BundleGenerator
from ..bundle.spec_parser import spec_to_entities
from ..bundle.validators import BundleValidator
from ..utils.env import AVNI_BASE_URL

logger = logging.getLogger(__name__)


async def handle_generate_bundle(request: Request) -> JSONResponse:
    """
    POST /generate-bundle
    Body: { "entities": {...}, "org_name": "MyOrg" }
    Returns: { "bundle": {...}, "validation": {...}, "confidence": {...}, "bundle_zip_b64": "..." }
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

    try:
        generator = BundleGenerator(org_name)
        result = generator.generate(entities)

        # Generate ZIP bytes
        zip_bytes = generator.to_zip_bytes()
        zip_b64 = base64.b64encode(zip_bytes).decode("ascii")

        return JSONResponse(
            {
                "success": True,
                "bundle": result["bundle"],
                "validation": result["validation"],
                "confidence": result["confidence"],
                "bundle_zip_b64": zip_b64,
                "summary": {
                    "concepts": len(result["bundle"]["concepts"]),
                    "forms": len(result["bundle"]["forms"]),
                    "subjectTypes": len(result["bundle"]["subjectTypes"]),
                    "programs": len(result["bundle"]["programs"]),
                    "encounterTypes": len(result["bundle"]["encounterTypes"]),
                    "formMappings": len(result["bundle"]["formMappings"]),
                    "groups": len(result["bundle"]["groups"]),
                },
            }
        )
    except Exception as e:
        logger.exception("Bundle generation failed")
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


async def handle_validate_bundle(request: Request) -> JSONResponse:
    """
    POST /validate-bundle
    Body: { "bundle": {...} }   (the bundle dict, not a ZIP)
    Returns: { "valid": bool, "errors": [...], "warnings": [...] }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    bundle = body.get("bundle")
    if not bundle:
        return JSONResponse(
            {"error": "Missing 'bundle' in request body"}, status_code=400
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
    Headers: avni-auth-token
    Proxies Avni server's /implementation/export/{includeLocations} endpoint.
    Returns the raw ZIP bytes with appropriate content-type.
    """
    auth_token = request.headers.get("avni-auth-token")
    if not auth_token:
        return JSONResponse(
            {"error": "Missing avni-auth-token header"}, status_code=401
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
    GET /download-bundle-b64?includeLocations=true|false
    Headers: avni-auth-token
    Same as /download-bundle but returns base64-encoded ZIP in JSON.
    Useful for Dify code nodes that can't handle binary responses.
    """
    auth_token = request.headers.get("avni-auth-token")
    if not auth_token:
        return JSONResponse(
            {"error": "Missing avni-auth-token header"}, status_code=401
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

        zip_b64 = base64.b64encode(response.content).decode("ascii")
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
    Body: multipart/form-data with fields existing_bundle_b64 and spec_yaml
    No auth needed — deterministic local processing.

    Flow:
      1. Decode existing bundle ZIP from base64
      2. Unzip into memory (dict of filename → bytes)
      3. Parse spec_yaml into entities via spec_parser
      4. Generate a fresh bundle from those entities
      5. Merge: overwrite only the files that the spec touches
      6. Re-zip using canonical order
      7. Return patched ZIP as base64
    """
    content_type = request.headers.get("content-type", "")
    logger.info("patch-bundle: content-type=%r", content_type)
    try:
        form = await request.form()
    except Exception as e:
        logger.error("patch-bundle: form parse failed: %s", e)
        return JSONResponse({"error": f"Form parse failed: {e}"}, status_code=400)
    existing_b64 = form.get("existing_bundle_b64")
    spec_yaml = form.get("spec_yaml")
    logger.info("patch-bundle: existing_b64 len=%s spec_yaml len=%s",
                len(existing_b64) if existing_b64 else "MISSING",
                len(spec_yaml) if spec_yaml else "MISSING")

    if not existing_b64:
        return JSONResponse(
            {"error": "Missing 'existing_bundle_b64' in request body"},
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
                        patches["formMappings.json"] = json.dumps(stale_fm + new_fm, indent=2).encode("utf-8")
                        logger.info(
                            "patch-bundle: voided %d stale formMappings, kept %d new",
                            len(stale_fm), len(new_fm),
                        )
                    # else: no stale mappings — new spec's formMappings.json patch is already correct
            except Exception as exc:
                logger.warning("patch-bundle: could not process existing formMappings: %s", exc)

        # Void only forms whose name is absent from the new spec (stale forms like old MCH forms)
        new_form_names = {form.get("name", "") for form in fresh_bundle.get("forms", [])}
        for zip_entry, content_bytes in existing_file_map.items():
            if not zip_entry.startswith("forms/") or zip_entry in patches:
                continue
            form_name = zip_entry[len("forms/"):]
            if form_name.endswith(".json"):
                form_name = form_name[:-5]
            if form_name not in new_form_names:
                try:
                    existing_form = json.loads(content_bytes)
                    if isinstance(existing_form, dict):
                        patches[zip_entry] = json.dumps({**existing_form, "isVoided": True}, indent=2).encode("utf-8")
                        logger.info("patch-bundle: voided stale form '%s'", zip_entry)
                except Exception:
                    pass

        # 6. Apply patches to existing ZIP
        patched_zip = patch_bundle_zip(existing_zip_bytes, patches)

        # 7. Return result
        patched_b64 = base64.b64encode(patched_zip).decode("ascii")

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
