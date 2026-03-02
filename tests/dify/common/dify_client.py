import json as _json
import requests
import logging
from typing import Dict, Any, Optional
import os
import time

logger = logging.getLogger(__name__)
DEFAULT_DIFY_API_BASE_URL = "https://api.dify.ai/v1"


class DifyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = (
            os.getenv("DIFY_API_BASE_URL", DEFAULT_DIFY_API_BASE_URL).rstrip("/")
        )
        self.max_retries = int(os.getenv("DIFY_MAX_RETRIES", "3"))
        self.retry_backoff_seconds = float(os.getenv("DIFY_RETRY_BACKOFF_SECONDS", "2"))
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    # ── public API ────────────────────────────────────────────────────────

    def send_message(
        self,
        query: str,
        conversation_id: str = "",
        user: str = "automated_prompts_tester",
        inputs: Optional[Dict[str, Any]] = None,
        timeout: int = 120,
    ) -> Dict[str, Any]:
        if not self.api_key:
            return self._error_result(
                conversation_id,
                "DIFY_API_KEY is missing. Set DIFY_API_KEY (or a compatible alias) "
                "before running Dify-backed tests.",
            )

        if not self.base_url.startswith(("http://", "https://")):
            return self._error_result(
                conversation_id,
                "DIFY_API_BASE_URL is invalid. Expected a full URL like "
                "https://api.dify.ai/v1.",
            )

        url = f"{self.base_url}/chat-messages"

        # Use streaming mode — Dify chatflow/workflow apps require it.
        payload = {
            "inputs": inputs or {},
            "query": query,
            "response_mode": "streaming",
            "conversation_id": conversation_id,
            "user": user,
        }

        attempts = max(1, self.max_retries)
        last_error = ""

        for attempt in range(1, attempts + 1):
            try:
                logger.info(
                    "Sending message to Dify (attempt %s/%s)", attempt, attempts
                )

                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout,
                    stream=True,
                )
                response.raise_for_status()

                return self._consume_sse_stream(response, conversation_id)

            except requests.exceptions.HTTPError as e:
                response_snippet = ""
                if e.response is not None and e.response.text:
                    response_snippet = e.response.text[:300]
                last_error = str(e)
                if response_snippet:
                    last_error = f"{last_error} | response={response_snippet}"
                retryable = self._is_retryable_error(e)
                logger.error(
                    "Error calling Dify API (attempt %s/%s): %s", attempt, attempts, last_error
                )

                if not retryable or attempt == attempts:
                    break

                sleep_seconds = self.retry_backoff_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "Retrying Dify API call after %.1fs due to retryable error.",
                    sleep_seconds,
                )
                time.sleep(sleep_seconds)
            except requests.exceptions.RequestException as e:
                last_error = str(e)
                retryable = self._is_retryable_error(e)
                logger.error(
                    "Error calling Dify API (attempt %s/%s): %s", attempt, attempts, e
                )

                if not retryable or attempt == attempts:
                    break

                sleep_seconds = self.retry_backoff_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "Retrying Dify API call after %.1fs due to retryable error.",
                    sleep_seconds,
                )
                time.sleep(sleep_seconds)

        return self._error_result(conversation_id, last_error)

    # ── SSE stream consumer ───────────────────────────────────────────────

    @staticmethod
    def _consume_sse_stream(
        response: requests.Response,
        fallback_conversation_id: str,
    ) -> Dict[str, Any]:
        """Parse a Dify SSE stream and return a blocking-style result dict.

        Collects all ``event: message`` tokens into the full answer, and
        extracts ``conversation_id`` / ``message_id`` from the first data
        payload that carries them.
        """
        answer_parts: list[str] = []
        conversation_id = fallback_conversation_id
        message_id = ""

        for raw_line in response.iter_lines(decode_unicode=True):
            if not raw_line:
                continue  # blank keep-alive line

            # SSE lines are either "event: <type>" or "data: <json>"
            if raw_line.startswith("data: "):
                json_str = raw_line[len("data: "):]
                try:
                    data = _json.loads(json_str)
                except _json.JSONDecodeError:
                    continue

                event_type = data.get("event", "")

                # Accumulate streamed answer tokens
                if event_type == "message":
                    answer_parts.append(data.get("answer", ""))

                # Capture IDs from any event that carries them
                if data.get("conversation_id"):
                    conversation_id = data["conversation_id"]
                if data.get("message_id"):
                    message_id = data["message_id"]

                # Check for workflow/message errors
                if event_type == "error":
                    error_msg = data.get("message") or data.get("error", "Unknown Dify error")
                    return {
                        "answer": "".join(answer_parts) or "Sorry, I encountered an error.",
                        "conversation_id": conversation_id,
                        "message_id": message_id,
                        "success": False,
                        "error": error_msg,
                    }

                # message_end carries the final aggregated answer in some Dify versions
                if event_type == "message_end":
                    if not answer_parts and data.get("answer"):
                        answer_parts.append(data["answer"])

        response.close()

        full_answer = "".join(answer_parts)
        return {
            "answer": full_answer,
            "conversation_id": conversation_id,
            "message_id": message_id,
            "success": bool(full_answer),
            **({"error": "Empty response from Dify"} if not full_answer else {}),
        }

    # ── helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _error_result(conversation_id: str, error: str) -> Dict[str, Any]:
        return {
            "answer": "Sorry, I encountered an error connecting to the assistant.",
            "conversation_id": conversation_id,
            "message_id": "",
            "success": False,
            "error": error,
        }

    @staticmethod
    def _is_retryable_error(error: requests.exceptions.RequestException) -> bool:
        if isinstance(
            error,
            (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ),
        ):
            return True

        if isinstance(error, requests.exceptions.HTTPError) and error.response is not None:
            # Retry on throttling and transient server failures
            if error.response.status_code in {429, 500, 502, 503, 504}:
                return True

        message = str(error).lower()
        retryable_markers = (
            "response ended prematurely",
            "read timed out",
            "connection reset",
            "temporarily unavailable",
        )
        return any(marker in message for marker in retryable_markers)


def extract_config_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    # Check if the response starts with { (JSON config)
    response_text = response_text.strip()
    if response_text.startswith("{"):
        try:
            parsed = _json.loads(response_text)
            if isinstance(parsed, dict):
                return parsed
        except _json.JSONDecodeError:
            logger.error("Failed to parse JSON response that starts with {{")
            return None

    return None
