"""HTTP handlers for configuration endpoints."""

import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..services.avni.config_fetcher import ConfigFetcher

logger = logging.getLogger(__name__)

_config_fetcher = ConfigFetcher()


async def handle_get_existing_config(request: Request) -> JSONResponse:
    """
    Return existing configuration from the Avni server.

    Query params (all optional):
      sections  — comma-separated list of section keys to fetch, e.g.
                  ``sections=subjectTypes,programs``.  Default: all six sections.
      max_items — cap each array to this many items.  Default: MAX_CONFIG_ITEMS
                  env var (100).  Pass 0 for unlimited.
    """
    from ..auth_store import resolve_auth_token

    auth_token = resolve_auth_token(request)
    if not auth_token:
        return JSONResponse(
            {
                "error": "Missing auth: provide avni-auth-token header or conversation_id"
            },
            status_code=401,
        )

    # Parse optional query params
    sections_raw = request.query_params.get("sections")
    sections = (
        [s.strip() for s in sections_raw.split(",") if s.strip()]
        if sections_raw
        else None
    )

    max_items_raw = request.query_params.get("max_items")
    max_items: int | None = None
    if max_items_raw is not None:
        try:
            max_items = int(max_items_raw)
            if max_items == 0:
                max_items = None  # 0 means unlimited
        except ValueError:
            return JSONResponse(
                {"error": "max_items must be an integer"}, status_code=400
            )

    try:
        config = await _config_fetcher.fetch_complete_config(
            auth_token, sections=sections, max_items=max_items
        )
        if "error" in config:
            return JSONResponse({"error": config["error"]}, status_code=502)
        return JSONResponse(config)
    except Exception as e:
        logger.error(f"Error fetching existing config: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
