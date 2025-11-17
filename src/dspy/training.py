#!/usr/bin/env python3
"""
Simplified DSPy MIPROv2 training for Avni form analysis.

This module trains two simplified modules:
1. IssueIdentifier - identifies problems in forms
2. SuggestionGenerator - generates improvement recommendations

Can be run directly: python simplified_training.py [options]
"""

import dspy
from typing import List, Dict, Any
import logging
import json
import pickle
import os
import asyncio
import argparse
import sys
from pathlib import Path
from issue_identifier import IssueIdentifier
from suggestion_generator import SuggestionGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_issue_identification_examples() -> List[dspy.Example]:
    """Create training examples for issue identification on single form elements."""

    examples = [
        dspy.Example(
            form_element='{"name": "Name", "uuid": "name-123", "concept": {"dataType": "Text"}}',
            issues='[{"message": "Manual name field in registration form. Remove - system auto-handles names", "formElementUuid": "name-123"}]',
        ).with_inputs("form_element"),
        dspy.Example(
            form_element='{"name": "Age", "uuid": "age-123", "concept": {"dataType": "Text"}}',
            issues='[{"message": "Age field using Text dataType should use Numeric. Change dataType from Text to Numeric with bounds 0-120", "formElementUuid": "age-123"}]',
        ).with_inputs("form_element"),
        dspy.Example(
            form_element='{"name": "Phone Number", "uuid": "phone-123", "concept": {"dataType": "Text"}}',
            issues='[{"message": "Phone field missing validation pattern. Change dataType to PhoneNumber or add regex validation", "formElementUuid": "phone-123"}]',
        ).with_inputs("form_element"),
        dspy.Example(
            form_element='{"name": "Do you have insurance?", "uuid": "insurance-123", "concept": {"dataType": "Coded", "answers": ["yes", "no"]}, "type": "MultiSelect"}',
            issues='[{"message": "Yes/No question using MultiSelect should use SingleSelect. Change type from MultiSelect to SingleSelect", "formElementUuid": "insurance-123"}]',
        ).with_inputs("form_element"),
        dspy.Example(
            form_element='{"name": "Weight", "uuid": "weight-123", "concept": {"dataType": "Numeric", "lowAbsolute": 1, "highAbsolute": 200, "unit": "kg"}}',
            issues="[]",
        ).with_inputs("form_element"),
    ]

    return examples


def create_suggestion_generation_examples() -> List[dspy.Example]:
    """Create training examples for suggestion generation on single form elements."""

    examples = [
        dspy.Example(
            form_element='{"name": "Name", "uuid": "name-123", "concept": {"dataType": "Text"}}',
            identified_issues='[{"message": "Manual name field in registration form. Remove - system auto-handles names", "formElementUuid": "name-123"}]',
            suggestions='[{"message": "Remove Name field from registration form. System auto-handles name fields in registration forms", "formElementUuid": "name-123"}]',
        ).with_inputs("form_element", "identified_issues"),
        dspy.Example(
            form_element='{"name": "Age", "uuid": "age-123", "concept": {"dataType": "Text"}}',
            identified_issues='[{"message": "Age field using Text dataType should use Numeric. Change dataType from Text to Numeric with bounds 0-120", "formElementUuid": "age-123"}]',
            suggestions='[{"message": "Change Age field from Text to Numeric. Age should be numeric for proper validation and analysis", "formElementUuid": "age-123"}]',
        ).with_inputs("form_element", "identified_issues"),
        dspy.Example(
            form_element='{"name": "Phone Number", "uuid": "phone-123", "concept": {"dataType": "Text"}}',
            identified_issues='[{"message": "Phone field missing validation pattern. Change dataType to PhoneNumber or add regex validation", "formElementUuid": "phone-123"}]',
            suggestions='[{"message": "Change phone field to use PhoneNumber dataType. PhoneNumber dataType provides built-in validation", "formElementUuid": "phone-123"}]',
        ).with_inputs("form_element", "identified_issues"),
        dspy.Example(
            form_element='{"name": "Do you have insurance?", "uuid": "insurance-123", "concept": {"dataType": "Coded", "answers": ["yes", "no"]}, "type": "MultiSelect"}',
            identified_issues='[{"message": "Yes/No question using MultiSelect should use SingleSelect. Change type from MultiSelect to SingleSelect", "formElementUuid": "insurance-123", "formElementName": "Do you have insurance?"}]',
            suggestions='[{"message": "Change from MultiSelect to SingleSelect for Yes/No question. Binary questions should use SingleSelect", "formElementUuid": "insurance-123"}]',
        ).with_inputs("form_element", "identified_issues"),
        dspy.Example(
            form_element='{"name": "Weight", "uuid": "weight-123", "concept": {"dataType": "Numeric", "lowAbsolute": 1, "highAbsolute": 200, "unit": "kg"}}',
            identified_issues="[]",
            suggestions='[{"message": "Add unit validation to ensure consistency. Unit validation prevents data entry errors", "formElementUuid": "weight-123"}]',
        ).with_inputs("form_element", "identified_issues"),
    ]

    return examples


