from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class EntitiesData:
    subject_types: list[dict[str, Any]] = field(default_factory=list)
    programs: list[dict[str, Any]] = field(default_factory=list)
    encounter_types: list[dict[str, Any]] = field(default_factory=list)
    address_levels: list[dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "EntitiesData":
        return cls(
            subject_types=data.get("subject_types", []),
            programs=data.get("programs", []),
            encounter_types=data.get("encounter_types", []),
            address_levels=data.get("address_levels", []),
        )

    def is_empty(self) -> bool:
        return not (self.subject_types or self.programs or self.encounter_types or self.address_levels)


@dataclass
class GenerateBundleRequest:
    entities: EntitiesData
    org_name: str

    @classmethod
    def from_body(cls, body: dict) -> "GenerateBundleRequest":
        return cls(
            entities=EntitiesData.from_dict(body.get("entities", {})),
            org_name=body.get("org_name", ""),
        )

    def validate(self) -> Optional[str]:
        if not self.org_name:
            return "org_name is required"
        if self.entities.is_empty():
            return "entities is required (must contain at least one of: subject_types, programs, encounter_types, address_levels)"
        return None
