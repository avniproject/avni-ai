"""
Integration tests for asset_store against a real MongoDB instance.

Requires MONGODB_URI and MONGO_DB_NAME environment variables.
Tests clean up after themselves by deleting test sessions.
"""

import json
import os
import zipfile
import io

import pytest
import pytest_asyncio

# Load .env before importing asset_store
from dotenv import load_dotenv
load_dotenv()

from src.tools.bundle import asset_store
from src.tools.bundle.spec_parser import parse_modelling_excel
from src.tools.bundle.ambiguity_checker import check_ambiguities
from src.tools.bundle.bundle_generator import generate_bundle
from pathlib import Path

SAMPLE_FILE = Path(__file__).parent.parent / "Field workflow specification.xlsx"

# Skip all tests if MongoDB URI is not configured
MONGO_URI = os.getenv("MONGODB_URI", "")

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skipif(not MONGO_URI, reason="MONGODB_URI not configured"),
]


# ─── Fixtures ──────────────────────────────────────────────────────────────

@pytest_asyncio.fixture(autouse=True)
async def reset_db_connection():
    """Reset the cached DB connection between tests."""
    asset_store._client = None
    asset_store._db = None
    yield


@pytest_asyncio.fixture
async def session_id():
    """Create a test session and clean it up after the test."""
    sid = await asset_store.create_session("test-org")
    yield sid
    # Cleanup
    try:
        db = await asset_store._get_db()
        await db["bundle_sessions"].delete_one({"session_id": sid})
    except Exception:
        pass


@pytest_asyncio.fixture
async def cleanup_sessions():
    """Track and clean up all sessions created during a test."""
    created: list[str] = []
    yield created
    try:
        db = await asset_store._get_db()
        if created:
            await db["bundle_sessions"].delete_many({"session_id": {"$in": created}})
    except Exception:
        pass


# ─── create_session / get_session ──────────────────────────────────────────


class TestCreateSession:
    async def test_create_session_returns_uuid(self, session_id):
        assert session_id
        parts = session_id.split("-")
        assert len(parts) == 5  # UUID format

    async def test_get_session_returns_doc(self, session_id):
        doc = await asset_store.get_session(session_id)
        assert doc is not None
        assert doc["session_id"] == session_id
        assert doc["org"] == "test-org"
        assert doc["status"] == "created"
        assert doc["version"] == 1
        assert doc["entities_jsonl"] is None
        assert doc["assets"] == {}


# ─── find_or_create_session ───────────────────────────────────────────────


class TestFindOrCreateSession:
    async def test_resumes_existing_session(self, session_id, cleanup_sessions):
        cleanup_sessions.append(session_id)
        resumed = await asset_store.find_or_create_session("test-org")
        cleanup_sessions.append(resumed)
        assert resumed == session_id

    async def test_creates_new_if_none_exist(self, cleanup_sessions):
        unique_org = "test-org-nonexistent-12345"
        sid = await asset_store.find_or_create_session(unique_org)
        cleanup_sessions.append(sid)
        assert sid
        doc = await asset_store.get_session(sid)
        assert doc["org"] == unique_org


# ─── store_jsonl / get_jsonl ──────────────────────────────────────────────


class TestJsonlStorage:
    async def test_store_and_retrieve_entities(self, session_id):
        rows = [
            {"type": "subject_type", "name": "Individual", "row": 2},
            {"type": "program", "name": "Pregnancy", "row": 5},
        ]
        await asset_store.store_jsonl(session_id, "entities", rows)

        retrieved = await asset_store.get_jsonl(session_id, "entities")
        assert len(retrieved) == 2
        assert retrieved[0]["name"] == "Individual"
        assert retrieved[1]["name"] == "Pregnancy"

    async def test_version_increments(self, session_id):
        await asset_store.store_jsonl(session_id, "entities", [{"type": "subject_type"}])
        doc = await asset_store.get_session(session_id)
        assert doc["version"] == 2  # 1 (create) + 1 (store)

    async def test_get_jsonl_returns_empty_for_missing(self, session_id):
        result = await asset_store.get_jsonl(session_id, "forms")
        assert result == []


# ─── store_asset / get_asset / update_asset / list_assets ─────────────────


