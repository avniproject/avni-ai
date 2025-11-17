#!/usr/bin/env python3
"""
DSPy Evaluation and Comparison Framework for Avni Form Analysis.

Tracks baseline performance, compares optimized models, and maintains optimization history.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Tuple
import logging
import dspy
from training import (
    create_issue_identification_examples,
    create_suggestion_generation_examples,
    create_avni_metric,
    SimplifiedAvniAnalyzer,
    IssueIdentifier,
    SuggestionGenerator,
)

logger = logging.getLogger(__name__)

HISTORY_FILE = "optimization_history.json"
BASELINE_FILE = "baseline_scores.json"


def create_evaluation_dataset() -> List[dspy.Example]:
    """
    Create a fixed evaluation dataset for SimplifiedAvniAnalyzer.
    Only use issue identification examples since the main analyzer only takes form_element.
    """
    issue_examples = create_issue_identification_examples()

    logger.info(
        f"Created evaluation dataset with {len(issue_examples)} issue identification examples"
    )

    return issue_examples


def evaluate_model(
    model, eval_dataset: List[dspy.Example], description: str = ""
) -> float:
    """
    Evaluate a model against the evaluation dataset.

    Args:
        model: The model to evaluate (SimplifiedAvniAnalyzer or individual modules)
        eval_dataset: List of examples to evaluate on
        description: Description for logging

    Returns:
        Average score across all examples
    """
    logger.info(f"Evaluating {description}...")

    evaluator = dspy.evaluate.Evaluate(
        devset=eval_dataset,
        metric=create_avni_metric(),
        num_threads=1,
        display_progress=True,
        display_table=False,
    )

    result = evaluator(model)

    # DSPy evaluator returns total score (e.g., 3.8 out of 5)
    # We need to convert to percentage by dividing by dataset size
    dataset_size = len(eval_dataset)
    score = float(result) / dataset_size  # Convert to 0-1 range
    logger.info(f"{description} score: {score:.2%}")

    return score


def evaluate_baseline_performance(eval_dataset: List[dspy.Example]) -> Dict[str, float]:
    """
    Evaluate baseline performance using original (non-optimized) prompts.
    """
    logger.info("=== Evaluating Baseline Performance ===")

    # Create models with original prompts
    baseline_analyzer = SimplifiedAvniAnalyzer()
    baseline_issue_identifier = IssueIdentifier()
    baseline_suggestion_generator = SuggestionGenerator()

    # Evaluate individual modules on their respective examples
    issue_examples = create_issue_identification_examples()
    suggestion_examples = create_suggestion_generation_examples()

    issue_score = evaluate_model(
        baseline_issue_identifier, issue_examples, "Baseline Issue Identifier"
    )

    suggestion_score = evaluate_model(
        baseline_suggestion_generator,
        suggestion_examples,
        "Baseline Suggestion Generator",
    )

    # Overall combined score
    overall_score = evaluate_model(
        baseline_analyzer, eval_dataset, "Baseline Combined Analyzer"
    )

    baseline_scores = {
        "timestamp": datetime.now().isoformat(),
        "issue_identifier": issue_score,
        "suggestion_generator": suggestion_score,
        "overall": overall_score,
    }

    # Save baseline scores
    save_baseline_scores(baseline_scores)

    return baseline_scores


def compare_models(
    original_model,
    optimized_model,
    eval_dataset: List[dspy.Example],
    config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Compare original vs optimized model performance.
    """
    logger.info("=== Comparing Original vs Optimized Models ===")

    # Evaluate both models
    original_score = evaluate_model(original_model, eval_dataset, "Original Model")
    optimized_score = evaluate_model(optimized_model, eval_dataset, "Optimized Model")

    # Calculate improvement
    improvement = optimized_score - original_score
    improvement_percent = improvement * 100

    # Create comparison results
    comparison = {
        "timestamp": datetime.now().isoformat(),
        "config": config,
        "original_score": original_score,
        "optimized_score": optimized_score,
        "improvement": improvement,
        "improvement_percent": improvement_percent,
        "dataset_size": len(eval_dataset),
    }

    # Display results
    print("\n" + "=" * 50)
    print("MODEL COMPARISON RESULTS")
    print("=" * 50)
    print(f"Original Model Score:  {original_score:.2%}")
    print(f"Optimized Model Score: {optimized_score:.2%}")
    print(
        f"Improvement:           {improvement:+.4f} ({improvement_percent:+.1f} percentage points)"
    )

    if improvement > 0:
        print("✅ Optimization IMPROVED performance!")
    elif improvement == 0:
        print("➖ No change in performance")
    else:
        print("❌ Optimization HURT performance")

    print("=" * 50)

    return comparison


