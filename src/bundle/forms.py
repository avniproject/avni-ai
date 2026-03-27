"""
Form generator — produces AVNI form JSON from fields + concepts.
Ported from srs-bundle-generator/generators/forms.js.
"""

from __future__ import annotations

from .uuid_utils import generate_deterministic_uuid

# All AVNI data types map to SingleSelect in the form element
_ELEMENT_TYPE_MAP: dict[str, str] = {
    "Coded": "SingleSelect",
    "Numeric": "SingleSelect",
    "Text": "SingleSelect",
    "Date": "SingleSelect",
    "DateTime": "SingleSelect",
    "Notes": "SingleSelect",
    "ImageV2": "SingleSelect",
    "Image": "SingleSelect",
    "File": "SingleSelect",
    "Audio": "SingleSelect",
    "Video": "SingleSelect",
    "PhoneNumber": "SingleSelect",
    "Location": "SingleSelect",
    "Duration": "Duration",
    "QuestionGroup": "SingleSelect",
}


class FormGenerator:
    def __init__(self) -> None:
        self.concept_map: dict[str, dict] = {}  # name -> {uuid, dataType, answers}
        self.form_uuid: str | None = None
        self.form_type: str | None = None

    # ── Skip logic → declarative rule ───────────────────────────────

    def _build_declarative_rule(self, skip_logic: dict, scope: str = "encounter") -> list[dict] | None:
        if not skip_logic or skip_logic.get("raw"):
            return None
        depends_on = skip_logic.get("dependsOn")
        depends_concept = self.concept_map.get(depends_on)
        if not depends_concept:
            return None

        rhs: dict = {}
        if skip_logic.get("condition") in ("equals", "contains"):
            value = skip_logic.get("value", "")
            answers = depends_concept.get("answers") or []
            answer_match = next(
                (a for a in answers if a["name"].lower() == value.lower()), None
            )
            rhs = {
                "type": "answerConcept",
                "answerConceptNames": [value],
                "answerConceptUuids": [answer_match["uuid"]] if answer_match else [],
            }

        return [
            {
                "actions": [{"actionType": "showFormElement"}],
                "conditions": [
                    {
                        "compoundRule": {
                            "rules": [
                                {
                                    "lhs": {
                                        "type": "concept",
                                        "scope": scope,
                                        "conceptName": depends_on,
                                        "conceptUuid": depends_concept["uuid"],
                                    },
                                    "rhs": rhs,
                                    "operator": "containsAnswerConceptName",
                                }
                            ]
                        }
                    }
                ],
            }
        ]

    # ── Form element ────────────────────────────────────────────────

    def _generate_form_element(self, field: dict, display_order: int) -> dict | None:
        concept = self.concept_map.get(field["name"])
        if not concept:
            return None

        element_uuid = generate_deterministic_uuid(
            f"element:{self.form_uuid}:{field['name']}"
        )
        data_type = concept.get("dataType", "Text")
        element: dict = {
            "name": field["name"],
            "uuid": element_uuid,
            "keyValues": [],
            "concept": {
                "name": field["name"],
                "uuid": concept["uuid"],
                "dataType": data_type,
                "active": True,
            },
            "displayOrder": display_order,
            "type": _ELEMENT_TYPE_MAP.get(data_type, "SingleSelect"),
            "mandatory": field.get("mandatory", False),
        }

        skip_logic = field.get("skipLogic")
        if skip_logic and not skip_logic.get("raw"):
            scope = "enrolment" if self.form_type == "ProgramEnrolment" else "encounter"
            decl = self._build_declarative_rule(skip_logic, scope)
            if decl:
                element["declarativeRule"] = decl

        return element

    # ── Grouping ────────────────────────────────────────────────────

    @staticmethod
    def _group_fields_by_section(fields: list[dict]) -> dict[str, list[dict]]:
        groups: dict[str, list[dict]] = {}
        no_group: list[dict] = []
        for field in fields:
            g = field.get("group")
            if g:
                groups.setdefault(g, []).append(field)
            else:
                no_group.append(field)
        if no_group:
            groups["General Information"] = no_group
        return groups

    def _generate_form_element_group(
        self, group_name: str, fields: list[dict], display_order: int
    ) -> dict:
        group_uuid = generate_deterministic_uuid(
            f"group:{self.form_uuid}:{group_name}"
        )
        elements = []
        for idx, field in enumerate(fields):
            elem = self._generate_form_element(field, idx + 1)
            if elem:
                elements.append(elem)
        return {
            "uuid": group_uuid,
            "name": group_name,
            "displayOrder": display_order,
            "formElements": elements,
            "timed": False,
        }

    # ── Public API ──────────────────────────────────────────────────

    def generate_form(
        self,
        name: str,
        form_type: str,
        fields: list[dict],
        concepts: dict[str, dict],
    ) -> dict:
        self.form_type = form_type
        self.form_uuid = generate_deterministic_uuid(f"form:{name}")
        self.concept_map = concepts

        grouped = self._group_fields_by_section(fields)
        form_element_groups = [
            self._generate_form_element_group(gname, gfields, idx + 1)
            for idx, (gname, gfields) in enumerate(grouped.items())
        ]

        return {
            "name": name,
            "uuid": self.form_uuid,
            "formType": form_type,
            "formElementGroups": form_element_groups,
            "decisionRule": "",
            "visitScheduleRule": "",
            "validationRule": "",
            "checklistsRule": "",
            "decisionConcepts": [],
        }

    def generate_cancellation_form(self, encounter_name: str, form_type: str) -> dict:
        cancellation_type = (
            "ProgramEncounterCancellation"
            if form_type == "ProgramEncounter"
            else "IndividualEncounterCancellation"
        )
        form_name = f"{encounter_name} Cancellation"
        self.form_uuid = generate_deterministic_uuid(f"form:{form_name}")

        return {
            "name": form_name,
            "uuid": self.form_uuid,
            "formType": cancellation_type,
            "formElementGroups": [
                {
                    "uuid": generate_deterministic_uuid(
                        f"group:{self.form_uuid}:cancellation"
                    ),
                    "name": "Cancellation Details",
                    "displayOrder": 1,
                    "formElements": [
                        {
                            "name": "Cancellation Reason",
                            "uuid": generate_deterministic_uuid(
                                f"element:{self.form_uuid}:cancellation_reason"
                            ),
                            "keyValues": [],
                            "concept": {
                                "name": f"{encounter_name} cancellation reason",
                                "uuid": generate_deterministic_uuid(
                                    f"concept:{encounter_name}_cancellation_reason"
                                ),
                                "dataType": "Text",
                                "active": True,
                            },
                            "displayOrder": 1,
                            "type": "SingleSelect",
                            "mandatory": True,
                        }
                    ],
                    "timed": False,
                }
            ],
            "decisionRule": "",
            "visitScheduleRule": "",
            "validationRule": "",
            "checklistsRule": "",
            "decisionConcepts": [],
        }
