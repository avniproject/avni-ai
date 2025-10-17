"""
MCH Integration Test - End-to-End Test for Maternal and Child Health Program

This test simulates a realistic conversation between an MCH program manager and the
Dify-Avni AI Assistant, triggers automatic configuration creation, and validates
the results against program requirements.

Flow:
1. AI Tester (MCH Program Manager) → Dify Assistant → Natural conversation
2. AI Tester says "I am happy with the configuration provided by the Avni assistant"
3. Wait for auto-creation to complete
4. Fetch actual configuration from Avni
5. Validate using enhanced AI Reviewer
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

load_dotenv()

from tests.dify.prompts.ai_tester import AITester
from tests.dify.common.dify_client import DifyClient
from src.clients.avni_client import AvniClient
from tests.dify.prompts.ai_reviewer import AIReviewer
from tests.dify.prompts.prompts import CONFIG_TESTER_PROMPTS, MCH_REQUIREMENTS
from .utils.conversation_utils import (
    generate_tester_message,
    create_dify_inputs,
    is_satisfaction_expressed,
    is_timeout_response,
    handle_satisfaction_response,
    handle_normal_conversation_timeout,
    record_normal_conversation,
)
from .utils.test_utils import (
    save_test_results,
    print_test_results,
    validate_environment_variables,
)

logger = logging.getLogger(__name__)


class MCHIntegrationTest:
    def __init__(self, dify_api_key: str, avni_auth_token: str):
        self.dify_client = DifyClient(dify_api_key)
        self.avni_client = AvniClient()
        self.auth_token = avni_auth_token
        self.ai_tester = AITester(CONFIG_TESTER_PROMPTS)
        self.ai_reviewer = AIReviewer()
        self.max_rounds = 15

    async def run_test(self) -> Dict[str, Any]:
        """Run the complete MCH integration test"""
        test_id = f"mch_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"🚀 Starting MCH integration test: {test_id}")

        try:
            # Step 1: Conduct realistic conversation
            conversation_result = await self._conduct_mch_conversation()

            if not conversation_result["success"]:
                return {
                    "test_id": test_id,
                    "success": False,
                    "error": "MCH conversation failed",
                    "conversation": conversation_result,
                }

            logger.info(
                f"✅ MCH conversation completed in {conversation_result['rounds']} rounds"
            )

            # Step 2: Check if timeout was detected and wait accordingly
            timeout_detected = any(
                msg.get("timeout_detected", False)
                for msg in conversation_result.get("history", [])
            )

            if timeout_detected:
                logger.info(
                    "⏳ Timeout detected - waiting 180 seconds for configuration creation..."
                )
                await asyncio.sleep(180)
            else:
                logger.info(
                    "⏳ Waiting 30 seconds for configuration creation to complete..."
                )
                await asyncio.sleep(30)

            # Step 3: Fetch actual configuration
            logger.info("📥 Fetching created configuration from Avni...")
            actual_config = await self.avni_client.fetch_complete_config(
                self.auth_token
            )

            if "error" in actual_config:
                return {
                    "test_id": test_id,
                    "success": False,
                    "error": "Failed to fetch configuration from Avni",
                    "details": actual_config,
                }

            logger.info("✅ Configuration fetched successfully")

            # Step 4: Validate configuration
            logger.info("🔍 Validating configuration against MCH requirements...")
            validation_result = AIReviewer.validate_created_configuration(
                actual_config=actual_config,
                program_requirements=MCH_REQUIREMENTS,
                scenario_name="Maternal and Child Health Program",
            )

            # Step 5: Compile results
            final_result = {
                "test_id": test_id,
                "success": validation_result.get("overall_success", False),
                "conversation": {
                    "rounds_completed": conversation_result["rounds"],
                    "satisfaction_achieved": conversation_result[
                        "satisfaction_achieved"
                    ],
                    "total_messages": len(conversation_result["history"]),
                },
                "validation": {
                    "scores": validation_result.get("scores", {}),
                    "configuration_assessment": validation_result.get(
                        "configuration_assessment", {}
                    ),
                    "overall_success": validation_result.get("overall_success", False),
                    "detailed_analysis": validation_result.get("detailed_analysis", ""),
                },
                "timestamp": datetime.now().isoformat(),
            }

            if final_result["success"]:
                logger.info("🎉 MCH integration test PASSED!")
            else:
                logger.error("❌ MCH integration test FAILED")

            return final_result

        except Exception as e:
            logger.error(f"💥 MCH integration test ERROR: {str(e)}")
            return {
                "test_id": test_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def _conduct_mch_conversation(self) -> Dict[str, Any]:
        """Conduct realistic MCH conversation using AI Tester"""
        conversation_id = ""
        conversation_history = []
        round_count = 0
        satisfaction_achieved = False

        logger.info("💬 Starting MCH conversation with AI Tester...")

        try:
            while round_count < self.max_rounds:
                round_count += 1

                # Generate tester message
                user_message = generate_tester_message(
                    self.ai_tester, conversation_history, round_count
                )

                if not user_message or "Error:" in user_message:
                    logger.error(
                        f"Failed to generate tester message in round {round_count}"
                    )
                    break

                logger.info(
                    f"Round {round_count}: Tester message ({len(user_message)} chars)"
                )

                # Prepare inputs for Dify
                inputs = create_dify_inputs(self.auth_token)

                # Check if AI Tester expressed satisfaction
                if is_satisfaction_expressed(user_message):
                    logger.info(
                        "✅ AI Tester expressed satisfaction with configuration"
                    )
                    satisfaction_achieved = True

                    # Send the satisfaction message and handle potential timeout
                    dify_response = self.dify_client.send_message(
                        query=user_message,
                        conversation_id=conversation_id,
                        inputs=inputs,
                        timeout=180,
                    )

                    handle_satisfaction_response(
                        dify_response, conversation_history, user_message, round_count
                    )
                    break

                # Normal flow - no satisfaction yet
                dify_response = self.dify_client.send_message(
                    query=user_message,
                    conversation_id=conversation_id,
                    inputs=inputs,
                    timeout=180,
                )

                # Check for timeout in normal conversation
                if is_timeout_response(dify_response):
                    timeout_handled = handle_normal_conversation_timeout(
                        conversation_history, user_message, round_count
                    )
                    if timeout_handled:
                        satisfaction_achieved = True
                        break

                elif not dify_response["success"]:
                    return {
                        "success": False,
                        "error": f"Dify API error in round {round_count}: {dify_response.get('error', 'Unknown')}",
                        "history": conversation_history,
                    }

                # Process successful response
                conversation_id = dify_response["conversation_id"]
                assistant_response = dify_response["answer"]

                logger.info(
                    f"Round {round_count}: Assistant response ({len(assistant_response)} chars)"
                )

                # Record normal conversation
                record_normal_conversation(
                    conversation_history, user_message, assistant_response, round_count
                )

                # Safety check for conversation length
                if round_count >= self.max_rounds:
                    logger.warning(
                        "⚠️ Conversation reached maximum rounds without satisfaction"
                    )
                    break

            return {
                "success": True,
                "rounds": round_count,
                "satisfaction_achieved": satisfaction_achieved,
                "history": conversation_history,
                "conversation_id": conversation_id,
            }

        except Exception as e:
            logger.error(f"Error in MCH conversation: {str(e)}")
            return {"success": False, "error": str(e), "history": conversation_history}


async def main():
    """Main function for running MCH integration test"""

    # Setup logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Validate environment variables
    if not validate_environment_variables(
        "DIFY_API_KEY", "AVNI_AUTH_TOKEN", "AVNI_BASE_URL"
    ):
        sys.exit(1)

    # Get environment variables
    dify_api_key = os.getenv("DIFY_API_KEY")
    avni_auth_token = os.getenv("AVNI_AUTH_TOKEN")

    print("🏥 MCH Integration Test Starting...")
    print("=" * 50)

    # Run the test
    test = MCHIntegrationTest(dify_api_key, avni_auth_token)
    result = await test.run_test()

    # Display results
    print_test_results(result, "MCH")

    # Save detailed results to tests/logs directory
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    output_file = save_test_results(result, "mch_integration", logs_dir)

    print(f"\n📄 Detailed results saved to: {output_file}")

    if result["success"]:
        print("\n🎉 MCH Integration Test completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️ MCH Integration Test failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
