"""
Rules Generation Test Subject for the Judge Framework
"""

import json
import os
from typing import Dict, Any

from tests.judge_framework.implementations.conversation.conversation_subject import (
    ConversationTestSubject,
)
from tests.judge_framework.interfaces.result_models import TestConfiguration
from tests.judge_framework.interfaces.test_subject import (
    TestSubjectFactory,
    TestSubject,
)


class RulesGenerationTestSubject(ConversationTestSubject):
    """
    Test subject for rules generation testing that includes form_context in inputs
    """

    def __init__(self, scenario_data: Dict[str, Any], config: TestConfiguration):
        super().__init__(scenario_data, config)

    def get_test_input(self) -> Dict[str, Any]:
        """Get input data for rules generation execution with form_context in inputs"""
        base_input = super().get_test_input()

        # Get the specific context for this test case
        test_case_context = self.test_data.get("reference_context", {})

        # Add form_context to inputs
        inputs = base_input.get("inputs", {})
        inputs.update(
            {
                "auth_token": os.getenv("AVNI_AUTH_TOKEN"),
                "org_name": "Social Welfare Foundation Trust",
                "org_type": "trial",
                "user_name": "xxx",
                "requestType": "VisitSchedule",
                "avni_mcp_server_url": os.getenv("AVNI_MCP_SERVER_URL"),
                "form_context": json.dumps(test_case_context),
            }
        )

        base_input["inputs"] = inputs
        return base_input

    def get_test_identifier(self) -> str:
        """Get identifier for this rules generation test"""
        return f"rules_gen_{self.scenario_index}_{self.scenario_name}"

    def get_expected_outputs(self) -> Dict[str, Any]:
        """Get expected outputs for rules generation evaluation"""
        expected = super().get_expected_outputs()

        # Add rules-specific expected outputs if available in scenario data
        if hasattr(self, "_scenario_data"):
            if "reference_rule" in self._scenario_data:
                expected["reference_rule"] = self._scenario_data["reference_rule"]
            if "reference_context" in self._scenario_data:
                expected["reference_context"] = self._scenario_data["reference_context"]
            if "rule_request" in self._scenario_data:
                expected["rule_request"] = self._scenario_data["rule_request"]

        return expected


class RulesGenerationTestSubjectFactory(TestSubjectFactory):
    """
    Factory for creating rules generation test subjects
    """

    def __init__(self, scenario_prompts: list[str]):
        self.scenario_prompts = scenario_prompts

    def create_from_static_data(
        self, static_case: Dict[str, Any], config: TestConfiguration
    ) -> TestSubject:
        """Create rules generation test subject from static test case data"""
        return RulesGenerationTestSubject(static_case, config)

    def create_from_ai_generation(
        self, ai_prompt: str, config: TestConfiguration
    ) -> TestSubject:
        """Create test subject from AI-generated test case"""
        # For rules generation, we could implement AI generation later
        # For now, create a basic test case from the prompt
        ai_case_data = {
            "scenario": "AI Generated Rules Scenario",
            "scenario_index": 0,
            "initial_query": ai_prompt,
            "expected_behavior": "Generate correct JavaScript scheduling rule from AI prompt",
        }
        return RulesGenerationTestSubject(ai_case_data, config)

    def get_generation_prompt_template(self) -> str:
        """Get the prompt template for AI test generation"""
        return """Generate a visit scheduling rule request for Avni platform.
        
The request should specify:
- What type of visit to schedule
- When to schedule it (timing relative to current encounter)
- Any conditions that should be checked
- Form types and encounter types involved

Example: "Schedule ANC follow-up visit 28 days after current ANC encounter"

Generate a similar but different rule request:"""

    def create_test_subject(
        self, test_case_data: Dict[str, Any], config: TestConfiguration
    ) -> RulesGenerationTestSubject:
        """Create a rules generation test subject from test case data"""
        return RulesGenerationTestSubject(test_case_data, config)

    def create_test_subjects_from_config(
        self, config: TestConfiguration
    ) -> list[RulesGenerationTestSubject]:
        """Create test subjects from configuration static test cases"""
        test_subjects = []

        for test_case in config.generation_config.static_test_cases:
            test_subject = self.create_test_subject(test_case, config)
            test_subjects.append(test_subject)

        return test_subjects
