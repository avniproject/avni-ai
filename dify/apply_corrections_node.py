"""
Apply Corrections code node for Dify chatflow.

Takes the current structured entities and the Correction LLM's output,
applies the changes. Matching is by name within each entity type's array.

Input:
  entities (object) — current entities {subject_types, programs, encounter_types, address_levels}
  corrections_str (str) — LLM's output: JSON with corrections object
Output:
  result (object) — updated entities in the same structured format
"""

import json


def _apply_to_list(items, corrections):
    """Apply corrections to a single entity type list. Returns updated list."""
    result = list(items)

    for correction in corrections:
        if not isinstance(correction, dict):
            continue

        name = correction.get("name", "")

        # Delete
        if correction.get("_delete"):
            result = [r for r in result if r.get("name", "").strip().lower() != name.strip().lower()]
            continue

        # Update or add
        matched_idx = None
        for i, item in enumerate(result):
            if item.get("name", "").strip().lower() == name.strip().lower():
                matched_idx = i
                break

        if matched_idx is not None:
            result[matched_idx] = correction
        else:
            result.append(correction)

    return result


def main(entities: dict, corrections_str: str):
    try:
        parsed = json.loads(corrections_str) if corrections_str else {}
        if isinstance(parsed, dict):
            corrections = parsed.get("corrections", parsed)
        else:
            corrections = {}
    except (json.JSONDecodeError, TypeError):
        return {"result": entities}

    if not corrections:
        return {"result": entities}

    updated = dict(entities)

    if "subject_types" in corrections:
        updated["subject_types"] = _apply_to_list(
            updated.get("subject_types", []), corrections["subject_types"])

    if "programs" in corrections:
        updated["programs"] = _apply_to_list(
            updated.get("programs", []), corrections["programs"])

    if "encounter_types" in corrections:
        updated["encounter_types"] = _apply_to_list(
            updated.get("encounter_types", []), corrections["encounter_types"])

    if "address_levels" in corrections:
        updated["address_levels"] = _apply_to_list(
            updated.get("address_levels", []), corrections["address_levels"])

    return {"result": updated}
