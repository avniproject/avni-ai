"""Logging utilities for Avni MCP Server."""

import logging
import os
from datetime import datetime


def setup_file_logging(session_id: str) -> logging.Logger:
    """Set up file logging for conversation history.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        Configured logger for the session
    """
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create a session-specific logger
    session_logger = logging.getLogger(f"config_session_{session_id}")
    session_logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    for handler in session_logger.handlers[:]:
        session_logger.removeHandler(handler)
    
    # Create file handler
    log_file = os.path.join(logs_dir, f"config_session_{session_id}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add handler to logger
    session_logger.addHandler(file_handler)
    
    return session_logger


def create_session_id() -> str:
    """Create a unique session ID based on current timestamp.
    
    Returns:
        Session ID string in format: YYYYMMDD_HHMMSS_mmm
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # milliseconds