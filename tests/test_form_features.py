"""
Tests for form generation features: skip logic detection, MultiSelect, QG/RQG, readOnly.
"""

from pathlib import Path

import pytest

from src.bundle.scoping_parser import parse_scoping_docs, _detect_skip_logic_patterns
from src.bundle.forms import FormGenerator
from src.schemas.bundle_models import FieldSpec

_MAZI_FILES = [
    Path("tests/resources/scoping/Mazi Saheli Charitable Trust Scoping .xlsx"),
    Path("tests/resources/scoping/Mazi Saheli Charitable Trust Modelling.xlsx"),
]

pytestmark = pytest.mark.skipif(
    not all(f.exists() for f in _MAZI_FILES),
    reason="Mazi Saheli resource files not present",
)


@pytest.fixture(scope="module")
def mazi_spec():
    spec, _ = parse_scoping_docs([str(f) for f in _MAZI_FILES])
    return spec


class TestSkipLogicDetection:
    """Auto-detection of skip logic patterns from field relationships."""

    def test_others_pattern_detected(self, mazi_spec):
        """'Specify Details - Others' should depend on 'Activity Type' = 'Others'."""
        form = next(f for f in mazi_spec.forms if "Activity Registration" in f.name)
        field = next(f for f in form.fields if "Specify Details" in f.name)
        assert field.skipLogic is not None
        assert field.skipLogic.dependsOn == "Activity Type"
        assert field.skipLogic.value == "Others"

    def test_subtype_pattern_detected(self, mazi_spec):
        """'Health Activity Sub-Type' should depend on 'Activity Type' = 'Health'."""
        form = next(f for f in mazi_spec.forms if "Activity Registration" in f.name)
        field = next(f for f in form.fields if "Health Activity Sub-Type" in f.name)
        assert field.skipLogic is not None
        assert field.skipLogic.dependsOn == "Activity Type"
        assert field.skipLogic.value == "Health"

    def test_others_pattern_in_activity_summary(self, mazi_spec):
        """'Specify details - Others' in Activity Summary depends on 'Initiative' = 'Other'."""
        form = next(f for f in mazi_spec.forms if "Activity Summary" in f.name)
        field = next(f for f in form.fields if "Specify details" in f.name)
        assert field.skipLogic is not None
        assert field.skipLogic.dependsOn == "Initiative"

    def test_no_false_skip_logic(self, mazi_spec):
        """Fields that shouldn't have skip logic don't get any."""
        form = next(f for f in mazi_spec.forms if "Activity Registration" in f.name)
        for field in form.fields:
            if field.name in ("Activity Type", "Distribution Type", "Number of Days"):
                assert field.skipLogic is None, (
                    f"'{field.name}' should not have skip logic"
                )


class TestSkipLogicPatternDetector:
    """Unit tests for _detect_skip_logic_patterns."""

    def test_others_pattern(self):
        fields = [
            FieldSpec(
                name="Blood Group", dataType="Coded", options=["A+", "B+", "Others"]
            ),
            FieldSpec(name="Specify Blood Group", dataType="Text"),
        ]
        _detect_skip_logic_patterns(fields)
        assert fields[1].skipLogic is not None
        assert fields[1].skipLogic.dependsOn == "Blood Group"
        assert fields[1].skipLogic.value == "Others"

    def test_yes_no_detail_pattern(self):
        fields = [
            FieldSpec(
                name="Has Complications", dataType="Coded", options=["Yes", "No"]
            ),
            FieldSpec(name="Complication Details", dataType="Text"),
        ]
        _detect_skip_logic_patterns(fields)
        assert fields[1].skipLogic is not None
        assert fields[1].skipLogic.dependsOn == "Has Complications"
        assert fields[1].skipLogic.value == "Yes"

    def test_no_skip_logic_on_first_field(self):
        fields = [
            FieldSpec(name="Name", dataType="Text"),
            FieldSpec(name="Age", dataType="Numeric"),
        ]
        _detect_skip_logic_patterns(fields)
        assert fields[0].skipLogic is None
        assert fields[1].skipLogic is None


class TestMultiSelectSupport:
    """Form elements should use MultiSelect when specified."""

    def test_multiselect_type(self):
        fg = FormGenerator()
        fg.concept_map = {
            "Training Type": {"uuid": "abc", "dataType": "Coded", "answers": []}
        }
        fg.form_uuid = "test"
        field = {
            "name": "Training Type",
            "selectionType": "MultiSelect",
            "dataType": "Coded",
        }
        elements = fg._generate_form_element(field, 1.0)
        assert len(elements) == 1
        assert elements[0]["type"] == "MultiSelect"

    def test_default_single_select(self):
        fg = FormGenerator()
        concepts = {"Gender": {"uuid": "abc", "dataType": "Coded", "answers": []}}
        fg.concept_map = concepts
        fg.form_uuid = "test"
        field = {"name": "Gender", "dataType": "Coded"}
        elements = fg._generate_form_element(field, 1.0)
        assert elements[0]["type"] == "SingleSelect"

    def test_none_selection_type_defaults(self):
        fg = FormGenerator()
        fg.concept_map = {"X": {"uuid": "abc", "dataType": "Coded"}}
        fg.form_uuid = "test"
        field = {"name": "X", "selectionType": None}
        elements = fg._generate_form_element(field, 1.0)
        assert elements[0]["type"] == "SingleSelect"


