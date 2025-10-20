"""Contract classes for User operations."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class UserFindContract:
    """Contract for user search operations."""

    name: str  # Used as a query parameter for user search


@dataclass
class UserUpdateContract:
    """Contract for user update operations."""

    id: int  # Used in URL path parameter
    name: str
    username: str
    phoneNumber: str
    email: str
    organisationId: int
    catchmentId: int