class SimplifiedAvniAnalyzer(dspy.Module):
    """Simplified analyzer that coordinates IssueIdentifier and SuggestionGenerator for single form elements."""

    def __init__(self):
        super().__init__()
        self.issue_identifier = IssueIdentifier()
        self.suggestion_generator = SuggestionGenerator()

    def forward(self, form_element: str):
        """Analyze single form element by first identifying issues, then generating suggestions."""

        # Step 1: Identify issues
        issue_result = self.issue_identifier(form_element)

        # Step 2: Generate suggestions based on issues
        suggestion_result = self.suggestion_generator(form_element, issue_result.issues)

        # Create combined result object
        class CombinedResult:
            def __init__(self, issue_result, suggestion_result):
                self.issues = issue_result.issues
                self.suggestions = suggestion_result.suggestions

        return CombinedResult(issue_result, suggestion_result)


# Define the evaluation signature at module level
class AvniEvaluationRubric(dspy.Signature):
    """
    You are an expert evaluator for Avni form analysis. Evaluate the AI's response against the expected output.

    Compare the predicted output with the expected output and score based on:
    1. Accuracy: Are the same issues/suggestions identified?
    2. Completeness: Is all important information covered?
    3. Quality: Are messages clear and actionable?

    Return a score as a decimal number between 0.0 and 1.0 where:
    - 1.0 = Perfect match or equivalent quality
    - 0.8 = Good with minor differences
    - 0.6 = Partially correct
    - 0.4 = Poor but some relevance
    - 0.0 = Completely wrong or irrelevant
    """

    form_element = dspy.InputField(desc="The form element JSON being analyzed")
    expected_output = dspy.InputField(desc="Expected analysis result")
    predicted_output = dspy.InputField(desc="AI-generated analysis result")

    score = dspy.OutputField(desc="Accuracy score as decimal from 0.0 to 1.0")


# Create the judge module at module level
class AvniJudge(dspy.Module):
    def __init__(self):
        super().__init__()
        self.evaluator = dspy.ChainOfThought(AvniEvaluationRubric)

    def forward(self, form_element, expected_output, predicted_output):
        return self.evaluator(
            form_element=form_element,
            expected_output=expected_output,
            predicted_output=predicted_output,
        )


def create_avni_metric() -> callable:
    """Create LLM-as-a-judge metric following DSPy patterns."""

    judge = AvniJudge()

    def avni_correctness_metric(example, pred, trace=None):
        try:
            # Get expected and predicted outputs based on example type
            if hasattr(example, "issues"):
                if not hasattr(pred, "issues"):
                    return 0.0
                expected = example.issues
                predicted = pred.issues
            elif hasattr(example, "suggestions"):
                if not hasattr(pred, "suggestions"):
                    return 0.0
                expected = example.suggestions
                predicted = pred.suggestions
            else:
                return 0.0

            # Evaluate using the judge
            evaluation = judge(
                form_element=example.form_element,
                expected_output=str(expected),
                predicted_output=str(predicted),
            )

            # DSPy should handle parsing automatically
            return float(evaluation.score)

        except Exception as e:
            logger.warning(f"Judge evaluation error: {e}")
            return 0.0

    return avni_correctness_metric


