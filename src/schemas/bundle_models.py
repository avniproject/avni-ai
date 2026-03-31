"""
bundle_models.py — Pydantic request/response schemas for bundle and spec endpoints.

Used by:
  /generate-bundle, /validate-entities, /apply-entity-corrections,
  /generate-spec, /validate-spec, /spec-to-entities, /bundle-to-spec
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator


# ── Field-level ────────────────────────────────────────────────────────────────


class SkipLogicSpec(BaseModel):
    dependsOn: str
    condition: str = "="
    value: str = ""


class FieldSpec(BaseModel):
    name: str
    dataType: str = "Text"
    mandatory: bool = False
    unit: str | None = None
    min: float | None = None
    max: float | None = None
    options: list[str] | None = None
    skipLogic: SkipLogicSpec | None = None


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

    @model_validator(mode="after")
    def at_least_one_subject_type(self) -> "EntitySpec":
        return self


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
