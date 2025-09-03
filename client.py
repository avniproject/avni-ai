"""HTTP client for Avni API."""

import httpx
from config import BASE_URL, get_headers
from utils import ApiResult


async def make_avni_request(
    method: str, endpoint: str, auth_token: str, data: dict = None, files: dict = None
) -> ApiResult:
    """Make a request to the Avni API with proper error handling."""
    url = f"{BASE_URL}{endpoint}"

    headers = get_headers()
    headers["USER-NAME"] = auth_token   

    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method.upper() == "POST":
                response = await client.post(
                    url, headers=headers, json=data, files=files, timeout=30.0
                )
            else:
                return ApiResult.error_result("Unsupported HTTP method")

            response.raise_for_status()
            response_data = response.json()

            return ApiResult.success_result(response_data or [])

        except httpx.HTTPStatusError as e:
            return ApiResult.error_result(f"HTTP {e.response.status_code}")
        except httpx.TimeoutException:
            return ApiResult.error_result("Request timeout")
        except httpx.RequestError as e:
            return ApiResult.error_result(f"Network error: {str(e)}")
        except Exception as e:
            return ApiResult.error_result(str(e))
