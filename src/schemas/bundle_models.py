"""
bundle_models.py — Pydantic request/response schemas for bundle and spec endpoints.

Used by:
  /generate-bundle, /validate-entities, /apply-entity-corrections,
  /generate-spec, /validate-spec, /spec-to-entities, /bundle-to-spec
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


# ── Field-level ────────────────────────────────────────────────────────────────


class SkipLogicSpec(BaseModel):
    dependsOn: str
    condition: str = "="
    value: str = ""


class FieldSpec(BaseModel):
    name: str
    dataType: str = "Text"
    mandatory: bool = False
    readOnly: bool = False
    group: str | None = None
    unit: str | None = None
    min: float | None = None
    max: float | None = None
    options: list[str] | None = None
    selectionType: str | None = None  # "SingleSelect" or "MultiSelect"
    skipLogic: SkipLogicSpec | None = None
    keyValues: dict[str, Any] | None = None
    isQuestionGroup: bool = False
    isRepeatable: bool = False  # Only meaningful when isQuestionGroup=True
    children: list["FieldSpec"] | None = None  # Child fields for QG/RQG


# ── Form-level ─────────────────────────────────────────────────────────────────


class SectionSpec(BaseModel):
    name: str = "Details"
    fields: list[FieldSpec] = Field(default_factory=list)


class FormSpec(BaseModel):
    name: str
    formType: str
    subjectType: str | None = None
    program: str | None = None
    encounterType: str | None = None
    fields: list[FieldSpec] = Field(default_factory=list)
    sections: list[SectionSpec] = Field(default_factory=list)


# ── Entity-level ───────────────────────────────────────────────────────────────


class AddressLevelSpec(BaseModel):
    name: str
    level: int = 1
    parent: str | None = None


class SubjectTypeSpec(BaseModel):
    name: str
    type: str = "Person"
    allowProfilePicture: bool = False
    uniqueName: bool = False
    lastNameOptional: bool = True


class ProgramSpec(BaseModel):
    name: str
    target_subject_type: str = ""
    colour: str = "#4A148C"
    allow_multiple_enrolments: bool = False


class EncounterTypeSpec(BaseModel):
    name: str
    program_name: str = ""
    subject_type: str = ""
    is_program_encounter: bool = False
    is_scheduled: bool = True

    @field_validator("program_name", mode="before")
    @classmethod
    def coerce_none_to_empty(cls, v: object) -> str:
        return "" if v is None else v


class GroupSpec(BaseModel):
    name: str
    has_all_privileges: bool = False


# ── Top-level entity bundle ────────────────────────────────────────────────────


class EntitySpec(BaseModel):
    subject_types: list[SubjectTypeSpec] = Field(default_factory=list)
    programs: list[ProgramSpec] = Field(default_factory=list)
    encounter_types: list[EncounterTypeSpec] = Field(default_factory=list)
    address_levels: list[AddressLevelSpec] = Field(default_factory=list)
    groups: list[GroupSpec] = Field(default_factory=list)
    forms: list[FormSpec] = Field(default_factory=list)

    # Cross-ref issues stored as warnings instead of raising ValueError.
    # Populated by the validator; downstream code can inspect these.
    validation_warnings: list[str] = Field(default_factory=list, exclude=True)

    # Set to True to raise on cross-ref errors (strict mode).
    # Default False = lenient mode (store as warnings).
    _strict_validation: bool = False

    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    def create_strict(cls, **kwargs) -> "EntitySpec":
        """Create an EntitySpec that raises on cross-ref errors."""
        spec = cls(**kwargs)
        spec._strict_validation = True
        spec._run_cross_ref_checks()
        return spec

    @model_validator(mode="after")
    def validate_no_duplicates_and_cross_refs(self) -> "EntitySpec":
        self._run_cross_ref_checks()
        return self

    def _run_cross_ref_checks(self) -> None:
        errors: list[str] = []

        # ── Duplicate checks ──────────────────────────────────────────────────
        def _check_dupes(items: list, label: str) -> set[str]:
            seen: set[str] = set()
            for item in items:
                name = getattr(item, "name", "").strip()
                if not name:
                    continue
                key = name.lower()
                if key in seen:
                    errors.append(f"Duplicate {label}: '{name}'")
                seen.add(key)
            return seen

        st_names = _check_dupes(self.subject_types, "subject_type")
        prog_names = _check_dupes(self.programs, "program")
        _check_dupes(self.encounter_types, "encounter_type")
        _check_dupes(self.address_levels, "address_level")

        # ── Cross-reference checks ────────────────────────────────────────────
        for prog in self.programs:
            target = (prog.target_subject_type or "").strip()
            if target and target.lower() not in st_names:
                errors.append(
                    f"Program '{prog.name}' references unknown subject_type '{target}'"
                )

        for enc in self.encounter_types:
            prog_ref = (enc.program_name or "").strip()
            st_ref = (enc.subject_type or "").strip()
            if prog_ref and prog_ref.lower() not in prog_names:
                errors.append(
                    f"EncounterType '{enc.name}' references unknown program '{prog_ref}'"
                )
            if st_ref and st_ref.lower() not in st_names:
                errors.append(
                    f"EncounterType '{enc.name}' references unknown subject_type '{st_ref}'"
                )

        if errors:
            if self._strict_validation:
                raise ValueError(
                    "EntitySpec validation failed:\n"
                    + "\n".join(f"  - {e}" for e in errors)
                )
            self.validation_warnings = errors

    def to_entities_dict(self) -> dict:
        """Return a plain dict compatible with AppConfiguratorFlow.state.entities_jsonl."""
        return {
            "subject_types": [st.model_dump() for st in self.subject_types],
            "programs": [p.model_dump() for p in self.programs],
            "encounter_types": [e.model_dump() for e in self.encounter_types],
            "address_levels": [a.model_dump() for a in self.address_levels],
            "groups": [g.model_dump() for g in self.groups],
            "forms": [f.model_dump() for f in self.forms],
        }


# ── Request bodies ─────────────────────────────────────────────────────────────


class GenerateBundleRequest(BaseModel):
    entities: dict[str, Any]
    org_name: str = ""


class ValidateEntitiesRequest(BaseModel):
    entities: dict[str, Any]


class ApplyEntityCorrectionsRequest(BaseModel):
    entities: dict[str, Any]
    corrections: list[dict[str, Any]] = Field(default_factory=list)


class GenerateSpecRequest(BaseModel):
    entities: dict[str, Any]
    org_name: str = ""


class ValidateSpecRequest(BaseModel):
    spec_yaml: str


class SpecToEntitiesRequest(BaseModel):
    spec_yaml: str


class BundleToSpecRequest(BaseModel):
    bundle: dict[str, Any]
    org_name: str = ""


# ── Response shapes ────────────────────────────────────────────────────────────


class ValidationIssue(BaseModel):
    severity: str
    entity_type: str
    message: str


class ValidateEntitiesResponse(BaseModel):
    entities: dict[str, Any]
    issues: list[ValidationIssue]
    error_count: int
    warning_count: int
    issues_summary: str
    has_errors: bool
    has_warnings: bool


class ValidateSpecResponse(BaseModel):
    valid: bool
    errors: list[str]
    warnings: list[str]
    suggestions: list[str]
