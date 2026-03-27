"""
See: avni-server/.../web/request/SubjectTypeContract.java
Inherits from: ReferenceDataContract -> CHSRequest
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class SubjectTypeEnum(str, Enum):
    GROUP = "Group"
    HOUSEHOLD = "Household"
    INDIVIDUAL = "Individual"
    PERSON = "Person"
    USER = "User"

    @classmethod
    def from_raw(cls, raw: str) -> "SubjectTypeEnum":
        lower = raw.strip().lower()
        for member in cls:
            if member.value.lower() == lower:
                return member
        raise ValueError(f"Unknown subject type: '{raw}'. Must be one of: {[m.value for m in cls]}")


@dataclass
class SubjectTypeContract:
    name: str
    uuid: str
    type: SubjectTypeEnum
    active: bool = True
    voided: bool = False
    group: bool = False
    household: bool = False
    allow_empty_location: bool = False
    allow_middle_name: bool = False
    last_name_optional: bool = False
    allow_profile_picture: bool = False
    unique_name: bool = False
    directly_assignable: bool = False
    should_sync_by_location: bool = True
    subject_summary_rule: Optional[str] = None
    program_eligibility_check_rule: Optional[str] = None
    member_addition_eligibility_check_rule: Optional[str] = None
    program_eligibility_check_declarative_rule: Optional[list[dict]] = None
    valid_first_name_format: Optional[dict[str, str]] = None
    valid_middle_name_format: Optional[dict[str, str]] = None
    valid_last_name_format: Optional[dict[str, str]] = None
    icon_file_s3_key: Optional[str] = None
    sync_registration_concept1: Optional[str] = None
    sync_registration_concept2: Optional[str] = None
    sync_registration_concept1_usable: bool = False
    sync_registration_concept2_usable: bool = False
    name_help_text: Optional[str] = None
    settings: dict[str, Any] = field(default_factory=lambda: {
        "displayRegistrationDetails": True,
        "displayPlannedEncounters": True,
    })

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "uuid": self.uuid,
            "type": self.type,
            "active": self.active,
            "voided": self.voided,
            "group": self.group,
            "household": self.household,
            "allowEmptyLocation": self.allow_empty_location,
            "allowMiddleName": self.allow_middle_name,
            "lastNameOptional": self.last_name_optional,
            "allowProfilePicture": self.allow_profile_picture,
            "uniqueName": self.unique_name,
            "directlyAssignable": self.directly_assignable,
            "shouldSyncByLocation": self.should_sync_by_location,
            "syncRegistrationConcept1Usable": self.sync_registration_concept1_usable,
            "syncRegistrationConcept2Usable": self.sync_registration_concept2_usable,
            "settings": self.settings,
        }
        if self.subject_summary_rule is not None:
            d["subjectSummaryRule"] = self.subject_summary_rule
        if self.program_eligibility_check_rule is not None:
            d["programEligibilityCheckRule"] = self.program_eligibility_check_rule
        if self.member_addition_eligibility_check_rule is not None:
            d["memberAdditionEligibilityCheckRule"] = self.member_addition_eligibility_check_rule
        if self.program_eligibility_check_declarative_rule is not None:
            d["programEligibilityCheckDeclarativeRule"] = self.program_eligibility_check_declarative_rule
        if self.valid_first_name_format is not None:
            d["validFirstNameFormat"] = self.valid_first_name_format
        if self.valid_middle_name_format is not None:
            d["validMiddleNameFormat"] = self.valid_middle_name_format
        if self.valid_last_name_format is not None:
            d["validLastNameFormat"] = self.valid_last_name_format
        if self.icon_file_s3_key is not None:
            d["iconFileS3Key"] = self.icon_file_s3_key
        if self.sync_registration_concept1 is not None:
            d["syncRegistrationConcept1"] = self.sync_registration_concept1
        if self.sync_registration_concept2 is not None:
            d["syncRegistrationConcept2"] = self.sync_registration_concept2
        if self.name_help_text is not None:
            d["nameHelpText"] = self.name_help_text
        return d
