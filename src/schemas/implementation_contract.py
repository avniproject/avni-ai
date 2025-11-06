"""Contract classes for Implementation operations."""

from dataclasses import dataclass


@dataclass
class ImplementationDeleteContract:
    """Contract for Implementation deletion."""

    deleteMetadata: bool
    deleteAdminConfig: bool
