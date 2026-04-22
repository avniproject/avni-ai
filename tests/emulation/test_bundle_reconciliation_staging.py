"""Staging end-to-end test for bundle reconciliation.

Validates that entity mutations reach the bundle via three-way merge WITHOUT
wiping agent patches (reportCards, skip-logic, etc.).

Runs against the deployed avni-ai when AVNI_AI_BASE_URL is set (via the
existing `staging_client` fixture), else against the in-process ASGI app.

Zero LLM calls — this is pure HTTP against the server. Fast, deterministic,
reproducible.

Run:
    AVNI_AI_BASE_URL=https://staging-ai.avniproject.org/ \
        .venv/bin/python -m pytest \
        tests/emulation/test_bundle_reconciliation_staging.py -v
"""

from __future__ import annotations

import copy
import json
import uuid as _uuid

import httpx
import pytest


def _entities_v1() -> dict:
    return {
        "subject_types": [{"name": "Beneficiary", "type": "Person"}],
        "programs": [{"name": "Nutrition", "target_subject_type": "Beneficiary"}],
        "encounter_types": [
            {
                "name": "Intake",
                "subject_type": "Beneficiary",
                "program_name": "Nutrition",
                "is_program_encounter": True,
            }
        ],
        "forms": [],
    }


@pytest.mark.asyncio
async def test_reconciliation_preserves_report_cards(staging_client: httpx.AsyncClient):
    """Spec change adds an encounter → new encounter in bundle, Reports Agent's
    reportCards entry survives."""
    conv_id = f"recon-staging-{_uuid.uuid4()}"
    entities = _entities_v1()

    # 1. Seed entities on the server.
    r = await staging_client.post(
        "/store-entities",
        json={"conversation_id": conv_id, "entities": entities},
    )
    assert r.status_code == 200, r.text

    # 2. Generate initial bundle.
    r = await staging_client.post(
        "/generate-bundle",
        json={"conversation_id": conv_id, "org_name": "ReconTest"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("success") is True, body
    assert body.get("reconciled") is not True, (
        "first generate must be full regen, not reconcile"
    )
    initial_summary = body["summary"]
    assert initial_summary["encounterTypes"] >= 1

    # 3. Fetch current reportCard.json (parsed list/dict; 404 if missing).
    r = await staging_client.get(
        "/bundle-file",
        params={"conversation_id": conv_id, "filename": "reportCard.json"},
    )
    if r.status_code == 200:
        existing_cards = r.json().get("content") or []
    elif r.status_code == 404:
        existing_cards = []
    else:
        raise AssertionError(f"unexpected {r.status_code}: {r.text}")

    # 4. Simulate Reports Agent: write a new reportCard.json via put_bundle_file.
    new_card = {
        "uuid": "rc-recon-probe",
        "name": "Reconcile Probe Card",
        "description": "Proof this card survives entity mutation",
        "type": "Count",
    }
    patched_cards = list(existing_cards) + [new_card]
    r = await staging_client.put(
        "/bundle-file",
        json={
            "conversation_id": conv_id,
            "filename": "reportCard.json",
            "content": patched_cards,  # handler serializes dict/list to JSON
        },
    )
    assert r.status_code == 200, r.text

    # Verify the patch landed.
    r = await staging_client.get(
        "/bundle-file",
        params={"conversation_id": conv_id, "filename": "reportCard.json"},
    )
    assert r.status_code == 200, r.text
    cards_after_patch = r.json()["content"]
    assert any(c.get("uuid") == "rc-recon-probe" for c in cards_after_patch), (
        "put_bundle_file did not persist the reportCards patch"
    )

    # 5. Mutate entities: add a Followup encounter via PUT /entities-section.
    new_encounters = copy.deepcopy(entities["encounter_types"])
    new_encounters.append(
        {
            "name": "Followup",
            "subject_type": "Beneficiary",
            "program_name": "Nutrition",
            "is_program_encounter": True,
        }
    )
    r = await staging_client.put(
        "/entities-section",
        json={
            "conversation_id": conv_id,
            "section": "encounter_types",
            "items": new_encounters,
        },
    )
    assert r.status_code == 200, r.text

    # 6. Regenerate bundle — should reconcile, not full-regen.
    r = await staging_client.post(
        "/generate-bundle",
        json={"conversation_id": conv_id, "org_name": "ReconTest"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("success") is True, body
    assert body.get("reconciled") is True, (
        "expected reconciled=True on stale bundle; got " + json.dumps(body)
    )

    # 7. Assert new encounter landed in the bundle.
    r = await staging_client.get(
        "/bundle-file",
        params={"conversation_id": conv_id, "filename": "encounterTypes.json"},
    )
    assert r.status_code == 200, r.text
    enc_types = r.json()["content"]
    enc_names = {e.get("name") for e in enc_types}
    assert "Intake" in enc_names and "Followup" in enc_names, enc_names

    # 8. Assert the Reports Agent's probe card survived reconciliation.
    r = await staging_client.get(
        "/bundle-file",
        params={"conversation_id": conv_id, "filename": "reportCard.json"},
    )
    assert r.status_code == 200, r.text
    cards_after_reconcile = r.json()["content"]
    assert any(c.get("uuid") == "rc-recon-probe" for c in cards_after_reconcile), (
        "reconcile wiped the Reports Agent's patched reportCards entry; "
        f"got: {[c.get('uuid') for c in cards_after_reconcile]}"
    )


@pytest.mark.asyncio
async def test_noop_when_not_stale(staging_client: httpx.AsyncClient):
    """Generate, then generate again without any mutation — second call must
    be the noop path (already_existed=True) not a reconcile."""
    conv_id = f"recon-noop-{_uuid.uuid4()}"
    entities = _entities_v1()

    r = await staging_client.post(
        "/store-entities",
        json={"conversation_id": conv_id, "entities": entities},
    )
    assert r.status_code == 200

    r = await staging_client.post(
        "/generate-bundle",
        json={"conversation_id": conv_id, "org_name": "NoopTest"},
    )
    assert r.status_code == 200

    # Second call with no mutation.
    r = await staging_client.post(
        "/generate-bundle",
        json={"conversation_id": conv_id, "org_name": "NoopTest"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body.get("already_existed") is True, body
    assert body.get("reconciled") is not True
