"""
Simplified DSPy MIPROv2 training for Avni form analysis.

This module trains two simplified modules:
1. IssueIdentifier - identifies problems in forms
2. SuggestionGenerator - generates improvement recommendations
"""

import dspy
from typing import List, Dict, Any
import logging
import json
import pickle
import os
from .issue_identifier import IssueIdentifier
from .suggestion_generator import SuggestionGenerator

logger = logging.getLogger(__name__)


def create_issue_identification_examples() -> List[dspy.Example]:
    """Create training examples for issue identification."""

    examples = [
        # Form with critical name field issue
        dspy.Example(
            form_structure='{"name": "Registration", "formType": "IndividualProfile", "formElementGroups": [{"formElements": [{"name": "Name", "uuid": "name-123", "concept": {"dataType": "Text"}}, {"name": "Age", "uuid": "age-123", "concept": {"dataType": "Text"}}]}]}',
            issues='[{"category": "Critical Rule Violation", "message": "Manual name field in registration form", "severity": "critical", "formElementUuid": "name-123", "formElementName": "Name", "suggestedFix": "Remove - system auto-handles names"}, {"category": "Data Type", "message": "Age field using Text dataType should use Numeric", "severity": "high", "formElementUuid": "age-123", "formElementName": "Age", "suggestedFix": "Change dataType from Text to Numeric with bounds 0-120"}]',
            summary="Found 2 issues: 1 critical name field violation and 1 high priority dataType issue",
        ).with_inputs("form_structure"),
        # Form with phone validation issue
        dspy.Example(
            form_structure='{"name": "Contact Form", "formElementGroups": [{"formElements": [{"name": "Phone Number", "uuid": "phone-123", "concept": {"dataType": "Text"}}, {"name": "Do you have insurance?", "uuid": "insurance-123", "concept": {"dataType": "Coded", "answers": ["yes", "no"]}, "type": "MultiSelect"}]}]}',
            issues='[{"category": "Validation", "message": "Phone field missing validation pattern", "severity": "medium", "formElementUuid": "phone-123", "formElementName": "Phone Number", "suggestedFix": "Change dataType to PhoneNumber or add regex validation"}, {"category": "Field Type", "message": "Yes/No question using MultiSelect should use SingleSelect", "severity": "medium", "formElementUuid": "insurance-123", "formElementName": "Do you have insurance?", "suggestedFix": "Change type from MultiSelect to SingleSelect"}]',
            summary="Found 2 medium priority issues: phone validation and incorrect select type",
        ).with_inputs("form_structure"),
        # Well-structured form with no issues
        dspy.Example(
            form_structure='{"name": "Assessment Form", "formElementGroups": [{"formElements": [{"name": "Weight", "uuid": "weight-123", "concept": {"dataType": "Numeric", "lowAbsolute": 1, "highAbsolute": 200, "unit": "kg"}}, {"name": "Blood Group", "uuid": "blood-123", "concept": {"dataType": "Coded", "answers": ["A+", "B+", "O+", "AB+"]}, "type": "SingleSelect"}]}]}',
            issues="[]",
            summary="No issues found - form follows Avni best practices",
        ).with_inputs("form_structure"),
        # Form with relatives field issue
        dspy.Example(
            form_structure='{"name": "Individual Registration", "formType": "IndividualProfile", "formElementGroups": [{"formElements": [{"name": "Relatives", "uuid": "relatives-123", "concept": {"dataType": "Subject"}}, {"name": "Emergency Contact", "uuid": "contact-123", "concept": {"dataType": "Text"}}]}]}',
            issues='[{"category": "Field Type", "message": "Relatives field in individual registration should use household subject types", "severity": "high", "formElementUuid": "relatives-123", "formElementName": "Relatives", "suggestedFix": "Replace with household subject type or remove if not needed"}, {"category": "Validation", "message": "Emergency contact field should use PhoneNumber dataType", "severity": "medium", "formElementUuid": "contact-123", "formElementName": "Emergency Contact", "suggestedFix": "Change dataType to PhoneNumber for built-in validation"}]',
            summary="Found 2 issues: incorrect relatives field implementation and missing phone validation",
        ).with_inputs("form_structure"),
        # Form with voided fields
        dspy.Example(
            form_structure='{"name": "Survey Form", "formElementGroups": [{"formElements": [{"name": "Old Question", "uuid": "old-123", "concept": {"dataType": "Text"}, "voided": true}, {"name": "Current Question", "uuid": "current-123", "concept": {"dataType": "Text"}}]}]}',
            issues='[{"category": "Data Quality", "message": "Voided field present in active form", "severity": "medium", "formElementUuid": "old-123", "formElementName": "Old Question", "suggestedFix": "Remove voided fields completely from active forms"}]',
            summary="Found 1 medium issue: voided field should be removed",
        ).with_inputs("form_structure"),
    ]

    return examples


