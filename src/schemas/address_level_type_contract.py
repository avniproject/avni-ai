"""Contract classes for AddressLevelType operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressLevelTypeContract:
    """Contract for AddressLevelType creation."""

    name: str
    level: float
    parentId: Optional[int] = None  # Match API payload field name
    voided: bool = False


@dataclass
class AddressLevelTypeUpdateContract:
    """Contract for AddressLevelType update operations."""

    id: int  # Used in URL path parameter
    uuid: str  # Required in request body to identify the entity
    name: str
    level: float
    parentId: Optional[int] = None  # Match API payload field name


@dataclass
class AddressLevelTypeDeleteContract:
    """Contract for AddressLevelType delete operations."""

    id: int
