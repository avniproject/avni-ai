"""
Judge Strategy interface for the Judge Framework
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json

# Handle optional openai dependency
try:
    import openai

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

from .result_models import TestConfiguration, EvaluationResult


class JudgeStrategy(ABC):
    """
    Abstract interface for judge strategies - evaluation logic.
    Each implementation knows how to evaluate a specific type of test output.
    """

    def __init__(self, config: TestConfiguration):
        self.config = config
        self.evaluation_prompt = self._get_evaluation_prompt()

    @abstractmethod
    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate test output against expected behavior

        Args:
            test_input: Input data from TestSubject
            test_output: Output data from TestExecutor

        Returns:
            EvaluationResult with scores and details
        """
        pass

    @abstractmethod
    def _get_evaluation_prompt(self) -> str:
        """Get the evaluation prompt template for this strategy"""
        pass

    @abstractmethod
    def _get_evaluation_metrics(self) -> List[str]:
        """Get the list of metrics this strategy evaluates"""
        pass

    def _call_openai_for_evaluation(self, evaluation_context: str) -> Dict[str, Any]:
        """
        Common method to call OpenAI for evaluation
        """
        if not OPENAI_AVAILABLE:
            return {
                "scores": {metric: 0 for metric in self._get_evaluation_metrics()},
                "overall_success": False,
                "error_message": "OpenAI module not available. Please install openai package.",
                "error_categories": ["dependency_error"],
            }

        try:
            full_prompt = self.evaluation_prompt + evaluation_context

            response = openai.chat.completions.create(
                model=self.config.openai_model,
                messages=[{"role": "system", "content": full_prompt}],
                temperature=self.config.openai_temperature,
                max_tokens=1500,
            )

            response_content = response.choices[0].message.content.strip()

            # Parse JSON response, handling markdown code blocks
            if response_content.startswith("```json"):
                lines = response_content.split("\n")
                start_idx = 1
                end_idx = len(lines)
                for i in range(1, len(lines)):
                    if lines[i].strip() == "```":
                        end_idx = i
                        break

                json_content = "\n".join(lines[start_idx:end_idx])
                result = json.loads(json_content)

                # Add any analysis after the JSON block
                remaining_text = "\n".join(lines[end_idx + 1 :]).strip()
                if remaining_text:
                    result["detailed_analysis"] = remaining_text

                return result

            elif response_content.startswith("{"):
                # Find the end of JSON object
                brace_count = 0
                json_end = 0
                for i, char in enumerate(response_content):
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break

                if json_end > 0:
                    json_part = response_content[:json_end]
                    remaining_text = response_content[json_end:].strip()

                    result = json.loads(json_part)
                    if remaining_text:
                        result["detailed_analysis"] = remaining_text

                    return result

            return json.loads(response_content)

        except json.JSONDecodeError as e:
            return {
                "scores": {metric: 0 for metric in self._get_evaluation_metrics()},
                "overall_success": False,
                "error_message": f"JSON parsing error: {str(e)}",
                "raw_response": response_content
                if "response_content" in locals()
                else None,
            }
        except Exception as e:
            return {
                "scores": {metric: 0 for metric in self._get_evaluation_metrics()},
                "overall_success": False,
                "error_message": str(e),
            }

    def _calculate_overall_success(self, scores: Dict[str, float]) -> bool:
        """
        Calculate overall success based on scores and thresholds
        """
        for metric, score in scores.items():
            threshold = self.config.success_thresholds.get(
                metric, 75.0
            )  # Default 75% threshold
            if score < threshold:
                return False
        return True


class ConversationJudgeStrategy(JudgeStrategy):
    """
    Judge strategy for evaluating chat conversation quality
    """

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate conversation quality
        """
        test_identifier = test_input.get("test_identifier", "unknown")
        scenario = test_input.get("scenario", "")
        expected_behavior = test_input.get("expected_behavior", "")
        conversation_history = test_output.get("conversation_history", [])

        # Format conversation for evaluation
        conversation_text = f"Scenario: {scenario}\n"
        conversation_text += f"Expected Behavior: {expected_behavior}\n\n"

        for turn in conversation_history:
            conversation_text += f"User: {turn.get('user_message', '')}\n"
            conversation_text += f"Assistant: {turn.get('assistant_response', '')}\n\n"

        evaluation_context = f"""