async def train_simplified_analyzer(
    config: Dict[str, Any],
) -> SimplifiedAvniAnalyzer:
    """Train the simplified analyzer using MIPROv2."""

    logger.info("Starting simplified Avni analyzer training...")

    # Create training examples - only use issue identification examples
    # since SimplifiedAvniAnalyzer.forward() only takes form_element
    issue_examples = create_issue_identification_examples()

    logger.info(f"Created {len(issue_examples)} issue identification training examples")
    logger.info("=== Training Examples Overview ===")
    for i, example in enumerate(issue_examples[:3], 1):
        logger.info(f"Example {i}:")
        logger.info(f"  Has form_element: {hasattr(example, 'form_element')}")
        logger.info(f"  Has issues: {hasattr(example, 'issues')}")

    # Initialize the modules
    issue_identifier = IssueIdentifier()
    suggestion_generator = SuggestionGenerator()

    # Train issue identifier first
    logger.info("=== Training Issue Identifier ===")
    issue_optimizer = dspy.MIPROv2(
        metric=create_avni_metric(),
        auto="light",
        num_threads=config.get("num_threads", 1),
        max_bootstrapped_demos=config["max_bootstrapped_demos"],
        max_labeled_demos=config["max_labeled_demos"],
        verbose=True,
    )

    optimized_issue_identifier = issue_optimizer.compile(
        issue_identifier, trainset=issue_examples, valset=issue_examples[:2]
    )

    # Train suggestion generator with suggestion examples
    suggestion_examples = create_suggestion_generation_examples()
    logger.info(
        f"=== Training Suggestion Generator with {len(suggestion_examples)} examples ==="
    )

    suggestion_optimizer = dspy.MIPROv2(
        metric=create_avni_metric(),
        auto="light",
        num_threads=config.get("num_threads", 1),
        max_bootstrapped_demos=config["max_bootstrapped_demos"],
        max_labeled_demos=config["max_labeled_demos"],
        verbose=True,
    )

    optimized_suggestion_generator = suggestion_optimizer.compile(
        suggestion_generator,
        trainset=suggestion_examples,
        valset=suggestion_examples[:2],
    )

    # Create final analyzer with trained components
    final_analyzer = SimplifiedAvniAnalyzer()
    final_analyzer.issue_identifier = optimized_issue_identifier
    final_analyzer.suggestion_generator = optimized_suggestion_generator

    logger.info("=== MIPROv2 Optimization Completed ===")

    return final_analyzer


def save_trained_model(model, filepath: str):
    """Save trained model using DSPy's save method."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Use DSPy's built-in save method instead of pickle
        model.save(filepath)
        logger.info(f"✅ Model saved to {filepath}")
    except Exception as e:
        logger.error(f"Failed to save model with DSPy save: {e}")
        # Fallback: try to save just the essential parts
        try:
            import json

            # Save the prompts and configurations in a readable format
            model_data = {
                "model_type": "SimplifiedAvniAnalyzer",
                "issue_identifier_prompt": str(
                    model.issue_identifier.analyzer.signature
                ),
                "suggestion_generator_prompt": str(
                    model.suggestion_generator.suggester.signature
                ),
            }
            json_filepath = filepath.replace(".pkl", ".json")
            with open(json_filepath, "w") as f:
                json.dump(model_data, f, indent=2)
            logger.info(f"✅ Model prompts saved to {json_filepath}")
        except Exception as fallback_error:
            logger.error(f"Fallback save also failed: {fallback_error}")


def load_trained_model(filepath: str):
    """Load trained model using DSPy's load method."""
    try:
        # Try DSPy's built-in load method first
        analyzer = SimplifiedAvniAnalyzer()
        analyzer.load(filepath)
        logger.info(f"✅ Model loaded from {filepath}")
        return analyzer
    except Exception as e:
        logger.error(f"Failed to load model with DSPy load: {e}")
        # Fallback: check if JSON file exists
        try:
            json_filepath = filepath.replace(".pkl", ".json")
            if os.path.exists(json_filepath):
                logger.info(f"Found JSON backup at {json_filepath}")
                return None  # JSON file exists but we can't recreate the full model
            return None
        except Exception:
            return None


