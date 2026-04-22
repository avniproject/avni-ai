"""Tests for the bundle three-way-merge reconciler.

Covers the cases documented in the plan:
 - base == theirs, no patch → identity
 - base == theirs, agent patched one file → patch preserved
 - theirs adds an entity → new entries show up, untouched files unchanged
 - theirs removes an entity → patched version dropped, integrity pass cleans mappings
 - Per-field three-way conflict → patched wins, flagged
 - Rules-agent-style skip logic survives a spec rename on an UNRELATED field
 - Rules-agent-style skip logic is dropped when its target form is removed
"""

from __future__ import annotations

import copy

from src.bundle.reconciler import (
    _merge_dict_fields,
    _merge_uuid_keyed_list,
    merge_bundle,
    referential_integrity_pass,
)


def _form(uuid, name, elements=None):
    return {
        "uuid": uuid,
        "name": name,
        "formElementGroups": [
            {
                "uuid": f"grp-{uuid}",
                "name": "Details",
                "formElements": elements or [],
            }
        ],
    }


def _fe(uuid, name, rules=None):
    fe = {"uuid": uuid, "name": name, "concept": {"uuid": f"c-{uuid}", "name": name}}
    if rules is not None:
        fe["rules"] = rules
    return fe


# ---------------------------------------------------------------------------
# Identity + simple patch preservation
# ---------------------------------------------------------------------------


def test_identity_when_base_equals_theirs_no_patch():
    base = {"forms": [_form("f1", "A")], "reportCards": []}
    merged, flags = merge_bundle(base, copy.deepcopy(base), copy.deepcopy(base))
    assert merged == base
    assert flags == []


def test_agent_patch_preserved_when_spec_unchanged():
    base = {"forms": [_form("f1", "A")], "reportCards": []}
    theirs = copy.deepcopy(base)
    # Agent added two report cards; spec did not touch reportCards
    patched = copy.deepcopy(base)
    patched["reportCards"] = [
        {"uuid": "rc1", "name": "Active Count"},
        {"uuid": "rc2", "name": "Dropout Rate"},
    ]
    merged, flags = merge_bundle(base, patched, theirs)
    assert [c["name"] for c in merged["reportCards"]] == [
        "Active Count",
        "Dropout Rate",
    ]
    assert flags == []


# ---------------------------------------------------------------------------
# Spec changes interact correctly with unrelated patches
# ---------------------------------------------------------------------------


def test_spec_adds_entity_agent_patches_unrelated_file_preserved():
    base = {
        "forms": [_form("f1", "A")],
        "encounterTypes": [{"uuid": "e1", "name": "E1"}],
        "reportCards": [],
    }
    # Agent added a report card.
    patched = copy.deepcopy(base)
    patched["reportCards"] = [{"uuid": "rc1", "name": "Active Count"}]
    # Spec added a new encounter type.
    theirs = copy.deepcopy(base)
    theirs["encounterTypes"].append({"uuid": "e2", "name": "E2"})

    merged, flags = merge_bundle(base, patched, theirs)
    assert {e["uuid"] for e in merged["encounterTypes"]} == {"e1", "e2"}
    assert [c["name"] for c in merged["reportCards"]] == ["Active Count"]
    assert flags == []


def test_spec_removes_form_patched_formmapping_is_dropped():
    base = {
        "forms": [_form("f1", "A"), _form("f2", "B")],
        "formMappings": [
            {"uuid": "m1", "formUUID": "f1", "formName": "A"},
            {"uuid": "m2", "formUUID": "f2", "formName": "B"},
        ],
    }
    # Agent had not touched anything.
    patched = copy.deepcopy(base)
    # Spec removed form f2.
    theirs = {
        "forms": [_form("f1", "A")],
        "formMappings": [{"uuid": "m1", "formUUID": "f1", "formName": "A"}],
    }
    merged, flags = merge_bundle(base, patched, theirs)
    assert [f["uuid"] for f in merged["forms"]] == ["f1"]
    assert [m["uuid"] for m in merged["formMappings"]] == ["m1"]
    assert flags == []  # no integrity drops needed; theirs already removed the mapping


def test_patched_formmapping_orphaned_when_form_removed():
    # Spec removed the form; patched bundle still carried the mapping.
    base = {
        "forms": [_form("f1", "A"), _form("f2", "B")],
        "formMappings": [
            {"uuid": "m1", "formUUID": "f1", "formName": "A"},
            {"uuid": "m2", "formUUID": "f2", "formName": "B"},
        ],
    }
    patched = copy.deepcopy(base)
    # Spec dropped form f2 but (artificially) retained its mapping in theirs
    # — this simulates the generator not cleaning up yet. The integrity pass
    # must drop the orphaned mapping.
    theirs = {
        "forms": [_form("f1", "A")],
        "formMappings": [
            {"uuid": "m1", "formUUID": "f1", "formName": "A"},
            {"uuid": "m2", "formUUID": "f2", "formName": "B"},
        ],
    }
    merged, flags = merge_bundle(base, patched, theirs)
    assert [f["uuid"] for f in merged["forms"]] == ["f1"]
    assert [m["uuid"] for m in merged["formMappings"]] == ["m1"]
    assert any(
        f["type"] == "integrity_drop" and f["entity"] == "formMapping" for f in flags
    )


