# import asyncio
# import os
# import sys
# import pytest
# from pathlib import Path
# from dotenv import load_dotenv
#
# from .config_generation_manager import DifyConversationManager
# from .validators.test_config_create_validator import (
#     TestConfigCreateValidator,
# )
# from .validators.test_config_update_validator import (
#     TestConfigUpdateValidator,
# )
# from .validators.test_config_delete_validator import (
#     TestConfigDeleteValidator,
# )
# from ..common.utils import validate_all_env_variables
#
# load_dotenv()
#
#
# async def run_dify_config_test(test_type: str, dify_api_key: str, avni_auth_token: str):
#     """Run a single Dify configuration test and return results"""
#
#     conversation_manager = DifyConversationManager(dify_api_key)
#     base_path = Path(__file__).parent.parent.parent.parent / "dify"
#     config_file_path = str(base_path / f"test-config-{test_type}.json")
#
#     validators = {
#         "create": TestConfigCreateValidator,
#         "update": TestConfigUpdateValidator,
#         "delete": TestConfigDeleteValidator,
#     }
#     validator_class = validators.get(test_type)
#
#     if not validator_class:
#         raise ValueError(f"Unknown test type: {test_type}")
#
#     result = conversation_manager.conduct_config_conversation(
#         config_file_path=config_file_path,
#         auth_token=avni_auth_token,
#     )
#
#     if not result.success:
#         raise AssertionError(f"Dify conversation failed: {result.error_message}")
#
#     if not result.has_config:
#         raise AssertionError("No configuration extracted from Dify response")
#
#     if test_type == "create":
#         validation_result = validator_class.validate_test_create_config(
#             result.extracted_config
#         )
#     elif test_type == "update":
#         validation_result = validator_class.validate_test_update_config(
#             result.extracted_config
#         )
#     elif test_type == "delete":
#         validation_result = validator_class.validate_test_delete_config(
#             result.extracted_config
#         )
#
#     if not validation_result.is_valid:
#         error_msg = f"Configuration validation failed with {validation_result.error_count} errors:\n"
#         for i, error in enumerate(validation_result.errors[:10], 1):
#             error_msg += f"  {i}. {error}\n"
#         if validation_result.error_count > 10:
#             error_msg += f"  ... and {validation_result.error_count - 10} more errors"
#         raise AssertionError(error_msg)
#
#     return True
#
#
# @pytest.mark.asyncio
# async def test_dify_create_config():
#     if not validate_all_env_variables():
#         pytest.skip("Required environment variables not set")
#     await run_dify_config_test(
#         "create", os.getenv("DIFY_STAGING_TEST_API_KEY"), os.getenv("AVNI_AUTH_TOKEN")
#     )
#
#
# @pytest.mark.asyncio
# async def test_dify_update_config():
#     if not validate_all_env_variables():
#         pytest.skip("Required environment variables not set")
#     await run_dify_config_test(
#         "update", os.getenv("DIFY_STAGING_TEST_API_KEY"), os.getenv("AVNI_AUTH_TOKEN")
#     )
#
#
# @pytest.mark.asyncio
# async def test_dify_delete_config():
#     if not validate_all_env_variables():
#         pytest.skip("Required environment variables not set")
#     await run_dify_config_test(
#         "delete", os.getenv("DIFY_STAGING_TEST_API_KEY"), os.getenv("AVNI_AUTH_TOKEN")
#     )
#
#
# async def main():
#     if not validate_all_env_variables():
#         sys.exit(1)
#
#     dify_api_key = os.getenv("DIFY_STAGING_TEST_API_KEY")
#     avni_auth_token = os.getenv("AVNI_AUTH_TOKEN")
#
#     test_types = ["create", "update", "delete"]
#     print("Running Config Generation tests ")
#
#     for test_type in test_types:
#         print(f"\n Running {test_type.upper()} test...")
#         try:
#             await run_dify_config_test(test_type, dify_api_key, avni_auth_token)
#             print(f"{test_type.upper()} test passed!")
#         except Exception as e:
#             print(f"{test_type.upper()} test failed: {e}")
#             print(f"Stopping test execution due to failure in {test_type.upper()} test")
#             sys.exit(1)
#
#     print("\nAll tests passed successfully!")
#
#
# def _is_running_under_pytest():
#     """Check if we're running under pytest"""
#     import sys
#
#     return (
#         "pytest" in sys.modules or "pytest" in sys.argv[0]
#         if sys.argv
#         else False
#         or any("pytest" in arg for arg in sys.argv)
#         or "PYTEST_CURRENT_TEST" in os.environ
#     )
#
#
# if __name__ == "__main__":
#     # Only run main if we're not being executed by pytest
#     if not _is_running_under_pytest():
#         asyncio.run(main())