TEST IDENTIFIER: {test_identifier}

{conversation_text}

Evaluate this conversation based on the criteria provided in the prompt.
"""

        # Get AI evaluation
        ai_evaluation = self._call_openai_for_evaluation(evaluation_context)

        # Extract scores and details
        scores = ai_evaluation.get("scores", {})
        overall_success = ai_evaluation.get("overall_success", False)

        # Calculate overall success if not provided
        if "overall_success" not in ai_evaluation:
            overall_success = self._calculate_overall_success(scores)

        return EvaluationResult(
            test_identifier=test_identifier,
            test_type="conversation",
            success=overall_success,
            scores=scores,
            details={
                "scenario": scenario,
                "conversation_length": len(conversation_history),
                "ai_evaluation": ai_evaluation,
            },
            error_categories=ai_evaluation.get("error_categories", []),
            error_message=ai_evaluation.get("error_message"),
            execution_metadata={
                "total_iterations": len(conversation_history),
                "final_conversation_id": test_output.get("final_conversation_id", ""),
            },
            raw_input=test_input,
            raw_output=test_output,
        )

    def _get_evaluation_prompt(self) -> str:
        return """
You are an expert evaluator for AI assistant conversations with Avni healthcare system. 
Evaluate the conversation quality based on these criteria:

1. CONFIGURATION_CORRECTNESS (0-100): Does the assistant correctly configure Avni entities?
2. CONSISTENCY (0-100): Are responses consistent throughout the conversation?
3. COMMUNICATION_QUALITY (0-100): Is the communication clear, helpful, and professional?
4. TASK_COMPLETION (0-100): Does the assistant successfully complete the requested task?

For each score, provide:
- A numerical score from 0-100
- Brief justification for the score

Mark overall_success as TRUE only if ALL scores are 75 or higher.

Respond in JSON format:
{
    "scores": {
        "configuration_correctness": <0-100>,
        "consistency": <0-100>, 
        "communication_quality": <0-100>,
        "task_completion": <0-100>
    },
    "overall_success": <true/false>,
    "error_categories": ["list of any issues found"],
    "detailed_analysis": "Overall assessment of the conversation"
}

CONVERSATION TO EVALUATE:
"""

    def _get_evaluation_metrics(self) -> List[str]:
        return [
            "configuration_correctness",
            "consistency",
            "communication_quality",
            "task_completion",
        ]


class FormValidationJudgeStrategy(JudgeStrategy):
    """
    Judge strategy for evaluating Avni form element validations
    """

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate form validation correctness
        """
        test_identifier = test_input.get("test_identifier", "unknown")
        form_definition = test_input.get("form_definition", {})
        validation_rules = test_input.get("validation_rules", [])
        test_scenarios = test_input.get("test_scenarios", [])

        actual_validation_result = test_output.get("validation_result", {})

        evaluation_context = f"""
TEST IDENTIFIER: {test_identifier}

FORM DEFINITION:
{json.dumps(form_definition, indent=2)}

VALIDATION RULES:
{json.dumps(validation_rules, indent=2)}

TEST SCENARIOS:
{json.dumps(test_scenarios, indent=2)}

ACTUAL VALIDATION RESULT:
{json.dumps(actual_validation_result, indent=2)}

Evaluate if the form validation correctly implements all rules and handles edge cases.
"""

        ai_evaluation = self._call_openai_for_evaluation(evaluation_context)

        scores = ai_evaluation.get("scores", {})
        overall_success = ai_evaluation.get("overall_success", False)

        if "overall_success" not in ai_evaluation:
            overall_success = self._calculate_overall_success(scores)

        return EvaluationResult(
            test_identifier=test_identifier,
            test_type="form_validation",
            success=overall_success,
            scores=scores,
            details={
                "form_name": form_definition.get("name", "unknown"),
                "validation_rules_count": len(validation_rules),
                "test_scenarios_count": len(test_scenarios),
                "ai_evaluation": ai_evaluation,
            },
            error_categories=ai_evaluation.get("error_categories", []),
            error_message=ai_evaluation.get("error_message"),
            raw_input=test_input,
            raw_output=test_output,
        )

    def _get_evaluation_prompt(self) -> str:
        return """
You are an expert evaluator for Avni form validation systems. 
Evaluate the form validation implementation based on these criteria:

1. VALIDATION_CORRECTNESS (0-100): Are all validation rules correctly implemented?
2. EDGE_CASE_HANDLING (0-100): Are edge cases and invalid inputs properly handled?
3. USER_EXPERIENCE (0-100): Are validation messages clear and helpful?
4. DATA_INTEGRITY (0-100): Does the validation ensure data integrity?

For each score, provide a numerical score from 0-100.

Mark overall_success as TRUE only if ALL scores are 75 or higher.

Respond in JSON format:
{
    "scores": {
        "validation_correctness": <0-100>,
        "edge_case_handling": <0-100>,
        "user_experience": <0-100>,
        "data_integrity": <0-100>
    },
    "overall_success": <true/false>,
    "error_categories": ["list of any issues found"],
    "detailed_analysis": "Detailed assessment of the form validation"
}

FORM VALIDATION TO EVALUATE:
"""

    def _get_evaluation_metrics(self) -> List[str]:
        return [
            "validation_correctness",
            "edge_case_handling",
            "user_experience",
            "data_integrity",
        ]


