#!/usr/bin/env python3
"""
Simplified DSPy Form Analysis Example

This example demonstrates the new simplified approach with two modules:
1. IssueIdentifier - finds problems in forms
2. SuggestionGenerator - generates improvement recommendations
"""

import asyncio
import logging
from pathlib import Path

# Add src to path for imports
import sys

sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.dspy_modules import FormImprovementProgram
from src.dspy_modules.issue_identifier import IssueIdentifier
from src.dspy_modules.suggestion_generator import SuggestionGenerator
import dspy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_form_with_issues():
    """Create a sample form with various issues for testing."""
    return {
        "name": "Patient Registration",
        "formType": "IndividualProfile",
        "formElementGroups": [
            {
                "name": "Basic Information",
                "formElements": [
                    {
                        "name": "Name",
                        "uuid": "name-field-123",
                        "concept": {"dataType": "Text"},
                    },
                    {
                        "name": "Age",
                        "uuid": "age-field-456",
                        "concept": {
                            "dataType": "Text"  # Should be Numeric
                        },
                    },
                    {
                        "name": "Phone Number",
                        "uuid": "phone-field-789",
                        "concept": {
                            "dataType": "Text"  # Should be PhoneNumber
                        },
                    },
                    {
                        "name": "Do you have insurance?",
                        "uuid": "insurance-field-101",
                        "concept": {"dataType": "Coded", "answers": ["yes", "no"]},
                        "type": "MultiSelect",  # Should be SingleSelect
                    },
                ],
            }
        ],
    }


def create_good_form():
    """Create a well-structured form with no issues."""
    return {
        "name": "Health Assessment",
        "formElementGroups": [
            {
                "name": "Measurements",
                "formElements": [
                    {
                        "name": "Weight",
                        "uuid": "weight-field-123",
                        "concept": {
                            "dataType": "Numeric",
                            "lowAbsolute": 1,
                            "highAbsolute": 200,
                            "unit": "kg",
                        },
                    },
                    {
                        "name": "Blood Group",
                        "uuid": "blood-field-456",
                        "concept": {
                            "dataType": "Coded",
                            "answers": ["A+", "B+", "O+", "AB+"],
                        },
                        "type": "SingleSelect",
                    },
                ],
            }
        ],
    }


async def demonstrate_issue_identification():
    """Demonstrate the IssueIdentifier module."""
    print("\n" + "=" * 60)
    print("ISSUE IDENTIFICATION EXAMPLE")
    print("=" * 60)

    # Initialize issue identifier
    identifier = IssueIdentifier()

    # Test with problematic form
    problematic_form = create_sample_form_with_issues()
    print(f"\nAnalyzing form: {problematic_form['name']}")
    print("Form has several issues:")
    print("- Manual Name field in registration")
    print("- Age as Text instead of Numeric")
    print("- Phone without validation")
    print("- MultiSelect for Yes/No question")

    # Identify issues
    issue_results = identifier.forward(problematic_form)

    print("\nISSUES FOUND:")
    issues = issue_results.get("issues", [])
    for issue in issues:
        print(
            f"- {issue.get('severity', 'Unknown').upper()}: {issue.get('message', 'No message')}"
        )
        print(f"  Element: {issue.get('formElementName', 'Unknown')}")
        print(f"  Fix: {issue.get('suggestedFix', 'No fix suggested')}")
        print()

    print(f"Summary: {issue_results.get('summary', 'No summary')}")


async def demonstrate_suggestion_generation():
    """Demonstrate the SuggestionGenerator module."""
    print("\n" + "=" * 60)
    print("SUGGESTION GENERATION EXAMPLE")
    print("=" * 60)

    # Initialize modules
    identifier = IssueIdentifier()
    suggester = SuggestionGenerator()

    # First identify issues
    form = create_sample_form_with_issues()
    issue_results = identifier.forward(form)
    issues = issue_results.get("issues", [])

    print(f"Generating suggestions for {len(issues)} identified issues...")

    # Generate suggestions based on issues
    suggestion_results = suggester.forward(form, issues)

    print("\nSUGGESTIONS GENERATED:")
    suggestions = suggestion_results.get("suggestions", [])
    for suggestion in suggestions:
        print(
            f"- {suggestion.get('priority', 'Unknown')} Priority: {suggestion.get('title', 'No title')}"
        )
        print(f"  Type: {suggestion.get('type', 'Unknown')}")
        print(f"  Description: {suggestion.get('description', 'No description')}")
        print(f"  Element: {suggestion.get('formElementUuid', 'No UUID')}")
        print()


async def demonstrate_full_analysis():
    """Demonstrate the complete FormImprovementProgram."""
    print("\n" + "=" * 60)
    print("COMPLETE FORM ANALYSIS EXAMPLE")
    print("=" * 60)

    # Initialize the main program
    analyzer = FormImprovementProgram()

    # Test with both problematic and good forms
    forms = [create_sample_form_with_issues(), create_good_form()]

    for form in forms:
        print(f"\nAnalyzing: {form.get('name', 'Unnamed Form')}")
        print("-" * 40)

        # Perform complete analysis
        results = analyzer.forward(form)

        # Display results
        metadata = results.get("analysis_metadata", {})
        print(f"Analysis completed in {metadata.get('duration_seconds', 0):.2f}s")

        exec_summary = results.get("executive_summary", {})
        print(f"Total Issues: {exec_summary.get('total_issues', 0)}")
        print(f"Critical Issues: {exec_summary.get('critical_issues', 0)}")
        print(f"Total Suggestions: {exec_summary.get('total_suggestions', 0)}")
        print(f"Overall Score: {exec_summary.get('overall_score', 0)}/100")
        print(f"Top Priority: {exec_summary.get('top_priority', 'None')}")

        print(f"Assessment: {exec_summary.get('overview', 'No overview')}")


async def main():
    """Main example function."""
    try:
        # Configure DSPy
        lm = dspy.LM(
            model="openai/gpt-4o-mini",
            api_key="your_openai_key_here",  # Replace with actual key
            max_tokens=2000,
        )
        dspy.configure(lm=lm)

        print("DSPy Simplified Form Analysis Example")
        print("=====================================")

        # Run demonstrations
        await demonstrate_issue_identification()
        await demonstrate_suggestion_generation()
        await demonstrate_full_analysis()

        print("\n" + "=" * 60)
        print("EXAMPLE COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as e:
        logger.error(f"Example failed: {e}")
        print(f"\nExample failed: {e}")
        print("Make sure to:")
        print("1. Set your OpenAI API key")
        print("2. Install required dependencies")
        print("3. Train the models first: python train_models.py")


if __name__ == "__main__":
    asyncio.run(main())
