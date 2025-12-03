"""
Form Validation Judge Strategy interface for the Judge Framework
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


class FormValidationJudgeStrategy(ABC):
    """
    Abstract interface for form validation judge strategies.
    Evaluates the quality of form validation feedback and recommendations.
    """

    def __init__(self, config: TestConfiguration):
        self.config = config
        self.evaluation_prompt = self._get_evaluation_prompt()

    @abstractmethod
    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate form validation results

        Args:
            test_input: Original form validation test data
            test_output: Results from form validation executor

        Returns:
            EvaluationResult with scores and detailed feedback
        """
        pass

    @abstractmethod
    def _get_evaluation_prompt(self) -> str:
        """Get the evaluation prompt for form validation"""
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

            print(f"🔍 DEBUG - OpenAI evaluation prompt length: {len(full_prompt)}")
            print(
                f"🔍 DEBUG - Evaluation context preview: {evaluation_context[:300]}..."
            )

            response = openai.chat.completions.create(
                model=self.config.openai_model,
                messages=[{"role": "system", "content": full_prompt}],
                temperature=self.config.openai_temperature,
                max_tokens=1500,
            )

            response_text = response.choices[0].message.content.strip()
            print(f"🔍 DEBUG - OpenAI raw response: {response_text}")

            # Try to parse JSON response
            try:
                # Extract JSON from response if it's wrapped in markdown
                if response_text.startswith("```json"):
                    import re

                    json_match = re.search(
                        r"```json\s*\n?(.*?)\n?```", response_text, re.DOTALL
                    )
                    if json_match:
                        json_text = json_match.group(1).strip()
                        evaluation_data = json.loads(json_text)
                    else:
                        # Fallback: try to find JSON object in the text
                        json_start = response_text.find("{")
                        json_end = response_text.rfind("}") + 1
                        if json_start != -1 and json_end != -1:
                            json_text = response_text[json_start:json_end]
                            evaluation_data = json.loads(json_text)
                        else:
                            raise json.JSONDecodeError(
                                "No JSON found", response_text, 0
                            )
                else:
                    evaluation_data = json.loads(response_text)
                print(f"🔍 DEBUG - Successfully parsed JSON: {evaluation_data}")
            except json.JSONDecodeError as e:
                print(f"🔍 DEBUG - JSON parse error: {e}")
                # Fallback: extract scores from text
                evaluation_data = self._extract_scores_from_text(response_text)
                print(f"🔍 DEBUG - Fallback parsed scores: {evaluation_data}")

            return evaluation_data

        except Exception as e:
            print(f"🔍 DEBUG - OpenAI evaluation exception: {e}")
            return {
                "scores": {metric: 0 for metric in self._get_evaluation_metrics()},
                "overall_success": False,
                "error_message": f"Evaluation failed: {str(e)}",
                "error_categories": ["evaluation_error"],
            }

    def _extract_scores_from_text(self, text: str) -> Dict[str, Any]:
        """Extract scores from unstructured text response"""
        scores = {}
        metrics = self._get_evaluation_metrics()

        for metric in metrics:
            # Simple pattern matching for scores in text
            import re

            pattern = f"{metric}[:\\s]*(\\d+)"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                scores[metric] = float(match.group(1))
            else:
                scores[metric] = 50.0  # Default score

        return {
            "scores": scores,
            "overall_success": all(score >= 75 for score in scores.values()),
            "error_message": None,
            "error_categories": [],
        }

    def _calculate_overall_success(self, scores: Dict[str, float]) -> bool:
        """Calculate overall success based on scores and thresholds"""
        thresholds = self.config.evaluation_config.success_thresholds

        for metric, score in scores.items():
            threshold = thresholds.get(metric, 75.0)
            if score < threshold:
                return False

        return True


