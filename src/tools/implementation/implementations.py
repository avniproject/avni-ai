import logging
from src.clients import AvniClient
from src.utils.result_utils import (
    format_error_message,
    format_implementation_deletion_response,
)
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def delete_implementation(auth_token: str) -> str:
    query_params = "deleteMetadata=true&deleteAdminConfig=true"
    
    result = await AvniClient().call_avni_server(
        "DELETE", f"/implementation/delete?{query_params}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete implementation")

    return format_implementation_deletion_response()


def register_implementation_tools() -> None:
    tool_registry.register_tool(delete_implementation)