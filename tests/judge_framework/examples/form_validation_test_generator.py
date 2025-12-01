#!/usr/bin/env python3
"""
Consolidated Form Validation Test Generator
Combines test matrix generation and new form type test case generation
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any


# All Avni Form Types
FORM_TYPES = [
    "IndividualProfile",
    "HouseholdProfile",
    "PersonProfile",
    "Encounter",
    "ProgramEnrolment",
    "ProgramEncounter",
    "IndividualEncounterCancellation",
    "ProgramEncounterCancellation",
    "ProgramExit",
]

# All Avni Concept Types with their characteristics
CONCEPT_TYPES = {
    "Date": {
        "description": "Date fields for dates of birth, visit dates, etc.",
        "valid_patterns": ["Date of Birth", "Visit Date", "Registration Date"],
        "invalid_patterns": ["Age as Date", "Weight as Date"],
        "common_violations": [
            "Date field used for numeric data",
            "Missing date validation",
        ],
    },
    "DateTime": {
        "description": "DateTime fields for precise timestamps",
        "valid_patterns": ["Visit DateTime", "Measurement DateTime"],
        "invalid_patterns": ["Birth DateTime instead of Date", "Age as DateTime"],
        "common_violations": ["DateTime overkill for simple dates", "Timezone issues"],
    },
    "Text": {
        "description": "Text fields for names, descriptions",
        "valid_patterns": ["Description", "Comments", "Notes"],
        "invalid_patterns": ["Age as Text", "Weight as Text", "Phone as Text"],
        "common_violations": ["Numeric data as Text", "Phone without validation"],
    },
    "Notes": {
        "description": "Long text fields for detailed notes",
        "valid_patterns": ["Clinical Notes", "Observation Notes"],
        "invalid_patterns": ["Age as Notes", "Structured data as Notes"],
        "common_violations": ["Structured data in Notes field", "Character limits"],
    },
    "Numeric": {
        "description": "Numeric fields with bounds",
        "valid_patterns": ["Age", "Weight", "Height", "Temperature"],
        "invalid_patterns": ["Name as Numeric", "Phone as Numeric"],
        "common_violations": ["Missing bounds for age/weight", "Inappropriate ranges"],
    },
    "SingleSelect": {
        "description": "Single selection from predefined options",
        "valid_patterns": ["Gender", "Yes/No questions", "Categories"],
        "invalid_patterns": [
            "Multi-select as SingleSelect",
            "Open text as SingleSelect",
        ],
        "common_violations": [
            "Binary questions as MultiSelect",
            "Insufficient options",
        ],
    },
    "MultiSelect": {
        "description": "Multiple selections from predefined options",
        "valid_patterns": ["Symptoms", "Multiple conditions", "Multiple services"],
        "invalid_patterns": [
            "Binary Yes/No as MultiSelect",
            "Single choice as MultiSelect",
        ],
        "common_violations": [
            "Binary questions as MultiSelect",
            "Related but not multiple",
        ],
    },
    "Image": {
        "description": "Image upload fields",
        "valid_patterns": ["Photo", "Document Scan", "X-ray Image"],
        "invalid_patterns": ["Text data as Image", "Required data as optional Image"],
        "common_violations": ["Image for structured data", "File size/format issues"],
    },
    "Video": {
        "description": "Video upload fields",
        "valid_patterns": ["Training Video", "Procedure Recording"],
        "invalid_patterns": ["Text data as Video", "Patient data as Video"],
        "common_violations": ["Video for simple data", "Storage/bandwidth issues"],
    },
    "Audio": {
        "description": "Audio upload fields",
        "valid_patterns": ["Voice Recording", "Audio Note"],
        "invalid_patterns": ["Text data as Audio", "Structured data as Audio"],
        "common_violations": ["Audio for transcribable data", "Format issues"],
    },
    "File": {
        "description": "General file upload fields",
        "valid_patterns": ["Document Upload", "Report Attachment"],
        "invalid_patterns": ["Structured data as File", "Text data as File"],
        "common_violations": ["File for structured data", "Security concerns"],
    },
    "Coded": {
        "description": "Coded concepts with predefined answer lists",
        "valid_patterns": ["Standardized responses", "Medical codes", "Categories"],
        "invalid_patterns": ["Free text as Coded", "Subject relationships as Coded"],
        "common_violations": [
            "Subject dataType instead of Coded",
            "Missing answer options",
        ],
    },
    "QuestionGroup": {
        "description": "Groups of related questions",
        "valid_patterns": ["Address Group", "Contact Information Group"],
        "invalid_patterns": [
            "Repeatable children as QuestionGroup",
            "Single field as Group",
        ],
        "common_violations": ["Children as QuestionGroup", "Over-grouping"],
    },
    "PhoneNumber": {
        "description": "Phone number fields with validation",
        "valid_patterns": ["Phone Number", "Mobile Number", "Contact Number"],
        "invalid_patterns": ["Phone as Text", "Numeric as Phone"],
        "common_violations": [
            "Phone without validation",
            "International format issues",
        ],
    },
    "Location": {
        "description": "Location selection fields",
        "valid_patterns": ["Village", "District", "Facility Location"],
        "invalid_patterns": ["Text as Location", "Coordinates as Text"],
        "common_violations": ["Location as Text", "Hierarchy validation"],
    },
    "Subject": {
        "description": "Subject relationship fields",
        "valid_patterns": ["Mother Subject", "Household Head"],
        "invalid_patterns": ["Categories as Subject", "Names as Subject"],
        "common_violations": ["Subject for categorical data", "Invalid relationships"],
    },
    "GroupAffiliation": {
        "description": "Group membership fields",
        "valid_patterns": ["Support Group", "Self-Help Group"],
        "invalid_patterns": ["Individual data as GroupAffiliation"],
        "common_violations": ["GroupAffiliation for individual data"],
    },
    "Encounter": {
        "description": "Encounter relationship fields",
        "valid_patterns": ["Previous Visit", "Follow-up Encounter"],
        "invalid_patterns": ["Individual data as Encounter"],
        "common_violations": ["Encounter for individual data"],
    },
}


def generate_critical_violation_tests() -> List[Dict[str, Any]]:
    """Generate critical violation test cases"""

    critical_violations = [
        {
            "test_case_name": "name_field_individual_profile",
            "form_element": {
                "name": "First Name",
                "type": "Text",
                "concept": {"dataType": "Text", "name": "First Name"},
                "mandatory": True,
                "uuid": "name-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": [
                "CRITICAL: Name field should not be in IndividualProfile form"
            ],
            "test_priority": "CRITICAL",
        },
        {
            "test_case_name": "age_as_text_violation",
            "form_element": {
                "name": "Age",
                "type": "SingleSelect",
                "concept": {"dataType": "Text", "name": "Age"},
                "mandatory": True,
                "uuid": "age-text-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": [
                "HIGH: Age field using Text dataType instead of Numeric"
            ],
            "test_priority": "CRITICAL",
        },
        {
            "test_case_name": "phone_as_text_violation",
            "form_element": {
                "name": "Phone Number",
                "type": "Text",
                "concept": {"dataType": "Text", "name": "Phone Number"},
                "mandatory": False,
                "uuid": "phone-text-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": ["MEDIUM: Phone field should use PhoneNumber dataType"],
            "test_priority": "CRITICAL",
        },
        {
            "test_case_name": "binary_yes_no_multiselect",
            "form_element": {
                "name": "Has Ration Card",
                "type": "MultiSelect",
                "concept": {
                    "dataType": "Coded",
                    "name": "Has Ration Card",
                    "answers": [{"name": "Yes"}, {"name": "No"}],
                },
                "mandatory": True,
                "uuid": "binary-multiselect-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": [
                "MEDIUM: Binary question should use SingleSelect instead of MultiSelect"
            ],
            "test_priority": "CRITICAL",
        },
    ]

    return critical_violations


def generate_high_priority_tests() -> List[Dict[str, Any]]:
    """Generate high priority violation test cases"""

    high_priority_violations = [
        {
            "test_case_name": "weight_as_text",
            "form_element": {
                "name": "Weight",
                "type": "SingleSelect",
                "concept": {"dataType": "Text", "name": "Weight"},
                "mandatory": False,
                "uuid": "weight-text-uuid",
            },
            "form_context": {
                "formType": "ProgramEncounter",
                "domain": "health",
                "formName": "Growth Monitoring",
            },
            "expected_issues": ["HIGH: Weight field should use Numeric dataType"],
            "test_priority": "HIGH",
        },
        {
            "test_case_name": "height_as_text",
            "form_element": {
                "name": "Height",
                "type": "Text",
                "concept": {"dataType": "Text", "name": "Height"},
                "mandatory": False,
                "uuid": "height-text-uuid",
            },
            "form_context": {
                "formType": "ProgramEncounter",
                "domain": "health",
                "formName": "Growth Monitoring",
            },
            "expected_issues": ["HIGH: Height field should use Numeric dataType"],
            "test_priority": "HIGH",
        },
        {
            "test_case_name": "subject_for_categorical_data",
            "form_element": {
                "name": "Education Level",
                "type": "SingleSelect",
                "concept": {"dataType": "Subject", "name": "Education Level"},
                "mandatory": False,
                "uuid": "subject-categorical-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": [
                "MEDIUM: Subject dataType should only be used for relationships"
            ],
            "test_priority": "HIGH",
        },
        {
            "test_case_name": "children_as_question_group",
            "form_element": {
                "name": "Children Details",
                "type": "QuestionGroup",
                "concept": {"dataType": "QuestionGroup", "name": "Children Details"},
                "mandatory": False,
                "repeatable": True,
                "uuid": "children-group-uuid",
            },
            "form_context": {
                "formType": "HouseholdProfile",
                "domain": "health",
                "formName": "Household Registration",
            },
            "expected_issues": [
                "HIGH: Children should be separate subject types, not QuestionGroup"
            ],
            "test_priority": "HIGH",
        },
    ]

    return high_priority_violations


def generate_cancellation_form_tests() -> List[Dict[str, Any]]:
    """Generate test cases for Cancellation form types"""

    cancellation_tests = [
        {
            "test_case_name": "cancellation_form_mandatory_reason",
            "form_element": {
                "name": "Cancellation Reason",
                "type": "SingleSelect",
                "concept": {
                    "dataType": "Coded",
                    "name": "Cancellation Reason",
                    "answers": [
                        {"name": "User Request"},
                        {"name": "System Error"},
                        {"name": "Data Entry Error"},
                        {"name": "Duplicate Entry"},
                    ],
                },
                "mandatory": False,
                "uuid": "cancellation-reason-uuid",
            },
            "form_context": {
                "formType": "IndividualEncounterCancellation",
                "domain": "health",
                "formName": "Encounter Cancellation",
            },
            "expected_issues": [
                "HIGH: Cancellation reason should be mandatory in cancellation forms"
            ],
            "test_priority": "HIGH",
            "source": "new_form_type_analysis",
        },
        {
            "test_case_name": "cancellation_form_text_reason_instead_of_coded",
            "form_element": {
                "name": "Cancellation Reason",
                "type": "Text",
                "concept": {"dataType": "Text", "name": "Cancellation Reason"},
                "mandatory": True,
                "uuid": "cancellation-text-uuid",
            },
            "form_context": {
                "formType": "ProgramEncounterCancellation",
                "domain": "health",
                "formName": "Program Encounter Cancellation",
            },
            "expected_issues": [
                "MEDIUM: Cancellation reason should use Coded dataType with predefined options"
            ],
            "test_priority": "MEDIUM",
            "source": "new_form_type_analysis",
        },
        {
            "test_case_name": "cancellation_form_datetime_validation",
            "form_element": {
                "name": "Cancellation Date",
                "type": "Text",
                "concept": {"dataType": "Text", "name": "Cancellation Date"},
                "mandatory": True,
                "uuid": "cancellation-date-uuid",
            },
            "form_context": {
                "formType": "IndividualEncounterCancellation",
                "domain": "health",
                "formName": "Encounter Cancellation",
            },
            "expected_issues": ["HIGH: Date fields should use Date dataType, not Text"],
            "test_priority": "HIGH",
            "source": "new_form_type_analysis",
        },
    ]

    return cancellation_tests


def generate_program_exit_form_tests() -> List[Dict[str, Any]]:
    """Generate test cases for ProgramExit form types"""

    program_exit_tests = [
        {
            "test_case_name": "program_exit_mandatory_exit_reason",
            "form_element": {
                "name": "Exit Reason",
                "type": "SingleSelect",
                "concept": {
                    "dataType": "Coded",
                    "name": "Exit Reason",
                    "answers": [
                        {"name": "Completed"},
                        {"name": "Transferred Out"},
                        {"name": "Lost to Follow-up"},
                        {"name": "Deceased"},
                        {"name": "Withdrawn Consent"},
                    ],
                },
                "mandatory": False,
                "uuid": "exit-reason-uuid",
            },
            "form_context": {
                "formType": "ProgramExit",
                "domain": "health",
                "formName": "Program Exit Form",
            },
            "expected_issues": [
                "HIGH: Exit reason should be mandatory in program exit forms"
            ],
            "test_priority": "HIGH",
            "source": "new_form_type_analysis",
        },
        {
            "test_case_name": "program_exit_exit_date_validation",
            "form_element": {
                "name": "Exit Date",
                "type": "Text",
                "concept": {"dataType": "Text", "name": "Exit Date"},
                "mandatory": True,
                "uuid": "exit-date-uuid",
            },
            "form_context": {
                "formType": "ProgramExit",
                "domain": "health",
                "formName": "Program Exit Form",
            },
            "expected_issues": ["HIGH: Date fields should use Date dataType, not Text"],
            "test_priority": "HIGH",
            "source": "new_form_type_analysis",
        },
        {
            "test_case_name": "program_exit_followup_plan_text_instead_of_notes",
            "form_element": {
                "name": "Follow-up Plan",
                "type": "Text",
                "concept": {"dataType": "Text", "name": "Follow-up Plan"},
                "mandatory": False,
                "uuid": "followup-plan-uuid",
            },
            "form_context": {
                "formType": "ProgramExit",
                "domain": "health",
                "formName": "Program Exit Form",
            },
            "expected_issues": [
                "LOW: Follow-up plans should use Notes dataType for detailed text"
            ],
            "test_priority": "LOW",
            "source": "new_form_type_analysis",
        },
    ]

    return program_exit_tests


def generate_valid_configuration_tests() -> List[Dict[str, Any]]:
    """Generate valid configuration test cases"""

    valid_configurations = [
        {
            "test_case_name": "valid_numeric_age",
            "form_element": {
                "name": "Age",
                "type": "Text",
                "concept": {
                    "dataType": "Numeric",
                    "name": "Age",
                    "lowAbsolute": 0,
                    "highAbsolute": 120,
                },
                "mandatory": True,
                "uuid": "valid-age-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": [],
            "test_priority": "VALID",
        },
        {
            "test_case_name": "valid_phone_number",
            "form_element": {
                "name": "Phone Number",
                "type": "Text",
                "concept": {"dataType": "PhoneNumber", "name": "Phone Number"},
                "mandatory": False,
                "uuid": "valid-phone-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": [],
            "test_priority": "VALID",
        },
        {
            "test_case_name": "valid_date_field",
            "form_element": {
                "name": "Date of Birth",
                "type": "Text",
                "concept": {"dataType": "Date", "name": "Date of Birth"},
                "mandatory": True,
                "uuid": "valid-dob-uuid",
            },
            "form_context": {
                "formType": "IndividualProfile",
                "domain": "health",
                "formName": "Patient Registration",
            },
            "expected_issues": [],
            "test_priority": "VALID",
        },
        {
            "test_case_name": "valid_cancellation_form_proper_setup",
            "form_element": {
                "name": "Cancellation Reason",
                "type": "SingleSelect",
                "concept": {
                    "dataType": "Coded",
                    "name": "Cancellation Reason",
                    "answers": [
                        {"name": "User Request"},
                        {"name": "System Error"},
                        {"name": "Data Entry Error"},
                    ],
                },
                "mandatory": True,
                "uuid": "valid-cancellation-uuid",
            },
            "form_context": {
                "formType": "IndividualEncounterCancellation",
                "domain": "health",
                "formName": "Encounter Cancellation",
            },
            "expected_issues": [],
            "test_priority": "VALID",
            "source": "new_form_type_analysis",
        },
        {
            "test_case_name": "valid_program_exit_form_proper_setup",
            "form_element": {
                "name": "Exit Date",
                "type": "Text",
                "concept": {"dataType": "Date", "name": "Exit Date"},
                "mandatory": True,
                "uuid": "valid-exit-date-uuid",
            },
            "form_context": {
                "formType": "ProgramExit",
                "domain": "health",
                "formName": "Program Exit Form",
            },
            "expected_issues": [],
            "test_priority": "VALID",
            "source": "new_form_type_analysis",
        },
    ]

    return valid_configurations


def generate_comprehensive_test_matrix() -> List[Dict[str, Any]]:
    """Generate comprehensive test matrix with all test cases"""

    print("🔍 Generating Comprehensive Form Validation Test Matrix")
    print("=" * 60)

    # Generate all test case categories
    critical_tests = generate_critical_violation_tests()
    high_priority_tests = generate_high_priority_tests()
    cancellation_tests = generate_cancellation_form_tests()
    program_exit_tests = generate_program_exit_form_tests()
    valid_tests = generate_valid_configuration_tests()

    # Combine all test cases
    all_test_cases = (
        critical_tests
        + high_priority_tests
        + cancellation_tests
        + program_exit_tests
        + valid_tests
    )

    # Analyze distribution
    priority_counts = {}
    concept_type_counts = {}
    form_type_counts = {}

    for test_case in all_test_cases:
        priority = test_case["test_priority"]
        concept_type = test_case["form_element"]["concept"]["dataType"]
        form_type = test_case["form_context"]["formType"]

        priority_counts[priority] = priority_counts.get(priority, 0) + 1
        concept_type_counts[concept_type] = concept_type_counts.get(concept_type, 0) + 1
        form_type_counts[form_type] = form_type_counts.get(form_type, 0) + 1

    print(f"📊 Generated {len(all_test_cases)} comprehensive test cases")
    print(f"   Priority Distribution: {dict(priority_counts)}")
    print(f"   Concept Types Covered: {len(concept_type_counts)}")
    print(f"   Form Types Covered: {len(form_type_counts)}")

    return all_test_cases


def generate_new_form_type_tests() -> List[Dict[str, Any]]:
    """Generate test cases specifically for new form types discovered"""

    print("🧪 Generating Test Cases for New Form Types")
    print("=" * 50)

    cancellation_tests = generate_cancellation_form_tests()
    program_exit_tests = generate_program_exit_form_tests()
    valid_tests = [
        {
            "test_case_name": "valid_cancellation_form_proper_setup",
            "form_element": {
                "name": "Cancellation Reason",
                "type": "SingleSelect",
                "concept": {
                    "dataType": "Coded",
                    "name": "Cancellation Reason",
                    "answers": [
                        {"name": "User Request"},
                        {"name": "System Error"},
                        {"name": "Data Entry Error"},
                    ],
                },
                "mandatory": True,
                "uuid": "valid-cancellation-uuid",
            },
            "form_context": {
                "formType": "IndividualEncounterCancellation",
                "domain": "health",
                "formName": "Encounter Cancellation",
            },
            "expected_issues": [],
            "test_priority": "VALID",
            "source": "new_form_type_analysis",
        }
    ]

    all_new_tests = cancellation_tests + program_exit_tests + valid_tests

    print("📊 Test Cases Generated:")
    print(f"   Cancellation Form Tests: {len(cancellation_tests)}")
    print(f"   Program Exit Form Tests: {len(program_exit_tests)}")
    print(f"   Valid Form Type Tests: {len(valid_tests)}")
    print(f"   Total New Tests: {len(all_new_tests)}")

    return all_new_tests


def save_test_matrix(test_cases: List[Dict[str, Any]], filename: str) -> bool:
    """Save test matrix to file and update comprehensive matrix if needed"""

    try:
        # Save to specified file
        output_dir = Path(
            "/Users/himeshr/IdeaProjects/avni-ai/tests/judge_framework/test_suites/formElementValidation"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / filename
        with open(output_file, "w") as f:
            json.dump(test_cases, f, indent=2)

        print(f"✅ Test matrix saved to: {output_file}")

        # If this is the comprehensive matrix, also save to docs
        if filename == "comprehensive_form_validation_test_matrix.json":
            docs_dir = Path("/Users/himeshr/IdeaProjects/avni-ai/docs/form_validation")
            docs_dir.mkdir(parents=True, exist_ok=True)

            docs_file = docs_dir / filename
            with open(docs_file, "w") as f:
                json.dump(test_cases, f, indent=2)

            print(f"✅ Test matrix also saved to: {docs_file}")

        return True

    except Exception as e:
        print(f"❌ Failed to save test matrix: {e}")
        return False


def update_comprehensive_matrix(new_test_cases: List[Dict[str, Any]]) -> bool:
    """Update the comprehensive test matrix with new test cases"""

    comprehensive_matrix_file = "/Users/himeshr/IdeaProjects/avni-ai/tests/judge_framework/test_suites/formElementValidation/comprehensive_form_validation_test_matrix.json"

    if not Path(comprehensive_matrix_file).exists():
        print("⚠️  Comprehensive test matrix not found, creating new one")
        return save_test_matrix(
            new_test_cases, "comprehensive_form_validation_test_matrix.json"
        )

    try:
        with open(comprehensive_matrix_file, "r") as f:
            existing_matrix = json.load(f)

        original_count = len(existing_matrix)
        existing_matrix.extend(new_test_cases)

        with open(comprehensive_matrix_file, "w") as f:
            json.dump(existing_matrix, f, indent=2)

        print("✅ Enhanced comprehensive test matrix:")
        print(f"   Original test cases: {original_count}")
        print(f"   Added new test cases: {len(new_test_cases)}")
        print(f"   Total test cases: {len(existing_matrix)}")

        return True

    except Exception as e:
        print(f"❌ Failed to update comprehensive test matrix: {e}")
        return False


def main():
    """Main entry point for consolidated test generator"""
    parser = argparse.ArgumentParser(description="Form Validation Test Generator")
    parser.add_argument(
        "mode",
        choices=["comprehensive", "new-form-types", "update-comprehensive"],
        help="Generation mode: comprehensive (all tests), new-form-types (only new form types), update-comprehensive (add new tests to existing matrix)",
    )

    args = parser.parse_args()

    print("🧪 Form Validation Test Generator")
    print("=" * 50)

    # Generate test cases based on mode
    if args.mode == "comprehensive":
        test_cases = generate_comprehensive_test_matrix()
        success = save_test_matrix(
            test_cases, "comprehensive_form_validation_test_matrix.json"
        )

    elif args.mode == "new-form-types":
        test_cases = generate_new_form_type_tests()
        success = save_test_matrix(test_cases, "new_form_type_test_cases.json")

    elif args.mode == "update-comprehensive":
        test_cases = generate_new_form_type_tests()
        success = update_comprehensive_matrix(test_cases)

    # Generate summary
    if success and test_cases:
        summary = {
            "generation_mode": args.mode,
            "total_test_cases": len(test_cases),
            "form_types_covered": list(
                set(tc["form_context"]["formType"] for tc in test_cases)
            ),
            "concept_types_covered": list(
                set(tc["form_element"]["concept"]["dataType"] for tc in test_cases)
            ),
            "priority_distribution": {},
        }

        for tc in test_cases:
            priority = tc["test_priority"]
            summary["priority_distribution"][priority] = (
                summary["priority_distribution"].get(priority, 0) + 1
            )

        # Save summary
        output_dir = Path("/Users/himeshr/IdeaProjects/avni-ai/docs/form_validation")
        output_dir.mkdir(parents=True, exist_ok=True)

        summary_file = output_dir / f"test_generation_summary_{args.mode}.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"✅ Generation summary saved to: {summary_file}")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
