"""
Bundle — top-level container for all generated entity assets.

Holds typed lists of each entity and provides serialization
to the dict-of-lists format used for JSON export and MongoDB storage.
"""

from dataclasses import dataclass, field
from typing import Any

from .subject_type import SubjectTypeContract
from .program import ProgramContract
from .encounter_type import EncounterTypeContract
from .address_level_type import AddressLevelTypeContract
from .form_mapping import FormMappingContract


@dataclass
class Bundle:
    subject_types: list[SubjectTypeContract] = field(default_factory=list)
    programs: list[ProgramContract] = field(default_factory=list)
    encounter_types: list[EncounterTypeContract] = field(default_factory=list)
    address_level_types: list[AddressLevelTypeContract] = field(default_factory=list)
    form_mappings: list[FormMappingContract] = field(default_factory=list)
    operational_encounter_types: list[dict[str, Any]] = field(default_factory=list)
    operational_programs: list[dict[str, Any]] = field(default_factory=list)
    operational_subject_types: list[dict[str, Any]] = field(default_factory=list)
    individual_relations: list[dict[str, Any]] = field(default_factory=list)
    relationship_types: list[dict[str, Any]] = field(default_factory=list)
    organisation_config: dict[str, Any] = field(default_factory=dict)

    def to_asset_dict(self) -> dict[str, Any]:
        """Convert to the dict-of-lists format for JSON export and MongoDB storage."""
        return {
            "subjectTypes": [st.to_dict() for st in self.subject_types],
            "programs": [p.to_dict() for p in self.programs],
            "encounterTypes": [et.to_dict() for et in self.encounter_types],
            "addressLevelTypes": [alt.to_dict() for alt in self.address_level_types],
            "formMappings": [fm.to_dict() for fm in self.form_mappings],
            "operationalEncounterTypes": self.operational_encounter_types,
            "operationalPrograms": self.operational_programs,
            "operationalSubjectTypes": self.operational_subject_types,
            "individualRelation": self.individual_relations,
            "relationshipType": self.relationship_types,
            "organisationConfig": self.organisation_config,
        }
