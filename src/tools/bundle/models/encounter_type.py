"""
Bundle EncounterType model — matches avni-server's EncounterType domain entity.

See: avni-server/.../domain/EncounterType.java
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class BundleEncounterType:
    name: str
    uuid: str
    active: bool = True
    immutable: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize to the JSON format expected by Avni's importMetaData endpoint."""
        return {
            "name": self.name,
            "uuid": self.uuid,
            "entityEligibilityCheckRule": "",
            "active": self.active,
            "immutable": self.immutable,
        }