class DifyFormValidationJudgeStrategy(FormValidationJudgeStrategy):
    """
    Form validation judge strategy that evaluates Dify workflow validation results
    """

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate form validation results from Dify workflow
        """
        test_identifier = test_input.get("test_identifier", "unknown")
        form_element = test_input.get("form_element", {})
        validation_feedback = test_output.get("validation_feedback", "")
        expected_issues = test_input.get("expected_issues", [])
        performance_metrics = test_output.get("performance_metrics", {})

        # DEBUG: Print actual structure being received
        print(f"\n🔍 DEBUG - Test: {test_identifier}")
        print(f"🔍 DEBUG - test_output keys: {list(test_output.keys())}")
        print(f"🔍 DEBUG - performance_metrics: {performance_metrics}")
        print(f"🔍 DEBUG - validation_feedback length: {len(validation_feedback)}")
        if validation_feedback:
            print(
                f"🔍 DEBUG - validation_feedback preview: {validation_feedback[:200]}..."
            )

        # Extract validation details from enhanced JSON response
        validation_details = self._parse_validation_response(validation_feedback)

        # Calculate performance score
        performance_score = self._calculate_performance_score(
            performance_metrics, test_input
        )

        print(f"🔍 DEBUG - calculated performance_score: {performance_score}")
        print(f"🔍 DEBUG - validation_details: {validation_details}")

        # Format evaluation context
        evaluation_context = f"""
TEST IDENTIFIER: {test_identifier}

FORM ELEMENT:
{json.dumps(form_element, indent=2)}

VALIDATION FEEDBACK:
{validation_feedback}

PARSED VALIDATION DETAILS:
- Message: {validation_details.get("message", "No message")}
- UUID: {validation_details.get("uuid", "No UUID")}
- Issues Count: {validation_details.get("issues_count", "N/A")}
- Response Format: {validation_details.get("response_format", "Unknown")}

PERFORMANCE METRICS:
- Total Response Time: {performance_metrics.get("total_response_time_ms", "N/A")}ms
- Dify API Time: {performance_metrics.get("dify_api_time_ms", "N/A")}ms
- Within Ideal (≤500ms): {performance_metrics.get("within_ideal_threshold", "N/A")}
- Within Max (≤1500ms): {performance_metrics.get("within_max_threshold", "N/A")}
- Performance Score: {performance_score}/100

EXPECTED ISSUES:
{", ".join(expected_issues) if expected_issues else "None"}

