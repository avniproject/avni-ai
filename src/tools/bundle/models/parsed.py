"""
Parsed entity models — the intermediate representation between
LLM extraction and bundle generation.

These represent what was extracted from the specification document,
before any UUID generation or Avni-specific transformation.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedLocationLevel:
    name: str
    level: int
    parent: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "ParsedLocationLevel":
        return cls(
            name=data["name"],
            level=data.get("level", 0),
            parent=data.get("parent"),
        )


@dataclass
class ParsedLocationHierarchy:
    levels: list[ParsedLocationLevel] = field(default_factory=list)


@dataclass
class ParsedSubjectType:
    name: str
    type: str
    form_link: str = ""
    lowest_address_level: str = ""
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "ParsedSubjectType":
        return cls(
            name=data["name"],
            type=data.get("type", ""),
            form_link=data.get("form_link", ""),
            lowest_address_level=data.get("lowest_address_level", ""),
            description=data.get("description", ""),
        )


@dataclass
class ParsedProgram:
    name: str
    enrolment_form: str = ""
    exit_form: str = ""
    description: str = ""
    target_subject_type: str = ""
    program_start_condition: str = ""
    program_end_condition: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "ParsedProgram":
        return cls(
            name=data["name"],
            target_subject_type=data.get("target_subject_type", ""),
            enrolment_form=data.get("enrolment_form", ""),
            exit_form=data.get("exit_form", ""),
            description=data.get("description", ""),
            program_start_condition=data.get("program_start_condition", ""),
            program_end_condition=data.get("program_end_condition", ""),
        )


@dataclass
class ParsedEncounter:
    name: str
    subject_type: str = ""
    encounter_type: str = ""
    frequency: str = ""
    forms_linked: str = ""
    cancellation_form: str = ""
    is_program_encounter: bool = False
    program_name: Optional[str] = None
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "ParsedEncounter":
        return cls(
            name=data["name"],
            subject_type=data.get("subject_type", ""),
            program_name=data.get("program_name", "") or None,
            is_program_encounter=data.get("is_program_encounter", False) in (True, "true", "True"),
            encounter_type=data.get("encounter_type", ""),
            frequency=data.get("frequency", ""),
            forms_linked=data.get("forms_linked", ""),
            cancellation_form=data.get("cancellation_form", ""),
            description=data.get("description", ""),
        )


@dataclass
class ParsedEntities:
    location_hierarchies: list[ParsedLocationHierarchy] = field(default_factory=list)
    subject_types: list[ParsedSubjectType] = field(default_factory=list)
    programs: list[ParsedProgram] = field(default_factory=list)
    encounters: list[ParsedEncounter] = field(default_factory=list)
    program_encounters: list[ParsedEncounter] = field(default_factory=list)
