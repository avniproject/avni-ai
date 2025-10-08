from src.clients import make_avni_request
from src.utils.format_utils import format_creation_response
from src.core import tool_registry

async def create_encounter_type(
    auth_token: str, name: str, subject_type_uuid: str, program_uuid: str
) -> str:
    """Create an encounter type for a program and subject type in Avni.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the encounter type
        subject_type_uuid: Subject type UUID
        program_uuid: Program UUID
    """
    payload = {
        "name": name,
        "encounterEligibilityCheckRule": name,
        "loaded": True,
        "subjectTypeUuid": subject_type_uuid,
        "programUuid": program_uuid,
    }

    result = await make_avni_request(
        "POST", "/web/encounterType", auth_token, payload
    )

    if not result.success:
        return result.format_error("create encounter type")

    return format_creation_response("Encounter type", name, "uuid", result.data)


def register_encounter_tools() -> None:
    tool_registry.register_tool(create_encounter_type)
