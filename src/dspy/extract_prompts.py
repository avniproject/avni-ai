#!/usr/bin/env python3
"""
Extract optimized prompts from trained DSPy model.
"""

import sys
import os

sys.path.append(os.path.dirname(__file__))

from training import load_trained_model
import json


def extract_optimized_prompts(model_path: str):
    """Extract and display the optimized prompts from trained DSPy model."""

    print("Loading trained model...")
    model = load_trained_model(model_path)

    if not model:
        print("Failed to load model!")
        return

    print("\n" + "=" * 50)
    print("OPTIMIZED PROMPTS FROM DSPY TRAINING")
    print("=" * 50)

    # Extract Issue Identifier prompt
    try:
        # DSPy ChainOfThought stores signature in different ways
        issue_cot = model.issue_identifier.analyzer
        print("\n📋 ISSUE IDENTIFIER OPTIMIZED PROMPT:")
        print("-" * 40)
        print("ChainOfThought attributes:")
        print(f"Available attributes: {dir(issue_cot)}")

        # Access the predictors to get the optimized prompts
        predictors = issue_cot.predictors()
        print(f"Number of predictors: {len(predictors)}")

        for i, predictor in enumerate(predictors):
            print(f"\nPredictor {i}:")
            print(f"  Type: {type(predictor)}")
            print(
                f"  Attributes: {[attr for attr in dir(predictor) if not attr.startswith('_')]}"
            )

            if hasattr(predictor, "signature"):
                sig = predictor.signature
                print(f"  Instructions: {getattr(sig, 'instructions', 'Not found')}")
                if hasattr(sig, "input_fields"):
                    print(f"  Input fields: {list(sig.input_fields.keys())}")
                if hasattr(sig, "output_fields"):
                    print(f"  Output fields: {list(sig.output_fields.keys())}")

    except Exception as e:
        print(f"Could not extract issue identifier prompt: {e}")

    # Extract Suggestion Generator prompt
    try:
        suggestion_cot = model.suggestion_generator.suggester
        print("\n💡 SUGGESTION GENERATOR OPTIMIZED PROMPT:")
        print("-" * 40)
        print("ChainOfThought attributes:")
        print(f"Available attributes: {dir(suggestion_cot)}")

        # Access the predictors to get the optimized prompts
        predictors = suggestion_cot.predictors()
        print(f"Number of predictors: {len(predictors)}")

        for i, predictor in enumerate(predictors):
            print(f"\nPredictor {i}:")
            print(f"  Type: {type(predictor)}")
            print(
                f"  Attributes: {[attr for attr in dir(predictor) if not attr.startswith('_')]}"
            )

            if hasattr(predictor, "signature"):
                sig = predictor.signature
                print(f"  Instructions: {getattr(sig, 'instructions', 'Not found')}")
                if hasattr(sig, "input_fields"):
                    print(f"  Input fields: {list(sig.input_fields.keys())}")
                if hasattr(sig, "output_fields"):
                    print(f"  Output fields: {list(sig.output_fields.keys())}")

    except Exception as e:
        print(f"Could not extract suggestion generator prompt: {e}")

    print("\n" + "=" * 50)


def save_prompts_as_json(model_path: str, output_file: str):
    """Save optimized prompts as JSON for easy use."""

    model = load_trained_model(model_path)
    if not model:
        print("Failed to load model!")
        return

    prompts = {}

    try:
        issue_signature = model.issue_identifier.analyzer.signature
        prompts["issue_identifier"] = {
            "instructions": issue_signature.instructions,
            "input_fields": {
                name: field.desc for name, field in issue_signature.input_fields.items()
            },
            "output_fields": {
                name: field.desc
                for name, field in issue_signature.output_fields.items()
            },
        }
    except Exception as e:
        print(f"Could not extract issue identifier: {e}")

    try:
        suggestion_signature = model.suggestion_generator.suggester.signature
        prompts["suggestion_generator"] = {
            "instructions": suggestion_signature.instructions,
            "input_fields": {
                name: field.desc
                for name, field in suggestion_signature.input_fields.items()
            },
            "output_fields": {
                name: field.desc
                for name, field in suggestion_signature.output_fields.items()
            },
        }
    except Exception as e:
        print(f"Could not extract suggestion generator: {e}")

    with open(output_file, "w") as f:
        json.dump(prompts, f, indent=2)

    print(f"✅ Optimized prompts saved to {output_file}")


if __name__ == "__main__":
    # Calculate path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(
        script_dir, "..", "..", "trained_models", "avni_analyzer.pkl"
    )

    # Display prompts
    extract_optimized_prompts(model_path)

    # Save as JSON
    save_prompts_as_json(model_path, "optimized_prompts.json")
