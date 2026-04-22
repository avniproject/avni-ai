"""
reconciler.py — three-way merge for the bundle store.

When entities mutate after agents have patched the bundle, we want the
entity delta to propagate to the bundle WITHOUT wiping agent patches
(Rules Agent skip-logic, Reports Agent report cards, Bundle Config Agent
manual fixes).

Approach: given
    base    = BundleGenerator.generate(baseline_entities)   # deterministic
    patched = current cached bundle (generate + agent patches)
    theirs  = BundleGenerator.generate(new_entities)        # deterministic

compute a file-level three-way merge:

    if base[f] == theirs[f]:       keep patched[f]      (spec did not touch file)
    elif base[f] == patched[f]:    take theirs[f]       (agent did not touch file)
    else:                           structural merge     (both diverged)

The `generate_deterministic_uuid` / UUID v5 invariant in BundleGenerator
guarantees that identical entities → identical bundle. That's what lets us
compute `base` and `theirs` on demand without storing snapshots.

Pure functions only; no I/O. Callers own the bundle store.
"""

from __future__ import annotations

import copy
import logging
from typing import Any

logger = logging.getLogger(__name__)


# Top-level bundle keys that are stored as JSON files in the ZIP. Matches
# BundleGenerator.to_zip_bytes and the set that handle_put_bundle_file can
# write to. Used as the iteration domain for three-way merge.
_LIST_KEYS = (
    "concepts",
    "forms",
    "formMappings",
    "subjectTypes",
    "programs",
    "encounterTypes",
    "groups",
    "addressLevelTypes",
    "reportCards",
    "reportDashboards",
    "operationalSubjectTypes",
    "operationalPrograms",
    "operationalEncounterTypes",
    "groupPrivileges",
    "groupDashboards",
)

_OBJECT_KEYS = ("organisationConfig",)


# ---------------------------------------------------------------------------
# Per-file three-way merge
# ---------------------------------------------------------------------------


def _merge_dict_fields(
    base: dict, patched: dict, theirs: dict, path: str, flags: list[dict]
) -> dict:
    """Field-by-field three-way merge of two dicts.

    Rules per key k:
      base[k] == patched[k]   → take theirs[k] (agent did not touch this field)
      base[k] == theirs[k]    → take patched[k] (spec did not touch; keep agent's)
      all three differ        → conflict, prefer patched, flag it
      key only in theirs      → take theirs (spec added)
      key only in patched     → take patched (agent added)
      key in base+patched, gone in theirs → drop (spec removed)
      key in base+theirs, gone in patched → take theirs (agent had default; respect spec change)
    """
    merged: dict[str, Any] = {}
    all_keys = set(base.keys()) | set(patched.keys()) | set(theirs.keys())
    for k in all_keys:
        in_base = k in base
        in_patched = k in patched
        in_theirs = k in theirs
        b = base.get(k)
        p = patched.get(k)
        t = theirs.get(k)

        # Recurse on nested dicts so structural changes deep in an object
        # merge field-by-field rather than wholesale.
        if (
            in_base
            and in_patched
            and in_theirs
            and isinstance(b, dict)
            and isinstance(p, dict)
            and isinstance(t, dict)
        ):
            merged[k] = _merge_dict_fields(b, p, t, f"{path}.{k}", flags)
            continue

        # Recurse on nested UUID-keyed lists (e.g. formElementGroups inside a form)
        if (
            in_base
            and in_patched
            and in_theirs
            and _is_uuid_keyed_list(b)
            and _is_uuid_keyed_list(p)
            and _is_uuid_keyed_list(t)
        ):
            merged[k] = _merge_uuid_keyed_list(b, p, t, f"{path}.{k}", flags)
            continue

        if not in_theirs and in_base and in_patched:
            # Spec removed; drop.
            continue
        if not in_theirs and not in_base and in_patched:
            merged[k] = p
            continue
        if not in_patched and in_theirs:
            merged[k] = t
            continue
        if not in_base and in_theirs and in_patched:
            # Both added the same key independently; prefer patched if they differ.
            if p == t:
                merged[k] = t
            else:
                merged[k] = p
                flags.append(
                    {
                        "type": "merge_conflict",
                        "path": f"{path}.{k}",
                        "reason": "both spec and agent added the same key with different values; kept agent's",
                    }
                )
            continue

        # All three present
        if b == p:
            merged[k] = t
        elif b == t:
            merged[k] = p
        elif p == t:
            merged[k] = t
        else:
            merged[k] = p
            flags.append(
                {
                    "type": "merge_conflict",
                    "path": f"{path}.{k}",
                    "reason": "three-way divergence on field; kept agent's value",
                }
            )
    return merged


