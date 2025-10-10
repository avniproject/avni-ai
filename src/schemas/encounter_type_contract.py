"""Contract classes for EncounterType operations."""

from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class EncounterTypeContract:
    """Contract for EncounterType creation."""

    name: str
    uuid: str  # Required for creation
    subjectTypeUuid: str
    programUuid: Optional[str] = None  # None for general encounters
    active: bool = True
    voided: bool = False
    isImmutable: bool = False
    entityEligibilityCheckRule: Optional[str] = None  # None (null) by default
    # TODO: Convert to proper structure expected by server
    entityEligibilityCheckDeclarativeRule: Optional[Any] = None


@dataclass
class EncounterTypeUpdateContract:
    """Contract for EncounterType update operations."""

    id: int  # Used in URL path parameter AND for internal search
    name: str
    subjectTypeUuid: str
    programUuid: Optional[str] = None  # None for general encounters
    active: bool = True
    voided: bool = False
    isImmutable: bool = False
    entityEligibilityCheckRule: Optional[str] = None  # None (null) by default
    # TODO: Convert to proper structure expected by server
    entityEligibilityCheckDeclarativeRule: Optional[Any] = None


@dataclass
class EncounterTypeDeleteContract:
    """Contract for EncounterType delete operations."""

    id: int
