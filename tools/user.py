"""User management tools."""

from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from client import make_avni_request
from utils import format_list_response, format_creation_response


def register_user_tools(mcp: FastMCP) -> None:
    """Register user-related tools with the MCP server."""

    @mcp.tool()
    async def get_groups() -> str:
        """Retrieve a list of user groups for an organization to find IDs for assigning users."""
        result = await make_avni_request("GET", "/web/groups")

        if not result.success:
            return result.format_error("retrieve user groups")

        if not result.data:
            return result.format_empty("user groups")

        return format_list_response(result.data)

    @mcp.tool()
    async def create_a_user(
        org_name: str,
        first_name: str,
        email: str,
        phone_number: str,
        last_name: Optional[str] = None,
        group_ids: Optional[List[int]] = None,
    ) -> str:
        """Create a user for an Avni organization to manage app configuration and data entry, requires group ID if you also need to assign a group to the user.

        Args:
            org_name: Organization name
            first_name: First name of the user
            email: Email address
            phone_number: Phone number
            last_name: Last name of the user (optional)
            group_ids: List of group IDs (optional)
        """
        username_prefix = (
            first_name[:4].lower() if len(first_name) >= 4 else first_name.lower()
        )
        username = f"{username_prefix}@{org_name.lower().replace(' ', '_')}"
        full_name = f"{first_name} {last_name}" if last_name else first_name

        settings = {
            "locale": "en",
            "isAllowedToInvokeTokenGenerationAPI": False,
            "datePickerMode": "calendar",
            "timePickerMode": "clock",
        }

        payload = {
            "operatingIndividualScope": "None",
            "username": username,
            "ignored": username_prefix,
            "name": full_name,
            "email": email,
            "phoneNumber": phone_number,
            "groupIds": group_ids or [],
            "settings": settings,
        }

        result = await make_avni_request(
            "POST", "/user", payload
        )

        if not result.success:
            return result.format_error("create admin user")

        return f"Admin user '{username}' created successfully with ID {result.data.get('id')}"

    @mcp.tool()
    async def create_user(
        org_name: str,
        username: str,
        name: str,
        email: str,
        phone_number: str,
        catchment_id: Optional[int] = None,
        group_ids: Optional[List[int]] = None,
        track_location: bool = False,
        allow_token_api: bool = False,
        beneficiary_mode: bool = False,
        disable_auto_refresh: bool = False,
        disable_auto_sync: bool = False,
        enable_call_masking: bool = False,
        register_enrol: bool = False,
    ) -> str:
        """Create a user in Avni with customizable settings for data entry or app access.

        Args:
            org_name: Organization name
            username: Username (without org suffix)
            name: Full name of the user
            email: Email address
            phone_number: Phone number
            catchment_id: Catchment ID (optional)
            group_ids: List of group IDs (optional)
            track_location: Enable location tracking in Field App
            allow_token_api: Allow token generation API access
            beneficiary_mode: Enable beneficiary mode in Field App
            disable_auto_refresh: Disable dashboard auto-refresh
            disable_auto_sync: Disable auto-sync in Field App
            enable_call_masking: Enable call masking via Exotel
            register_enrol: Enable register and enrol flow
        """
        settings = {
            "locale": "en",
            "trackLocation": track_location,
            "isAllowedToInvokeTokenGenerationAPI": allow_token_api,
            "showBeneficiaryMode": beneficiary_mode,
            "disableAutoRefresh": disable_auto_refresh,
            "disableAutoSync": disable_auto_sync,
            "enableCallMasking": enable_call_masking,
            "registerEnrol": register_enrol,
            "datePickerMode": "calendar",
            "timePickerMode": "clock",
        }

        payload = {
            "operatingIndividualScope": "ByCatchment" if catchment_id else "None",
            "username": f"{username}@{org_name.lower().replace(' ', '_')}",
            "ignored": username,
            "name": name,
            "email": email,
            "phoneNumber": phone_number,
            "catchmentId": catchment_id,
            "groupIds": group_ids or [],
            "settings": settings,
        }

        result = await make_avni_request(
            "POST", "/user", payload
        )

        if not result.success:
            return result.format_error("create user")

        return f"User '{username}' created successfully with ID {result.data.get('id')}"

    @mcp.tool()
    async def create_user_group(name: str) -> str:
        """Create a user group in Avni for assigning roles to users.

        Args:
            name: Name of the user group
        """
        payload = {"name": name}

        result = await make_avni_request(
            "POST", "/web/groups", payload
        )

        if not result.success:
            return result.format_error("create user group")

        return format_creation_response("User group", name, "id", result.data)