def _is_uuid_keyed_list(obj: Any) -> bool:
    """True if obj is a list of dicts that all carry a `uuid`. Empty lists
    count — the empty list is shape-compatible with a UUID-keyed list and
    commonly appears when spec has removed every item."""
    if not isinstance(obj, list):
        return False
    if not obj:
        return True
    return all(isinstance(x, dict) and "uuid" in x for x in obj)


def _index_by_uuid(items: list[dict]) -> dict[str, dict]:
    return {
        item["uuid"]: item
        for item in items
        if isinstance(item, dict) and "uuid" in item
    }


def _merge_uuid_keyed_list(
    base: list[dict],
    patched: list[dict],
    theirs: list[dict],
    path: str,
    flags: list[dict],
) -> list[dict]:
    """Merge three UUID-keyed lists.

      Key in theirs only              → include (spec added)
      Key in theirs and patched       → field-merge
      Key in patched only             → include (agent added; integrity pass may drop)
      Key in base + patched, gone in theirs → drop (spec removed; patch cannot survive)
      Key in base + theirs, gone in patched → include theirs (agent did not touch)

    Output order: theirs' order first (spec is authoritative for structure),
    then any patched-only items appended.
    """
    b_idx = _index_by_uuid(base)
    p_idx = _index_by_uuid(patched)
    t_idx = _index_by_uuid(theirs)

    merged: list[dict] = []
    for item in theirs:
        uuid = item.get("uuid")
        if uuid is None:
            merged.append(copy.deepcopy(item))
            continue
        if uuid in p_idx:
            # Merge the two dicts.
            base_obj = b_idx.get(uuid, {})
            merged.append(
                _merge_dict_fields(
                    base_obj, p_idx[uuid], t_idx[uuid], f"{path}[{uuid}]", flags
                )
            )
        else:
            merged.append(copy.deepcopy(item))

    # Patched-only items: agent added something spec does not know about.
    for uuid, p_item in p_idx.items():
        if uuid in t_idx or uuid in b_idx:
            continue
        merged.append(copy.deepcopy(p_item))

    return merged


def _three_way_merge_value(
    base: Any, patched: Any, theirs: Any, path: str, flags: list[dict]
) -> Any:
    """Dispatch by shape. Used for both top-level keys and nested values."""
    if base == theirs:
        # Spec didn't change this; keep patched (may equal theirs if no patch).
        return copy.deepcopy(patched)
    if base == patched:
        # Agent didn't patch this; take theirs.
        return copy.deepcopy(theirs)

    if (
        isinstance(base, dict)
        and isinstance(patched, dict)
        and isinstance(theirs, dict)
    ):
        return _merge_dict_fields(base, patched, theirs, path, flags)

    if (
        _is_uuid_keyed_list(base)
        and _is_uuid_keyed_list(patched)
        and _is_uuid_keyed_list(theirs)
    ):
        return _merge_uuid_keyed_list(base, patched, theirs, path, flags)

    # Fallback: non-structural scalar divergence; prefer patched.
    flags.append(
        {
            "type": "merge_conflict",
            "path": path,
            "reason": "non-mergeable three-way divergence; kept agent's value",
        }
    )
    return copy.deepcopy(patched)


# ---------------------------------------------------------------------------
# Top-level bundle merge
# ---------------------------------------------------------------------------


