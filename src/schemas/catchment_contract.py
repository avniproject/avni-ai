"""Contract classes for Catchment operations."""

from dataclasses import dataclass
from typing import List


@dataclass
class LocationReference:
    """Location reference in catchment."""

    id: int


@dataclass
class CatchmentContract:
    """Contract for Catchment creation."""

    name: str
    locationIds: List[int]  # Match API payload structure


@dataclass
class CatchmentUpdateContract:
    """Contract for Catchment update operations."""

    id: int  # Used in URL path parameter
    name: str
    locationIds: List[int]  # Match API payload structure
    deleteFastSync: bool = False


@dataclass
class CatchmentDeleteContract:
    """Contract for Catchment delete operations."""

    id: int
