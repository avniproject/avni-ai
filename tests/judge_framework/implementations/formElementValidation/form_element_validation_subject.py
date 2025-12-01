"""
Correct Form Element Validation test subject implementations based on actual Dify workflow
"""

from typing import Dict, List, Any
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.test_subject import (
    TestSubject,
    TestSubjectFactory,
)
from tests.judge_framework.interfaces.result_models import TestConfiguration


class FormElementValidationTestSubject(TestSubject):
    """
    Test subject for form element validation that matches the actual Dify workflow
    """

    def __init__(self, form_test_case: Dict[str, Any], config: TestConfiguration):
        super().__init__(form_test_case, config)
        self.form_element = form_test_case.get("form_element", {})
        self.form_context = form_test_case.get("form_context", {})
        self.test_case_name = form_test_case.get("test_case_name", "")
        self.expected_issues = form_test_case.get("expected_issues", [])

    def get_test_identifier(self) -> str:
        """Get unique identifier for this form validation test"""
        element_name = self.form_element.get("name", "unnamed")
        return f"form_validation_{element_name.replace(' ', '_').lower()}_{self.test_case_name}"

    def get_test_input(self) -> Dict[str, Any]:
        """Get input data for form validation execution"""
        return {
            "form_element": self.form_element,
            "form_context": self.form_context,
            "auth_token": self._get_auth_token(),
            "org_name": "Social Welfare Foundation Trust",
            "org_type": "trial",
            "user_name": "Arjun",
            "avni_mcp_server_url": self._get_mcp_server_url(),
        }

    def get_expected_behavior(self) -> str:
        """Get description of expected behavior for evaluation"""
        if self.expected_issues:
            return f"System should identify these issues: {', '.join(self.expected_issues)}"
        else:
            return f"System should validate {self.form_element.get('name', 'form element')} correctly"

    def get_evaluation_context(self) -> Dict[str, Any]:
        """Get additional context needed for evaluation"""
        return {
            "test_case_name": self.test_case_name,
            "form_element_name": self.form_element.get("name", ""),
            "form_element_type": self.form_element.get("type", ""),
            "form_element_datatype": self.form_element.get("concept", {}).get(
                "dataType", ""
            ),
            "test_type": "form_validation",
            "expected_issues": self.expected_issues,
        }

    def _get_auth_token(self) -> str:
        """Get auth token from environment"""
        import os

        return os.getenv("AVNI_AUTH_TOKEN", "")

    def _get_mcp_server_url(self) -> str:
        """Get MCP server URL from environment"""
        import os

        return os.getenv("AVNI_MCP_SERVER_URL", "")


