"""
Conversation test subject implementations that wrap existing conversation testing logic
"""

from typing import Dict, List, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.test_subject import (
    TestSubject,
    TestSubjectFactory,
)
from tests.judge_framework.interfaces.result_models import TestConfiguration


class ConversationTestSubject(TestSubject):
    """
    Test subject for conversation testing that wraps existing scenario data
    """

    def __init__(self, scenario_data: Dict[str, Any], config: TestConfiguration):
        super().__init__(scenario_data, config)
        self.scenario_name = scenario_data.get("scenario", "")
        self.scenario_index = scenario_data.get("scenario_index", 0)
        self.initial_query = scenario_data.get("initial_query", "")
        self.expected_behavior = scenario_data.get("expected_behavior", "")

    def get_test_identifier(self) -> str:
        """Get unique identifier for this conversation test"""
        return f"conversation_scenario_{self.scenario_index}_{self.scenario_name.replace(' ', '_')}"

    def get_test_input(self) -> Dict[str, Any]:
        """Get input data for conversation execution"""
        return {
            "query": self.initial_query,
            "scenario": self.scenario_name,
            "scenario_index": self.scenario_index,
            "max_iterations": self.config.max_iterations,
            "inputs": self._get_default_dify_inputs(),
        }

    def get_expected_behavior(self) -> str:
        """Get description of expected behavior for evaluation"""
        return (
            self.expected_behavior
            or f"AI assistant should handle {self.scenario_name} scenario correctly"
        )

    def get_evaluation_context(self) -> Dict[str, Any]:
        """Get additional context needed for evaluation"""
        return {
            "scenario": self.scenario_name,
            "scenario_index": self.scenario_index,
            "test_type": "conversation",
        }

    def _get_default_dify_inputs(self) -> Dict[str, Any]:
        """Get default inputs for Dify workflow"""
        import os

        return {
            "auth_token": os.getenv("AVNI_AUTH_TOKEN"),
            "org_name": "Social Welfare Foundation Trust",
            "org_type": "trial",
            "user_name": "Arjun",
            "avni_mcp_server_url": os.getenv("AVNI_MCP_SERVER_URL"),
        }


class ConversationTestSubjectFactory(TestSubjectFactory):
    """
    Factory for creating conversation test subjects from static and AI-generated data
    """

    def __init__(self, scenario_prompts: List[str]):
        self.scenario_prompts = scenario_prompts
        self.scenario_names = self._extract_scenario_names()

    def create_from_static_data(
        self, static_case: Dict[str, Any], config: TestConfiguration
    ) -> TestSubject:
        """Create conversation test subject from static test case data"""
        return ConversationTestSubject(static_case, config)

    def create_from_ai_generation(
        self, ai_case_data: Dict[str, Any], config: TestConfiguration
    ) -> TestSubject:
        """Create conversation test subject from AI-generated test case"""
        # AI should generate scenario data in the expected format
        scenario_data = {
            "scenario": ai_case_data.get("scenario", "AI Generated Scenario"),
            "scenario_index": ai_case_data.get("scenario_index", 0),
            "initial_query": ai_case_data.get("initial_query", ""),
            "expected_behavior": ai_case_data.get("expected_behavior", ""),
        }
        return ConversationTestSubject(scenario_data, config)

    def get_generation_prompt_template(self) -> str:
        """Get the prompt template for AI test generation"""
        return """
You are generating test scenarios for Avni AI assistant conversation testing.

Generate a realistic conversation scenario that a program manager might have with the Avni AI assistant when setting up a healthcare program.

Return a JSON object with these fields:
{
    "scenario": "Brief descriptive name of the scenario",
    "scenario_index": <integer index>,
    "initial_query": "The first message the program manager would send",
    "expected_behavior": "Description of what the AI assistant should accomplish in this conversation"
}

Example scenarios to consider:
- Setting up a new maternal health program
- Configuring form validation for patient registration
- Creating visit scheduling rules for chronic disease management
- Setting up location hierarchy for a new district

Make the initial query realistic and specific. The expected behavior should clearly describe what success looks like.
"""

    def _extract_scenario_names(self) -> List[str]:
        """Extract scenario names from prompts for reference"""
        # Simple extraction - in real implementation, this might be more sophisticated
        names = []
        for i, prompt in enumerate(self.scenario_prompts):
            # Try to extract a scenario name from the prompt
            lines = prompt.split("\n")
            for line in lines:
                if line.strip().startswith("Scenario:") or "SCENARIO" in line.upper():
                    name = line.split(":", 1)[-1].strip()
                    if name:
                        names.append(name)
                        break
            else:
                # Fallback to generic name
                names.append(f"Scenario {i + 1}")
        return names

    def create_static_test_cases(self) -> List[Dict[str, Any]]:
        """Create static test cases from existing scenario prompts"""
        static_cases = []
        for i, (prompt, name) in enumerate(
            zip(self.scenario_prompts, self.scenario_names)
        ):
            # Extract initial query from prompt if available, otherwise use generic
            initial_query = self._extract_initial_query_from_prompt(prompt)

            static_case = {
                "scenario": name,
                "scenario_index": i,
                "initial_query": initial_query,
                "expected_behavior": f"AI assistant should handle {name} scenario correctly and configure appropriate Avni entities",
            }
            static_cases.append(static_case)

        return static_cases

    def _extract_initial_query_from_prompt(self, prompt: str) -> str:
        """Extract or generate initial query from scenario prompt"""
        # Look for sample queries in the prompt
        lines = prompt.split("\n")
        for line in lines:
            if "query:" in line.lower() or "ask:" in line.lower():
                return line.split(":", 1)[-1].strip().strip("\"'")

        # Fallback: generate a reasonable initial query based on scenario
        if "maternal" in prompt.lower():
            return "I need to set up a maternal health program for our organization. Can you help me configure this?"
        elif "form" in prompt.lower():
            return "I need to create a new form with proper validation rules. How do I get started?"
        elif "scheduling" in prompt.lower():
            return "I need to configure visit scheduling rules for our chronic disease program. What are the steps?"
        else:
            return "I need help setting up a new healthcare program in Avni. Can you guide me through the configuration?"
