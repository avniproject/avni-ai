"""
Dify API client for interacting with the Avni AI Assistant.
"""

import requests
import json
from typing import Dict, Any


class DifyClient:
    """Client for interacting with Dify API"""

    def __init__(self, api_key: str, base_url: str = "https://api.dify.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def send_message(
        self, query: str, conversation_id: str = "", user: str = "automated_tester"
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/chat-messages"

        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": user,
        }

        try:
            response = requests.post(
                url, headers=self.headers, data=json.dumps(payload)
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
            print(f"Error calling Dify API: {e}")
            return {
                "answer": "Sorry, I encountered an error connecting to the assistant.",
                "conversation_id": conversation_id,
                "message_id": "",
                "success": False,
                "error": str(e),
            }
        except json.JSONDecodeError as e:
            print(f"Error parsing Dify response: {e}")
            return {
                "answer": "Sorry, I received an invalid response from the assistant.",
                "conversation_id": conversation_id,
                "message_id": "",
                "success": False,
                "error": str(e),
            }
