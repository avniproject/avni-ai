"""Contract classes for Location operations."""

from dataclasses import dataclass, field
from typing import List
from typing import Optional

@dataclass
class LocationParent:
    """Parent reference in location hierarchy."""

    id: int


@dataclass
class LocationContract:
    """Contract for Location creation."""

    name: str
    level: int
    type: str  # addressLevelType name
    parents: List[LocationParent] = field(default_factory=list)


@dataclass
class LocationUpdateContract:
    """Contract for Location update operations."""

    id: int  # Used in URL path parameter AND in request body
    title: str  # API uses 'title' for updates
    level: int
    parentId: Optional[int] = None


@dataclass
class LocationDeleteContract:
    """Contract for Location delete operations."""

    id: int
