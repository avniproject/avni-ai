import json

def main(entities_jsonl: list, corrections_str: str):
    entities = list(entities_jsonl) if entities_jsonl else []

    try:
        parsed = json.loads(corrections_str) if corrections_str else {}
        if isinstance(parsed, dict):
            corrections = parsed.get("corrections", [])
        elif isinstance(parsed, list):
            corrections = parsed
        else:
            corrections = []
    except (json.JSONDecodeError, TypeError):
        return {"result": entities}

    if not corrections:
        return {"result": entities}

    for correction in corrections:
        if not isinstance(correction, dict):
            continue

        if correction.get("_delete"):
            sheet = correction.get("sheet", "")
            row = correction.get("row", 0)
            name = correction.get("name", "")
            entity_type = correction.get("type", "")

            for i, entity in enumerate(entities):
                if sheet and row and entity.get("sheet") == sheet and entity.get("row") == row:
                    entities.pop(i)
                    break
                elif entity.get("type") == entity_type and entity.get("name") == name:
                    entities.pop(i)
                    break
            continue

        sheet = correction.get("sheet", "")
        row = correction.get("row", 0)
        matched_idx = None

        if sheet and row:
            for i, entity in enumerate(entities):
                if entity.get("sheet") == sheet and entity.get("row") == row:
                    matched_idx = i
                    break

        if matched_idx is None:
            c_type = correction.get("type", "")
            c_name = correction.get("name", "")
            for i, entity in enumerate(entities):
                if entity.get("type") == c_type and entity.get("name") == c_name:
                    matched_idx = i
                    break

        if matched_idx is not None:
            entities[matched_idx] = correction
        else:
            entities.append(correction)

    return {"result": entities}
