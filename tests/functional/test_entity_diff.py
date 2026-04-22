"""Tests for /entity-diff — covers the four lifecycle phases the classifier
uses as a routing rubric: fresh, pre_bundle, stable, dirty."""

from __future__ import annotations

import asyncio
import copy
import json


from src.handlers.bundle_handlers import _bundle_store
from src.handlers.entity_handlers import _entity_store, handle_entity_diff


class FakeReq:
    def __init__(self, query=None):
        self._query = query or {}

    @property
    def query_params(self):
        return self._query


def _entities():
    return {
        "subject_types": [{"name": "Beneficiary", "type": "Person"}],
        "programs": [{"name": "Enrich", "target_subject_type": "Beneficiary"}],
        "encounter_types": [
            {
                "name": "Intake",
                "subject_type": "Beneficiary",
                "program_name": "Enrich",
                "is_program_encounter": True,
            }
        ],
        "forms": [],
        "address_levels": [],
    }


def _call(conv_id: str) -> dict:
    resp = asyncio.run(handle_entity_diff(FakeReq({"conversation_id": conv_id})))
    assert resp.status_code == 200
    return json.loads(resp.body)


def test_fresh_phase_no_entities_no_bundle():
    conv = "diff-fresh-1"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)
    out = _call(conv)
    assert out["phase_hint"] == "fresh"
    assert out["affected_sections"] == []
    assert out["entity_diff"] == {}
    assert "No entities stored" in out["summary"]


def test_pre_bundle_phase_entities_stored_no_bundle():
    conv = "diff-pre-bundle-1"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)
    _entity_store.put(conv, _entities())
    out = _call(conv)
    assert out["phase_hint"] == "pre_bundle"
    assert out["affected_sections"] == []
    assert "parsed" in out["summary"].lower()
    assert "1 subject_types" in out["summary"] or "1 programs" in out["summary"]


def test_stable_phase_entities_match_baseline():
    conv = "diff-stable-1"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)
    ents = _entities()
    _entity_store.put(conv, ents)
    _bundle_store.put(
        conv, "FAKE_ZIP", {}, flags=[], baseline_entities=copy.deepcopy(ents)
    )
    out = _call(conv)
    assert out["phase_hint"] == "stable"
    assert out["affected_sections"] == []
    assert out["summary"] == "No changes since last upload."


def test_dirty_phase_program_added():
    conv = "diff-dirty-1"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)
    baseline = _entities()
    current = copy.deepcopy(baseline)
    current["programs"].append(
        {"name": "Nourish", "target_subject_type": "Beneficiary"}
    )
    _entity_store.put(conv, current)
    _bundle_store.put(conv, "FAKE_ZIP", {}, flags=[], baseline_entities=baseline)

    out = _call(conv)
    assert out["phase_hint"] == "dirty"
    assert "programs" in out["affected_sections"]
    assert "Nourish" in out["entity_diff"]["programs"]["added"]
    assert "programs" in out["summary"].lower()


def test_dirty_phase_form_modified():
    conv = "diff-dirty-2"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)
    baseline = _entities()
    baseline["forms"] = [
        {
            "name": "F",
            "formType": "Encounter",
            "sections": [{"name": "S", "fields": [{"name": "A"}]}],
        }
    ]
    current = copy.deepcopy(baseline)
    current["forms"][0]["sections"][0]["fields"].append({"name": "B"})
    _entity_store.put(conv, current)
    _bundle_store.put(conv, "FAKE_ZIP", {}, flags=[], baseline_entities=baseline)

    out = _call(conv)
    assert out["phase_hint"] == "dirty"
    assert "forms" in out["affected_sections"]
    assert "F" in out["entity_diff"]["forms"]["modified"]


def test_dirty_phase_spec_level_enrolment_form_added():
    """When a ProgramEnrolment form is added in entities, the spec diff should
    surface 'programs.Enrich.enrolmentForm added'."""
    conv = "diff-dirty-spec"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)
    baseline = _entities()
    current = copy.deepcopy(baseline)
    current["forms"].append(
        {
            "name": "Enrich Enrolment",
            "formType": "ProgramEnrolment",
            "subjectType": "Beneficiary",
            "program": "Enrich",
            "sections": [{"name": "Details", "fields": []}],
        }
    )
    _entity_store.put(conv, current)
    _bundle_store.put(conv, "FAKE_ZIP", {}, flags=[], baseline_entities=baseline)

    out = _call(conv)
    assert out["phase_hint"] == "dirty"
    assert "forms" in out["affected_sections"]
    spec_prog_bits = out["spec_diff"].get("programs", [])
    assert any(
        "Enrich" in s and "enrolmentForm" in s and "added" in s for s in spec_prog_bits
    ), spec_prog_bits


def test_missing_conversation_id_returns_400():
    resp = asyncio.run(handle_entity_diff(FakeReq()))
    assert resp.status_code == 400


def test_summary_never_exceeds_500_chars():
    conv = "diff-big"
    _entity_store._store.pop(conv, None)
    _bundle_store._store.pop(conv, None)
    baseline = _entities()
    current = copy.deepcopy(baseline)
    # Add 50 forms to stress the summary builder
    current["forms"] = [
        {"name": f"Form{i}", "formType": "Encounter", "sections": []} for i in range(50)
    ]
    _entity_store.put(conv, current)
    _bundle_store.put(conv, "FAKE_ZIP", {}, flags=[], baseline_entities=baseline)

    out = _call(conv)
    assert out["phase_hint"] == "dirty"
    assert len(out["summary"]) <= 500
