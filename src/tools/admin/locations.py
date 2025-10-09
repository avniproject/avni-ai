import logging
from typing import Optional
from src.clients import make_avni_request
from src.utils.format_utils import format_list_response, format_creation_response
from src.utils.session_context import log_payload
from src.core import tool_registry

logger = logging.getLogger(__name__)

async def get_locations(auth_token: str) -> str:
    """Retrieve a list of location types for an organization to find IDs for creating locations or sub-location types."""
    result = await make_avni_request("GET", "/locations", auth_token)

    if not result.success:
        return result.format_error("retrieve location types")

    if not result.data:
        return result.format_empty("location types")

    return format_list_response(result.data, extra_key="level")

async def create_location(
        auth_token: str,
        name: str,
        level: int,
        location_type: str,
        parent_id: Optional[int] = None,
) -> str:
    """Create a real location (e.g., Himachal Pradesh, Kullu) in Avni's location hierarchy.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the location
        level: Level of the location (e.g., 1 for Village)
        location_type: Type of the location
        parent_id: Parent location ID (optional)
    """
    # Handle parent_id conversion and validation
    if parent_id is not None:
        if isinstance(parent_id, str):
            if parent_id.strip() == "":
                # Empty string means no parent - set to None
                parent_id = None
            else:
                try:
                    parent_id = int(parent_id)
                except ValueError as e:
                    return f"Error converting parent_id to integer for '{name}': {e}. parent_id: {parent_id}"
    
    parents = [{"id": parent_id}] if parent_id is not None else []
    payload = [
        {"name": name, "level": level, "type": location_type, "parents": parents}
    ]
    
    # Log the actual API payload to both standard and session loggers
    log_payload("Location API payload:", payload)

    result = await make_avni_request("POST", "/locations", auth_token, payload)

    if not result.success:
        return result.format_error("create location")

    return format_creation_response("Location", name, "id", result.data)

def register_location_tools() -> None:
    tool_registry.register_tool(get_locations)
    tool_registry.register_tool(create_location)