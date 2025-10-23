import os
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from ..common.dify_client import DifyClient, extract_config_from_response
from .message_templates import (
    get_create_message,
    get_update_message,
    get_delete_message,
)

logger = logging.getLogger(__name__)


@dataclass
class ConversationResult:
    success: bool
    extracted_config: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[Dict[str, Any]]] = None
    error_message: Optional[str] = None
    
    @property
    def has_config(self) -> bool:
        return self.success and self.extracted_config is not None


class DifyConversationManager:

    def __init__(self, dify_api_key: str):
        self.dify_client = DifyClient(dify_api_key)
        self.conversation_id = ""
        self.max_rounds = 10  # Safety limit

    def conduct_config_conversation(
        self,
        config_file_path: str,
        auth_token: str,
        org_name: str = "Test Organization",
        org_type: str = "Demo",
        user_name: str = "Test User",
    ) -> ConversationResult:
        try:
            with open(config_file_path, "r") as f:
                test_config = json.load(f)

            self.conversation_id = ""

            initial_message = DifyConversationManager._create_initial_message(
                test_config
            )

            conversation_history = []
            round_count = 0

            current_message = initial_message

            while round_count < self.max_rounds:
                round_count += 1

                inputs = {
                    "auth_token": auth_token,
                    "org_name": org_name,
                    "org_type": org_type,
                    "user_name": user_name,
                    "avni_mcp_server_url": os.getenv("AVNI_MCP_SERVER_URL"),
                }

                response = self.dify_client.send_message(
                    query=current_message,
                    conversation_id=self.conversation_id,
                    inputs=inputs,
                )

                if response["success"]:
                    self.conversation_id = response["conversation_id"]

                if not response["success"]:
                    error_msg = f"Dify API error in round {round_count}: {response.get('error')}"
                    logger.error(error_msg)
                    return ConversationResult(
                        success=False,
                        conversation_history=conversation_history,
                        error_message=error_msg
                    )

                assistant_response = response["answer"]

                conversation_history.append(
                    {
                        "round": round_count,
                        "user_message": current_message,
                        "assistant_response": assistant_response,
                        "response_length": len(assistant_response),
                    }
                )

                logger.info(
                    f"Assistant response length: {len(assistant_response)} characters"
                )

                extracted_config = extract_config_from_response(assistant_response)

                if extracted_config:
                    logger.info(f"Configuration extracted in round {round_count}")
                    return ConversationResult(
                        success=True,
                        extracted_config=extracted_config,
                        conversation_history=conversation_history
                    )

                current_message = DifyConversationManager._generate_follow_up_message()

            error_msg = f"Conversation reached max rounds ({self.max_rounds}) without extracting config"
            logger.error(error_msg)
            return ConversationResult(
                success=False,
                conversation_history=conversation_history,
                error_message=error_msg
            )

        except Exception as e:
            error_msg = f"Error in conversation: {e}"
            logger.error(error_msg)
            return ConversationResult(
                success=False,
                error_message=error_msg
            )

    @staticmethod
    def _create_initial_message(test_config: Dict[str, Any]) -> str:
        config_data = test_config.get("config", {})

        if "create" in config_data:
            return get_create_message()
        elif "update" in config_data:
            return get_update_message()
        elif "delete" in config_data:
            return get_delete_message()
        else:
            return (
                "Hi, I need help setting up an Avni configuration for my organization."
            )

    @staticmethod
    def _generate_follow_up_message() -> str:
        """Generate the follow-up message - always the same response."""
        return "Yeah you are correct, create this config automatically now"
