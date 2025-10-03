"""Location management tools."""

from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from client import make_avni_request
from utils import format_list_response, format_creation_response
from tool_registry import tool_registry


def register_location_tools(mcp: FastMCP) -> None:
    """Register location-related tools with the MCP server."""

    @mcp.tool()
    async def get_location_types(auth_token: str) -> str:
        """Retrieve a list of location types for an organization to find IDs for creating locations or sub-location types."""
        result = await make_avni_request("GET", "/addressLevelType", auth_token)

        if not result.success:
            return result.format_error("retrieve location types")

        if not result.data:
            return result.format_empty("location types")

        return format_list_response(result.data, extra_key="level")

    @mcp.tool()
    async def get_catchments(auth_token: str) -> str:
        """Retrieve a list of catchments for an organization to find IDs for assigning users."""
        result = await make_avni_request("GET", "/catchment", auth_token)

        if not result.success:
            return result.format_error("retrieve catchments")

        if not result.data:
            return result.format_empty("catchments")

        return format_list_response(result.data)

    @mcp.tool()
    async def create_location_type(
        auth_token: str, name: str, level: float, parent_id: Optional[int] = None
    ) -> str:
        """Create a location type (e.g., State, District) for hierarchical location setup in Avni.

        Args:
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

    @mcp.tool()
    async def create_location(
        auth_token: str,
        name: str,
        level: int,
        location_type: str,
        parent_id: Optional[int] = None,
    ) -> str:
        """Create a real location (e.g., Himachal Pradesh, Kullu) in Avni's location hierarchy.

        Args:
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

    @mcp.tool()
    async def create_catchment(
        auth_token: str, name: str, location_ids: List[int]
    ) -> str:
        """Create a catchment grouping locations for data collection in Avni.

        Args:
            name: Name of the catchment
            location_ids: List of location IDs
        """
        payload = {"deleteFastSync": False, "name": name, "locationIds": location_ids}

        result = await make_avni_request("POST", "/catchment", auth_token, payload)

        if not result.success:
            return result.format_error("create catchment")

        return format_creation_response("Catchment", name, "id", result.data)


# Direct tool functions for function calling
async def get_location_types(auth_token: str) -> str:
    """Retrieve a list of location types for an organization to find IDs for creating locations or sub-location types."""
    result = await make_avni_request("GET", "/addressLevelType", auth_token)

    if not result.success:
        return result.format_error("retrieve location types")

    if not result.data:
        return result.format_empty("location types")

    return format_list_response(result.data, extra_key="level")


async def get_catchments(auth_token: str) -> str:
    """Retrieve a list of catchments for an organization to find IDs for assigning users."""
    result = await make_avni_request("GET", "/catchment", auth_token)

    if not result.success:
        return result.format_error("retrieve catchments")

    if not result.data:
        return result.format_empty("catchments")

    return format_list_response(result.data)


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


def register_location_tools_direct() -> None:
    """Register location tools for direct function calling."""
    tool_registry.register_tool(get_location_types)
    tool_registry.register_tool(get_catchments)
    tool_registry.register_tool(create_location_type)
    tool_registry.register_tool(create_location)
    tool_registry.register_tool(create_catchment)
