import logging
import os

logger = logging.getLogger(__name__)


def validate_environment_variables(*required_vars: str) -> bool:
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False

    return True


def validate_all_env_variables() -> bool:
    required_vars = [
        "AVNI_BASE_URL",
        "AVNI_MCP_SERVER_URL",
        "OPENAI_API_KEY",
        "DIFY_API_KEY",
        "DIFY_STAGING_TEST_API_KEY",
        "AVNI_AUTH_TOKEN",
        "DIFY_API_BASE_URL",
    ]
    return validate_environment_variables(*required_vars)
