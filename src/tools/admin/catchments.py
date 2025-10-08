from typing import List
from src.clients import make_avni_request
from src.utils.format_utils import format_list_response, format_creation_response
from src.core import tool_registry

async def get_catchments(auth_token: str) -> str:
    """Retrieve a list of catchments for an organization to find IDs for assigning users."""
    result = await make_avni_request("GET", "/catchment", auth_token)

    if not result.success:
        return result.format_error("retrieve catchments")

    if not result.data:
        return result.format_empty("catchments")

    return format_list_response(result.data)


async def create_catchment(
        auth_token: str, name: str, location_ids: List[int]
) -> str:
    """Create a catchment grouping locations for data collection in Avni.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the catchment
        location_ids: List of location IDs
    """
    payload = {"deleteFastSync": False, "name": name, "locationIds": location_ids}

    result = await make_avni_request("POST", "/catchment", auth_token, payload)

    if not result.success:
        return result.format_error("create catchment")

    return format_creation_response("Catchment", name, "id", result.data)


def register_catchment_tools() -> None:
    tool_registry.register_tool(get_catchments)
    tool_registry.register_tool(create_catchment)