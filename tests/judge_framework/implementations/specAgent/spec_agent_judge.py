"""
Judge strategy for Spec Agent testing.

Evaluates whether the Spec Agent correctly generated a YAML spec from entities,
called appropriate tools, and followed the expected workflow.
"""

import yaml
import json
import logging
from typing import Dict, Any, List
from tests.judge_framework.interfaces.judge_strategy import JudgeStrategy
from tests.judge_framework.interfaces.result_models import (
    EvaluationResult,
    TestConfiguration,
)

logger = logging.getLogger(__name__)


class SpecAgentJudge(JudgeStrategy):
    """Judge strategy for evaluating Spec Agent behavior and spec generation quality."""

    def __init__(self, config: TestConfiguration):
        """
        Initialize Spec Agent judge.

        Args:
            config: Test configuration with evaluation settings
        """
        super().__init__(config)

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate Spec Agent test results.

        Evaluation criteria:
        1. Tool call correctness: Did agent call generate_spec with conversation_id?
        2. Spec structure validity: Is the YAML valid and well-formed?
        3. Entity coverage: Are all input entities present in spec?
        4. Conversation flow: Did agent follow expected workflow?

        Args:
            test_input: Input from SpecAgentTestSubject
            test_output: Output from SpecAgentExecutor

        Returns:
            EvaluationResult with scores and feedback
        """
        test_scenario = test_input.get("test_scenario", "unknown")
        entities = test_input.get("entities", {})
        expected_behavior = test_input.get("expected_behavior", {})

        logger.info(f"Evaluating Spec Agent test: {test_scenario}")

        # Check if execution succeeded
        if not test_output.get("success", False):
            return EvaluationResult(
                test_identifier=test_scenario,
                test_type="spec_agent",
                success=False,
                scores={},
                details={
                    "error": test_output.get("error", "Unknown error"),
                    "execution_failed": True,
                },
                error_message="Test execution failed",
            )

        # Evaluate each criterion
        tool_call_score, tool_call_feedback = self._evaluate_tool_calls(
            test_output, entities, expected_behavior
        )
        spec_validity_score, spec_validity_feedback = self._evaluate_spec_validity(
            test_output
        )
        entity_coverage_score, entity_coverage_feedback = self._evaluate_entity_coverage(
            test_output, entities
        )
        conversation_flow_score, conversation_flow_feedback = (
            self._evaluate_conversation_flow(test_output, entities, expected_behavior)
        )

        # Calculate weighted overall score
        weights = {
            "tool_call_correctness": 0.3,
            "spec_validity": 0.3,
            "entity_coverage": 0.25,
            "conversation_flow": 0.15,
        }

        overall_score = (
            tool_call_score * weights["tool_call_correctness"]
            + spec_validity_score * weights["spec_validity"]
            + entity_coverage_score * weights["entity_coverage"]
            + conversation_flow_score * weights["conversation_flow"]
        )

        # Determine if test passed based on thresholds
        thresholds = self.config.evaluation_config.success_thresholds
        tool_call_threshold = thresholds.get("tool_call_correctness", 80.0)
        spec_validity_threshold = thresholds.get("spec_validity", 90.0)

        passed = (
            tool_call_score >= tool_call_threshold
            and spec_validity_score >= spec_validity_threshold
            and overall_score >= 70.0
        )

        # Compile feedback
        feedback_parts = [
            f"Tool Calls: {tool_call_feedback}",
            f"Spec Validity: {spec_validity_feedback}",
            f"Entity Coverage: {entity_coverage_feedback}",
            f"Conversation Flow: {conversation_flow_feedback}",
        ]

        return EvaluationResult(
            test_identifier=test_scenario,
            test_type="spec_agent",
            success=passed,
            scores={
                "overall": overall_score,
                "tool_call_correctness": tool_call_score,
                "spec_validity": spec_validity_score,
                "entity_coverage": entity_coverage_score,
                "conversation_flow": conversation_flow_score,
            },
            details={
                "tool_calls": test_output.get("tool_calls", []),
                "spec_yaml_length": len(test_output.get("spec_yaml", "")),
                "conversation_id": test_output.get("conversation_id", ""),
                "feedback": "\n".join(feedback_parts),
            },
        )

    def _evaluate_tool_calls(
        self,
        test_output: Dict[str, Any],
        entities: Dict[str, Any],
        expected_behavior: Dict[str, Any],
    ) -> tuple:
        """
        Evaluate whether agent made correct tool calls.

        Expected: generate_spec called with conversation_id (if entities present)

        Returns:
            (score, feedback) tuple
        """
        tool_calls = test_output.get("tool_calls", [])
        agent_response = test_output.get("agent_response", "")

        # If no entities, agent should NOT call generate_spec
        if not entities or len(entities) == 0:
            if not tool_calls:
                return (
                    100.0,
                    "Correctly did not call generate_spec (no entities provided)",
                )
            else:
                return (
                    50.0,
                    f"Called tools when no entities present: {[t['tool'] for t in tool_calls]}",
                )

        # If entities present, agent should call generate_spec
        generate_spec_called = any(
            "generate_spec" in tc.get("tool", "").lower() for tc in tool_calls
        )

        if generate_spec_called:
            # Check if validate_spec was also called
            validate_spec_called = any(
                "validate_spec" in tc.get("tool", "").lower() for tc in tool_calls
            )

            if validate_spec_called:
                return (
                    100.0,
                    f"Called generate_spec and validate_spec ({len(tool_calls)} total calls)",
                )
            else:
                return (
                    80.0,
                    f"Called generate_spec but not validate_spec ({len(tool_calls)} total calls)",
                )
        else:
            # Check if agent at least mentioned generating spec
            if "generate" in agent_response.lower() and "spec" in agent_response.lower():
                return (
                    40.0,
                    f"Mentioned spec generation but didn't call tool. Tools called: {[t['tool'] for t in tool_calls]}",
                )
            else:
                return (
                    0.0,
                    f"Did not call generate_spec. Tools called: {[t['tool'] for t in tool_calls]}",
                )

    def _evaluate_spec_validity(self, test_output: Dict[str, Any]) -> tuple:
        """
        Evaluate whether generated spec is valid YAML.

        Returns:
            (score, feedback) tuple
        """
        spec_yaml = test_output.get("spec_yaml", "")

        if not spec_yaml:
            return (0.0, "No spec YAML generated")

        try:
            # Try to parse as YAML
            parsed = yaml.safe_load(spec_yaml)

            if not parsed or not isinstance(parsed, dict):
                return (30.0, "Spec parsed but is not a valid dict structure")

            # Check for expected top-level keys
            expected_keys = [
                "subject_types",
                "programs",
                "encounter_types",
                "address_levels",
                "forms",
            ]
            present_keys = [key for key in expected_keys if key in parsed]

            if len(present_keys) == 0:
                return (
                    40.0,
                    f"Valid YAML but missing all expected keys. Keys present: {list(parsed.keys())}",
                )

            coverage = (len(present_keys) / len(expected_keys)) * 100
            return (
                min(100.0, 60.0 + coverage * 0.4),
                f"Valid YAML with {len(present_keys)}/{len(expected_keys)} expected keys",
            )

        except yaml.YAMLError as e:
            return (0.0, f"Invalid YAML: {str(e)[:100]}")
        except Exception as e:
            return (0.0, f"Error parsing spec: {str(e)[:100]}")

    def _evaluate_entity_coverage(
        self, test_output: Dict[str, Any], entities: Dict[str, Any]
    ) -> tuple:
        """
        Evaluate whether all input entities are represented in the spec.

        Returns:
            (score, feedback) tuple
        """
        spec_yaml = test_output.get("spec_yaml", "")

        if not entities or len(entities) == 0:
            return (100.0, "No entities to cover (N/A)")

        if not spec_yaml:
            return (0.0, "No spec generated to evaluate coverage")

        try:
            parsed_spec = yaml.safe_load(spec_yaml)
            if not parsed_spec or not isinstance(parsed_spec, dict):
                return (0.0, "Cannot evaluate coverage - invalid spec structure")

            # Count entities in input vs spec
            coverage_scores = []

            for entity_type in [
                "subject_types",
                "programs",
                "encounter_types",
                "forms",
            ]:
                input_entities = entities.get(entity_type, [])
                spec_entities = parsed_spec.get(entity_type, [])

                if len(input_entities) == 0:
                    continue

                # Count how many input entities appear in spec
                input_names = {e.get("name", "") for e in input_entities}
                spec_names = {e.get("name", "") for e in spec_entities}

                covered = len(input_names & spec_names)
                total = len(input_names)

                if total > 0:
                    coverage_scores.append((covered / total) * 100)

            if not coverage_scores:
                return (50.0, "No entity types to evaluate coverage")

            avg_coverage = sum(coverage_scores) / len(coverage_scores)
            return (
                avg_coverage,
                f"Entity coverage: {avg_coverage:.1f}% across {len(coverage_scores)} entity types",
            )

        except Exception as e:
            return (0.0, f"Error evaluating coverage: {str(e)[:100]}")

    def _evaluate_conversation_flow(
        self,
        test_output: Dict[str, Any],
        entities: Dict[str, Any],
        expected_behavior: Dict[str, Any],
    ) -> tuple:
        """
        Evaluate whether agent followed expected conversation flow.

        Returns:
            (score, feedback) tuple
        """
        agent_response = test_output.get("agent_response", "")

        # If no entities, agent should ask for documents
        if not entities or len(entities) == 0:
            if any(
                keyword in agent_response.lower()
                for keyword in ["upload", "document", "file", "srs"]
            ):
                return (100.0, "Correctly asked for documents when no entities present")
            else:
                return (
                    50.0,
                    "No entities but didn't ask for documents (may be acceptable)",
                )

        # If entities present, check for expected flow markers
        flow_markers = {
            "spec_approved": "SPEC_APPROVED" in agent_response,
            "asks_confirmation": any(
                keyword in agent_response.lower()
                for keyword in ["confirm", "correct", "approve", "yes/no", "look correct"]
            ),
            "shows_summary": len(agent_response) > 100,  # Reasonable length response
        }

        score = 0.0
        feedback_parts = []

        if flow_markers["spec_approved"]:
            score += 50.0
            feedback_parts.append("✓ Output SPEC_APPROVED marker")
        else:
            feedback_parts.append("✗ Missing SPEC_APPROVED marker")

        if flow_markers["asks_confirmation"]:
            score += 30.0
            feedback_parts.append("✓ Asked for user confirmation")
        else:
            feedback_parts.append("✗ Didn't ask for confirmation")

        if flow_markers["shows_summary"]:
            score += 20.0
            feedback_parts.append("✓ Provided summary/details")

        return (score, "; ".join(feedback_parts))

    def _get_evaluation_metrics(self) -> list:
        """Return list of evaluation metrics used by this judge."""
        return [
            "tool_call_correctness",
            "spec_validity",
            "entity_coverage",
            "conversation_flow",
        ]

    def _get_evaluation_prompt(self) -> str:
        """
        Return evaluation prompt template.

        Not used for Spec Agent judge (uses programmatic evaluation).
        """
        return ""
