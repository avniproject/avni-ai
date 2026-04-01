"""
Test subject for Spec Agent testing.

Loads entities from Durga India scoping documents and creates test cases
with different entity combinations and conversation variable states.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from tests.judge_framework.interfaces.test_subject import (
    TestSubject,
    TestSubjectFactory,
)
from tests.judge_framework.interfaces.result_models import TestConfiguration


class SpecAgentTestSubject(TestSubject):
    """Test subject representing a Spec Agent test case with pre-populated entities."""

    def __init__(
        self,
        entities: Dict[str, Any],
        conversation_vars: Dict[str, Any],
        test_scenario: str,
        config: TestConfiguration,
        expected_behavior: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize Spec Agent test subject.

        Args:
            entities: Entity data (subject_types, programs, encounter_types, etc.)
            conversation_vars: Conversation variables to inject (entities_jsonl, setup_mode_active, etc.)
            test_scenario: Name/description of the test scenario
            config: Test configuration
            expected_behavior: Expected agent behavior (tool calls, outputs, etc.)
        """
        self.entities = entities
        self.conversation_vars = conversation_vars
        self.test_scenario = test_scenario
        self.config = config
        self.expected_behavior = expected_behavior or {}

    def get_test_identifier(self) -> str:
        """Return unique identifier for this test."""
        return f"spec_agent_{self.test_scenario}"

    def get_test_input(self) -> Dict[str, Any]:
        """
        Return test input for Dify execution.

        Returns dict with:
        - query: User message to send to Spec Agent
        - inputs: Dify conversation variables (auth_token, entities_jsonl, etc.)
        - conversation_vars: Additional state to inject
        """
        # Prepare entities_jsonl for injection
        entities_jsonl = json.dumps(self.entities) if self.entities else "{}"

        # Build Dify inputs
        dify_inputs = {
            "auth_token": getattr(self.config, "avni_auth_token", ""),
            "avni_mcp_server_url": getattr(self.config, "avni_mcp_server_url", ""),
            "org_name": self.conversation_vars.get("org_name", "Durga India"),
            "user_name": self.conversation_vars.get("user_name", "Test User"),
            # Inject conversation state
            "entities_jsonl": entities_jsonl,
            "setup_mode_active": self.conversation_vars.get("setup_mode_active", True),
            "spec_yaml": self.conversation_vars.get("spec_yaml", ""),
        }

        # User query to trigger Spec Agent
        query = self.conversation_vars.get(
            "query",
            "I've uploaded the scoping documents. Please generate the spec.",
        )

        return {
            "query": query,
            "inputs": dify_inputs,
            "conversation_vars": self.conversation_vars,
            "entities": self.entities,
            "test_scenario": self.test_scenario,
        }

    def get_expected_spec_structure(self) -> Dict[str, Any]:
        """Return expected YAML spec structure based on entities."""
        if not self.entities:
            return {}

        expected = {
            "has_subject_types": len(self.entities.get("subject_types", [])) > 0,
            "has_programs": len(self.entities.get("programs", [])) > 0,
            "has_encounter_types": len(self.entities.get("encounter_types", [])) > 0,
            "has_address_levels": len(self.entities.get("address_levels", [])) > 0,
            "has_forms": len(self.entities.get("forms", [])) > 0,
            "expected_subject_type_count": len(self.entities.get("subject_types", [])),
            "expected_program_count": len(self.entities.get("programs", [])),
            "expected_encounter_type_count": len(
                self.entities.get("encounter_types", [])
            ),
            "expected_form_count": len(self.entities.get("forms", [])),
        }

        return expected

    def get_evaluation_context(self) -> Dict[str, Any]:
        """Return context for evaluation."""
        return {
            "entities": self.entities,
            "test_scenario": self.test_scenario,
            "conversation_vars": self.conversation_vars,
            "expected_spec_structure": self.get_expected_spec_structure(),
        }

    def get_expected_behavior(self) -> Dict[str, Any]:
        """Return expected behavior for this test."""
        return self.expected_behavior


class SpecAgentTestSubjectFactory(TestSubjectFactory):
    """Factory for creating Spec Agent test subjects from static test cases."""

    def __init__(self, entities_file_path: str):
        """
        Initialize factory with path to entities file.

        Args:
            entities_file_path: Path to entities_summary.json
        """
        self.entities_file_path = Path(entities_file_path)
        self.base_entities = self._load_entities()

    def _load_entities(self) -> Dict[str, Any]:
        """Load entities from JSON file."""
        if not self.entities_file_path.exists():
            raise FileNotFoundError(
                f"Entities file not found: {self.entities_file_path}"
            )

        with open(self.entities_file_path, "r") as f:
            data = json.load(f)

        # Extract actual_value from the structure
        if "conditions" in data and len(data["conditions"]) > 0:
            return data["conditions"][0].get("actual_value", {})

        return data

    def create_from_static_data(
        self, static_case: Dict[str, Any], config: TestConfiguration
    ) -> SpecAgentTestSubject:
        """
        Create test subject from static test case definition.

        Args:
            static_case: Test case definition with scenario, entities_filter, conversation_vars
            config: Test configuration

        Returns:
            SpecAgentTestSubject instance
        """
        scenario = static_case.get("scenario", "unknown")
        entities_filter = static_case.get("entities_filter", "full")
        conversation_vars = static_case.get("conversation_vars", {})
        expected_behavior = static_case.get("expected_behavior", {})

        # Filter entities based on test case
        entities = self._filter_entities(entities_filter)

        return SpecAgentTestSubject(
            entities=entities,
            conversation_vars=conversation_vars,
            test_scenario=scenario,
            config=config,
            expected_behavior=expected_behavior,
        )

    def _filter_entities(self, filter_type: str) -> Dict[str, Any]:
        """
        Filter entities based on test scenario requirements.

        Args:
            filter_type: Type of filtering (full, empty, partial_subject_types, etc.)

        Returns:
            Filtered entities dict
        """
        if filter_type == "empty":
            return {}

        if filter_type == "full":
            return self.base_entities.copy()

        if filter_type == "partial_subject_types":
            # Only subject types, no programs/encounters
            return {
                "subject_types": self.base_entities.get("subject_types", []),
                "programs": [],
                "encounter_types": [],
                "address_levels": self.base_entities.get("address_levels", []),
                "forms": [],
            }

        if filter_type == "partial_no_forms":
            # Everything except forms
            return {
                "subject_types": self.base_entities.get("subject_types", []),
                "programs": self.base_entities.get("programs", []),
                "encounter_types": self.base_entities.get("encounter_types", []),
                "address_levels": self.base_entities.get("address_levels", []),
                "forms": [],
            }

        # Default to full entities
        return self.base_entities.copy()

    def create_from_ai_generation(
        self, generation_params: Dict[str, Any], config: TestConfiguration
    ) -> SpecAgentTestSubject:
        """
        Create test subject from AI-generated parameters.

        Not implemented for Spec Agent testing (using static scenarios only).
        """
        raise NotImplementedError(
            "AI generation not supported for Spec Agent tests. Use static test cases."
        )

    def get_generation_prompt_template(self) -> str:
        """
        Get prompt template for AI generation.

        Not used for Spec Agent testing (static scenarios only).
        """
        return ""
