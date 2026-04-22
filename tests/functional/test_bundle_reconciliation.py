"""End-to-end test for bundle snapshot+reconcile on entity mutation.

Scenario: generate bundle from entities A. Simulate Reports Agent writing
reportCards.json via put_bundle_file. Mutate entities to add a new encounter
type. Call generate_bundle again — it should reconcile (not noop, not full
regen), reflect the new encounter, and PRESERVE the agent-added report cards.
"""

from __future__ import annotations

import asyncio
import copy
import json

from src.handlers.bundle_handlers import (
    _bundle_store,
    handle_generate_bundle,
    handle_put_bundle_file,
)
from src.handlers.entity_handlers import _entity_store, _invalidate_bundle


class FakeReq:
    def __init__(self, body, query=None):
        self._body = body
        self._query = query or {}

    async def json(self):
        return self._body

    @property
    def query_params(self):
        return self._query


def _entities_v1():
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


def test_reconcile_preserves_agent_patch_after_entity_mutation():
    conv_id = "recon-test-1"

    # Clean state
    _entity_store._store.pop(conv_id, None)
    _bundle_store._store.pop(conv_id, None)

    entities = _entities_v1()
    _entity_store.put(conv_id, entities)

    # 1. Generate bundle from v1 entities.
    resp = asyncio.run(
        handle_generate_bundle(
            FakeReq({"conversation_id": conv_id, "org_name": "TestOrg"})
        )
    )
    assert resp.status_code == 200, resp.body
    body = json.loads(resp.body)
    assert body.get("success") is True

    entry = _bundle_store.get(conv_id)
    assert entry is not None
    assert entry.get("baseline_entities") is not None
    assert entry.get("stale") is False

    # 2. Simulate Reports Agent: write reportCards.json via put_bundle_file.
    card = {
        "uuid": "rc-active-count",
        "name": "Active Beneficiary Count",
        "type": "Count",
    }
    resp = asyncio.run(
        handle_put_bundle_file(
            FakeReq(
                {
                    "conversation_id": conv_id,
                    "filename": "reportCards.json",
                    "content": json.dumps([card]),
                }
            )
        )
    )
    assert resp.status_code == 200, resp.body

    entry = _bundle_store.get(conv_id)
    assert entry["bundle"]["reportCards"] == [card]
    # baseline_entities and stale must be preserved across put_bundle_file.
    assert entry.get("baseline_entities") is not None
    assert entry.get("stale") is False

    # 3. Mutate entities: add a new encounter type. This is what
    #    apply_entity_corrections / apply_ambiguity_answers do in production.
    new_entities = copy.deepcopy(entities)
    new_entities["encounter_types"].append(
        {
            "name": "Followup",
            "subject_type": "Beneficiary",
            "program_name": "Nutrition",
            "is_program_encounter": True,
        }
    )
    _entity_store.put(conv_id, new_entities)
    assert _invalidate_bundle(conv_id) is True

    entry = _bundle_store.get(conv_id)
    assert entry.get("stale") is True, "bundle should be stale after entity mutation"
    # Current bundle and patches still in place.
    assert entry["bundle"]["reportCards"] == [card]

    # 4. Regenerate — should take the reconcile path, not the noop path.
    resp = asyncio.run(
        handle_generate_bundle(
            FakeReq({"conversation_id": conv_id, "org_name": "TestOrg"})
        )
    )
    assert resp.status_code == 200, resp.body
    body = json.loads(resp.body)
    assert body.get("reconciled") is True, body

    entry = _bundle_store.get(conv_id)
    bundle = entry["bundle"]

    # New encounter type propagated.
    enc_names = [e["name"] for e in bundle.get("encounterTypes", [])]
    assert "Intake" in enc_names and "Followup" in enc_names

    # Agent-added report card survived.
    assert any(
        c.get("uuid") == "rc-active-count" for c in bundle.get("reportCards", [])
    ), "Reports Agent's report card was wiped by reconcile"

    # stale cleared, baseline_entities updated.
    assert entry.get("stale") is False
    assert entry.get("baseline_entities") is not None


def test_generate_is_noop_when_fresh():
    conv_id = "recon-test-2"
    _entity_store._store.pop(conv_id, None)
    _bundle_store._store.pop(conv_id, None)

    _entity_store.put(conv_id, _entities_v1())
    asyncio.run(
        handle_generate_bundle(
            FakeReq({"conversation_id": conv_id, "org_name": "TestOrg"})
        )
    )
    # Second call without mutation → noop path.
    resp = asyncio.run(
        handle_generate_bundle(
            FakeReq({"conversation_id": conv_id, "org_name": "TestOrg"})
        )
    )
    body = json.loads(resp.body)
    assert body.get("already_existed") is True
    assert body.get("reconciled") is not True
