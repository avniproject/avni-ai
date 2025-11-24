import dspy
import logging

logger = logging.getLogger(__name__)


class SuggestionGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.suggester = dspy.ChainOfThought(AvniSuggestionSignature)

    def forward(self, form_element: str, identified_issues: str):
        try:
            result = self.suggester(
                form_element_structure=form_element, identified_issues=identified_issues
            )
            return result
        except Exception as e:
            logger.error(f"Suggestion generation failed: {e}")

            # Return a simple object with the expected attributes
            class ErrorResult:
                def __init__(self):
                    self.suggestions = "[]"

            return ErrorResult()


class AvniSuggestionSignature(dspy.Signature):
    """You are an expert Avni form element improvement consultant specializing in generating actionable suggestions.

    Your task is to analyze identified form issues and generate practical, prioritized recommendations for improvement.

    Key Responsibilities:
    1. Generate specific suggestions to fix each identified issue
    2. Provide additional improvement recommendations beyond just fixing issues
    3. Suggest new fields that would benefit the form

    Suggestion Categories:
    - Issue Fixes: Direct solutions to identified problems
    - Field Improvements: Better dataTypes, validation, constraints
    - New Fields: Additional beneficial fields for the form
    - Structure Improvements: Better organization, grouping, flow
    - Validation Enhancements: Add missing validations and constraints

    Output Format Requirements:
    - Suggestions: JSON array with affected element, description

    Always provide specific implementation details and reference form element UUIDs when available."""

    form_element_structure = dspy.InputField(
        desc="Avni form element JSON with field configuration, concept details, and UUID"
    )
    identified_issues = dspy.InputField(
        desc="JSON array of identified issues with messages and affected elements"
    )

    suggestions = dspy.OutputField(
        desc='JSON array of suggestions: [{"message": "Change Age field from Text to Numeric. Age should be numeric for proper validation", "formElementUuid": "uuid-123"}]'
    )
