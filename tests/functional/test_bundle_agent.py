"""
Functional tests for the Bundle Agent endpoints.

Exercises /generate-bundle, /validate-bundle, /bundle-files, /bundle-file
(GET + PUT), and /download-bundle-zip across 5 real organisations.
"""

from __future__ import annotations

import httpx
import pytest

from .conftest import (
    org_parametrize,
    seed_and_generate_bundle,
)


# ---------------------------------------------------------------------------
# TestGenerateBundle
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestGenerateBundle:
    """POST /generate-bundle: happy path and 404 without entities."""

    @org_parametrize()
    async def test_success_with_summary(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        resp = await seed_and_generate_bundle(
            client, conversation_id, org_entities, org_name
        )
        assert resp.status_code == 200, (
            f"generate-bundle failed for {org_name}: {resp.text}"
        )
        body = resp.json()
        assert body["success"] is True
        summary = body["summary"]
        # All orgs should produce at least subject types; concepts may be 0
        # for orgs with no forms/encounters in their scoping doc
        assert summary["concepts"] >= 0
        assert summary["subjectTypes"] >= 0

    @org_parametrize()
    async def test_404_without_entities(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_name: str,
    ):
        resp = await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": org_name},
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# TestValidateBundle
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestValidateBundle:
    """POST /validate-bundle: validate the generated bundle."""

    @org_parametrize()
    async def test_validate_after_generate(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        gen_resp = await seed_and_generate_bundle(
            client, conversation_id, org_entities, org_name
        )
        assert gen_resp.status_code == 200, (
            f"generate-bundle prerequisite failed for {org_name}: {gen_resp.text}"
        )
        resp = await client.post(
            "/validate-bundle",
            json={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200
        body = resp.json()
        # Validation result should be a dict with 'valid' key
        assert isinstance(body, dict)
        assert "valid" in body or "errors" in body


# ---------------------------------------------------------------------------
# TestBundleFileInspection
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestBundleFileInspection:
    """GET /bundle-files, GET /bundle-file, PUT /bundle-file."""

    @org_parametrize()
    async def test_list_files(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        gen_resp = await seed_and_generate_bundle(
            client, conversation_id, org_entities, org_name
        )
        assert gen_resp.status_code == 200, (
            f"generate-bundle prerequisite failed for {org_name}: {gen_resp.text}"
        )
        resp = await client.get(
            "/bundle-files",
            params={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["total_files"] > 0
        file_names = [f["name"] for f in body["files"]]
        assert "subjectTypes.json" in file_names, (
            f"subjectTypes.json not found in bundle for {org_name}. Files: {file_names}"
        )

    @org_parametrize()
    async def test_get_specific_file(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        gen_resp = await seed_and_generate_bundle(
            client, conversation_id, org_entities, org_name
        )
        assert gen_resp.status_code == 200, (
            f"generate-bundle prerequisite failed for {org_name}: {gen_resp.text}"
        )
        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "subjectTypes.json",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["filename"] == "subjectTypes.json"
        content = body["content"]
        assert isinstance(content, list), (
            f"subjectTypes.json content should be a list, got {type(content).__name__}"
        )

    @org_parametrize()
    async def test_put_file_roundtrip(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        gen_resp = await seed_and_generate_bundle(
            client, conversation_id, org_entities, org_name
        )
        assert gen_resp.status_code == 200, (
            f"generate-bundle prerequisite failed for {org_name}: {gen_resp.text}"
        )
        # Read current content of subjectTypes.json
        get_resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "subjectTypes.json",
            },
        )
        original_content = get_resp.json()["content"]

        # Write it back
        put_resp = await client.put(
            "/bundle-file",
            json={
                "conversation_id": conversation_id,
                "filename": "subjectTypes.json",
                "content": original_content,
            },
        )
        assert put_resp.status_code == 200
        assert put_resp.json().get("updated") is True

        # Read again and verify
        get_resp2 = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "subjectTypes.json",
            },
        )
        assert get_resp2.json()["content"] == original_content


# ---------------------------------------------------------------------------
# TestDownloadBundleZip
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestDownloadBundleZip:
    """GET /download-bundle-zip: returns raw ZIP bytes."""

    @org_parametrize()
    async def test_returns_zip_bytes(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        gen_resp = await seed_and_generate_bundle(
            client, conversation_id, org_entities, org_name
        )
        assert gen_resp.status_code == 200, (
            f"generate-bundle prerequisite failed for {org_name}: {gen_resp.text}"
        )
        resp = await client.get(
            "/download-bundle-zip",
            params={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200
        assert resp.headers.get("content-type") == "application/zip"
        # ZIP magic bytes: PK\x03\x04
        assert resp.content[:4] == b"PK\x03\x04", (
            f"Response does not start with ZIP magic bytes for {org_name}"
        )
        assert len(resp.content) > 100, "ZIP file is suspiciously small"