class FormElementValidationTestSubjectFactory(TestSubjectFactory):
    """
    Factory for creating form element validation test subjects
    """

    def __init__(self, form_test_cases: List[Dict[str, Any]]):
        self.form_test_cases = form_test_cases

    def create_from_static_data(
        self, static_case: Dict[str, Any], config: TestConfiguration
    ) -> TestSubject:
        """Create form validation test subject from static test case"""
        return FormElementValidationTestSubject(static_case, config)

    def create_from_ai_generation(
        self, ai_case_data: Dict[str, Any], config: TestConfiguration
    ) -> TestSubject:
        """Create form validation test subject from AI-generated test case"""
        return FormElementValidationTestSubject(ai_case_data, config)

    def get_generation_prompt_template(self) -> str:
        """Get the prompt template for AI test generation"""
        return """
You are generating test cases for Avni form element validation testing.

Generate a realistic form element test case that should be validated by the AI assistant.

Return a JSON object with these fields:
{
    "test_case_name": "Brief descriptive name of the test case",
    "form_element": {
        "name": "Field name",
        "type": "SingleSelect/MultiSelect/Text/etc",
        "concept": {
            "dataType": "Numeric/Text/Coded/etc",
            "answers": ["option1", "option2"] // if applicable
        },
        "mandatory": true/false,
        "uuid": "unique-identifier"
    },
    "form_context": {
        "formType": "IndividualProfile/Encounter/etc",
        "domain": "health/education/survey",
        "formName": "Form name"
    },
    "expected_issues": ["issue1", "issue2"] // what issues should be found
}

Example test cases to consider:
- Age field using Text dataType instead of Numeric
- Name field in IndividualProfile form (should be critical issue)
- Phone field without proper validation
- Binary question using MultiSelect instead of SingleSelect

Make the test cases realistic and cover common Avni rule violations.
"""

    def create_static_test_cases(self) -> List[Dict[str, Any]]:
        """Create static test cases from curated reference bundle analysis"""
        # Try to load curated test cases first (highest priority)
        try:
            import json

            curated_test_cases_file = "/Users/himeshr/IdeaProjects/avni-ai/curated_form_validation_test_cases.json"

            if os.path.exists(curated_test_cases_file):
                with open(curated_test_cases_file, "r") as f:
                    curated_cases = json.load(f)
                print(
                    f"✅ Loaded {len(curated_cases)} curated test cases with clear Avni violations"
                )
                return curated_cases
            else:
                print("⚠️  Curated test cases file not found")
        except Exception as e:
            print(f"⚠️  Could not load curated test cases: {e}")

        # Fallback to enhanced test cases (may contain false positives)
        try:
            enhanced_test_cases_file = "/Users/himeshr/IdeaProjects/avni-ai/enhanced_form_validation_test_cases.json"

            if os.path.exists(enhanced_test_cases_file):
                with open(enhanced_test_cases_file, "r") as f:
                    enhanced_cases = json.load(f)
                print(
                    f"⚠️  Using enhanced test cases (may contain false positives): {len(enhanced_cases)} cases"
                )
                return enhanced_cases
            else:
                print("⚠️  Enhanced test cases file not found, using default test cases")
        except Exception as e:
            print(f"⚠️  Could not load enhanced test cases: {e}")

        # Final fallback to default test cases
        print("⚠️  Using basic default test cases")
        return [
            {
                "test_case_name": "age_as_text",
                "form_element": {
                    "name": "Age of patient",
                    "type": "SingleSelect",
                    "concept": {"dataType": "Text"},
                    "mandatory": True,
                    "uuid": "age-field-uuid",
                },
                "form_context": {
                    "formType": "IndividualProfile",
                    "domain": "health",
                    "formName": "Patient Registration",
                },
                "expected_issues": [
                    "HIGH: Age field incorrectly using Text dataType instead of Numeric"
                ],
            },
            {
                "test_case_name": "name_in_individual_profile",
                "form_element": {
                    "name": "Patient Name",
                    "type": "Text",
                    "concept": {"dataType": "Text"},
                    "mandatory": True,
                    "uuid": "name-field-uuid",
                },
                "form_context": {
                    "formType": "IndividualProfile",
                    "domain": "health",
                    "formName": "Patient Registration",
                },
                "expected_issues": [
                    "CRITICAL: Name fields should not be manually added to registration forms"
                ],
            },
            {
                "test_case_name": "phone_without_validation",
                "form_element": {
                    "name": "Phone Number",
                    "type": "Text",
                    "concept": {"dataType": "Text"},
                    "mandatory": False,
                    "uuid": "phone-field-uuid",
                },
                "form_context": {
                    "formType": "IndividualProfile",
                    "domain": "health",
                    "formName": "Patient Registration",
                },
                "expected_issues": ["MEDIUM: Phone field missing validation pattern"],
            },
            {
                "test_case_name": "binary_question_multiselect",
                "form_element": {
                    "name": "Do you have a ration card?",
                    "type": "MultiSelect",
                    "concept": {"dataType": "Coded", "answers": ["yes", "no"]},
                    "mandatory": True,
                    "uuid": "ration-card-uuid",
                },
                "form_context": {
                    "formType": "IndividualProfile",
                    "domain": "health",
                    "formName": "Patient Registration",
                },
                "expected_issues": [
                    "MEDIUM: Binary question using MultiSelect should use SingleSelect"
                ],
            },
            {
                "test_case_name": "correct_numeric_age",
                "form_element": {
                    "name": "Age",
                    "type": "Text",
                    "concept": {
                        "dataType": "Numeric",
                        "lowAbsolute": 0,
                        "highAbsolute": 120,
                    },
                    "mandatory": True,
                    "uuid": "correct-age-uuid",
                },
                "form_context": {
                    "formType": "IndividualProfile",
                    "domain": "health",
                    "formName": "Patient Registration",
                },
                "expected_issues": [],  # No issues expected
            },
        ]
