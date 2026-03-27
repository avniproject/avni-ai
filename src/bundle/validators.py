"""
Bundle validator — checks a generated bundle dict for common issues.
Ported from srs-bundle-generator/validators/bundle_validator.js.
"""

from __future__ import annotations

from typing import Any


class BundleValidator:
    """Validate an in-memory bundle dict (not a directory)."""

    def __init__(self, bundle: dict[str, list]) -> None:
        self.bundle = bundle
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate(self) -> dict[str, Any]:
        self._validate_concepts()
        self._validate_concept_name_hygiene()
        self._validate_forms()
        self._validate_form_concept_references()
        self._validate_form_mappings()
        self._validate_encounter_type_completeness()
        self._check_required_sections()
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    # ── Concepts ────────────────────────────────────────────────────

    def _validate_concepts(self) -> None:
        concepts = self.bundle.get("concepts", [])
        uuid_set: set[str] = set()
        name_map: dict[str, list[dict]] = {}
        concepts_by_uuid: dict[str, dict] = {}

        for c in concepts:
            uid = c.get("uuid", "")
            if uid in uuid_set:
                existing = concepts_by_uuid.get(uid, {})
                # Allow equivalent NA answers (Other/Others etc.)
                if not (c.get("dataType") == "NA" and existing.get("dataType") == "NA"):
                    self.errors.append(
                        f'Duplicate UUID: "{uid}" used by "{existing.get("name")}" and "{c.get("name")}"'
                    )
            uuid_set.add(uid)
            concepts_by_uuid[uid] = c

            lower = c["name"].lower()
            name_map.setdefault(lower, []).append(c)

        # Duplicate names with different UUIDs
        for lower_name, clist in name_map.items():
            if len(clist) > 1:
                uuids = {c["uuid"] for c in clist}
                if len(uuids) > 1:
                    self.errors.append(
                        f'Duplicate concept name: "{clist[0]["name"]}" has {len(clist)} entries with different UUIDs'
                    )
                types = {c["dataType"] for c in clist}
                if len(types) > 1:
                    self.errors.append(
                        f'Inconsistent data type: "{clist[0]["name"]}" has types {types}'
                    )

        # Coded concepts missing answer definitions
        answer_uuids = {c["uuid"] for c in concepts if c.get("dataType") == "NA"}
        for c in concepts:
            if c.get("dataType") == "Coded":
                for a in c.get("answers", []):
                    if a.get("uuid") and a["uuid"] not in answer_uuids:
                        # Check if defined elsewhere in concepts
                        if a["uuid"] not in concepts_by_uuid:
                            self.warnings.append(
                                f'Missing answer definition for "{a["name"]}" in concept "{c["name"]}"'
                            )

    def _validate_concept_name_hygiene(self) -> None:
        for c in self.bundle.get("concepts", []):
            name = c.get("name", "")
            if name.endswith(","):
                self.errors.append(f'Trailing comma in concept name: "{name}"')
            if name != name.strip():
                self.warnings.append(f'Whitespace issue in concept name: "{name}"')
            for a in c.get("answers", []):
                if a.get("name", "").endswith(","):
                    self.errors.append(
                        f'Trailing comma in answer name: "{a["name"]}" in concept "{name}"'
                    )

    # ── Forms ───────────────────────────────────────────────────────

    def _validate_forms(self) -> None:
        form_uuids: set[str] = set()
        element_uuids: set[str] = set()
        for form in self.bundle.get("forms", []):
            if form["uuid"] in form_uuids:
                self.errors.append(
                    f'Duplicate form UUID: "{form["uuid"]}" in "{form["name"]}"'
                )
            form_uuids.add(form["uuid"])

            for group in form.get("formElementGroups", []):
                for elem in group.get("formElements", []):
                    if elem["uuid"] in element_uuids:
                        self.warnings.append(
                            f'Duplicate form element UUID: "{elem["uuid"]}" for "{elem["name"]}"'
                        )
                    element_uuids.add(elem["uuid"])

    def _validate_form_concept_references(self) -> None:
        concepts_by_uuid = {c["uuid"]: c for c in self.bundle.get("concepts", [])}
        for form in self.bundle.get("forms", []):
            for group in form.get("formElementGroups", []):
                for elem in group.get("formElements", []):
                    concept = elem.get("concept", {})
                    uid = concept.get("uuid")
                    if uid and uid not in concepts_by_uuid:
                        self.warnings.append(
                            f'Form "{form["name"]}" references concept '
                            f'"{concept.get("name")}" not found in concepts'
                        )

    # ── Form mappings ───────────────────────────────────────────────

    def _validate_form_mappings(self) -> None:
        st_uuids = {s["uuid"] for s in self.bundle.get("subjectTypes", [])}
        prog_uuids = {p["uuid"] for p in self.bundle.get("programs", [])}
        et_uuids = {e["uuid"] for e in self.bundle.get("encounterTypes", [])}

        for m in self.bundle.get("formMappings", []):
            if m.get("subjectTypeUUID") and m["subjectTypeUUID"] not in st_uuids:
                self.errors.append(
                    f'Form mapping "{m["formName"]}" references unknown subjectTypeUUID'
                )
            if m.get("programUUID") and m["programUUID"] not in prog_uuids:
                self.errors.append(
                    f'Form mapping "{m["formName"]}" references unknown programUUID'
                )
            if m.get("encounterTypeUUID") and m["encounterTypeUUID"] not in et_uuids:
                self.errors.append(
                    f'Form mapping "{m["formName"]}" references unknown encounterTypeUUID'
                )

    # ── Encounter completeness ──────────────────────────────────────

    def _validate_encounter_type_completeness(self) -> None:
        mappings = self.bundle.get("formMappings", [])
        for et in self.bundle.get("encounterTypes", []):
            has_form = any(
                m.get("encounterTypeUUID") == et["uuid"]
                and m.get("formType") in ("Encounter", "ProgramEncounter")
                for m in mappings
            )
            if not has_form:
                self.warnings.append(
                    f'Encounter type "{et["name"]}" has no form mapping'
                )

    # ── Required sections ───────────────────────────────────────────

    def _check_required_sections(self) -> None:
        for key in ("concepts", "subjectTypes", "formMappings"):
            if not self.bundle.get(key):
                self.warnings.append(f"Bundle has no {key}")
        if not self.bundle.get("groups"):
            self.errors.append("Missing groups (user groups for permissions)")
