"""
IssueIdentifier module for detecting problems in Avni forms.

This DSPy module analyzes form structures to identify:
- Critical violations (Name fields in registration forms)
- High priority issues (wrong dataTypes like Age as Text)
- Medium priority issues (validation problems)
- Low priority issues (missing optional fields)
"""

import dspy
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class IssueIdentifier(dspy.Module):
    """
    Identifies issues and problems in Avni form configurations.

    Analyzes form JSON structure to find violations of Avni rules,
    data type mismatches, validation problems, and other issues.
    """

    def __init__(self):
        super().__init__()
        self.analyzer = dspy.ChainOfThought(AvniIssueIdentificationSignature)

    def forward(self, form_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify all issues in the form.

        Args:
            form_json: Complete form configuration as dictionary

        Returns:
            Structured list of identified issues with severity and details
        """
        form_str = json.dumps(form_json, indent=2)

        try:
            result = self.analyzer(form_structure=form_str)

            # Parse JSON outputs if they're strings
            try:
                issues = (
                    json.loads(result.issues)
                    if isinstance(result.issues, str)
                    else result.issues
                )
            except json.JSONDecodeError:
                issues = result.issues

            return {"issues": issues, "summary": result.summary}

        except Exception as e:
            logger.error(f"Issue identification failed: {e}")
            return {"issues": [], "summary": f"Issue identification failed: {str(e)}"}


class AvniIssueIdentificationSignature(dspy.Signature):
    """You are an expert Avni form validator specializing in identifying form issues and rule violations.

    Your task is to analyze Avni form JSON structures and identify all problems, violations, and issues.

    Key Responsibilities:
    1. Identify CRITICAL violations (Name fields in registration - system auto-handles these)
    2. Detect HIGH priority issues (wrong dataTypes like Age as Text instead of Numeric)
    3. Find MEDIUM priority issues (validation problems, inconsistent naming)
    4. Identify LOW priority issues (missing optional fields, minor improvements)

    Critical Avni Rules to Check:
    - Name/Relatives in IndividualProfile: CRITICAL - system auto-handles, remove immediately
    - Numeric data as Text dataType: HIGH - use Numeric with bounds (age: 0-120, weight: 0.5-200)
    - Phone without validation: MEDIUM - use PhoneNumber dataType with regex
    - Voided fields present: MEDIUM - remove completely from active forms
    - Subject dataType for categories: MEDIUM - use Coded dataType instead
    - MultiSelect for Yes/No questions: MEDIUM - should be SingleSelect
    - Missing mandatory field declarations: LOW - ensure important fields are marked mandatory

    Output Format Requirements:
    - Issues: JSON array with category, message, severity, formElementUuid, formElementName, suggestedFix
    - Summary: Brief text summary of total issues found

    Always reference specific form element UUIDs when available so the UI can highlight exact fields needing changes."""

    form_structure = dspy.InputField(
        desc="Complete Avni form JSON with formElementGroups, field configurations, and UUIDs"
    )

    issues = dspy.OutputField(
        desc='JSON array of issues: [{"category": "Data Type", "message": "Age field using Text dataType should use Numeric", "severity": "High", "formElementUuid": "uuid-123", "formElementName": "Age", "suggestedFix": "Change dataType from Text to Numeric with bounds 0-120"}]'
    )
    summary = dspy.OutputField(
        desc="Brief summary text of total issues found and main problems"
    )