class SchedulingRuleJudgeStrategy(JudgeStrategy):
    """
    Judge strategy for evaluating Avni visit scheduling rules
    """

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate scheduling rule correctness
        """
        test_identifier = test_input.get("test_identifier", "unknown")
        rule_definition = test_input.get("rule_definition", {})
        test_scenarios = test_input.get("test_scenarios", [])

        actual_scheduling_result = test_output.get("scheduling_result", {})

        evaluation_context = f"""
TEST IDENTIFIER: {test_identifier}

SCHEDULING RULE DEFINITION:
{json.dumps(rule_definition, indent=2)}

TEST SCENARIOS:
{json.dumps(test_scenarios, indent=2)}

ACTUAL SCHEDULING RESULT:
{json.dumps(actual_scheduling_result, indent=2)}

Evaluate if the scheduling rule correctly handles all scenarios and edge cases.
"""

        ai_evaluation = self._call_openai_for_evaluation(evaluation_context)

        scores = ai_evaluation.get("scores", {})
        overall_success = ai_evaluation.get("overall_success", False)

        if "overall_success" not in ai_evaluation:
            overall_success = self._calculate_overall_success(scores)

        return EvaluationResult(
            test_identifier=test_identifier,
            test_type="scheduling_rule",
            success=overall_success,
            scores=scores,
            details={
                "rule_name": rule_definition.get("name", "unknown"),
                "test_scenarios_count": len(test_scenarios),
                "ai_evaluation": ai_evaluation,
            },
            error_categories=ai_evaluation.get("error_categories", []),
            error_message=ai_evaluation.get("error_message"),
            raw_input=test_input,
            raw_output=test_output,
        )

    def _get_evaluation_prompt(self) -> str:
        return """
You are an expert evaluator for Avni visit scheduling systems. 
Evaluate the scheduling rule implementation based on these criteria:

1. LOGIC_CORRECTNESS (0-100): Are scheduling calculations and logic correct?
2. EDGE_CASE_HANDLING (0-100): Are edge cases (holidays, conflicts, etc.) properly handled?
3. PERFORMANCE (0-100): Is the scheduling performance acceptable?
4. COMPLIANCE (0-100): Does the scheduling comply with healthcare requirements?

For each score, provide a numerical score from 0-100.

Mark overall_success as TRUE only if ALL scores are 75 or higher.

Respond in JSON format:
{
    "scores": {
        "logic_correctness": <0-100>,
        "edge_case_handling": <0-100>,
        "performance": <0-100>,
        "compliance": <0-100>
    },
    "overall_success": <true/false>,
    "error_categories": ["list of any issues found"],
    "detailed_analysis": "Detailed assessment of the scheduling rule"
}

SCHEDULING RULE TO EVALUATE:
"""

    def _get_evaluation_metrics(self) -> List[str]:
        return ["logic_correctness", "edge_case_handling", "performance", "compliance"]
