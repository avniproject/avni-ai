"""Organization management tools."""

from mcp.server.fastmcp import FastMCP
from client import make_avni_request
from utils import format_creation_response


def register_organization_tools(mcp: FastMCP) -> None:
    """Register organization-related tools with the MCP server."""

    @mcp.tool()
    async def create_organization(name: str) -> str:
        """Create a new organization in Avni with default settings, enabling data entry app setup.

        Args:
            name: Name of the organization
        """
        org_name = name.lower().replace(" ", "_")
        payload = {
            "name": name,
            "dbUser": org_name,
            "schemaName": org_name,
            "mediaDirectory": org_name,
            "usernameSuffix": org_name,
            "categoryId": 1,
            "statusId": 1,
        }

        result = await make_avni_request(
            "POST", "/organisation", payload
        )

        if not result.success:
            return result.format_error("create organization")

        return format_creation_response("Organization", name, "id", result.data)
