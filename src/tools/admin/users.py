import logging
from src.clients import make_avni_request
from src.utils.session_context import log_payload
from src.schemas.user_contract import UserFindContract, UserUpdateContract
from src.schemas.field_names import UserFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def find_user(auth_token: str, contract: UserFindContract) -> str:
    """Find a user by name using the search endpoint.

    Args:
        auth_token: Authentication token for Avni API
        contract: UserFindContract with name to search for
    """
    # Construct the endpoint with a query parameter
    endpoint = f"/user/search/find?name={contract.name}"

    # Log the search operation
    log_payload("User SEARCH endpoint:", endpoint)

    result = await make_avni_request("GET", endpoint, auth_token)

    if not result.success:
        return result.format_error("search for user")

    if not result.data:
        return result.format_empty("users")

    return f"Found user: {result.data}"


async def update_user(auth_token: str, contract: UserUpdateContract) -> str:
    """Update an existing user in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: UserUpdateContract with user update details
    """
    payload = {
        UserFields.ID.value: contract.id,
        UserFields.NAME.value: contract.name,
        UserFields.USERNAME.value: contract.username,
        UserFields.PHONE_NUMBER.value: contract.phoneNumber,
        UserFields.EMAIL.value: contract.email,
        UserFields.ORGANISATION_ID.value: contract.organisationId,
        UserFields.CATCHMENT_ID.value: contract.catchmentId,
    }

    # Log the actual API payload
    log_payload("User UPDATE payload:", payload)

    result = await make_avni_request("PUT", f"/user/{contract.id}", auth_token, payload)

    if not result.success:
        return result.format_error("update user")

    return f"User {contract.name} (ID: {contract.id}) successfully updated"


def register_user_tools() -> None:
    tool_registry.register_tool(find_user)
    tool_registry.register_tool(update_user)
