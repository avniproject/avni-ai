from dataclasses import dataclass

import httpx
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class ApiResult:
    success: bool
    data: Any = None
    error: Optional[str] = None

    @classmethod
    def success_result(cls, data: Any) -> "ApiResult":
        return cls(success=True, data=data)

    @classmethod
    def error_result(cls, error: str) -> "ApiResult":
        return cls(success=False, error=error)


class AvniClient:
    def __init__(
        self, base_url=os.getenv("AVNI_BASE_URL"), timeout_seconds: float = 30.0
    ):
        self.base_url = base_url
        self.timeout = timeout_seconds

    @staticmethod
    def get_headers() -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def call_avni_server(
        self,
        method: str,
        endpoint: str,
        auth_token: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> ApiResult:
        url = f"{self.base_url.rstrip('/')}{endpoint}"

        headers = AvniClient.get_headers()
        headers["AUTH-TOKEN"] = auth_token

        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=headers, timeout=30.0)
                elif method.upper() == "POST":
                    response = await client.post(
                        url, headers=headers, json=data, timeout=30.0
                    )
                elif method.upper() == "PUT":
                    response = await client.put(
                        url, headers=headers, json=data, timeout=30.0
                    )
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=headers, timeout=30.0)
                else:
                    return ApiResult.error_result("Unsupported HTTP method")

                response.raise_for_status()
                response_data = response.json() if response.content else {}

                return ApiResult.success_result(response_data or [])

            except httpx.HTTPStatusError as e:
                error_msg = f"HTTP {e.response.status_code}"
                logger.error(
                    f"HTTP error for {endpoint}: {e.response.status_code} - {e.response.text}"
                )
                return ApiResult.error_result(error_msg)
            except httpx.TimeoutException:
                logger.error(f"Timeout error for {endpoint}")
                return ApiResult.error_result("Request timeout")
            except httpx.RequestError as e:
                logger.error(f"Network error for {endpoint}: {str(e)}")
                return ApiResult.error_result(f"Network error: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error for {endpoint}: {str(e)}")
                return ApiResult.error_result(str(e))
