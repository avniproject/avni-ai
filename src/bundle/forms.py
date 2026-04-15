"""
Form generator — produces AVNI form JSON from fields + concepts.
Supports: MultiSelect, QuestionGroup, Repeatable QG, skip logic (declarativeRule),
readOnly (keyValues.editable=false), mandatory, lowAbsolute/highAbsolute.
"""

from __future__ import annotations

from .uuid_utils import generate_deterministic_uuid


class FormGenerator:
    def __init__(self) -> None:
        self.concept_map: dict[str, dict] = {}  # name -> {uuid, dataType, answers}
        self.form_uuid: str | None = None
        self.form_type: str | None = None

    # ── Element type resolution ────────────────────────────────────

    @staticmethod
    def _get_element_type(data_type: str, field: dict) -> str:
        """Determine SingleSelect vs MultiSelect for form elements."""
        if data_type == "Coded":
            sel = (field.get("selectionType") or "").lower()
            if sel in ("multiselect", "multi-select", "multi select", "checkbox"):
                return "MultiSelect"
        return "SingleSelect"

    # ── Skip logic → declarative rule ───────────────────────────────

    def _build_declarative_rule(
        self, skip_logic: dict, scope: str = "encounter"
    ) -> list[dict] | None:
        if not skip_logic:
            return None

        depends_on = skip_logic.get("dependsOn")
        condition = skip_logic.get("condition", "")
        value = skip_logic.get("value", "")

        depends_concept = self.concept_map.get(depends_on)
        if not depends_concept:
            return None

        # Build LHS
        lhs = {
            "type": "concept",
            "scope": scope,
            "conceptName": depends_on,
            "conceptUuid": depends_concept["uuid"],
            "conceptDataType": depends_concept.get("dataType", "Coded"),
        }

        # Build RHS based on condition type
        if condition in ("containsAnswerConceptName", "equals", "contains", "="):
            answers = depends_concept.get("answers") or []
            answer_match = next(
                (a for a in answers if a["name"].lower() == value.lower()), None
            )
            rhs = {
                "type": "answerConcept",
                "answerConceptNames": [value],
                "answerConceptUuids": [answer_match["uuid"]] if answer_match else [],
            }
            operator = "containsAnswerConceptName"
        elif condition in ("defined", "notDefined"):
            rhs = {"type": "value", "value": None}
            operator = condition
        elif condition in (
            "greaterThan",
            "lessThan",
            "greaterThanOrEqualTo",
            "lessThanOrEqualTo",
        ):
            rhs = {"type": "value", "value": value}
            operator = condition
        else:
            # Fallback: treat as containsAnswerConceptName
            rhs = {
                "type": "answerConcept",
                "answerConceptNames": [value],
            }
            operator = "containsAnswerConceptName"

        return [
            {
                "actions": [{"actionType": "showFormElement"}],
                "conditions": [
                    {
                        "compoundRule": {
                            "rules": [{"lhs": lhs, "rhs": rhs, "operator": operator}]
                        }
                    }
                ],
            }
        ]

    # ── Form element ────────────────────────────────────────────────

    def _generate_form_element(
        self,
        field: dict,
        display_order: float,
        parent_element_uuid: str | None = None,
    ) -> list[dict]:
        """Generate one or more form elements for a field.
        Returns a list because QG fields produce parent + children."""
        concept = self.concept_map.get(field["name"])
        if not concept:
            return []

        data_type = concept.get("dataType", "Text")
        element_uuid = generate_deterministic_uuid(
            f"element:{self.form_uuid}:{field['name']}"
        )

        # Build keyValues
        key_values = []
        if field.get("readOnly"):
            key_values.append({"key": "editable", "value": False})
        if field.get("isQuestionGroup") and field.get("isRepeatable"):
            key_values.append({"key": "repeatable", "value": True})

        element: dict = {
            "name": field["name"],
            "uuid": element_uuid,
            "keyValues": key_values,
            "concept": {
                "name": field["name"],
                "uuid": concept["uuid"],
                "dataType": data_type,
                "active": True,
            },
            "displayOrder": display_order,
            "type": self._get_element_type(data_type, field),
            "mandatory": field.get("mandatory", False),
            "voided": False,
        }

        # Add parent link for RQG children
        if parent_element_uuid:
            element["parentFormElementUuid"] = parent_element_uuid

        # Add answers for Coded concepts
        if data_type == "Coded" and concept.get("answers"):
            element["concept"]["answers"] = concept["answers"]

        # Add numeric bounds
        if data_type == "Numeric":
            if field.get("min") is not None:
                element["lowAbsolute"] = field["min"]
            if field.get("max") is not None:
                element["highAbsolute"] = field["max"]

        # Add declarative rule (skip logic)
        skip_logic = field.get("skipLogic")
        if skip_logic:
            scope = "enrolment" if self.form_type == "ProgramEnrolment" else "encounter"
            decl = self._build_declarative_rule(skip_logic, scope)
            if decl:
                element["declarativeRule"] = decl

        elements = [element]

        # Handle QuestionGroup children
        if field.get("isQuestionGroup") and field.get("children"):
            children = field["children"]
            for child_idx, child_field in enumerate(children):
                child_order = display_order + (child_idx + 1) * 0.1
                # RQG children need parentFormElementUuid
                parent_uuid = element_uuid if field.get("isRepeatable") else None
                child_elements = self._generate_form_element(
                    child_field, child_order, parent_element_uuid=parent_uuid
                )
                elements.extend(child_elements)

        return elements

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
        group_uuid = generate_deterministic_uuid(f"group:{self.form_uuid}:{group_name}")
        elements = []
        for idx, field in enumerate(fields):
            field_elements = self._generate_form_element(field, idx + 1)
            elements.extend(field_elements)
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
                            "voided": False,
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
