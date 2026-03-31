"""
Main bundle generator — orchestrates concept + form generation
and produces a complete AVNI bundle from an entities config.
Ported from srs-bundle-generator/generators/bundle.js.
"""

from __future__ import annotations

import io
import json
import logging
import zipfile
from typing import Any

from .concepts import ConceptGenerator
from .forms import FormGenerator
from .uuid_utils import generate_deterministic_uuid

logger = logging.getLogger(__name__)


class BundleGenerator:
    def __init__(self, org_name: str) -> None:
        self.org_name = org_name
        self.concept_generator = ConceptGenerator()
        self.form_generator = FormGenerator()
        self.bundle: dict[str, list] = {
            "concepts": [],
            "forms": [],
            "subjectTypes": [],
            "programs": [],
            "encounterTypes": [],
            "formMappings": [],
            "groups": [],
            "groupPrivileges": [],
        }
        self.validation: dict[str, list] = {"errors": [], "warnings": []}
        self.confidence: dict[str, Any] = {}

    # ── Entity processors ───────────────────────────────────────────

    def process_subject_types(self, subject_types: list[dict]) -> None:
        for st in subject_types:
            self.bundle["subjectTypes"].append(
                {
                    "name": st["name"],
                    "uuid": generate_deterministic_uuid(f"subjectType:{st['name']}"),
                    "active": True,
                    "type": st.get("type", "Person"),
                    "subjectSummaryRule": "",
                    "programEligibilityCheckRule": "",
                    "allowEmptyLocation": False,
                    "allowMiddleName": False,
                    "lastNameOptional": True,
                    "validFirstNameFormat": {
                        "regex": "[A-Za-z0-9\\s]+",
                        "descriptionKey": "alphanumericAndSpaces",
                    },
                    "iconFileS3Key": None,
                    "settings": None,
                }
            )

    def process_programs(self, programs: list[dict]) -> None:
        for prog in programs:
            self.bundle["programs"].append(
                {
                    "name": prog["name"],
                    "uuid": generate_deterministic_uuid(f"program:{prog['name']}"),
                    "colour": prog.get("colour", "#3949AB"),
                    "programSubjectLabel": prog.get("subjectLabel", prog["name"]),
                    "enrolmentSummaryRule": "",
                    "enrolmentEligibilityCheckRule": "",
                    "active": True,
                    "manualEnrolmentEligibilityCheckRule": "",
                    "manualEligibilityCheckRequired": False,
                    "allowMultipleEnrolments": False,
                }
            )

    def process_encounter_types(self, encounter_types: list[dict]) -> None:
        for et in encounter_types:
            self.bundle["encounterTypes"].append(
                {
                    "name": et["name"],
                    "uuid": generate_deterministic_uuid(f"encounterType:{et['name']}"),
                    "encounterEligibilityCheckRule": "",
                    "active": True,
                    "immutable": False,
                    "programEncounter": et.get("programEncounter", True),
                }
            )

    def process_groups(self, groups: list[dict]) -> None:
        for group in groups:
            self.bundle["groups"].append(
                {
                    "name": group["name"],
                    "uuid": generate_deterministic_uuid(f"group:{group['name']}"),
                    "hasAllPrivileges": group.get("admin", False),
                }
            )

    # ── Forms ───────────────────────────────────────────────────────

    def process_forms(self, forms: list[dict]) -> None:
        for form_spec in forms:
            fields = form_spec.get("fields", [])

            # Generate concepts from the fields
            concepts = self.concept_generator.generate_from_fields(fields)

            # Build concept lookup for form generator
            concept_map: dict[str, dict] = {}
            for c in concepts:
                concept_map[c["name"]] = {
                    "uuid": c["uuid"],
                    "dataType": c["dataType"],
                    "answers": c.get("answers"),
                }

            # Generate form
            form = self.form_generator.generate_form(
                name=form_spec["name"],
                form_type=form_spec.get("formType", "Encounter"),
                fields=fields,
                concepts=concept_map,
            )
            self.bundle["forms"].append(form)

            # Auto-generate cancellation form for encounter types
            if form_spec.get("formType") in ("ProgramEncounter", "Encounter"):
                cancel_form = self.form_generator.generate_cancellation_form(
                    form_spec["name"], form_spec["formType"]
                )
                self.bundle["forms"].append(cancel_form)

            # Generate form mapping
            self._generate_form_mapping(form_spec, form["uuid"])

        # Store all concepts
        self.bundle["concepts"] = self.concept_generator.generated_concepts

    def _generate_form_mapping(self, form_spec: dict, form_uuid: str) -> None:
        mapping: dict[str, Any] = {
            "uuid": generate_deterministic_uuid(f"mapping:{form_spec['name']}"),
            "formUUID": form_uuid,
            "formType": form_spec.get("formType", "Encounter"),
            "formName": form_spec["name"],
            "enableApproval": False,
        }
        # Resolve references
        st = next(
            (
                s
                for s in self.bundle["subjectTypes"]
                if s["name"] == form_spec.get("subjectType")
            ),
            None,
        )
        prog = next(
            (
                p
                for p in self.bundle["programs"]
                if p["name"] == form_spec.get("program")
            ),
            None,
        )
        et = next(
            (
                e
                for e in self.bundle["encounterTypes"]
                if e["name"] == form_spec.get("encounterType")
            ),
            None,
        )
        if st:
            mapping["subjectTypeUUID"] = st["uuid"]
        if prog:
            mapping["programUUID"] = prog["uuid"]
        if et:
            mapping["encounterTypeUUID"] = et["uuid"]

        self.bundle["formMappings"].append(mapping)

    # ── Validation ──────────────────────────────────────────────────

    def validate(self) -> bool:
        errors: list[str] = []
        warnings: list[str] = []

        # Check form mapping references
        for m in self.bundle["formMappings"]:
            if not m.get("subjectTypeUUID"):
                warnings.append(f'Form mapping "{m["formName"]}" missing subject type')
            if "Program" in m.get("formType", "") and not m.get("programUUID"):
                errors.append(
                    f'Form mapping "{m["formName"]}" missing program reference'
                )

        # Duplicate concept names
        seen_names: set[str] = set()
        for c in self.bundle["concepts"]:
            lower = c["name"].lower()
            if lower in seen_names:
                errors.append(f"Duplicate concept name: {c['name']}")
            seen_names.add(lower)

        # Missing answer UUIDs
        for c in self.bundle["concepts"]:
            if c["dataType"] == "Coded":
                for a in c.get("answers", []):
                    if not a.get("uuid"):
                        errors.append(
                            f'Missing UUID for answer "{a["name"]}" in concept "{c["name"]}"'
                        )

        self.validation = {"errors": errors, "warnings": warnings}
        return len(errors) == 0

    # ── Confidence ──────────────────────────────────────────────────

    def calculate_confidence(self) -> dict:
        concept_conf = self.concept_generator.get_confidence()
        n_forms = len(self.bundle["forms"])
        n_errors = len(self.validation.get("errors", []))
        form_conf = round((n_forms - n_errors) / n_forms, 2) if n_forms > 0 else 0
        overall = round((concept_conf + form_conf) / 2, 2)
        self.confidence = {
            "concepts": concept_conf,
            "forms": form_conf,
            "overall": overall,
            "flaggedItems": len(self.validation.get("warnings", []))
            + len(self.validation.get("errors", [])),
        }
        return self.confidence

    # ── Main entry ──────────────────────────────────────────────────

    def generate(self, entities: dict) -> dict:
        logger.info("Generating bundle for: %s", self.org_name)

        # Normalise snake_case keys to camelCase (idempotent — camelCase passes through)
        _key_map = {
            "subject_types": "subjectTypes",
            "encounter_types": "encounterTypes",
            "address_levels": "addressLevels",
        }
        entities = {_key_map.get(k, k): v for k, v in entities.items()}

        if entities.get("subjectTypes"):
            self.process_subject_types(entities["subjectTypes"])
        if entities.get("programs"):
            self.process_programs(entities["programs"])
        if entities.get("encounterTypes"):
            self.process_encounter_types(entities["encounterTypes"])
        if entities.get("forms"):
            self.process_forms(entities["forms"])
        if entities.get("groups"):
            self.process_groups(entities["groups"])

        self.validate()
        self.calculate_confidence()

        return {
            "bundle": self.bundle,
            "validation": self.validation,
            "confidence": self.confidence,
        }

    # ── Export to ZIP ────────────────────────────────────────────────

    def to_zip_bytes(self) -> bytes:
        """Create an in-memory ZIP file of the bundle."""
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            # Top-level JSON files
            for key in (
                "subjectTypes",
                "programs",
                "encounterTypes",
                "formMappings",
                "groups",
                "groupPrivileges",
            ):
                zf.writestr(f"{key}.json", json.dumps(self.bundle[key], indent=2))

            # Concepts
            zf.writestr("concepts.json", json.dumps(self.bundle["concepts"], indent=2))

            # Forms in subdirectory
            for form in self.bundle["forms"]:
                zf.writestr(f"forms/{form['name']}.json", json.dumps(form, indent=2))

            # Validation report
            zf.writestr(
                "validation_report.json",
                json.dumps(
                    {
                        "confidence": self.confidence,
                        "validation": self.validation,
                        "summary": {
                            "concepts": len(self.bundle["concepts"]),
                            "forms": len(self.bundle["forms"]),
                            "subjectTypes": len(self.bundle["subjectTypes"]),
                            "programs": len(self.bundle["programs"]),
                            "encounterTypes": len(self.bundle["encounterTypes"]),
                            "formMappings": len(self.bundle["formMappings"]),
                        },
                    },
                    indent=2,
                ),
            )

        return buf.getvalue()
