from typing import Optional
from src.clients import make_avni_request
from src.utils.format_utils import  format_creation_response
from src.core import tool_registry

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
    if parent_id is not None:
        payload["parentId"] = parent_id

    result = await make_avni_request(
        "POST", "/addressLevelType", auth_token, payload
    )

    if not result.success:
        return result.format_error("create location type")

    return format_creation_response("Location type", name, "id", result.data)

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
    parents = [{"id": parent_id}] if parent_id is not None else []
    payload = [
        {"name": name, "level": level, "type": location_type, "parents": parents}
    ]

    result = await make_avni_request("POST", "/locations", auth_token, payload)

    if not result.success:
        return result.format_error("create location")

    return format_creation_response("Location", name, "id", result.data)

def register_address_level_type_tools() -> None:
    tool_registry.register_tool(create_location_type)
    tool_registry.register_tool(create_location)