def create_suggestion_generation_examples() -> List[dspy.Example]:
    """Create training examples for suggestion generation."""

    examples = [
        # Suggestions based on critical and high issues
        dspy.Example(
            form_structure='{"name": "Registration", "formType": "IndividualProfile", "formElementGroups": [{"formElements": [{"name": "Name", "uuid": "name-123", "concept": {"dataType": "Text"}}, {"name": "Age", "uuid": "age-123", "concept": {"dataType": "Text"}}]}]}',
            identified_issues='[{"category": "Critical Rule Violation", "message": "Manual name field in registration form", "severity": "critical", "formElementUuid": "name-123", "formElementName": "Name", "suggestedFix": "Remove - system auto-handles names"}, {"category": "Data Type", "message": "Age field using Text dataType should use Numeric", "severity": "high", "formElementUuid": "age-123", "formElementName": "Age", "suggestedFix": "Change dataType from Text to Numeric with bounds 0-120"}]',
            suggestions='[{"type": "Critical Fix", "title": "Remove manual name field", "description": "Remove Name field from registration form", "priority": "Critical", "formElementUuid": "name-123", "implementation": {"action": "remove"}, "rationale": "System auto-handles name fields in registration forms"}, {"type": "Data Type Fix", "title": "Fix Age dataType", "description": "Change Age field from Text to Numeric", "priority": "High", "formElementUuid": "age-123", "implementation": {"dataType": "Numeric", "lowAbsolute": 0, "highAbsolute": 120}, "rationale": "Age should be numeric for proper validation and analysis"}, {"type": "Enhancement", "title": "Add emergency contact", "description": "Consider adding emergency contact field", "priority": "Medium", "implementation": {"dataType": "PhoneNumber", "mandatory": true}, "rationale": "Emergency contact is useful for registration forms"}]',
        ).with_inputs("form_structure", "identified_issues"),
        # Suggestions for medium priority issues
        dspy.Example(
            form_structure='{"name": "Contact Form", "formElementGroups": [{"formElements": [{"name": "Phone Number", "uuid": "phone-123", "concept": {"dataType": "Text"}}, {"name": "Do you have insurance?", "uuid": "insurance-123", "concept": {"dataType": "Coded", "answers": ["yes", "no"]}, "type": "MultiSelect"}]}]}',
            identified_issues='[{"category": "Validation", "message": "Phone field missing validation pattern", "severity": "medium", "formElementUuid": "phone-123", "formElementName": "Phone Number", "suggestedFix": "Change dataType to PhoneNumber or add regex validation"}, {"category": "Field Type", "message": "Yes/No question using MultiSelect should use SingleSelect", "severity": "medium", "formElementUuid": "insurance-123", "formElementName": "Do you have insurance?", "suggestedFix": "Change type from MultiSelect to SingleSelect"}]',
            suggestions='[{"type": "Validation Fix", "title": "Add phone validation", "description": "Change phone field to use PhoneNumber dataType", "priority": "Medium", "formElementUuid": "phone-123", "implementation": {"dataType": "PhoneNumber"}, "rationale": "PhoneNumber dataType provides built-in validation"}, {"type": "Field Type Fix", "title": "Fix insurance question type", "description": "Change from MultiSelect to SingleSelect for Yes/No question", "priority": "Medium", "formElementUuid": "insurance-123", "implementation": {"type": "SingleSelect"}, "rationale": "Binary questions should use SingleSelect"}, {"type": "Enhancement", "title": "Add email field", "description": "Consider adding email field for better contact options", "priority": "Low", "implementation": {"dataType": "Text", "validFormat": "email"}, "rationale": "Email provides alternative contact method"}]',
        ).with_inputs("form_structure", "identified_issues"),
        # Suggestions for form with no issues
        dspy.Example(
            form_structure='{"name": "Assessment Form", "formElementGroups": [{"formElements": [{"name": "Weight", "uuid": "weight-123", "concept": {"dataType": "Numeric", "lowAbsolute": 1, "highAbsolute": 200, "unit": "kg"}}, {"name": "Blood Group", "uuid": "blood-123", "concept": {"dataType": "Coded", "answers": ["A+", "B+", "O+", "AB+"]}, "type": "SingleSelect"}]}]}',
            identified_issues="[]",
            suggestions='[{"type": "Enhancement", "title": "Add height field", "description": "Consider adding height field to complement weight", "priority": "Low", "implementation": {"dataType": "Numeric", "lowAbsolute": 30, "highAbsolute": 250, "unit": "cm"}, "rationale": "Height and weight together provide better health metrics"}, {"type": "Enhancement", "title": "Add date of assessment", "description": "Consider adding assessment date for tracking", "priority": "Low", "implementation": {"dataType": "Date", "mandatory": true}, "rationale": "Date helps track when assessment was conducted"}]',
        ).with_inputs("form_structure", "identified_issues"),
    ]

    return examples


