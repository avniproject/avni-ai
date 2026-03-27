"""
Bundle EncounterType model — matches avni-server's EncounterTypeContract.

See: avni-server/.../web/request/EncounterTypeContract.java
Inherits from: ReferenceDataContract -> CHSRequest
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class EncounterTypeContract:
    name: str
    uuid: str
    active: bool = True
    immutable: bool = False
    entity_eligibility_check_rule: Optional[str] = None
    entity_eligibility_check_declarative_rule: Optional[list[dict]] = None
    voided: bool = False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "uuid": self.uuid,
            "active": self.active,
            "immutable": self.immutable,
        }
        if self.entity_eligibility_check_rule is not None:
            d["entityEligibilityCheckRule"] = self.entity_eligibility_check_rule
        if self.entity_eligibility_check_declarative_rule is not None:
            d["entityEligibilityCheckDeclarativeRule"] = self.entity_eligibility_check_declarative_rule
        if self.voided:
            d["voided"] = self.voided
        return d