class TestAssetStorage:
    async def test_store_and_get_asset(self, session_id):
        content = [{"name": "Individual", "uuid": "abc-123", "type": "Person"}]
        await asset_store.store_asset(session_id, "subjectTypes", content)

        retrieved = await asset_store.get_asset(session_id, "subjectTypes")
        assert retrieved == content

    async def test_list_assets(self, session_id):
        await asset_store.store_asset(session_id, "subjectTypes", [])
        await asset_store.store_asset(session_id, "programs", [])
        await asset_store.store_asset(session_id, "encounterTypes", [])

        assets = await asset_store.list_assets(session_id)
        assert set(assets) == {"subjectTypes", "programs", "encounterTypes"}

    async def test_get_asset_returns_none_for_missing(self, session_id):
        result = await asset_store.get_asset(session_id, "nonexistent")
        assert result is None

    async def test_list_assets_empty_session(self, session_id):
        assets = await asset_store.list_assets(session_id)
        assert assets == []


# ─── assemble_zip ─────────────────────────────────────────────────────────


class TestAssembleZip:
    async def test_assemble_zip_from_stored_assets(self, session_id):
        await asset_store.store_asset(session_id, "subjectTypes", [{"name": "Test"}])
        await asset_store.store_asset(session_id, "programs", [])

        zip_bytes = await asset_store.assemble_zip(session_id)
        assert len(zip_bytes) > 0

        zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
        assert "subjectTypes.json" in zf.namelist()
        assert "programs.json" in zf.namelist()

        content = json.loads(zf.read("subjectTypes.json"))
        assert content == [{"name": "Test"}]


# ─── update_session_status / store_ambiguity_report / add_upload_record ───


class TestSessionUpdates:
    async def test_update_status(self, session_id):
        await asset_store.update_session_status(session_id, "entities_confirmed")
        doc = await asset_store.get_session(session_id)
        assert doc["status"] == "entities_confirmed"

    async def test_store_ambiguity_report(self, session_id):
        report = {"issues": [], "summary": {"errors": 0, "warnings": 1}}
        await asset_store.store_ambiguity_report(session_id, report)
        doc = await asset_store.get_session(session_id)
        assert doc["ambiguity_report"] == report

    async def test_add_upload_record(self, session_id):
        result = {"success": True, "status_code": 200}
        await asset_store.add_upload_record(session_id, result)

        doc = await asset_store.get_session(session_id)
        assert doc["status"] == "uploaded"
        assert len(doc["upload_history"]) == 1
        assert doc["upload_history"][0]["success"] is True

    async def test_failed_upload_record(self, session_id):
        result = {"success": False, "error": "timeout"}
        await asset_store.add_upload_record(session_id, result)

        doc = await asset_store.get_session(session_id)
        assert doc["status"] == "upload_failed"


# ─── Full pipeline integration ────────────────────────────────────────────


class TestPipelineIntegration:
    @pytest.fixture(autouse=True)
    def skip_if_no_file(self):
        if not SAMPLE_FILE.exists():
            pytest.skip(f"Sample file not found: {SAMPLE_FILE}")

    async def test_full_pipeline_with_mongodb(self, session_id):
        """Parse → check → generate → store in MongoDB → assemble ZIP."""
        # 1. Parse
        entities = parse_modelling_excel(SAMPLE_FILE)

        # 2. Store JSONL
        await asset_store.store_jsonl(session_id, "entities", entities.to_jsonl())
        await asset_store.update_session_status(session_id, "entities_parsed")

        # 3. Check ambiguities
        report = check_ambiguities(entities)
        await asset_store.store_ambiguity_report(session_id, report.to_dict())

        # 4. Generate bundle
        bundle = generate_bundle(entities, org_name="Pipeline-Test")
        assets = bundle.to_asset_dict()

        # 5. Store each asset
        for filename, content in assets.items():
            await asset_store.store_asset(session_id, filename, content)
        await asset_store.update_session_status(session_id, "bundle_generated")

        # 6. Verify session state
        doc = await asset_store.get_session(session_id)
        assert doc["status"] == "bundle_generated"
        assert len(doc["entities_jsonl"]) > 0
        assert doc["ambiguity_report"] is not None

        stored_assets = await asset_store.list_assets(session_id)
        assert "subjectTypes" in stored_assets
        assert "programs" in stored_assets
        assert "encounterTypes" in stored_assets
        assert "formMappings" in stored_assets

        # 7. Assemble ZIP from stored data
        zip_bytes = await asset_store.assemble_zip(session_id)
        zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
        st_data = json.loads(zf.read("subjectTypes.json"))
        assert len(st_data) >= 3