Evaluate this form validation based on the criteria provided in the prompt.
"""

        # Get AI evaluation
        ai_evaluation = self._call_openai_for_evaluation(evaluation_context)

        # Extract scores and details
        scores = ai_evaluation.get("scores", {})
        overall_success = ai_evaluation.get("overall_success", False)

        # Add performance score to evaluation
        scores["performance_score"] = performance_score

        # Calculate overall success if not provided
        if "overall_success" not in ai_evaluation:
            overall_success = self._calculate_overall_success(scores)

        return EvaluationResult(
            test_identifier=test_identifier,
            test_type="form_validation",
            success=overall_success,
            scores=scores,
            details={
                "form_element_name": form_element.get("name", "Unknown"),
                "validation_feedback_length": len(validation_feedback),
                "parsed_validation_details": validation_details,
                "expected_issues": expected_issues,
                "performance_metrics": performance_metrics,
                "performance_score": performance_score,
                "ai_evaluation": ai_evaluation,
            },
            error_categories=ai_evaluation.get("error_categories", []),
            error_message=ai_evaluation.get("error_message"),
            execution_metadata={
                "form_element_type": form_element.get("type", "Unknown"),
                "form_element_datatype": form_element.get("concept", {}).get(
                    "dataType", "Unknown"
                ),
                "validation_response_format": validation_details.get(
                    "response_format", "unknown"
                ),
                "performance_evaluated": True,
            },
            raw_input=test_input,
            raw_output=test_output,
        )

    def _parse_validation_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the enhanced JSON response from Dify Form Assistant"""
        try:
            import json

            response_text = response_text.strip()

            # Extract JSON from markdown code blocks if present
            if response_text.startswith("```json"):
                # Extract JSON from markdown code blocks
                import re

                json_match = re.search(
                    r"```json\s*\n?(.*?)\n?```", response_text, re.DOTALL
                )
                if json_match:
                    response_text = json_match.group(1).strip()

            # Handle raw array format - wrap it in issues object
            if response_text.startswith("["):
                parsed_array = json.loads(response_text)

                # Filter out "validation passed" messages and minor suggestions for valid forms
                actual_issues = []
                for issue in parsed_array:
                    message = issue.get("message", "").lower()

                    # Check if this is a "validation passed" message that should be filtered out
                    if any(
                        keyword in message
                        for keyword in [
                            "correctly configured",
                            "no issue",
                            "valid",
                            "properly configured",
                            "matches avni rules",
                            "appropriately configured",
                            "no violation",
                        ]
                    ):
                        continue  # Skip success messages

                    # Check if this is a minor improvement suggestion (not a violation)
                    if any(
                        keyword in message
                        for keyword in [
                            "should configure bounds",
                            "consider making mandatory",
                            "should configure",
                            "recommend configuring",
                            "consider adding",
                            "ensure units are clear",
                            "you should configure",
                            "configure appropriate",
                        ]
                    ):
                        continue  # Skip minor suggestions for valid forms

                    actual_issues.append(issue)

                if actual_issues:
                    first_issue = actual_issues[0]
                    return {
                        "uuid": first_issue.get("formElementUuid", ""),
                        "message": first_issue.get("message", ""),
                        "is_valid": len(first_issue.get("message", "")) > 10,
                        "issues_count": len(actual_issues),
                        "response_format": "raw_array_filtered",
                    }
                else:
                    return {
                        "uuid": "",
                        "message": "[]",
                        "is_valid": True,
                        "issues_count": 0,
                        "response_format": "raw_array_empty",
                    }

            # Handle wrapped format with issues array
            elif response_text.startswith("{"):
                parsed = json.loads(response_text)

                if "issues" in parsed:
                    issues = parsed.get("issues", [])

                    # Filter out "validation passed" messages and minor suggestions for valid forms
                    actual_issues = []
                    for issue in issues:
                        message = issue.get("message", "").lower()

                        # Check if this is a "validation passed" message that should be filtered out
                        if any(
                            keyword in message
                            for keyword in [
                                "correctly configured",
                                "no issue",
                                "valid",
                                "properly configured",
                                "matches avni rules",
                                "appropriately configured",
                                "no violation",
                            ]
                        ):
                            continue  # Skip success messages

                        # Check if this is a minor improvement suggestion (not a violation)
                        if any(
                            keyword in message
                            for keyword in [
                                "should configure bounds",
                                "consider making mandatory",
                                "should configure",
                                "recommend configuring",
                                "consider adding",
                                "ensure units are clear",
                                "you should configure",
                                "configure appropriate",
                            ]
                        ):
                            continue  # Skip minor suggestions for valid forms

                        actual_issues.append(issue)

                    if actual_issues:
                        first_issue = actual_issues[0]
                        return {
                            "uuid": first_issue.get("formElementUuid", ""),
                            "message": first_issue.get("message", ""),
                            "is_valid": len(first_issue.get("message", "")) > 10,
                            "issues_count": len(actual_issues),
                            "response_format": "enhanced_json_filtered",
                        }
                    else:
                        return {
                            "uuid": "",
                            "message": "[]",
                            "is_valid": True,
                            "issues_count": 0,
                            "response_format": "enhanced_json",
                        }

                # Handle legacy format for backward compatibility
                else:
                    return {
                        "uuid": parsed.get("uuid", ""),
                        "message": parsed.get("message", ""),
                        "is_valid": len(parsed.get("message", "")) > 10,
                        "response_format": "legacy_json",
                    }
            else:
                # Fallback for non-JSON responses
                return {
                    "uuid": "",
                    "message": response_text,
                    "is_valid": len(response_text) > 10,
                    "response_format": "text",
                }
        except (json.JSONDecodeError, Exception):
            return {
                "uuid": "",
                "message": response_text.strip(),
                "is_valid": False,
                "response_format": "error",
            }

    def _calculate_performance_score(
        self, performance_metrics: Dict[str, Any], test_input: Dict[str, Any]
    ) -> float:
        """Calculate performance score based on response time thresholds"""
        if not performance_metrics:
            return 50.0  # Default score if no metrics available

        total_time_ms = performance_metrics.get("total_response_time_ms", 0)

        # Get test case expectations if available (performance_expectations is at root level)
        performance_expectations = test_input.get("performance_expectations", {})
        ideal_threshold = performance_expectations.get(
            "ideal_response_time_ms", 5000
        )  # Adjusted to 5s
        max_threshold = performance_expectations.get(
            "max_response_time_ms", 10000
        )  # Adjusted to 10s

        # Calculate score based on thresholds
        if total_time_ms <= ideal_threshold:
            return 100.0
        elif total_time_ms <= max_threshold:
            # Linear interpolation between ideal and max
            ratio = (total_time_ms - ideal_threshold) / (
                max_threshold - ideal_threshold
            )
            return 100.0 - (ratio * 25.0)  # Score from 100 down to 75
        else:
            # Over max threshold - score from 75 down to 0
            excess_ratio = min((total_time_ms - max_threshold) / max_threshold, 1.0)
            return 75.0 - (excess_ratio * 75.0)  # Score from 75 down to 0

    def _get_evaluation_prompt(self) -> str:
        """Get evaluation prompt for form validation"""
        return """You are an expert evaluator for AI-powered form validation systems. 

Evaluate the form validation feedback based on these criteria:

1. VALIDATION_CORRECTNESS (0-100): How accurately did the system identify form element issues according to Avni rules?
2. RULE_COVERAGE (0-100): How well did the system cover relevant Avni validation rules for this form element?
3. RECOMMENDATION_QUALITY (0-100): How actionable and specific are the improvement recommendations?
4. COMPLETENESS (0-100): How comprehensive is the validation feedback?

IMPORTANT: The validation system returns enhanced JSON responses like:
- {"issues": [{"formElementUuid": "uuid", "formElementName": "field", "message": "CRITICAL: Name field should not be in IndividualProfile form"}]}
- {"issues": []} (for valid forms with no issues)

Evaluate based on the ISSUES array content, not expecting a summary field. Consider:
- Does the message correctly identify the core issue?
- Does it provide a clear recommendation?
- Is the recommendation actionable?
- Does it address critical Avni rules?

Distinguish between CRITICAL violations and minor improvement suggestions:
- CRITICAL: Name fields in IndividualProfile, wrong dataType for numeric data, etc.
- MINOR: "Should configure bounds", "Consider making mandatory", etc.
- Score 90-100 for forms with only minor suggestions (they're essentially valid)
- Score 70-85 for forms with actual violations but good recommendations

Scoring Guidelines:
- 90-100: Perfect issue identification or only minor suggestions for valid forms
- 75-89: Correct issue identification but recommendation could be more specific
- 60-74: Partially correct but missing key details or unclear recommendation
- 40-59: Incorrect or vague feedback
- 0-39: No useful validation feedback

Critical Avni Rules to consider:
- Name/Relatives fields in IndividualProfile forms should be CRITICAL issues
- Numeric data (age, weight) should not use Text dataType
- Phone numbers should have proper validation
- Subject dataType should only be used for relationships
- Form elements should have appropriate dataTypes for their content

Return your evaluation as a JSON object with this format:
{
    "scores": {
        "validation_correctness": <score>,
        "rule_coverage": <score>,
        "recommendation_quality": <score>,
        "completeness": <score>
    },
    "overall_success": true/false,
    "error_message": "Any error message if applicable",
    "error_categories": ["category1", "category2"]
}

"""

    def _get_evaluation_metrics(self) -> List[str]:
        """Get evaluation metrics for form validation"""
        return [
            "validation_correctness",
            "rule_coverage",
            "recommendation_quality",
            "completeness",
        ]