def merge_bundle(base: dict, patched: dict, theirs: dict) -> tuple[dict, list[dict]]:
    """Three-way merge of whole bundle dicts.

    Returns (merged_bundle, flags). `flags` records conflicts and integrity
    drops so callers can surface them to agents or tests.
    """
    flags: list[dict] = []
    merged: dict[str, Any] = {}

    all_keys = set(base.keys()) | set(patched.keys()) | set(theirs.keys())
    for key in all_keys:
        b = base.get(key)
        p = patched.get(key)
        t = theirs.get(key)

        # Absent in base is rare (a new top-level bundle file); treat as empty same-shape.
        if key in _LIST_KEYS:
            b = b or []
            p = p or []
            t = t or []
        elif key in _OBJECT_KEYS:
            b = b or {}
            p = p or {}
            t = t or {}

        merged[key] = _three_way_merge_value(b, p, t, key, flags)

    cleaned, integrity_flags = referential_integrity_pass(merged)
    flags.extend(integrity_flags)
    return cleaned, flags


# ---------------------------------------------------------------------------
# Referential integrity pass
# ---------------------------------------------------------------------------


def referential_integrity_pass(bundle: dict) -> tuple[dict, list[dict]]:
    """Drop formMappings / reportCards that reference UUIDs missing after merge.

    Avoids returning a bundle where, e.g., a formMapping points at a form UUID
    that no longer exists because spec removed the form and the mapping was
    carried over by an agent patch.
    """
    flags: list[dict] = []
    result = copy.deepcopy(bundle)

    form_uuids = {
        f["uuid"]
        for f in result.get("forms", [])
        if isinstance(f, dict) and "uuid" in f
    }
    st_uuids = {
        s["uuid"]
        for s in result.get("subjectTypes", [])
        if isinstance(s, dict) and "uuid" in s
    }
    prog_uuids = {
        p["uuid"]
        for p in result.get("programs", [])
        if isinstance(p, dict) and "uuid" in p
    }
    enc_uuids = {
        e["uuid"]
        for e in result.get("encounterTypes", [])
        if isinstance(e, dict) and "uuid" in e
    }

    def _mapping_ok(m: dict) -> bool:
        fu = m.get("formUUID")
        su = m.get("subjectTypeUUID")
        pu = m.get("programUUID")
        eu = m.get("encounterTypeUUID")
        if fu and fu not in form_uuids:
            flags.append(
                {
                    "type": "integrity_drop",
                    "entity": "formMapping",
                    "name": m.get("formName"),
                    "reason": f"formUUID {fu} missing after merge",
                }
            )
            return False
        if su and su not in st_uuids:
            flags.append(
                {
                    "type": "integrity_drop",
                    "entity": "formMapping",
                    "name": m.get("formName"),
                    "reason": f"subjectTypeUUID {su} missing after merge",
                }
            )
            return False
        if pu and pu not in prog_uuids:
            flags.append(
                {
                    "type": "integrity_drop",
                    "entity": "formMapping",
                    "name": m.get("formName"),
                    "reason": f"programUUID {pu} missing after merge",
                }
            )
            return False
        if eu and eu not in enc_uuids:
            flags.append(
                {
                    "type": "integrity_drop",
                    "entity": "formMapping",
                    "name": m.get("formName"),
                    "reason": f"encounterTypeUUID {eu} missing after merge",
                }
            )
            return False
        return True

    if "formMappings" in result:
        result["formMappings"] = [m for m in result["formMappings"] if _mapping_ok(m)]

    # Report cards: drop if they reference a subjectType / program / encounterType
    # UUID that no longer exists. Card schemas vary; we check common fields.
    def _card_ok(c: dict) -> bool:
        for field in ("subjectTypeUUID", "programUUID", "encounterTypeUUID"):
            v = c.get(field)
            if not v:
                continue
            if field == "subjectTypeUUID" and v not in st_uuids:
                flags.append(
                    {
                        "type": "integrity_drop",
                        "entity": "reportCard",
                        "name": c.get("name"),
                        "reason": f"{field} {v} missing",
                    }
                )
                return False
            if field == "programUUID" and v not in prog_uuids:
                flags.append(
                    {
                        "type": "integrity_drop",
                        "entity": "reportCard",
                        "name": c.get("name"),
                        "reason": f"{field} {v} missing",
                    }
                )
                return False
            if field == "encounterTypeUUID" and v not in enc_uuids:
                flags.append(
                    {
                        "type": "integrity_drop",
                        "entity": "reportCard",
                        "name": c.get("name"),
                        "reason": f"{field} {v} missing",
                    }
                )
                return False
        return True

    if "reportCards" in result:
        result["reportCards"] = [c for c in result["reportCards"] if _card_ok(c)]

    return result, flags
