"""
See: avni-server/.../web/request/FormMappingContract.java
Inherits from: ReferenceDataContract -> CHSRequest
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class FormMappingContract:
    uuid: str
    form_uuid: str
    subject_type_uuid: str
    form_type: str
    form_name: str
    enable_approval: bool = False
    program_uuid: Optional[str] = None
    encounter_type_uuid: Optional[str] = None
    task_type_uuid: Optional[str] = None
    voided: bool = False

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "uuid": self.uuid,
            "formUUID": self.form_uuid,
            "subjectTypeUUID": self.subject_type_uuid,
            "formType": self.form_type,
            "formName": self.form_name,
            "enableApproval": self.enable_approval,
        }
        if self.program_uuid:
            d["programUUID"] = self.program_uuid
        if self.encounter_type_uuid:
            d["encounterTypeUUID"] = self.encounter_type_uuid
        if self.task_type_uuid:
            d["taskTypeUUID"] = self.task_type_uuid
        if self.voided:
            d["voided"] = self.voided
        return d
