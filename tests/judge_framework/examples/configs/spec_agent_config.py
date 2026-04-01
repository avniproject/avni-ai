"""
Example configuration for Spec Agent testing.

This module provides configuration templates and helper functions for
setting up Spec Agent tests with the judge framework.
"""

import os
from tests.judge_framework.interfaces.result_models import (
    TestConfiguration,
    DifyConfig,
    EvaluationConfig,
    TestGenerationConfig,
)


def get_spec_agent_config() -> TestConfiguration:
    """
    Get default Spec Agent test configuration.

    Loads settings from environment variables with sensible defaults.

    Required environment variables:
    - DIFY_API_KEY: Dify API key for workflow execution
    - AVNI_MCP_SERVER_URL: URL of avni-ai MCP server (e.g., http://localhost:8023)
    - AVNI_AUTH_TOKEN: Avni authentication token (optional for some tests)

    Returns:
        TestConfiguration instance
    """
    return TestConfiguration(
        dify_config=DifyConfig(
            api_key=os.getenv("DIFY_API_KEY", ""),
            base_url=os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1"),
            workflow_name="App Configurator [Staging] v2",
        ),
        evaluation_config=EvaluationConfig(
            evaluation_metrics=[
                "tool_call_correctness",
                "spec_validity",
                "entity_coverage",
                "conversation_flow",
            ],
            success_thresholds={
                "tool_call_correctness": 80.0,  # Agent must call generate_spec
                "spec_validity": 90.0,  # Generated YAML must be valid
                "entity_coverage": 70.0,  # Most entities should be in spec
                "conversation_flow": 60.0,  # Should follow expected workflow
            },
        ),
        generation_config=TestGenerationConfig(
            static_test_cases=[],  # Load from JSON file
            ai_generation_enabled=False,  # Use static scenarios only
        ),
        openai_model="gpt-4",  # For any AI-based evaluation (future)
        avni_auth_token=os.getenv("AVNI_AUTH_TOKEN", ""),
        avni_mcp_server_url=os.getenv("AVNI_MCP_SERVER_URL", ""),
    )


def get_strict_config() -> TestConfiguration:
    """
    Get strict configuration with higher thresholds.

    Use this for production-ready testing where all criteria must pass.

    Returns:
        TestConfiguration with strict thresholds
    """
    config = get_spec_agent_config()
    config.evaluation_config.success_thresholds = {
        "tool_call_correctness": 100.0,  # Must call correct tools
        "spec_validity": 100.0,  # YAML must be perfect
        "entity_coverage": 90.0,  # Nearly all entities must be covered
        "conversation_flow": 80.0,  # Must follow workflow precisely
    }
    return config


def get_lenient_config() -> TestConfiguration:
    """
    Get lenient configuration for development/debugging.

    Use this when testing new features or debugging issues.

    Returns:
        TestConfiguration with lenient thresholds
    """
    config = get_spec_agent_config()
    config.evaluation_config.success_thresholds = {
        "tool_call_correctness": 50.0,  # Some tool calls acceptable
        "spec_validity": 70.0,  # YAML should parse
        "entity_coverage": 50.0,  # Half of entities is okay
        "conversation_flow": 40.0,  # Basic flow is fine
    }
    return config


# Example usage patterns
EXAMPLE_SCENARIOS = {
    "happy_path": {
        "scenario": "happy_path_full_entities",
        "description": "Full entities loaded, agent generates spec, user approves",
        "entities_filter": "full",
        "conversation_vars": {
            "org_name": "Durga India",
            "user_name": "Test User",
            "setup_mode_active": True,
            "spec_yaml": "",
            "query": "I've uploaded the scoping documents. Please generate the spec.",
        },
        "expected_behavior": {
            "should_call_generate_spec": True,
            "should_call_validate_spec": True,
            "should_ask_confirmation": True,
            "should_output_spec_approved": True,
        },
    },
    "empty_entities": {
        "scenario": "empty_entities_should_ask_for_docs",
        "description": "No entities loaded, agent should ask for documents",
        "entities_filter": "empty",
        "conversation_vars": {
            "org_name": "Durga India",
            "user_name": "Test User",
            "setup_mode_active": False,
            "spec_yaml": "",
            "query": "I want to set up Avni using the scoping SRS docs.",
        },
        "expected_behavior": {
            "should_call_generate_spec": False,
            "should_ask_for_documents": True,
            "should_output_spec_approved": False,
        },
    },
}


def validate_environment() -> tuple[bool, list[str]]:
    """
    Validate that required environment variables are set.

    Returns:
        Tuple of (is_valid, list_of_missing_vars)
    """
    required_vars = ["DIFY_API_KEY", "AVNI_MCP_SERVER_URL"]
    optional_vars = ["AVNI_AUTH_TOKEN", "DIFY_API_BASE_URL"]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    warnings = []
    for var in optional_vars:
        if not os.getenv(var):
            warnings.append(f"{var} not set (optional)")

    is_valid = len(missing) == 0

    return is_valid, missing + warnings