# ---------------------------------------------------------------------------
# Rules-agent skip-logic preservation
# ---------------------------------------------------------------------------


def test_rules_skip_logic_survives_unrelated_spec_change():
    # Base: form with two elements, no rules yet.
    base_form = _form("f1", "A", elements=[_fe("u1", "Is Pregnant"), _fe("u2", "LMP")])
    base = {
        "forms": [base_form],
        "formMappings": [{"uuid": "m1", "formUUID": "f1", "formName": "A"}],
    }

    # Patched: Rules Agent added skip logic on LMP.
    patched_form = copy.deepcopy(base_form)
    patched_form["formElementGroups"][0]["formElements"][1]["rules"] = [
        {"fact": "Is Pregnant", "op": "==", "value": "Yes"}
    ]
    patched = {
        "forms": [patched_form],
        "formMappings": copy.deepcopy(base["formMappings"]),
    }

    # Theirs: spec added a third, unrelated form element "EDD". Existing elements unchanged.
    theirs_form = copy.deepcopy(base_form)
    theirs_form["formElementGroups"][0]["formElements"].append(_fe("u3", "EDD"))
    theirs = {
        "forms": [theirs_form],
        "formMappings": copy.deepcopy(base["formMappings"]),
    }

    merged, flags = merge_bundle(base, patched, theirs)
    # Three elements present (patch-preserved LMP + spec-added EDD).
    elems = merged["forms"][0]["formElementGroups"][0]["formElements"]
    assert [e["uuid"] for e in elems] == ["u1", "u2", "u3"]
    # Skip logic on LMP survived.
    lmp = next(e for e in elems if e["uuid"] == "u2")
    assert lmp.get("rules") == [{"fact": "Is Pregnant", "op": "==", "value": "Yes"}]


def test_rules_skip_logic_dropped_when_form_removed():
    base = {
        "forms": [_form("f1", "A", elements=[_fe("u1", "LMP")])],
        "formMappings": [{"uuid": "m1", "formUUID": "f1", "formName": "A"}],
    }
    # Rules Agent patched skip logic.
    patched = copy.deepcopy(base)
    patched["forms"][0]["formElementGroups"][0]["formElements"][0]["rules"] = [
        {"fact": "X", "op": "==", "value": "Y"}
    ]
    # Spec removed the form.
    theirs = {"forms": [], "formMappings": []}

    merged, flags = merge_bundle(base, patched, theirs)
    assert merged["forms"] == []
    assert merged["formMappings"] == []


# ---------------------------------------------------------------------------
# Conflict handling
# ---------------------------------------------------------------------------


def test_three_way_field_conflict_prefers_patched_and_flags():
    base = {"subjectTypes": [{"uuid": "s1", "name": "Individual", "type": "Person"}]}
    # Agent changed name.
    patched = copy.deepcopy(base)
    patched["subjectTypes"][0]["name"] = "Beneficiary"
    # Spec changed name differently.
    theirs = copy.deepcopy(base)
    theirs["subjectTypes"][0]["name"] = "Participant"

    merged, flags = merge_bundle(base, patched, theirs)
    assert merged["subjectTypes"][0]["name"] == "Beneficiary"
    assert any(f["type"] == "merge_conflict" and "name" in f["path"] for f in flags), (
        flags
    )


# ---------------------------------------------------------------------------
# Helper-level sanity checks
# ---------------------------------------------------------------------------


def test_uuid_keyed_list_agent_only_entry_kept():
    base = [{"uuid": "a", "x": 1}]
    patched = [{"uuid": "a", "x": 1}, {"uuid": "b", "x": 2}]
    theirs = [{"uuid": "a", "x": 1}]
    flags: list[dict] = []
    merged = _merge_uuid_keyed_list(base, patched, theirs, "test", flags)
    assert {m["uuid"] for m in merged} == {"a", "b"}


def test_dict_merge_field_added_by_patched_and_not_base():
    base = {"a": 1}
    patched = {"a": 1, "b": 2}
    theirs = {"a": 1}
    flags: list[dict] = []
    merged = _merge_dict_fields(base, patched, theirs, "root", flags)
    assert merged == {"a": 1, "b": 2}


def test_referential_integrity_cascades_on_formmapping():
    bundle = {
        "forms": [{"uuid": "f1", "name": "A"}],
        "subjectTypes": [{"uuid": "s1", "name": "P"}],
        "formMappings": [
            {"uuid": "m1", "formUUID": "f1", "subjectTypeUUID": "s1", "formName": "A"},
            {
                "uuid": "m2",
                "formUUID": "f_gone",
                "subjectTypeUUID": "s1",
                "formName": "Gone",
            },
            {
                "uuid": "m3",
                "formUUID": "f1",
                "subjectTypeUUID": "s_gone",
                "formName": "Orphan",
            },
        ],
    }
    cleaned, flags = referential_integrity_pass(bundle)
    assert [m["uuid"] for m in cleaned["formMappings"]] == ["m1"]
    assert len([f for f in flags if f["type"] == "integrity_drop"]) == 2