class TestReadOnlyKeyValues:
    """ReadOnly fields should have keyValues with editable=false."""

    def test_readonly_keyvalue(self):
        fg = FormGenerator()
        fg.concept_map = {"BMI": {"uuid": "abc", "dataType": "Numeric"}}
        fg.form_uuid = "test"
        field = {"name": "BMI", "readOnly": True}
        elements = fg._generate_form_element(field, 1.0)
        kv = elements[0]["keyValues"]
        assert any(k["key"] == "editable" and k["value"] is False for k in kv)

    def test_non_readonly_no_keyvalue(self):
        fg = FormGenerator()
        fg.concept_map = {"Weight": {"uuid": "abc", "dataType": "Numeric"}}
        fg.form_uuid = "test"
        field = {"name": "Weight", "readOnly": False}
        elements = fg._generate_form_element(field, 1.0)
        kv = elements[0]["keyValues"]
        assert not any(k.get("key") == "editable" for k in kv)


class TestQuestionGroupGeneration:
    """QuestionGroup and Repeatable QG form element generation."""

    def test_question_group_creates_parent_and_children(self):
        fg = FormGenerator()
        fg.concept_map = {
            "Blood Pressure": {"uuid": "bp-uuid", "dataType": "QuestionGroup"},
            "Systolic": {"uuid": "sys-uuid", "dataType": "Numeric"},
            "Diastolic": {"uuid": "dia-uuid", "dataType": "Numeric"},
        }
        fg.form_uuid = "test"
        field = {
            "name": "Blood Pressure",
            "dataType": "QuestionGroup",
            "isQuestionGroup": True,
            "isRepeatable": False,
            "children": [
                {"name": "Systolic", "dataType": "Numeric"},
                {"name": "Diastolic", "dataType": "Numeric"},
            ],
        }
        elements = fg._generate_form_element(field, 3.0)
        assert len(elements) == 3  # parent + 2 children
        assert elements[0]["concept"]["dataType"] == "QuestionGroup"
        assert elements[1]["displayOrder"] == 3.1
        assert elements[2]["displayOrder"] == 3.2
        # Non-repeatable: no parentFormElementUuid
        assert "parentFormElementUuid" not in elements[1]

    def test_repeatable_qg_has_keyvalue_and_parent_link(self):
        fg = FormGenerator()
        fg.concept_map = {
            "Child Details": {"uuid": "cd-uuid", "dataType": "QuestionGroup"},
            "Child Name": {"uuid": "cn-uuid", "dataType": "Text"},
            "Child Age": {"uuid": "ca-uuid", "dataType": "Numeric"},
        }
        fg.form_uuid = "test"
        field = {
            "name": "Child Details",
            "dataType": "QuestionGroup",
            "isQuestionGroup": True,
            "isRepeatable": True,
            "children": [
                {"name": "Child Name", "dataType": "Text"},
                {"name": "Child Age", "dataType": "Numeric"},
            ],
        }
        elements = fg._generate_form_element(field, 5.0)
        assert len(elements) == 3
        # Parent has repeatable keyValue
        parent_kv = elements[0]["keyValues"]
        assert any(k["key"] == "repeatable" and k["value"] is True for k in parent_kv)
        # Children have parentFormElementUuid
        assert elements[1]["parentFormElementUuid"] == elements[0]["uuid"]
        assert elements[2]["parentFormElementUuid"] == elements[0]["uuid"]


class TestDeclarativeRuleGeneration:
    """Skip logic: skipLogic field should NOT produce declarativeRule.

    New skip logic is generated as JS FormElementRules by the rules agent.
    Only pre-existing declarativeRule from bundles should pass through.
    """

    def test_skip_logic_does_not_generate_declarative_rule(self):
        fg = FormGenerator()
        fg.concept_map = {
            "Activity Type": {
                "uuid": "at-uuid",
                "dataType": "Coded",
                "answers": [
                    {"name": "Health", "uuid": "h-uuid"},
                    {"name": "Others", "uuid": "o-uuid"},
                ],
            },
            "Specify Details": {"uuid": "sd-uuid", "dataType": "Text"},
        }
        fg.form_uuid = "test"
        fg.form_type = "Encounter"
        field = {
            "name": "Specify Details",
            "skipLogic": {
                "dependsOn": "Activity Type",
                "condition": "containsAnswerConceptName",
                "value": "Others",
            },
        }
        elements = fg._generate_form_element(field, 2.0)
        assert "declarativeRule" not in elements[0]

    def test_existing_declarative_rule_passes_through(self):
        fg = FormGenerator()
        fg.concept_map = {
            "Specify Details": {"uuid": "sd-uuid", "dataType": "Text"},
        }
        fg.form_uuid = "test"
        fg.form_type = "Encounter"
        existing_rule = [
            {"actions": [{"actionType": "showFormElement"}], "conditions": []}
        ]
        field = {
            "name": "Specify Details",
            "declarativeRule": existing_rule,
        }
        elements = fg._generate_form_element(field, 2.0)
        assert "declarativeRule" in elements[0]
        assert elements[0]["declarativeRule"] == existing_rule
