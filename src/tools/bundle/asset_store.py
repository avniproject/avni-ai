"""
Asset Store: MongoDB-backed storage for bundle generation sessions and assets.

API matches RevisedImplementationPlan.md §5:
  create_session, find_or_create_session, store_jsonl, get_jsonl,
  store_asset, get_asset, update_asset, list_assets,
  assemble_zip, update_session_status, add_upload_record

Uses PyMongo's built-in async driver (pymongo 4.x AsyncMongoClient).
"""

import io
import json
import logging
import uuid as uuid_mod
import zipfile
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

_client = None
_db = None


async def _get_db():
    """Get or create the async MongoDB connection."""
    global _client, _db
    if _db is not None:
        return _db

    import os
    try:
        from pymongo import AsyncMongoClient
    except ImportError:
        raise ImportError(
            "pymongo>=4.16 is required for async MongoDB support. "
            "Install with: uv add 'pymongo>=4.16.0'"
        )

    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB_NAME", "avni_ai")

    _client = AsyncMongoClient(mongo_uri)
    _db = _client[db_name]
    logger.info(f"Connected to MongoDB: {db_name}")
    return _db


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def create_session(org: str) -> str:
    """Create a new bundle generation session. Returns session_id."""
    db = await _get_db()
    session_id = str(uuid_mod.uuid4())

    await db["bundle_sessions"].insert_one({
        "session_id": session_id,
        "org": org,
        "status": "created",
        "version": 1,
        "created_at": _now(),
        "updated_at": _now(),
        "entities_jsonl": None,
        "forms_jsonl": None,
        "ambiguity_report": None,
        "assets": {},
        "upload_history": [],
    })

    logger.info(f"Created session {session_id} for org '{org}'")
    return session_id


async def find_or_create_session(org: str) -> str:
    """Resume an existing session for the org, or create a new one."""
    db = await _get_db()
    existing = await db["bundle_sessions"].find_one(
        {"org": org, "status": {"$nin": ["complete", "failed"]}},
        sort=[("created_at", -1)],
    )
    if existing:
        logger.info(f"Resuming session {existing['session_id']} for org '{org}'")
        return existing["session_id"]
    return await create_session(org)


async def store_jsonl(session_id: str, kind: str, rows: list[dict]) -> None:
    """Store JSONL rows. kind is 'entities' or 'forms'."""
    db = await _get_db()
    field_name = f"{kind}_jsonl"
    await db["bundle_sessions"].update_one(
        {"session_id": session_id},
        {
            "$set": {field_name: rows, "updated_at": _now()},
            "$inc": {"version": 1},
        },
    )
    logger.info(f"Stored {len(rows)} {kind} JSONL rows for session {session_id}")


async def get_jsonl(session_id: str, kind: str) -> list[dict]:
    """Retrieve JSONL rows. kind is 'entities' or 'forms'."""
    db = await _get_db()
    doc = await db["bundle_sessions"].find_one(
        {"session_id": session_id},
        {f"{kind}_jsonl": 1},
    )
    if doc:
        return doc.get(f"{kind}_jsonl") or []
    return []


async def store_asset(session_id: str, filename: str, content: dict) -> None:
    """Store a single bundle asset (e.g., 'subjectTypes', 'programs')."""
    db = await _get_db()
    await db["bundle_sessions"].update_one(
        {"session_id": session_id},
        {
            "$set": {f"assets.{filename}": content, "updated_at": _now()},
            "$inc": {"version": 1},
        },
    )


async def get_asset(session_id: str, filename: str) -> Optional[dict]:
    """Retrieve a single bundle asset by filename."""
    db = await _get_db()
    doc = await db["bundle_sessions"].find_one(
        {"session_id": session_id},
        {f"assets.{filename}": 1},
    )
    if doc and doc.get("assets"):
        return doc["assets"].get(filename)
    return None


async def update_asset(session_id: str, filename: str, patch: dict) -> None:
    """Patch-update fields within an existing asset."""
    db = await _get_db()
    update_fields = {f"assets.{filename}.{k}": v for k, v in patch.items()}
    update_fields["updated_at"] = _now()
    await db["bundle_sessions"].update_one(
        {"session_id": session_id},
        {"$set": update_fields, "$inc": {"version": 1}},
    )


async def list_assets(session_id: str) -> list[str]:
    """List all asset filenames stored for a session."""
    db = await _get_db()
    doc = await db["bundle_sessions"].find_one(
        {"session_id": session_id},
        {"assets": 1},
    )
    if doc and doc.get("assets"):
        return list(doc["assets"].keys())
    return []


async def assemble_zip(session_id: str) -> bytes:
    """Assemble all stored assets into a Metadata ZIP."""
    db = await _get_db()
    doc = await db["bundle_sessions"].find_one(
        {"session_id": session_id},
        {"assets": 1},
    )
    assets = doc.get("assets", {}) if doc else {}

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename, content in assets.items():
            zf.writestr(f"{filename}.json", json.dumps(content, indent=2))
    buf.seek(0)
    return buf.read()


async def update_session_status(session_id: str, status: str) -> None:
    """Update the status of a session."""
    db = await _get_db()
    await db["bundle_sessions"].update_one(
        {"session_id": session_id},
        {"$set": {"status": status, "updated_at": _now()}},
    )


async def store_ambiguity_report(session_id: str, report: dict) -> None:
    """Store the ambiguity check report."""
    db = await _get_db()
    await db["bundle_sessions"].update_one(
        {"session_id": session_id},
        {"$set": {"ambiguity_report": report, "updated_at": _now()}},
    )


async def add_upload_record(session_id: str, result: dict) -> None:
    """Record an upload attempt in the session history."""
    db = await _get_db()
    entry = {**result, "timestamp": _now().isoformat()}
    await db["bundle_sessions"].update_one(
        {"session_id": session_id},
        {
            "$push": {"upload_history": entry},
            "$set": {
                "status": "uploaded" if result.get("success") else "upload_failed",
                "updated_at": _now(),
            },
        },
    )


async def get_session(session_id: str) -> Optional[dict]:
    """Retrieve a full session document."""
    db = await _get_db()
    return await db["bundle_sessions"].find_one(
        {"session_id": session_id},
        {"_id": 0},
    )
