"""
Bundle Uploader: Assembles a Bundle into a Metadata ZIP and uploads to Avni server.

The ZIP matches Avni's POST /api/importMetaData expected format.
Upload order (per RevisedImplementationPlan.md §8):
  1. addressLevelTypes  2. subjectTypes, programs, encounterTypes
  3. concepts  4. forms/*  5. formMappings  6. groups, groupPrivilege
"""

import io
import json
import logging
import os
import zipfile
from typing import Any

import httpx

from .models import Bundle

logger = logging.getLogger(__name__)


def assemble_metadata_zip(bundle: Bundle) -> bytes:
    """Assemble bundle assets into a ZIP file for Avni's importMetaData endpoint."""
    assets = bundle.to_asset_dict()

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, data in assets.items():
            zf.writestr(f"{filename}.json", json.dumps(data, indent=2))
    buf.seek(0)
    return buf.read()


def assemble_metadata_zip_from_dict(assets: dict[str, Any]) -> bytes:
    """Assemble a ZIP from a raw asset dict (e.g., from MongoDB storage)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, data in assets.items():
            zf.writestr(f"{filename}.json", json.dumps(data, indent=2))
    buf.seek(0)
    return buf.read()


async def upload_bundle(
    bundle: Bundle,
    auth_token: str,
    base_url: str = "",
) -> dict[str, Any]:
    """
    Upload a Bundle to Avni server via POST /api/importMetaData.

    Returns a result dict with success status and response data/error.
    """
    base_url = base_url or os.getenv("AVNI_BASE_URL", "")
    if not base_url:
        return {"success": False, "error": "AVNI_BASE_URL not configured"}

    zip_data = assemble_metadata_zip(bundle)
    return await _upload_zip(zip_data, auth_token, base_url)


async def upload_zip_bytes(
    zip_data: bytes,
    auth_token: str,
    base_url: str = "",
) -> dict[str, Any]:
    """Upload pre-assembled ZIP bytes (e.g., from asset_store.assemble_zip)."""
    base_url = base_url or os.getenv("AVNI_BASE_URL", "")
    if not base_url:
        return {"success": False, "error": "AVNI_BASE_URL not configured"}
    return await _upload_zip(zip_data, auth_token, base_url)


async def _upload_zip(
    zip_data: bytes,
    auth_token: str,
    base_url: str,
) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/api/importMetaData"
    logger.info(f"Uploading {len(zip_data)} bytes to {url}")

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url,
                headers={"AUTH-TOKEN": auth_token},
                files={"file": ("metadata.zip", zip_data, "application/zip")},
            )
            response.raise_for_status()
            logger.info(f"Upload successful: HTTP {response.status_code}")
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.text,
            }

    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
        logger.error(f"Upload failed: {error_msg}")
        return {"success": False, "error": error_msg, "status_code": e.response.status_code}

    except httpx.TimeoutException:
        logger.error("Upload timed out")
        return {"success": False, "error": "Upload timed out (120s)"}

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return {"success": False, "error": str(e)}
