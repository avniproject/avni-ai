"""
Concept generator — produces concepts.json from parsed entity fields.
Ported from srs-bundle-generator/generators/concepts.js.
"""

from __future__ import annotations

from .uuid_utils import generate_deterministic_uuid, lookup_answer_uuid


_MAX_CONCEPT_NAME = 255


class ConceptGenerator:
    def __init__(self) -> None:
        self.generated_concepts: list[dict] = []
        self.concept_map: dict[str, str] = {}  # lowercase name -> uuid
        self._canonical_name: dict[str, str] = {}  # lowercase name -> first-seen name
        self._answer_cache: dict[str, str] = {}  # lowercase answer_name -> uuid
        self._answer_canonical: dict[str, str] = {}  # lowercase -> first-seen name

    # ── Name safety ─────────────────────────────────────────────────

    @staticmethod
    def _safe_name(name: str) -> str:
        """Truncate concept/answer names to the Avni DB column limit (VARCHAR 255)."""
        if len(name) > _MAX_CONCEPT_NAME:
            import logging

            logging.getLogger(__name__).warning(
                "Concept name truncated from %d to %d chars: %s...",
                len(name),
                _MAX_CONCEPT_NAME,
                name[:60],
            )
            return name[:_MAX_CONCEPT_NAME].rstrip()
        return name

    # ── Answer UUID resolution ──────────────────────────────────────

    def get_answer_uuid(self, answer_name: str) -> str:
        cleaned = self._safe_name(answer_name.strip().rstrip(",").strip())
        key = cleaned.lower()
        if key in self._answer_cache:
            return self._answer_cache[key]
        # Canonical name = first-seen capitalisation
        self._answer_canonical[key] = cleaned
        # Registry lookup (try canonical first-seen name)
        from_registry = lookup_answer_uuid(cleaned)
        if from_registry:
            self._answer_cache[key] = from_registry
            return from_registry
        # Deterministic fallback — UUID derived from lowercase so it's stable regardless of case
        new_uuid = generate_deterministic_uuid(f"answer:{key}")
        self._answer_cache[key] = new_uuid
        return new_uuid

    def get_concept_uuid(self, concept_name: str) -> str:
        safe = self._safe_name(concept_name)
        key = safe.lower()
        if key in self.concept_map:
            return self.concept_map[key]
        # Canonical name = first-seen capitalisation
        self._canonical_name[key] = safe
        new_uuid = generate_deterministic_uuid(f"concept:{key}")
        self.concept_map[key] = new_uuid
        return new_uuid

    # ── Generators per data type ────────────────────────────────────

    def generate_answer_concept(self, answer_name: str) -> str:
        cleaned = self._safe_name(answer_name.strip().rstrip(",").strip())
        key = cleaned.lower()
        # Check if this name already exists as a question concept (Coded/Numeric/etc.)
        # If so, reuse that UUID instead of creating a duplicate NA concept.
        if key in self.concept_map:
            return self.concept_map[key]
        uid = self.get_answer_uuid(cleaned)
        # Avoid duplicates (case-insensitive — same UUID means already emitted)
        if any(c["uuid"] == uid for c in self.generated_concepts):
            return uid
        # Use first-seen capitalisation as the canonical name
        canonical = self._answer_canonical.get(key, cleaned)
        self.generated_concepts.append(
            {"name": canonical, "uuid": uid, "dataType": "NA", "active": True}
        )
        return uid

    def generate_coded_concept(self, field: dict) -> str:
        safe_name = self._safe_name(field["name"])
        key = safe_name.lower()

        # Check if this name already exists as an NA answer concept.
        # If so, upgrade it to Coded (remove the NA entry, reuse or create UUID).
        if key in self._answer_cache and key not in self.concept_map:
            existing_uuid = self._answer_cache[key]
            # Remove the NA entry from generated_concepts
            self.generated_concepts = [
                c
                for c in self.generated_concepts
                if not (c.get("name", "").lower() == key and c.get("dataType") == "NA")
            ]
            # Store in concept_map so future answer lookups find it
            self.concept_map[key] = existing_uuid
            self._canonical_name[key] = safe_name

        concept_uuid = self.get_concept_uuid(safe_name)
        # Deduplicate — same field name (case-insensitive) across forms produces same UUID
        if any(c["uuid"] == concept_uuid for c in self.generated_concepts):
            return concept_uuid
        canonical_name = self._canonical_name.get(safe_name.lower(), safe_name)
        answers = []
        seen_answer_uuids: set[str] = set()
        order = 0
        for option in field.get("options") or []:
            answer_uuid = self.generate_answer_concept(option)
            if answer_uuid in seen_answer_uuids:
                # Case-insensitive duplicate — skip to avoid concept_answer unique constraint
                continue
            seen_answer_uuids.add(answer_uuid)
            # Use first-seen capitalisation for answer name in the answers list too
            canonical_option = self._answer_canonical.get(
                self._safe_name(option.strip().rstrip(",").strip()).lower(),
                option.strip(),
            )
            answers.append(
                {"name": canonical_option, "uuid": answer_uuid, "order": order}
            )
            order += 1
        self.generated_concepts.append(
            {
                "name": canonical_name,
                "uuid": concept_uuid,
                "dataType": "Coded",
                "answers": answers,
                "active": True,
            }
        )
        return concept_uuid

    def generate_numeric_concept(self, field: dict) -> str:
        safe_name = self._safe_name(field["name"])
        concept_uuid = self.get_concept_uuid(safe_name)
        if any(c["uuid"] == concept_uuid for c in self.generated_concepts):
            return concept_uuid
        canonical_name = self._canonical_name.get(safe_name.lower(), safe_name)
        concept: dict = {
            "name": canonical_name,
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
        safe_name = self._safe_name(field["name"])
        concept_uuid = self.get_concept_uuid(safe_name)
        if any(c["uuid"] == concept_uuid for c in self.generated_concepts):
            return concept_uuid
        canonical_name = self._canonical_name.get(safe_name.lower(), safe_name)
        concept: dict = {
            "name": canonical_name,
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
