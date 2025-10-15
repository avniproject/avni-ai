"""
Utilities package for Avni MCP Server.

This package contains various utility modules organized by functionality:
- http_utils: HTTP response utilities
- api_utils: API result handling utilities
- request_utils: Request processing utilities
- format_utils: Data formatting utilities
- function_call_utils: OpenAI function call processing utilities
- logging_utils: Session logging utilities
- config_utils: Configuration processing utilities
- response_utils: Response handling utilities
"""

# Import commonly used utilities for convenience
from .http_utils import (
    create_error_response,
    create_success_response,
    create_cors_middleware,
)
from .api_utils import ApiResult
from .request_utils import extract_base_url
from .format_utils import format_list_response, format_creation_response
from .function_call_utils import (
    parse_function_arguments,
    add_function_output,
    format_tools_for_continuation,
    extract_function_calls,
    execute_function_call,
)
from .logging_utils import setup_file_logging, create_session_id
from .config_utils import (
    build_system_instructions,
    build_initial_input,
    parse_llm_response,
    extract_text_content,
)
from .response_utils import (
    create_success_result,
    create_error_result,
    create_max_iterations_result,
)
from .request_validation import validate_config_request

__all__ = [
    "create_error_response",
    "create_success_response",
    "create_cors_middleware",
    "ApiResult",
    "extract_base_url",
    "format_list_response",
    "format_creation_response",
    "parse_function_arguments",
    "add_function_output",
    "format_tools_for_continuation",
    "extract_function_calls",
    "execute_function_call",
    "setup_file_logging",
    "create_session_id",
    "build_system_instructions",
    "build_initial_input",
    "parse_llm_response",
    "extract_text_content",
    "create_success_result",
    "create_error_result",
    "create_max_iterations_result",
    "validate_config_request",
]
