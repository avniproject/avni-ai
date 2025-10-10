"""Contract classes for Program operations."""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ProgramContract:
    """Contract for Program creation."""

    name: str
    uuid: str  # Required for creation
    colour: str
    subjectTypeUuid: str
    programSubjectLabel: Optional[str] = None
    enrolmentSummaryRule: Optional[str] = None
    enrolmentEligibilityCheckRule: Optional[str] = None
    # TODO: Convert to proper structure expected by server
    enrolmentEligibilityCheckDeclarativeRule: Optional[Dict[str, Any]] = None
    manualEligibilityCheckRequired: bool = False
    showGrowthChart: bool = False
    manualEnrolmentEligibilityCheckRule: bool = False  # Boolean field
    # TODO: Convert to proper structure expected by server
    manualEnrolmentEligibilityCheckDeclarativeRule: Optional[Dict[str, Any]] = None
    allowMultipleEnrolments: bool = False
    programEnrolmentFormUuid: Optional[str] = None
    programExitFormUuid: Optional[str] = None
    active: bool = True
    voided: bool = False


@dataclass
class ProgramUpdateContract:
    """Contract for Program update operations."""

    id: int  # Used in URL path parameter AND for searching the program
    name: str
    colour: str
    subjectTypeUuid: str
    programSubjectLabel: Optional[str] = None
    enrolmentSummaryRule: Optional[str] = None
    enrolmentEligibilityCheckRule: Optional[str] = None
    # TODO: Convert to proper structure expected by server
    enrolmentEligibilityCheckDeclarativeRule: Optional[Dict[str, Any]] = None
    manualEligibilityCheckRequired: bool = False
    showGrowthChart: bool = False
    manualEnrolmentEligibilityCheckRule: bool = False  # Boolean field
    # TODO: Convert to proper structure expected by server
    manualEnrolmentEligibilityCheckDeclarativeRule: Optional[Dict[str, Any]] = None
    allowMultipleEnrolments: bool = False
    programEnrolmentFormUuid: Optional[str] = None
    programExitFormUuid: Optional[str] = None
    active: bool = True
    voided: bool = False


@dataclass
class ProgramDeleteContract:
    """Contract for Program delete operations."""

    id: int
