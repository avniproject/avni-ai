"""
See: avni-server/.../web/request/AddressLevelTypeContract.java
Inherits from: ReferenceDataContract -> CHSRequest
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AddressLevelTypeContract:
    name: str
    uuid: str
    level: float
    parent: Optional[dict[str, str]] = None
    voided: bool = False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "uuid": self.uuid,
            "name": self.name,
            "level": self.level,
        }
        if self.parent:
            d["parent"] = self.parent
        if self.voided:
            d["voided"] = self.voided
        return d
