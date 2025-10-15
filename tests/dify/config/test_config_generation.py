import asyncio
import os
import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add the parent directories to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from tests.dify.common.conversation_manager import DifyConversationManager
from tests.dify.config.validators.test_config_create_validator import (
    TestConfigCreateValidator,
)
from tests.dify.config.validators.test_config_update_validator import (
    TestConfigUpdateValidator,
)
from tests.dify.config.validators.test_config_delete_validator import (
    TestConfigDeleteValidator,
)


async def run_dify_config_test(
    test_type: str, dify_api_key: str, avni_auth_token: str, avni_base_url: str
):
    """Run a single Dify configuration test and return results"""

    conversation_manager = DifyConversationManager(dify_api_key)
    base_path = Path(__file__).parent.parent.parent.parent / "dify"
    config_file_path = str(base_path / f"test-config-{test_type}.json")

    # Get validator
    validators = {
        "create": TestConfigCreateValidator,
        "update": TestConfigUpdateValidator,
        "delete": TestConfigDeleteValidator,
    }
    validator_class = validators.get(test_type)

    if not validator_class:
        raise ValueError(f"Unknown test type: {test_type}")

    # Conduct conversation
    conversation_success, extracted_config, conversation_history = (
        conversation_manager.conduct_config_conversation(
            config_file_path=config_file_path,
            auth_token=avni_auth_token,
            avni_base_url=avni_base_url,
        )
    )

    if not conversation_success:
        raise AssertionError("Dify conversation failed")

    if not extracted_config:
        raise AssertionError("No configuration extracted from Dify response")

    # Validate configuration
    if test_type == "create":
        is_valid, validation_errors = validator_class.validate_test_create_config(
            extracted_config
        )
    elif test_type == "update":
        is_valid, validation_errors = validator_class.validate_test_update_config(
            extracted_config
        )
    elif test_type == "delete":
        is_valid, validation_errors = validator_class.validate_test_delete_config(
            extracted_config
        )

    if not is_valid:
        error_msg = (
            f"Configuration validation failed with {len(validation_errors)} errors:\n"
        )
        for i, error in enumerate(validation_errors[:10], 1):
            error_msg += f"  {i}. {error}\n"
        if len(validation_errors) > 10:
            error_msg += f"  ... and {len(validation_errors) - 10} more errors"
        raise AssertionError(error_msg)

    return True


# Test fixtures
@pytest.fixture
def dify_api_key():
    """Get Dify API key from environment"""
    api_key = os.getenv("DIFY_STAGING_TEST_API_KEY")
    if not api_key:
        pytest.skip("DIFY_STAGING_TEST_API_KEY environment variable not set")
    return api_key


@pytest.fixture
def avni_auth_token():
    """Get Avni auth token (dummy for testing)"""
    return os.getenv("AVNI_AUTH_TOKEN", "dummy-token")


@pytest.fixture
def avni_base_url():
    """Get Avni base URL"""
    return os.getenv("AVNI_BASE_URL", "https://app.avniproject.org")


# Test functions
@pytest.mark.asyncio
async def test_dify_create_config(dify_api_key, avni_auth_token, avni_base_url):
    """Test Dify CREATE configuration generation"""
    await run_dify_config_test("create", dify_api_key, avni_auth_token, avni_base_url)


@pytest.mark.asyncio
async def test_dify_update_config(dify_api_key, avni_auth_token, avni_base_url):
    """Test Dify UPDATE configuration generation"""
    await run_dify_config_test("update", dify_api_key, avni_auth_token, avni_base_url)


@pytest.mark.asyncio
async def test_dify_delete_config(dify_api_key, avni_auth_token, avni_base_url):
    """Test Dify DELETE configuration generation"""
    await run_dify_config_test("delete", dify_api_key, avni_auth_token, avni_base_url)


# CLI runner for individual tests
async def main():
    """Main function for CLI usage"""

    if len(sys.argv) != 2:
        print("Usage: python test_config_generation.py <create|update|delete>")
        sys.exit(1)

    test_type = sys.argv[1].lower()
    if test_type not in ["create", "update", "delete"]:
        print("Error: test_type must be 'create', 'update', or 'delete'")
        sys.exit(1)

    # Get environment variables
    dify_api_key = os.getenv("DIFY_STAGING_TEST_API_KEY")
    avni_auth_token = os.getenv("AVNI_AUTH_TOKEN", "dummy-token")
    avni_base_url = os.getenv("AVNI_BASE_URL", "https://staging.avniproject.org")

    if not dify_api_key:
        print("❌ Error: DIFY_STAGING_TEST_API_KEY environment variable not set")
        sys.exit(1)

    try:
        await run_dify_config_test(
            test_type, dify_api_key, avni_auth_token, avni_base_url
        )
        print(f"{test_type.upper()} test passed!")
    except Exception as e:
        print(f"❌ {test_type.upper()} test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
