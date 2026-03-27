"""HTTP handlers for configuration endpoints."""

import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..services.avni.config_fetcher import ConfigFetcher

logger = logging.getLogger(__name__)

_config_fetcher = ConfigFetcher()


async def handle_get_existing_config(request: Request) -> JSONResponse:
    """Return the complete existing configuration from the Avni server."""
    auth_token = request.headers.get("avni-auth-token")
    if not auth_token:
        return JSONResponse(
            {"error": "avni-auth-token header is required"}, status_code=401
        )
    try:
        config = await _config_fetcher.fetch_complete_config(auth_token)
        if "error" in config:
            return JSONResponse({"error": config["error"]}, status_code=502)
        return JSONResponse(config)
    except Exception as e:
        logger.error(f"Error fetching existing config: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
