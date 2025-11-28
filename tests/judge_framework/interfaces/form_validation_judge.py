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
    def evaluate(self, test_input: Dict[str, Any], test_output: Dict[str, Any]) -> EvaluationResult:
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
                "error_categories": ["dependency_error"]
            }
        
        try:
            full_prompt = self.evaluation_prompt + evaluation_context
            
            response = openai.chat.completions.create(
                model=self.config.openai_model,
                messages=[{"role": "system", "content": full_prompt}],
                temperature=self.config.openai_temperature,
                max_tokens=1500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                evaluation_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: extract scores from text
                evaluation_data = self._extract_scores_from_text(response_text)
            
            return evaluation_data
            
        except Exception as e:
            return {
                "scores": {metric: 0 for metric in self._get_evaluation_metrics()},
                "overall_success": False,
                "error_message": f"Evaluation failed: {str(e)}",
                "error_categories": ["evaluation_error"]
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
            "error_categories": []
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
    
    def evaluate(self, test_input: Dict[str, Any], test_output: Dict[str, Any]) -> EvaluationResult:
        """
        Evaluate form validation results from Dify workflow
        """
        test_identifier = test_input.get("test_identifier", "unknown")
        form_element = test_input.get("form_element", {})
        validation_feedback = test_output.get("validation_feedback", "")
        expected_issues = test_input.get("expected_issues", [])
        
        # Extract validation details from minimal JSON response
        validation_details = self._parse_validation_response(validation_feedback)
        
        # Format evaluation context
        evaluation_context = f"""
TEST IDENTIFIER: {test_identifier}

FORM ELEMENT:
{json.dumps(form_element, indent=2)}

VALIDATION FEEDBACK:
{validation_feedback}

PARSED VALIDATION DETAILS:
- Message: {validation_details.get('message', 'No message')}
- UUID: {validation_details.get('uuid', 'No UUID')}

EXPECTED ISSUES:
{', '.join(expected_issues) if expected_issues else 'None'}

Evaluate this form validation based on the criteria provided in the prompt.
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
            test_type="form_validation",
            success=overall_success,
            scores=scores,
            details={
                "form_element_name": form_element.get("name", "Unknown"),
                "validation_feedback_length": len(validation_feedback),
                "parsed_validation_details": validation_details,
                "expected_issues": expected_issues,
                "ai_evaluation": ai_evaluation
            },
            error_categories=ai_evaluation.get("error_categories", []),
            error_message=ai_evaluation.get("error_message"),
            execution_metadata={
                "form_element_type": form_element.get("type", "Unknown"),
                "form_element_datatype": form_element.get("concept", {}).get("dataType", "Unknown"),
                "validation_response_format": "minimal_json"
            },
            raw_input=test_input,
            raw_output=test_output
        )
    
    def _parse_validation_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the minimal JSON response from Dify Form Assistant"""
        try:
            import json
            # Try to parse as JSON
            if response_text.strip().startswith('{'):
                parsed = json.loads(response_text.strip())
                return {
                    "uuid": parsed.get("uuid", ""),
                    "message": parsed.get("message", ""),
                    "is_valid": len(parsed.get("message", "")) > 10  # Basic validation
                }
            else:
                # Fallback for non-JSON responses
                return {
                    "uuid": "",
                    "message": response_text.strip(),
                    "is_valid": len(response_text.strip()) > 10
                }
        except (json.JSONDecodeError, Exception):
            return {
                "uuid": "",
                "message": response_text.strip(),
                "is_valid": False
            }
    
    def _get_evaluation_prompt(self) -> str:
        """Get evaluation prompt for form validation"""
        return """You are an expert evaluator for AI-powered form validation systems. 

Evaluate the form validation feedback based on these criteria:

1. VALIDATION_CORRECTNESS (0-100): How accurately did the system identify form element issues according to Avni rules?
2. RULE_COVERAGE (0-100): How well did the system cover relevant Avni validation rules for this form element?
3. RECOMMENDATION_QUALITY (0-100): How actionable and specific are the improvement recommendations?
4. COMPLETENESS (0-100): How comprehensive is the validation feedback?

IMPORTANT: The validation system returns minimal JSON responses like:
- {"uuid": "1", "message": "Change dataType from Text to Numeric for Age field"}
- {"uuid": "4e2a73f4-f498-4a9a-ae51-84434e6d2cca", "message": "Age field should use Numeric dataType."}

Evaluate based on the MESSAGE content, not expecting detailed analysis. Consider:
- Does the message correctly identify the core issue?
- Does it provide a clear recommendation?
- Is the recommendation actionable?
- Does it address critical Avni rules?

Scoring Guidelines:
- 90-100: Perfect issue identification with clear, actionable recommendation
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
            "completeness"
        ]
