"""Comprehensive Avni API Client for all operations"""

import httpx
import logging
import os
from typing import Dict, Any, Optional
from ..utils.api_utils import ApiResult

logger = logging.getLogger(__name__)


def get_headers() -> Dict[str, str]:
    """Get base headers for API requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


async def make_avni_request(
    method: str,
    endpoint: str,
    auth_token: str,
    data: Optional[Dict[str, Any]] = None,
    base_url: Optional[str] = None,
) -> ApiResult:
    """
    Make a request to the Avni API with proper error handling.

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint (e.g., "/addressLevelType")
        auth_token: Avni API authentication token
        data: Request payload for POST requests
        base_url: Base URL for Avni API (optional, uses env var if not provided)

    Returns:
        ApiResult with success/error status and data
    """
    if not base_url:
        base_url = os.getenv("AVNI_BASE_URL")

    url = f"{base_url.rstrip('/')}{endpoint}"

    headers = get_headers()
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


class AvniClient:
    """Client for interacting with Avni API."""

    def __init__(self, timeout: float = 30.0):
        """
        Initialize Avni client.

        Args:
            timeout: Request timeout in seconds
        """
        self.base_url = os.getenv("AVNI_BASE_URL")
        self.timeout = timeout

    async def make_request(
        self,
        method: str,
        endpoint: str,
        auth_token: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> ApiResult:
        """
        Make a request using this client's base URL.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            auth_token: Avni API authentication token
            data: Request payload for POST requests

        Returns:
            ApiResult with success/error status and data
        """
        return await make_avni_request(
            method, endpoint, auth_token, data, self.base_url
        )

    async def fetch_complete_config(self, auth_token: str) -> Dict[str, Any]:
        """
        Fetch complete configuration from Avni API by calling specific endpoints.

        Args:
            auth_token: Avni API authentication token

        Returns:
            Dictionary containing complete configuration data or error information
        """
        try:
            complete_config = {}

            # Define all endpoints to fetch
            endpoints = {
                "addressLevelTypes": "/addressLevelType",
                "locations": "/locations",
                "catchments": "/catchment",
                "subjectTypes": "/web/subjectType",
                "programs": "/web/program",
                "encounterTypes": "/web/encounterType",
            }

            # Fetch data from each endpoint
            for config_key, endpoint in endpoints.items():
                logger.info(f"Fetching {config_key} from {endpoint}")
                result = await self.make_request("GET", endpoint, auth_token)

                if result.success:
                    complete_config[config_key] = result.data or []
                    logger.info(
                        f"Successfully fetched {len(complete_config[config_key])} {config_key}"
                    )
                else:
                    logger.error(f"Failed to fetch {config_key}: {result.error}")
                    return {"error": f"Failed to fetch {config_key}: {result.error}"}

            logger.info("Successfully fetched complete configuration")
            return complete_config

        except Exception as e:
            error_msg = f"Failed to fetch complete configuration: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}


def create_avni_client(timeout: float = 30.0) -> AvniClient:
    """
    Factory function to create an Avni client.

    Args:
        timeout: Request timeout in seconds

    Returns:
        Configured Avni client
    """
    return AvniClient(timeout)
