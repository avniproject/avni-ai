"""Response contracts for bundle handler endpoints."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class BundleSummary:
    subject_types: int
    programs: int
    encounter_types: int
    address_level_types: int
    form_mappings: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_types": self.subject_types,
            "programs": self.programs,
            "encounter_types": self.encounter_types,
            "address_level_types": self.address_level_types,
            "form_mappings": self.form_mappings,
        }


@dataclass
class GenerateBundleResponse:
    session_id: str
    status: str
    bundle_summary: BundleSummary
    upload_result: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "status": self.status,
            "bundle_summary": self.bundle_summary.to_dict(),
            "upload_result": self.upload_result,
        }
