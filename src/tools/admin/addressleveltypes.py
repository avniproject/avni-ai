import logging
from typing import Optional
from src.clients import make_avni_request
from src.utils.format_utils import  format_creation_response
from src.utils.session_context import log_payload
from src.core import tool_registry

logger = logging.getLogger(__name__)

async def create_location_type(
        auth_token: str, name: str, level: float, parent_id: Optional[int] = None
) -> str:
    """Create a location type (e.g., State, District) for hierarchical location setup in Avni.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the location type
        level: Level of the location type (e.g., 3 for State, 2 for District)
        parent_id: Parent location type ID, if any (optional)
    """
    payload = {"name": name, "level": level}
    if parent_id is not None and parent_id != "":
        # Convert parent_id to int if it's a string, but only include if not empty
        try:
            if isinstance(parent_id, str):
                if parent_id.strip() == "":
                    # Empty string means no parent - don't include parentId in payload
                    pass
                else:
                    payload["parentId"] = int(parent_id)
            else:
                payload["parentId"] = parent_id
        except ValueError as e:
            return f"Error converting parent_id to integer for '{name}': {e}. parent_id: {parent_id}"

    # Log the actual API payload to both standard and session loggers
    log_payload("AddressLevelType API payload:", payload)

    result = await make_avni_request(
        "POST", "/addressLevelType", auth_token, payload
    )

    if not result.success:
        return result.format_error("create location type")

    return format_creation_response("Location type", name, "id", result.data)

def register_address_level_type_tools() -> None:
    tool_registry.register_tool(create_location_type)