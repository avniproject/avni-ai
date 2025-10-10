"""Response handling utilities for config processing."""

from typing import Dict, Any


def create_success_result(
    llm_result: Dict[str, Any], iterations: int
) -> Dict[str, Any]:
    """Create successful completion result.

    Args:
        llm_result: Result from LLM processing
        iterations: Number of iterations completed

    Returns:
        Success result dictionary
    """
    return {
        "done": True,
        "status": "completed",
        "results": llm_result.get("results", {}),
        "iterations": iterations,
        "function_calls_made": 0,  # Not tracking individual function calls anymore
    }


def create_error_result(
    error_message: str, additional_errors: list = None
) -> Dict[str, Any]:
    """Create error result dictionary.

    Args:
        error_message: Main error message
        additional_errors: List of additional errors (optional)

    Returns:
        Error result dictionary
    """
    errors = [error_message]
    if additional_errors:
        errors.extend(additional_errors)

    return {
        "done": False,
        "status": "error",
        "results": {
            "deleted_address_level_types": [],
            "deleted_locations": [],
            "deleted_catchments": [],
            "deleted_subject_types": [],
            "deleted_programs": [],
            "deleted_encounter_types": [],
            "updated_address_level_types": [],
            "updated_locations": [],
            "updated_catchments": [],
            "updated_subject_types": [],
            "updated_programs": [],
            "updated_encounter_types": [],
            "created_address_level_types": [],
            "created_locations": [],
            "created_catchments": [],
            "created_subject_types": [],
            "created_programs": [],
            "created_encounter_types": [],
            "existing_address_level_types": [],
            "existing_locations": [],
            "existing_catchments": [],
            "existing_subject_types": [],
            "existing_programs": [],
            "existing_encounter_types": [],
            "errors": errors,
        },
        "message": error_message,
    }


def create_max_iterations_result(max_iterations: int) -> Dict[str, Any]:
    """Create result for when max iterations are reached.

    Args:
        max_iterations: Maximum number of iterations allowed

    Returns:
        Max iterations result dictionary
    """
    return {
        "done": False,
        "status": "error",
        "results": {
            "deleted_address_level_types": [],
            "deleted_locations": [],
            "deleted_catchments": [],
            "deleted_subject_types": [],
            "deleted_programs": [],
            "deleted_encounter_types": [],
            "updated_address_level_types": [],
            "updated_locations": [],
            "updated_catchments": [],
            "updated_subject_types": [],
            "updated_programs": [],
            "updated_encounter_types": [],
            "created_address_level_types": [],
            "created_locations": [],
            "created_catchments": [],
            "created_subject_types": [],
            "created_programs": [],
            "created_encounter_types": [],
            "existing_address_level_types": [],
            "existing_locations": [],
            "existing_catchments": [],
            "existing_subject_types": [],
            "existing_programs": [],
            "existing_encounter_types": [],
            "errors": ["Maximum iterations reached"],
        },
        "iterations": max_iterations,
        "message": "Processing incomplete - reached maximum iterations",
    }