def save_baseline_scores(scores: Dict[str, Any]):
    """Save baseline scores for future reference."""
    with open(BASELINE_FILE, "w") as f:
        json.dump(scores, f, indent=2)
    logger.info(f"Baseline scores saved to {BASELINE_FILE}")


def load_baseline_scores() -> Dict[str, Any]:
    """Load previously saved baseline scores."""
    try:
        with open(BASELINE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"No baseline scores found at {BASELINE_FILE}")
        return {}


def save_optimization_results(comparison: Dict[str, Any], model_path: str):
    """Save optimization results to history for tracking over time."""

    result = {
        **comparison,
        "model_path": model_path,
        "evaluation_framework_version": "1.0",
    }

    # Append to history file
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps(result) + "\n")

    logger.info(f"Optimization results saved to {HISTORY_FILE}")


def load_optimization_history() -> List[Dict[str, Any]]:
    """Load optimization history from file."""
    history = []

    try:
        with open(HISTORY_FILE, "r") as f:
            for line in f:
                if line.strip():
                    history.append(json.loads(line))
    except FileNotFoundError:
        logger.info(f"No optimization history found at {HISTORY_FILE}")

    return history


def display_optimization_history():
    """Display optimization history in a readable format."""
    history = load_optimization_history()

    if not history:
        print("No optimization history found.")
        return

    print("\n" + "=" * 60)
    print("OPTIMIZATION HISTORY")
    print("=" * 60)

    for i, result in enumerate(history, 1):
        timestamp = result.get("timestamp", "Unknown")
        original = result.get("original_score", 0)
        optimized = result.get("optimized_score", 0)
        improvement = result.get("improvement_percent", 0)
        config = result.get("config", {})

        print(f"\nRun {i} - {timestamp[:19]}")
        print(
            f"  Config: {config.get('model', 'Unknown')} | Steps: {config.get('training_steps', 'Unknown')}"
        )
        print(f"  Original:  {original:.2%}")
        print(f"  Optimized: {optimized:.2%}")
        print(f"  Change:    {improvement:+.1f}pp")

    print("=" * 60)


def run_comprehensive_evaluation(model_path: str, config: Dict[str, Any]):
    """
    Run comprehensive evaluation comparing baseline vs optimized model.
    """
    logger.info("Starting comprehensive evaluation...")

    # Create evaluation dataset
    eval_dataset = create_evaluation_dataset()

    # Load models
    from training import load_trained_model

    baseline_model = SimplifiedAvniAnalyzer()  # Original prompts
    optimized_model = load_trained_model(model_path)

    if not optimized_model:
        logger.error("Failed to load optimized model!")
        return

    # Compare models
    comparison = compare_models(baseline_model, optimized_model, eval_dataset, config)

    # Save results
    save_optimization_results(comparison, model_path)

    return comparison


if __name__ == "__main__":
    # Example usage
    eval_dataset = create_evaluation_dataset()

    # Evaluate baseline if no baseline exists
    if not os.path.exists(BASELINE_FILE):
        baseline_scores = evaluate_baseline_performance(eval_dataset)

    # Display optimization history
    display_optimization_history()
