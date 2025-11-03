"""Contract classes for SubjectType operations."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class GroupRole:
    """Group role definition within subject type."""

    subjectMemberName: str
    groupRoleUUID: str
    groupSubjectTypeUUID: str
    memberSubjectTypeUUID: str
    role: str
    minimumNumberOfMembers: int
    maximumNumberOfMembers: int
    isPrimary: bool = False
    voided: bool = False


@dataclass
class SubjectTypeSettings:
    """Settings for subject type."""

    displayRegistrationDetails: bool = True
    displayPlannedEncounters: bool = True


@dataclass
class SubjectTypeContract:
    """Contract for SubjectType creation."""

    name: str
    uuid: str  # Required for creation
    type: str  # Person, Individual, Group, Household, User
    active: bool = True
    voided: bool = False
    group: bool = False
    household: bool = False
    allowEmptyLocation: bool = True
    allowMiddleName: bool = False
    lastNameOptional: bool = False
    allowProfilePicture: bool = False
    uniqueName: bool = False
    directlyAssignable: bool = False
    shouldSyncByLocation: bool = True
    settings: SubjectTypeSettings = field(default_factory=SubjectTypeSettings)
    subjectSummaryRule: Optional[str] = None
    programEligibilityCheckRule: Optional[str] = None
    memberAdditionEligibilityCheckRule: Optional[str] = None
    # TODO: Convert to proper validation structure expected by server for validFirstNameFormat, validMiddleNameFormat, validLastNameFormat
    validFirstNameFormat: Optional[Dict[str, Any]] = None
    validMiddleNameFormat: Optional[Dict[str, Any]] = None
    validLastNameFormat: Optional[Dict[str, Any]] = None
    iconFileS3Key: Optional[str] = None
    syncRegistrationConcept1: Optional[str] = None
    syncRegistrationConcept2: Optional[str] = None
    nameHelpText: Optional[str] = None
    groupRoles: List[GroupRole] = field(default_factory=list)
    registrationFormUuid: Optional[str] = None  # None for creation


@dataclass
class SubjectTypeUpdateContract:
    """Contract for SubjectType update operations."""

    id: int  # Used in URL path parameter
    name: str
    # uuid not required for updates
    type: str
    active: bool = True
    voided: bool = False
    group: bool = False
    household: bool = False
    allowEmptyLocation: bool = True
    allowMiddleName: bool = False
    lastNameOptional: bool = False
    allowProfilePicture: bool = False
    uniqueName: bool = False
    directlyAssignable: bool = False
    shouldSyncByLocation: bool = True
    settings: SubjectTypeSettings = field(default_factory=SubjectTypeSettings)
    subjectSummaryRule: Optional[str] = None
    programEligibilityCheckRule: Optional[str] = None
    memberAdditionEligibilityCheckRule: Optional[str] = None
    # TODO: Convert to proper validation structure expected by server for validFirstNameFormat, validMiddleNameFormat, validLastNameFormat
    validFirstNameFormat: Optional[Dict[str, Any]] = None
    validMiddleNameFormat: Optional[Dict[str, Any]] = None
    validLastNameFormat: Optional[Dict[str, Any]] = None
    iconFileS3Key: Optional[str] = None
    syncRegistrationConcept1: Optional[str] = None
    syncRegistrationConcept2: Optional[str] = None
    nameHelpText: Optional[str] = None
    groupRoles: List[GroupRole] = field(default_factory=list)
    registrationFormUuid: Optional[str] = None


@dataclass
class SubjectTypeDeleteContract:
    """Contract for SubjectType delete operations."""

    id: int