class SimplifiedAvniAnalyzer(dspy.Module):
    """Simplified analyzer that coordinates IssueIdentifier and SuggestionGenerator."""

    def __init__(self):
        super().__init__()
        self.issue_identifier = IssueIdentifier()
        self.suggestion_generator = SuggestionGenerator()

    def forward(self, form_structure: str) -> Dict[str, Any]:
        """Analyze form by first identifying issues, then generating suggestions."""

        # Parse form structure
        form_json = json.loads(form_structure)

        # Step 1: Identify issues
        issue_results = self.issue_identifier.forward(form_json)
        issues = issue_results.get("issues", [])

        # Step 2: Generate suggestions based on issues
        suggestion_results = self.suggestion_generator.forward(form_json, issues)

        # Combine results
        return {**issue_results, **suggestion_results}


def create_avni_metric() -> callable:
    """Create metric function for MIPROv2 optimization."""

    def avni_correctness_metric(example, pred, trace=None):
        """
        Metric function that evaluates prediction quality for Avni forms.
        """
        score = 0.0

        try:
            # Check if issues are properly identified
            if hasattr(example, "issues") and hasattr(pred, "issues"):
                example_issues = (
                    json.loads(example.issues)
                    if isinstance(example.issues, str)
                    else example.issues
                )
                pred_issues = (
                    json.loads(pred.issues)
                    if isinstance(pred.issues, str)
                    else pred.issues
                )

                # Score based on issue identification accuracy
                if len(example_issues) == 0 and len(pred_issues) == 0:
                    score += 1.0  # Perfect - no issues correctly identified
                elif len(example_issues) > 0 and len(pred_issues) > 0:
                    score += 0.7  # Good - found some issues

                    # Check severity accuracy
                    example_severities = [
                        issue.get("severity", "") for issue in example_issues
                    ]
                    pred_severities = [
                        issue.get("severity", "") for issue in pred_issues
                    ]

                    critical_match = ("critical" in example_severities) == (
                        "critical" in pred_severities
                    )
                    if critical_match:
                        score += 0.3

            # Check suggestions quality
            if hasattr(example, "suggestions") and hasattr(pred, "suggestions"):
                score += 0.5  # Bonus for generating suggestions

            # Ensure score is between 0 and 3 (max score)
            return min(score, 3.0)

        except Exception as e:
            logger.warning(f"Metric evaluation error: {e}")
            return 0.0

    return avni_correctness_metric


async def train_simplified_analyzer(
    config: Dict[str, Any] = None,
) -> SimplifiedAvniAnalyzer:
    """Train the simplified analyzer using MIPROv2."""

    logger.info("Starting simplified Avni analyzer training...")

    # Default config
    if config is None:
        config = {
            "model": "gpt-4o-mini",
            "num_threads": 1,
            "max_bootstrapped_demos": 5,
            "max_labeled_demos": 8,
            "training_steps": 5,
        }

    # Create training examples
    issue_examples = create_issue_identification_examples()
    suggestion_examples = create_suggestion_generation_examples()

    # Combine examples for comprehensive training
    all_examples = issue_examples + suggestion_examples

    logger.info(f"Created {len(all_examples)} training examples")
    logger.info("=== Training Examples Overview ===")
    for i, example in enumerate(all_examples[:3], 1):
        logger.info(f"Example {i}:")
        logger.info(f"  Input fields: {list(example.inputs.keys())}")
        logger.info(f"  Output fields: {list(example.outputs.keys())}")

    # Initialize the module
    analyzer = SimplifiedAvniAnalyzer()

    # Create MIPROv2 optimizer
    training_steps = config.get("training_steps", 5)
    if training_steps <= 3:
        auto_mode = "light"
    elif training_steps <= 7:
        auto_mode = "medium"
    else:
        auto_mode = "heavy"

    optimizer = dspy.MIPROv2(
        metric=create_avni_metric(),
        auto=auto_mode,
        num_threads=config.get("num_threads", 1),
        max_bootstrapped_demos=config["max_bootstrapped_demos"],
        max_labeled_demos=config["max_labeled_demos"],
        verbose=True,
    )

    logger.info("=== Starting MIPROv2 Optimization ===")
    logger.info(f"Training Config: {config}")
    logger.info(f"Auto Mode: {auto_mode}")
    logger.info(f"Training Set Size: {len(all_examples)}")

    # Train the analyzer
    optimized_analyzer = optimizer.compile(
        analyzer, trainset=all_examples, valset=all_examples[:3]
    )

    logger.info("=== MIPROv2 Optimization Completed ===")

    return optimized_analyzer


def save_trained_model(model, filepath: str):
    """Save trained model using pickle."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(model, f)
        logger.info(f"✅ Model saved using pickle to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save model: {e}")


def load_trained_model(filepath: str):
    """Load trained model using pickle."""
    try:
        with open(filepath, "rb") as f:
            model = pickle.load(f)
        logger.info(f"✅ Model loaded from {filepath}")
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None


def check_trained_model_exists(filepath: str) -> bool:
    """Check if trained model file exists."""
    return os.path.exists(filepath)
