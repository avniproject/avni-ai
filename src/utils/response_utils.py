"""Response handling utilities for config processing."""

from typing import Dict, Any


def create_success_result(llm_result: Dict[str, Any], iterations: int) -> Dict[str, Any]:
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
        "function_calls_made": 0  # Not tracking individual function calls anymore
    }


def create_error_result(error_message: str, additional_errors: list = None) -> Dict[str, Any]:
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
        "results": {"created": [], "existing": [], "errors": errors},
        "message": error_message
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
        "results": {"created": [], "existing": [], "errors": ["Maximum iterations reached"]},
        "iterations": max_iterations,
        "message": "Processing incomplete - reached maximum iterations"
    }