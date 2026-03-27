"""
HTTP handlers for bundle generation, validation, and download.
Endpoints: POST /generate-bundle, POST /validate-bundle, GET /download-bundle
"""

from __future__ import annotations

import base64
import json
import logging

import httpx
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ..bundle.generator import BundleGenerator
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
        return JSONResponse({"error": "Missing 'entities' in request body"}, status_code=400)

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
        return JSONResponse(
            {"success": False, "error": str(e)}, status_code=500
        )


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
        return JSONResponse({"error": "Missing 'bundle' in request body"}, status_code=400)

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
        return JSONResponse({"error": "Missing avni-auth-token header"}, status_code=401)

    include_locations = request.query_params.get("includeLocations", "false").lower() == "true"
    base_url = request.query_params.get("baseUrl", AVNI_BASE_URL)

    url = f"{base_url.rstrip('/')}/implementation/export/{str(include_locations).lower()}"

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
        logger.error(f"Avni server returned {e.response.status_code}: {e.response.text}")
        return JSONResponse(
            {"error": f"Avni server error: HTTP {e.response.status_code}", "detail": e.response.text[:500]},
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
        return JSONResponse({"error": "Missing avni-auth-token header"}, status_code=401)

    include_locations = request.query_params.get("includeLocations", "false").lower() == "true"
    base_url = request.query_params.get("baseUrl", AVNI_BASE_URL)

    url = f"{base_url.rstrip('/')}/implementation/export/{str(include_locations).lower()}"

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
        return JSONResponse({
            "success": True,
            "bundle_zip_b64": zip_b64,
            "size_bytes": len(response.content),
            "include_locations": include_locations,
        })
    except httpx.HTTPStatusError as e:
        logger.error(f"Avni server returned {e.response.status_code}: {e.response.text}")
        return JSONResponse(
            {"error": f"Avni server error: HTTP {e.response.status_code}"},
            status_code=e.response.status_code,
        )
    except Exception as e:
        logger.exception("Bundle download failed")
        return JSONResponse({"error": str(e)}, status_code=500)
