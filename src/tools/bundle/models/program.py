"""
See: avni-server/.../web/request/ProgramRequest.java
     avni-server/.../web/request/ProgramContract.java
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ProgramContract:
    name: str
    uuid: str
    colour: str
    active: bool = True
    voided: bool = False
    enrolment_eligibility_check_rule: Optional[str] = None
    enrolment_summary_rule: Optional[str] = None
    enrolment_eligibility_check_declarative_rule: Optional[list[dict]] = None
    manual_eligibility_check_required: bool = False
    show_growth_chart: bool = False
    manual_enrolment_eligibility_check_rule: Optional[str] = None
    manual_enrolment_eligibility_check_declarative_rule: Optional[list[dict]] = None
    allow_multiple_enrolments: bool = False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "uuid": self.uuid,
            "colour": self.colour,
            "voided": self.voided,
            "active": self.active,
            "manualEligibilityCheckRequired": self.manual_eligibility_check_required,
            "showGrowthChart": self.show_growth_chart,
            "allowMultipleEnrolments": self.allow_multiple_enrolments,
        }
        if self.enrolment_eligibility_check_rule is not None:
            d["enrolmentEligibilityCheckRule"] = self.enrolment_eligibility_check_rule
        if self.enrolment_summary_rule is not None:
            d["enrolmentSummaryRule"] = self.enrolment_summary_rule
        if self.enrolment_eligibility_check_declarative_rule is not None:
            d["enrolmentEligibilityCheckDeclarativeRule"] = self.enrolment_eligibility_check_declarative_rule
        if self.manual_enrolment_eligibility_check_rule is not None:
            d["manualEnrolmentEligibilityCheckRule"] = self.manual_enrolment_eligibility_check_rule
        if self.manual_enrolment_eligibility_check_declarative_rule is not None:
            d["manualEnrolmentEligibilityCheckDeclarativeRule"] = self.manual_enrolment_eligibility_check_declarative_rule
        return d
