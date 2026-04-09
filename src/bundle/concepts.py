"""
Concept generator — produces concepts.json from parsed entity fields.
Ported from srs-bundle-generator/generators/concepts.js.
"""

from __future__ import annotations

from .uuid_utils import generate_deterministic_uuid, lookup_answer_uuid


class ConceptGenerator:
    def __init__(self) -> None:
        self.generated_concepts: list[dict] = []
        self.concept_map: dict[str, str] = {}  # name -> uuid
        self._answer_cache: dict[str, str] = {}  # answer_name -> uuid

    # ── Answer UUID resolution ──────────────────────────────────────

    def get_answer_uuid(self, answer_name: str) -> str:
        cleaned = answer_name.strip().rstrip(",").strip()
        if cleaned in self._answer_cache:
            return self._answer_cache[cleaned]
        # Registry lookup
        from_registry = lookup_answer_uuid(cleaned)
        if from_registry:
            self._answer_cache[cleaned] = from_registry
            return from_registry
        # Deterministic fallback
        new_uuid = generate_deterministic_uuid(f"answer:{cleaned}")
        self._answer_cache[cleaned] = new_uuid
        return new_uuid

    def get_concept_uuid(self, concept_name: str) -> str:
        if concept_name in self.concept_map:
            return self.concept_map[concept_name]
        new_uuid = generate_deterministic_uuid(f"concept:{concept_name}")
        self.concept_map[concept_name] = new_uuid
        return new_uuid

    # ── Generators per data type ────────────────────────────────────

    def generate_answer_concept(self, answer_name: str) -> str:
        cleaned = answer_name.strip().rstrip(",").strip()
        uid = self.get_answer_uuid(cleaned)
        # Avoid duplicates
        if any(c["uuid"] == uid for c in self.generated_concepts):
            return uid
        self.generated_concepts.append(
            {"name": cleaned, "uuid": uid, "dataType": "NA", "active": True}
        )
        return uid

    def generate_coded_concept(self, field: dict) -> str:
        concept_uuid = self.get_concept_uuid(field["name"])
        # Deduplicate — same field name across forms produces same UUID
        if any(c["uuid"] == concept_uuid for c in self.generated_concepts):
            return concept_uuid
        answers = []
        for idx, option in enumerate(field.get("options", [])):
            answer_uuid = self.generate_answer_concept(option)
            answers.append({"name": option.strip(), "uuid": answer_uuid, "order": idx})
        self.generated_concepts.append(
            {
                "name": field["name"],
                "uuid": concept_uuid,
                "dataType": "Coded",
                "answers": answers,
                "active": True,
            }
        )
        return concept_uuid

    def generate_numeric_concept(self, field: dict) -> str:
        concept_uuid = self.get_concept_uuid(field["name"])
        if any(c["uuid"] == concept_uuid for c in self.generated_concepts):
            return concept_uuid
        concept: dict = {
            "name": field["name"],
            "uuid": concept_uuid,
            "dataType": "Numeric",
            "active": True,
        }
        validation = field.get("validation") or {}
        if "min" in validation:
            concept["lowAbsolute"] = validation["min"]
        if "max" in validation:
            concept["highAbsolute"] = validation["max"]
        self.generated_concepts.append(concept)
        return concept_uuid

    def _generate_simple_concept(self, field: dict, data_type: str) -> str:
        concept_uuid = self.get_concept_uuid(field["name"])
        if any(c["uuid"] == concept_uuid for c in self.generated_concepts):
            return concept_uuid
        concept: dict = {
            "name": field["name"],
            "uuid": concept_uuid,
            "dataType": data_type,
            "active": True,
        }
        if data_type == "QuestionGroup":
            concept["answers"] = []
        self.generated_concepts.append(concept)
        return concept_uuid

    # ── Dispatcher ──────────────────────────────────────────────────

    def generate_concept(self, field: dict) -> str:
        dt = field.get("dataType", "Text")
        if dt == "Coded":
            return self.generate_coded_concept(field)
        if dt == "Numeric":
            return self.generate_numeric_concept(field)
        if dt in ("Date", "DateTime"):
            return self._generate_simple_concept(field, dt)
        if dt == "QuestionGroup":
            return self._generate_simple_concept(field, "QuestionGroup")
        # Text, Notes, ImageV2, PhoneNumber, Location, etc.
        return self._generate_simple_concept(field, dt if dt else "Text")

    def generate_from_fields(self, fields: list[dict]) -> list[dict]:
        for field in fields:
            self.generate_concept(field)
        # Sort: NA first, then alphabetical
        self.generated_concepts.sort(
            key=lambda c: (0 if c["dataType"] == "NA" else 1, c["name"])
        )
        return self.generated_concepts

    # ── Confidence ──────────────────────────────────────────────────

    def get_confidence(self) -> float:
        total = len(self.generated_concepts)
        if total == 0:
            return 0.0
        score = 0.0
        for c in self.generated_concepts:
            if c["dataType"] == "NA" and lookup_answer_uuid(c["name"]):
                score += 1.0
            elif c["dataType"] == "Coded":
                answers = c.get("answers", [])
                matched = sum(1 for a in answers if lookup_answer_uuid(a["name"]))
                denom = len(answers) if answers else 1
                score += 0.8 + 0.2 * matched / denom
            else:
                score += 0.9
        return round(score / total, 2)
