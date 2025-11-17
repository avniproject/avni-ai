import dspy
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class IssueIdentifier(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyzer = dspy.ChainOfThought(AvniIssueIdentificationSignature)

    def forward(self, form_element: str):
        try:
            result = self.analyzer(form_structure=form_element)
            return result

        except Exception as e:
            logger.error(f"Issue identification failed: {e}")

            # Return a simple object with the expected attributes
            class ErrorResult:
                def __init__(self):
                    self.issues = "[]"
                    self.summary = f"Issue identification failed: {str(e)}"

            return ErrorResult()


class AvniIssueIdentificationSignature(dspy.Signature):
    """You are an expert Avni form element validator specializing in identifying form issues and rule violations.

    Your task is to analyze Avni form element JSON structures and identify all problems, violations, and issues.

    Key Responsibilities:
    1. Identify violations (Name fields in registration - system auto-handles these)
    2. Detect issues (wrong dataTypes like Age as Text instead of Numeric, validation problems, inconsistent naming, missing optional fields, minor improvements)

    Critical Avni Rules to Check:
    - Name/Relatives in IndividualProfile: CRITICAL - system auto-handles, remove immediately
    - Numeric data as Text dataType: HIGH - use Numeric with bounds (age: 0-120, weight: 0.5-200)
    - Phone without validation: MEDIUM - use PhoneNumber dataType with regex
    - Voided fields present: MEDIUM - remove completely from active forms
    - Subject dataType for categories: MEDIUM - use Coded dataType instead
    - MultiSelect for Yes/No questions: MEDIUM - should be SingleSelect
    - Missing mandatory field declarations: LOW - ensure important fields are marked mandatory

    Output Format Requirements:
    - Issues: JSON array with formElementUuid, formElementName, message
    - Summary: Brief text summary of total issues found

    Always reference specific form element UUIDs when available so the UI can highlight exact fields needing changes."""

    form_structure = dspy.InputField(
        desc="Avni form element JSON with field configuration, concept details, and UUID"
    )

    issues = dspy.OutputField(
        desc='JSON array of issues: [{"message": "Age field using Text dataType should use Numeric", "formElementUuid": "uuid-123"}]'
    )