def check_trained_model_exists(filepath: str) -> bool:
    """Check if trained model file exists."""
    return os.path.exists(filepath)


async def main():
    """Main training function with CLI interface."""

    parser = argparse.ArgumentParser(description="Train Avni DSPy models")
    parser.add_argument("--steps", type=int, default=5, help="Number of training steps")
    parser.add_argument("--model", type=str, default="gpt-4-turbo", help="OpenAI model")
    parser.add_argument("--force", action="store_true", help="Force retrain")
    parser.add_argument("--test-imports", action="store_true", help="Test imports only")
    args = parser.parse_args()

    # Load environment directly
    try:
        from dotenv import load_dotenv

        load_dotenv()
        logger.info("✅ Environment loaded using dotenv")

        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment or .env file")

        logger.info(f"✅ OpenAI API key found: {OPENAI_API_KEY[:10]}...")

    except Exception as e:
        logger.error("❌ Failed to load environment!")
        logger.error(f"Error: {e}")
        logger.error("Solutions:")
        logger.error("1. Add OPENAI_API_KEY=your_key to .env file")
        logger.error("2. Or export OPENAI_API_KEY=your_key_here")
        logger.info(
            "For testing imports only, you can run: python simplified_training.py --test-imports"
        )
        if "--test-imports" not in sys.argv:
            return

    try:
        logger.info("✅ DSPy available")

        # Configure DSPy (skip if testing imports only)
        if not args.test_imports:
            lm = dspy.LM(
                model=f"openai/{args.model}",
                api_key=OPENAI_API_KEY,
                max_tokens=4000,
                temperature=0.7,
            )
            dspy.configure(lm=lm)
            logger.info(f"✅ DSPy configured with {args.model}")

        logger.info("✅ Training modules imported successfully")

        if args.test_imports:
            logger.info(
                "✅ All imports successful! You can now train with a real API key."
            )
            return

        logger.info("🚀 Starting training...")

        # Training config
        config = {
            "model": args.model,
            "num_threads": 1,
            "max_bootstrapped_demos": 5,
            "max_labeled_demos": 8,
            "training_steps": args.steps,
        }

        # Create output directory (relative to project root)
        output_dir = Path(__file__).parent.parent.parent / "trained_models"
        output_dir.mkdir(exist_ok=True)
        model_path = output_dir / "avni_analyzer.pkl"

        # Check if model exists
        if model_path.exists() and not args.force:
            logger.info(f"✅ Model already exists at {model_path}")
            logger.info("Use --force to retrain")
            return

        # Train the simplified model
        logger.info(f"Training with config: {config}")
        trained_analyzer = await train_simplified_analyzer(config)

        # Save the model
        save_trained_model(trained_analyzer, str(model_path))

        logger.info("✅ Training completed!")
        logger.info(f"📁 Model saved to: {model_path}")

        # Run comprehensive evaluation and comparison
        try:
            from evaluation_framework import run_comprehensive_evaluation

            logger.info("🔍 Running comprehensive evaluation...")
            run_comprehensive_evaluation(str(model_path), config)
        except Exception as e:
            logger.warning(f"Evaluation failed: {e}")

        logger.info("🚀 You can now start the server!")

    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        logger.error("Make sure you're running this from the avni-ai directory")
        logger.error("Try: uv run python simplified_training.py")
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        import traceback

        logger.error(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
