"""Logging utilities for Avni MCP Server."""

import logging
import os


def setup_file_logging(task_id: str) -> logging.Logger:
    """Set up file logging for conversation history.

    Args:
        task_id: Unique task identifier

    Returns:
        Configured logger for the task
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Create a task-specific logger
    task_logger = logging.getLogger(f"config_session_{task_id}")
    task_logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates
    for handler in task_logger.handlers[:]:
        task_logger.removeHandler(handler)

    # Create file handler
    log_file = os.path.join(logs_dir, f"config_session_{task_id}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add handler to logger
    task_logger.addHandler(file_handler)

    return task_logger
