from src.clients import make_avni_request
from src.utils.format_utils import format_creation_response
from src.core import tool_registry

async def create_program(auth_token: str, name: str, subject_type_uuid: str) -> str:
    """Create a program in Avni for managing data collection activities.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the program
        subject_type_uuid: Subject type UUID
    """
    payload = {
        "name": name,
        "colour": "#611717",
        "programSubjectLabel": name.lower().replace(" ", "_"),
        "enrolmentSummaryRule": "",
        "subjectTypeUuid": subject_type_uuid,
        "enrolmentEligibilityCheckRule": "",
        "enrolmentEligibilityCheckDeclarativeRule": None,
        "manualEligibilityCheckRequired": False,
        "showGrowthChart": False,
        "allowMultipleEnrolments": True,
        "manualEnrolmentEligibilityCheckRule": "",
    }

    result = await make_avni_request("POST", "/web/program", auth_token, payload)

    if not result.success:
        return result.format_error("create program")

    return format_creation_response("Program", name, "uuid", result.data)

def register_program_tools() -> None:
    tool_registry.register_tool(create_program)
