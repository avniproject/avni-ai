import dspy
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
            error_msg = str(e)

            # Return a simple object with the expected attributes
            class ErrorResult:
                def __init__(self):
                    self.issues = "[]"

            return ErrorResult()


class AvniIssueIdentificationSignature(dspy.Signature):
    """You are an expert Avni form element validator specializing in identifying form issues and rule violations.

    Your task is to analyze Avni form element JSON structures and identify all problems, violations, and issues.

    Key Responsibilities:
    1. Identify violations (Name fields in registration - system auto-handles these)
    2. Detect issues (wrong dataTypes like Age as Text instead of Numeric, validation problems, inconsistent naming, missing optional fields, minor improvements)

    Critical Avni Rules to Check:
    
    1. DATE FIELD VALIDATION (CRITICAL):
       - Date fields should NEVER be suggested as SingleSelect
       - Date dataType is used for: birth dates, visit dates, exit dates, cancellation dates
       - Any field representing a point in time should use Date dataType
       - Date selection is NOT categorical selection
       - INCORRECT: "Use SingleSelect for Exit Date field"
       - CORRECT: "Exit Date should use Date dataType, not Text"

    2. NEW FORM TYPES - CANCELLATION FORMS:
       - IndividualEncounterCancellation & ProgramEncounterCancellation forms
       - Cancellation reason should be MANDATORY and use Coded dataType
       - Cancellation date should use Date dataType (never SingleSelect)
       - These forms require different validation than regular encounters

    3. NEW FORM TYPES - PROGRAM EXIT FORMS:
       - ProgramExit forms have specific requirements
       - Exit reason should be MANDATORY and use Coded dataType
       - Exit date should use Date dataType (never SingleSelect)
       - Follow-up plans should use Text dataType (Notes is not recognized)

    4. NAME FIELD DETECTION:
       - Name fields in IndividualProfile forms are CRITICAL violations
       - ANY field named 'First Name', 'Last Name', 'Name' in IndividualProfile should be flagged
       - These fields should be removed or moved to subject details
       - Do not suggest keeping name fields in IndividualProfile forms

    5. DATA TYPE COMPLIANCE:
       - Numeric data (Age, Weight, Height) should use Numeric dataType with bounds
       - Phone numbers should use PhoneNumber dataType with validation
       - Binary questions (Yes/No) should use SingleSelect, not MultiSelect
       - Categorical data should use Coded dataType, not Subject

    6. FALSE POSITIVE PREVENTION:
       - Before suggesting changes, verify actual violation of Avni rules
       - Don't suggest changes to properly configured fields
       - Focus on actual violations, not theoretical improvements

    7. LEGACY RULES:
    - Name/Relatives in IndividualProfile: CRITICAL - system auto-handles, remove immediately
    - Numeric data as Text dataType: HIGH - use Numeric with bounds (age: 0-120, weight: 0.5-200)
    - Phone without validation: MEDIUM - use PhoneNumber dataType with regex
    - Voided fields present: MEDIUM - remove completely from active forms
    - Subject dataType for categories: MEDIUM - use Coded dataType instead
    - MultiSelect for Yes/No questions: MEDIUM - should be SingleSelect
    - Missing mandatory field declarations: LOW - ensure important fields are marked mandatory

    Output Format Requirements:
    - Issues: JSON array with formElementUuid, formElementName, message
    
    Always reference specific form element UUIDs when available so the UI can highlight exact fields needing changes."""

    form_structure = dspy.InputField(
        desc="Avni form element JSON with field configuration, concept details, and UUID"
    )

    issues = dspy.OutputField(
        desc='JSON array of issues: [{"message": "Age field using Text dataType should use Numeric", "formElementUuid": "uuid-123"}]'
    )
