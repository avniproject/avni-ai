"""
Conversation manager for Dify workflow testing.
Handles the multi-round conversations with the Dify-built Avni AI Assistant.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from .dify_client import DifyClient, extract_config_from_response
from ..utils.message_templates import (
    get_create_message,
    get_update_message,
    get_delete_message,
)

logger = logging.getLogger(__name__)


class DifyConversationManager:
    """
    Manages conversations with the Dify workflow for configuration testing.

    This class handles the multi-round conversation flow and extracts
    the final configuration from the Dify assistant's responses.
    """

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
        avni_base_url: str = "https://app.avniproject.org",
    ) -> Tuple[bool, Dict[str, Any], List[Dict[str, Any]]]:
        """
        Conduct a complete conversation with Dify to generate configuration.

        Args:
            config_file_path: Path to the test config JSON file
            auth_token: Avni authentication token
            org_name: Organization name
            org_type: Organization type
            user_name: User name
            avni_base_url: Avni base URL

        Returns:
            Tuple of (success, final_config, conversation_history)
        """
        try:
            # Load the test config to understand what we're asking for
            with open(config_file_path, "r") as f:
                test_config = json.load(f)

            # Reset conversation state
            self.conversation_id = ""

            # Start the conversation
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
                    "avnibaseurl": avni_base_url,
                }

                response = self.dify_client.send_message(
                    query=current_message,
                    conversation_id=self.conversation_id,
                    inputs=inputs,
                )

                if response["success"]:
                    self.conversation_id = response["conversation_id"]

                if not response["success"]:
                    logger.error(
                        f"Dify API error in round {round_count}: {response.get('error')}"
                    )
                    return False, {}, conversation_history

                assistant_response = response["answer"]

                # Record the conversation
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
                    return True, extracted_config, conversation_history

                # Generate follow-up message
                current_message = DifyConversationManager._generate_follow_up_message()

            # If we exit the loop, we've hit max rounds without finding config
            logger.error(
                f"Conversation reached max rounds ({self.max_rounds}) without extracting config"
            )
            return False, {}, conversation_history

        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            return False, {}, []

    @staticmethod
    def _create_initial_message(test_config: Dict[str, Any]) -> str:
        """Create a natural language initial message to send to Dify based on the test config"""

        # Extract the operation type
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
