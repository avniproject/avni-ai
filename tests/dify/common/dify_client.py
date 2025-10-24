import requests
import json
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)


class DifyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = os.getenv("DIFY_API_BASE_URL")
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def send_message(
        self,
        query: str,
        conversation_id: str = "",
        user: str = "automated_prompts_tester",
        inputs: Optional[Dict[str, Any]] = None,
        timeout: int = 120,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/chat-messages"

        payload = {
            "inputs": inputs or {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": user,
        }

        try:
            logger.info(f"Sending message to Dify")

            response = requests.post(
                url, headers=self.headers, data=json.dumps(payload), timeout=timeout
            )
            response.raise_for_status()

            data = response.json()

            return {
                "answer": data.get("answer", ""),
                "conversation_id": data.get("conversation_id", ""),
                "message_id": data.get("message_id", ""),
                "success": True,
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Dify API: {e}")
            return {
                "answer": "Sorry, I encountered an error connecting to the assistant.",
                "conversation_id": conversation_id,
                "message_id": "",
                "success": False,
                "error": str(e),
            }


def extract_config_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    # Check if the response starts with { (JSON config)
    response_text = response_text.strip()
    if response_text.startswith("{"):
        try:
            parsed = json.loads(response_text)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response that starts with {{")
            return None

    return None
