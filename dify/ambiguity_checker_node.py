"""
Ambiguity Checker code node for Dify chatflow.

Takes the structured extraction LLM output and validates for completeness,
consistency, and orphaned references. Runs in Dify's Python sandbox.

Input:  extracted_entities (object) — from Extraction LLM structured output
        {subject_types: [...], programs: [...], encounter_types: [...], address_levels: [...]}
Output: output (object) — contains validated entities (same structure) + issues
"""


def _fuzzy_match(name, known_names):
    lower = name.strip().lower()
    for known in known_names:
        if lower == known.lower() or lower in known.lower() or known.lower() in lower:
            return True
    return False


def main(extracted_entities: dict):
    st_rows = extracted_entities.get("subject_types", [])
    prog_rows = extracted_entities.get("programs", [])
    enc_rows = extracted_entities.get("encounter_types", [])
    addr_rows = extracted_entities.get("address_levels", [])

    subject_type_names = {r["name"] for r in st_rows if r.get("name")}
    program_names = {r["name"] for r in prog_rows if r.get("name")}

    issues = []

    # Check duplicate subject types
    seen = {}
    for r in st_rows:
        key = r.get("name", "").strip().lower()
        if not key:
            continue
        if key in seen:
            issues.append({"severity": "error", "entity_type": "subject_type",
                           "message": f"Duplicate subject type: '{r['name']}'"})
        else:
            seen[key] = r["name"]

    # Check subject type fields
    for r in st_rows:
        if not r.get("type"):
            issues.append({"severity": "warning", "entity_type": "subject_type",
                           "message": f"Subject type '{r.get('name', '?')}' is missing 'type'"})

    # Check duplicate programs
    seen = {}
    for r in prog_rows:
        key = r.get("name", "").strip().lower()
        if not key:
            continue
        if key in seen:
            issues.append({"severity": "error", "entity_type": "program",
                           "message": f"Duplicate program: '{r['name']}'"})
        else:
            seen[key] = r["name"]

    # Check program references
    for r in prog_rows:
        target = r.get("target_subject_type", "")
        if not target:
            issues.append({"severity": "warning", "entity_type": "program",
                           "message": f"Program '{r['name']}' is missing target subject type"})
        elif not _fuzzy_match(target, subject_type_names):
            issues.append({"severity": "warning", "entity_type": "program",
                           "message": f"Program '{r['name']}' references subject type '{target}' which doesn't match any defined subject type"})

    # Check encounter references
    for r in enc_rows:
        if r.get("is_program_encounter"):
            program = r.get("program_name", "")
            if program and not _fuzzy_match(program, program_names):
                issues.append({"severity": "warning", "entity_type": "program_encounter",
                               "message": f"Program encounter '{r['name']}' references program '{program}' which doesn't match any defined program"})
        else:
            subject = r.get("subject_type", "")
            if subject and not _fuzzy_match(subject, subject_type_names):
                issues.append({"severity": "warning", "entity_type": "encounter",
                               "message": f"Encounter '{r['name']}' references subject type '{subject}' which doesn't match any defined subject type"})

    # Check location hierarchy
    if not addr_rows:
        issues.append({"severity": "warning", "entity_type": "location_hierarchy",
                       "message": "No location hierarchy found. A default hierarchy will be generated."})

    error_count = sum(1 for i in issues if i["severity"] == "error")
    warning_count = sum(1 for i in issues if i["severity"] == "warning")

    if not issues:
        issues_summary = "No issues found. All entities look good."
    else:
        lines = []
        errors = [i for i in issues if i["severity"] == "error"]
        warnings = [i for i in issues if i["severity"] == "warning"]
        if errors:
            lines.append(f"{len(errors)} error(s):")
            for e in errors:
                lines.append(f"  [ERROR] {e['message']}")
        if warnings:
            lines.append(f"{len(warnings)} warning(s):")
            for w in warnings:
                lines.append(f"  [WARNING] {w['message']}")
        issues_summary = "\n".join(lines)

    return {"output": {
        "entities": extracted_entities,
        "issues_summary": issues_summary,
        "error_count": error_count,
        "warning_count": warning_count,
        "has_errors": error_count > 0,
        "has_warnings": warning_count > 0,
    }}
