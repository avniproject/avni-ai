"""
Org registry for emulation tests.

Centralises the mapping of organisation names to their SRS files,
modelling files, reference bundle ZIPs, and expected minimum entity counts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

SCOPING_DIR = Path(__file__).resolve().parents[1] / "resources" / "scoping"


@dataclass
class OrgConfig:
    """Configuration for a single organisation used in emulation tests."""

    org_id: str
    org_name: str
    srs_files: List[str] = field(default_factory=list)
    modelling_files: List[str] = field(default_factory=list)
    bundle_zip: str = ""
    sector: str = "health"
    min_subject_types: int = 1
    min_programs: int = 0
    min_encounter_types: int = 0

    # ── Path helpers ────────────────────────────────────────────────

    def srs_paths(self) -> List[Path]:
        """Absolute paths to SRS files."""
        return [SCOPING_DIR / f for f in self.srs_files]

    def modelling_paths(self) -> List[Path]:
        """Absolute paths to modelling files."""
        return [SCOPING_DIR / f for f in self.modelling_files]

    def bundle_zip_path(self) -> Path:
        """Absolute path to the reference bundle ZIP."""
        return SCOPING_DIR / self.bundle_zip

    def all_input_paths(self) -> List[Path]:
        """SRS + modelling paths combined, for passing to the parser."""
        return self.srs_paths() + self.modelling_paths()


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ALL_ORGS: List[OrgConfig] = [
    OrgConfig(
        org_id="astitva",
        org_name="Astitva",
        srs_files=["Astitva SRS .xlsx"],
        modelling_files=[],
        bundle_zip="Astitva UAT.zip",
        sector="health",
        min_subject_types=1,
        min_programs=1,
        min_encounter_types=1,
    ),
    OrgConfig(
        org_id="durga",
        org_name="Durga",
        srs_files=["Durga India Scoping Document.xlsx"],
        modelling_files=["Durga India Modelling.xlsx"],
        bundle_zip="Durga India Uat.zip",
        sector="health",
        min_subject_types=1,
        min_programs=1,
        min_encounter_types=1,
    ),
    OrgConfig(
        org_id="kshamata",
        org_name="Kshamata",
        srs_files=["Kshamata Scoping Document .xlsx"],
        modelling_files=["Kshamata Modelling.xlsx"],
        bundle_zip="kshmata_launchpad.zip",
        sector="health",
        min_subject_types=1,
        min_programs=1,
        min_encounter_types=1,
    ),
    OrgConfig(
        org_id="mazisaheli",
        org_name="MaziSaheli",
        srs_files=["Mazi Saheli Charitable Trust Scoping .xlsx"],
        modelling_files=["Mazi Saheli Charitable Trust Modelling.xlsx"],
        bundle_zip="Mazi Saheli UAT.zip",
        sector="health",
        min_subject_types=1,
        min_programs=1,
        min_encounter_types=1,
    ),
    OrgConfig(
        org_id="yenepoya",
        org_name="Yenepoya",
        srs_files=["Yenepoya_SRS.xlsx"],
        modelling_files=[],
        bundle_zip="Yenepoya.zip",
        sector="health",
        min_subject_types=1,
        min_programs=0,
        min_encounter_types=0,
    ),
]

# Lookup by org_id for convenience
ORG_BY_ID: dict[str, OrgConfig] = {o.org_id: o for o in ALL_ORGS}
ORG_BY_NAME: dict[str, OrgConfig] = {o.org_name: o for o in ALL_ORGS}
