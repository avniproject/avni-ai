import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

from dotenv import load_dotenv
from src.clients.avni_client import AvniClient
from ..common.dify_client import DifyClient
from ..prompts.ai_reviewer import AIReviewer
from ..prompts.ai_tester import AITester
from ..prompts.prompts import CONFIG_TESTER_PROMPTS, MCH_REQUIREMENTS
from ..common.utils import validate_all_env_variables

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class ConversationResult:
    rounds_completed: int
    satisfaction_achieved: bool
    total_messages: int


@dataclass
class ValidationResult:
    scores: Dict[str, Any]
    configuration_assessment: Dict[str, Any]
    overall_success: bool
    detailed_analysis: str


@dataclass
class MCHTestResult:
    success: bool
    conversation: ConversationResult = None
    validation: ValidationResult = None
    timestamp: str = None
    error: str = None
    details: Dict[str, Any] = None


class MCHIntegrationTest:
    def __init__(self, dify_api_key: str, avni_auth_token: str):
        self.dify_client = DifyClient(dify_api_key)
        self.avni_client = AvniClient()
        self.auth_token = avni_auth_token
        self.ai_tester = AITester(CONFIG_TESTER_PROMPTS)
        self.ai_reviewer = AIReviewer()
        self.max_rounds = 15

    async def run_test(self) -> MCHTestResult:
        try:
            conversation_result = await self._conduct_mch_conversation()

            if not conversation_result["success"]:
                return MCHTestResult(
                    success=False,
                    error="MCH conversation failed",
                    details=conversation_result,
                    timestamp=datetime.now().isoformat(),
                )

            logger.info(
                f" MCH conversation completed in {conversation_result['rounds']} rounds"
            )

            timeout_detected = any(
                msg.get("timeout_detected", False)
                for msg in conversation_result.get("history", [])
            )

            if timeout_detected:
                logger.info(
                    " Timeout detected - waiting 180 seconds for configuration creation..."
                )
                await asyncio.sleep(180)
            else:
                logger.info(
                    " Waiting 30 seconds for configuration creation to complete..."
                )
                await asyncio.sleep(30)

            logger.info("📥 Fetching created configuration from Avni...")
            actual_config = await self.avni_client.fetch_complete_config(
                self.auth_token
            )

            if "error" in actual_config:
                return MCHTestResult(
                    success=False,
                    error="Failed to fetch configuration from Avni",
                    details=actual_config,
                    timestamp=datetime.now().isoformat(),
                )

            validation_result = AIReviewer.validate_created_configuration(
                actual_config=actual_config,
                program_requirements=MCH_REQUIREMENTS,
                scenario_name="Maternal and Child Health Program",
            )

            conversation = ConversationResult(
                rounds_completed=conversation_result["rounds"],
                satisfaction_achieved=conversation_result["satisfaction_achieved"],
                total_messages=len(conversation_result["history"]),
            )

            validation = ValidationResult(
                scores=validation_result.get("scores", {}),
                configuration_assessment=validation_result.get(
                    "configuration_assessment", {}
                ),
                overall_success=validation_result.get("overall_success", False),
                detailed_analysis=validation_result.get("detailed_analysis", ""),
            )

            final_result = MCHTestResult(
                success=validation_result.get("overall_success", False),
                conversation=conversation,
                validation=validation,
                timestamp=datetime.now().isoformat(),
            )

            if final_result.success:
                logger.info(" MCH integration test PASSED!")
            else:
                logger.error(" MCH integration test FAILED")

            return final_result

        except Exception as e:
            logger.error(f" MCH integration test ERROR: {str(e)}")
            return MCHTestResult(
                success=False, error=str(e), timestamp=datetime.now().isoformat()
            )

    async def _conduct_mch_conversation(self) -> Dict[str, Any]:
        conversation_id = ""
        conversation_history = []
        round_count = 0
        satisfaction_achieved = False

        try:
            while round_count < self.max_rounds:
                round_count += 1

                user_message = self.generate_tester_message(
                    self.ai_tester, conversation_history, round_count
                )

                if not user_message or "Error:" in user_message:
                    logger.error(
                        f"Failed to generate tester message in round {round_count}"
                    )
                    break

                inputs = MCHIntegrationTest.create_dify_inputs(self.auth_token)

                if MCHIntegrationTest.is_satisfaction_expressed(user_message):
                    logger.info(" AI Tester expressed satisfaction with configuration")
                    satisfaction_achieved = True

                    # Send the satisfaction message and handle potential timeout
                    dify_response = self.dify_client.send_message(
                        query=user_message,
                        conversation_id=conversation_id,
                        inputs=inputs,
                        timeout=180,
                    )

                    MCHIntegrationTest.handle_satisfaction_response(
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
                if MCHIntegrationTest.is_timeout_response(dify_response):
                    timeout_handled = (
                        MCHIntegrationTest.handle_normal_conversation_timeout(
                            conversation_history, user_message, round_count
                        )
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

                conversation_id = dify_response["conversation_id"]
                assistant_response = dify_response["answer"]

                logger.info(f"Round {round_count}")

                MCHIntegrationTest.record_normal_conversation(
                    conversation_history, user_message, assistant_response, round_count
                )

                if round_count >= self.max_rounds:
                    logger.warning(
                        " Conversation reached maximum rounds without satisfaction"
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

    @staticmethod
    def generate_tester_message(
        ai_tester, conversation_history: List[Dict[str, Any]], round_count: int
    ) -> str:
        if round_count == 1:
            return ai_tester.generate_message([], 0)

        # Convert conversation history to tester's perspective
        tester_history = []
        for msg in conversation_history:
            if msg["role"] == "user":  # Tester's previous message
                tester_history.append({"role": "assistant", "content": msg["content"]})
            elif msg["role"] == "assistant":  # Dify's response becomes input to tester
                tester_history.append({"role": "user", "content": msg["content"]})

        return ai_tester.generate_message(tester_history, 0)

    @staticmethod
    def create_dify_inputs(auth_token: str) -> Dict[str, Any]:
        return {
            "auth_token": auth_token,
            "org_name": "Jan Swasthya Sahyog",
            "org_type": "Trial",
            "user_name": "Atul",
            "avni_mcp_server_url": os.getenv("AVNI_MCP_SERVER_URL"),
        }

    @staticmethod
    def is_satisfaction_expressed(user_message: str) -> bool:
        return (
            "i am happy with the configuration provided by the avni assistant"
            in user_message.lower()
        )

    @staticmethod
    def is_timeout_response(dify_response: Dict[str, Any]) -> bool:
        if dify_response["success"]:
            return False

        error_str = str(dify_response.get("error", "")).lower()
        return "timeout" in error_str or "504" in error_str

    @staticmethod
    def handle_satisfaction_response(
        dify_response: Dict[str, Any],
        conversation_history: List[Dict[str, Any]],
        user_message: str,
        round_count: int,
    ) -> None:
        conversation_history.append(
            {"role": "user", "content": user_message, "round": round_count}
        )

        if MCHIntegrationTest.is_timeout_response(dify_response):
            logger.info(
                "🔄 Dify timeout detected - configuration creation likely in progress "
            )
            conversation_history.append(
                {
                    "role": "assistant",
                    "content": "Configuration creation in progress (timeout detected)",
                    "round": round_count,
                    "timeout_detected": True,
                }
            )
        elif dify_response["success"]:
            conversation_history.append(
                {
                    "role": "assistant",
                    "content": dify_response["answer"],
                    "round": round_count,
                }
            )
        else:
            logger.warning(
                f"Dify error after satisfaction: {dify_response.get('error', 'Unknown')}"
            )
            conversation_history.append(
                {
                    "role": "assistant",
                    "content": f"Error after satisfaction: {dify_response.get('error', 'Unknown')}",
                    "round": round_count,
                }
            )

    @staticmethod
    def handle_normal_conversation_timeout(
        conversation_history: List[Dict[str, Any]], user_message: str, round_count: int
    ) -> bool:
        logger.info(
            "Dify timeout/504 detected during conversation - configuration creation in progress"
        )

        conversation_history.append(
            {"role": "user", "content": user_message, "round": round_count}
        )
        conversation_history.append(
            {
                "role": "assistant",
                "content": "Configuration creation in progress (timeout detected during conversation)",
                "round": round_count,
                "timeout_detected": True,
            }
        )

        return True

    @staticmethod
    def record_normal_conversation(
        conversation_history: List[Dict[str, Any]],
        user_message: str,
        assistant_response: str,
        round_count: int,
    ) -> None:
        conversation_history.append(
            {"role": "user", "content": user_message, "round": round_count}
        )
        conversation_history.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "round": round_count,
            }
        )


def print_test_results(result: MCHTestResult) -> None:
    print("=" * 50)
    print(f"Success: {' PASS' if result.success else ' FAIL'}")

    if result.success:
        validation = result.validation
        print("\n Validation Scores:")
        scores = validation.scores
        print(
            f"  • Functional Adequacy: {scores.get('functional_adequacy', 'N/A')}/100"
        )
        print(
            f"  • Structural Correctness: {scores.get('structural_correctness', 'N/A')}/100"
        )
        print(f"  • Completeness: {scores.get('completeness', 'N/A')}/100")

        config_assessment = validation.configuration_assessment
        print("\n Configuration Created:")
        print(
            f"  • Subject Types: {len(config_assessment.get('subject_types_created', []))}"
        )
        print(f"  • Programs: {len(config_assessment.get('programs_created', []))}")
        print(f"  • Encounters: {len(config_assessment.get('encounters_created', []))}")
        print(f"  • Catchments: {len(config_assessment.get('catchments_created', []))}")

    else:
        print(f"\n Error: {result.error or 'Unknown error'}")


async def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    if not validate_all_env_variables():
        sys.exit(1)

    dify_api_key = os.getenv("DIFY_API_KEY")
    avni_auth_token = os.getenv("AVNI_AUTH_TOKEN")

    print("MCH Integration Test Starting")
    print("=" * 50)

    test = MCHIntegrationTest(dify_api_key, avni_auth_token)
    result = await test.run_test()

    print_test_results(result)

    if result.success:
        print("\n🎉 MCH Integration Test completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️ MCH Integration Test failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
