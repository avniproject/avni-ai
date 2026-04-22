"""End-to-end simulation of the classifier routing flow.

Drives the server through: store-entities → generate-bundle → mutate-entities
→ entity-diff. Asserts the diff reports each lifecycle phase correctly so the
Dify Question Classifier has accurate signal to route on.
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
from src.handlers.entity_handlers import (
    _entity_store,
    handle_entity_diff,
    handle_put_entities_section,
    handle_store_entities,
)


class FakeReq:
    def __init__(self, body=None, query=None):
        self._body = body or {}
        self._query = query or {}

    async def json(self):
        return self._body

    @property
    def query_params(self):
        return self._query


def _call(h, body=None, query=None):
    resp = asyncio.run(h(FakeReq(body=body, query=query)))
    return resp.status_code, json.loads(resp.body)


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
        "address_levels": [],
    }


def test_full_lifecycle_fresh_to_dirty():
    """Walk the four phases a Dify conversation passes through and assert
    /entity-diff's phase_hint matches at each stage."""
    conv = "turn-flow-1"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)

    # Phase A: fresh — no entities, no bundle
    status, body = _call(handle_entity_diff, query={"conversation_id": conv})
    assert status == 200
    assert body["phase_hint"] == "fresh"

    # Phase B: pre_bundle — entities stored, no bundle
    status, _ = _call(
        handle_store_entities,
        body={"conversation_id": conv, "entities": _entities_v1()},
    )
    assert status == 200
    status, body = _call(handle_entity_diff, query={"conversation_id": conv})
    assert body["phase_hint"] == "pre_bundle"

    # Phase C: generate bundle → stable
    status, body = _call(
        handle_generate_bundle,
        body={"conversation_id": conv, "org_name": "TurnFlowTest"},
    )
    assert status == 200
    assert body["success"] is True
    status, body = _call(handle_entity_diff, query={"conversation_id": conv})
    assert body["phase_hint"] == "stable"
    assert body["summary"] == "No changes since last upload."

    # Phase D: mutate entities → dirty
    new_encs = copy.deepcopy(_entity_store.get(conv)["encounter_types"])
    new_encs.append(
        {
            "name": "Followup",
            "subject_type": "Beneficiary",
            "program_name": "Nutrition",
            "is_program_encounter": True,
        }
    )
    status, _ = _call(
        handle_put_entities_section,
        body={
            "conversation_id": conv,
            "section": "encounter_types",
            "items": new_encs,
        },
    )
    assert status == 200

    status, body = _call(handle_entity_diff, query={"conversation_id": conv})
    assert body["phase_hint"] == "dirty"
    assert "encounter_types" in body["affected_sections"]
    assert "Followup" in body["entity_diff"]["encounter_types"]["added"]
    assert "Followup" in body["summary"]

    # Phase E: regenerate bundle — reconciler moves us back to stable
    status, body = _call(
        handle_generate_bundle,
        body={"conversation_id": conv, "org_name": "TurnFlowTest"},
    )
    assert status == 200
    assert body.get("reconciled") is True
    status, body = _call(handle_entity_diff, query={"conversation_id": conv})
    assert body["phase_hint"] == "stable"


def test_reports_agent_patch_keeps_phase_stable():
    """Reports Agent writing reportCard.json via put_bundle_file must NOT flip
    phase_hint to 'dirty' — that file mutation isn't an entity change."""
    conv = "turn-flow-2"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)

    _entity_store.put(conv, _entities_v1())
    asyncio.run(
        handle_generate_bundle(
            FakeReq({"conversation_id": conv, "org_name": "StablePatchTest"})
        )
    )

    # Simulate Reports Agent writing a new report card
    asyncio.run(
        handle_put_bundle_file(
            FakeReq(
                {
                    "conversation_id": conv,
                    "filename": "reportCard.json",
                    "content": [
                        {"uuid": "rc-probe", "name": "Probe Card", "type": "Count"}
                    ],
                }
            )
        )
    )

    # Phase should STILL be stable — entities unchanged.
    _, body = _call(handle_entity_diff, query={"conversation_id": conv})
    assert body["phase_hint"] == "stable", (
        "put_bundle_file wrongly triggered a dirty phase; "
        "classifier would mistakenly route to bundle_config"
    )
