import logging
from src.clients import AvniClient
from src.utils.session_context import log_payload
from src.utils.result_utils import (
    format_error_message,
    format_empty_message,
    format_update_response,
)
from src.schemas.user_contract import UserFindContract, UserUpdateContract
from src.schemas.field_names import UserFields
from src.services import tool_registry

logger = logging.getLogger(__name__)


async def find_user(auth_token: str, contract: UserFindContract) -> str:
    result = await AvniClient().call_avni_server(
        "GET", f"/user/search/find?name={contract.name}", auth_token
    )

    if not result.success:
        return format_error_message(result, "search for user")

    if not result.data:
        return format_empty_message("users")

    return f"Found user: {result.data}"


async def update_user(auth_token: str, contract: UserUpdateContract) -> str:
    payload = {
        UserFields.ID.value: contract.id,
        UserFields.NAME.value: contract.name,
        UserFields.USERNAME.value: contract.username,
        UserFields.PHONE_NUMBER.value: contract.phoneNumber,
        UserFields.EMAIL.value: contract.email,
        UserFields.ORGANISATION_ID.value: contract.organisationId,
        UserFields.CATCHMENT_ID.value: contract.catchmentId,
    }

    log_payload("User UPDATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "PUT", f"/user/{contract.id}", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "update user")

    return format_update_response(
        "User", contract.name, UserFields.ID.value, {"id": contract.id}
    )


def register_user_tools() -> None:
    tool_registry.register_tool(find_user)
    tool_registry.register_tool(update_user)
