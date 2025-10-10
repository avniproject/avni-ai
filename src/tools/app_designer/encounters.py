import logging
from src.clients import make_avni_request
from src.utils.format_utils import format_creation_response
from src.utils.session_context import log_payload
from src.schemas.encounter_type_contract import (
    EncounterTypeContract,
    EncounterTypeUpdateContract,
    EncounterTypeDeleteContract,
)
from src.schemas.field_names import EncounterTypeFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


def add_non_empty_field(payload: dict, field_name: str, value) -> None:
    """Add a field to payload only if the value is not None and not empty string.

    This is specifically useful for optional fields like programUuid where empty
    strings should be treated as "not provided" and excluded from the payload.

    Args:
        payload: Dictionary to add the field to
        field_name: Name of the field to add
        value: Value to check and potentially add
    """
    if value is not None and value != "":
        payload[field_name] = value


async def create_encounter_type(
    auth_token: str, contract: EncounterTypeContract
) -> str:
    """Create an encounter type for a program and subject type in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: EncounterTypeContract with encounter type details
    """
    payload = {
        EncounterTypeFields.NAME.value: contract.name,
        EncounterTypeFields.UUID.value: contract.uuid,
        EncounterTypeFields.SUBJECT_TYPE_UUID.value: contract.subjectTypeUuid,
        EncounterTypeFields.ACTIVE.value: contract.active,
        EncounterTypeFields.VOIDED.value: contract.voided,
        EncounterTypeFields.IS_IMMUTABLE.value: contract.isImmutable,
    }

    # Only include programUuid if it's provided, not None, and not empty string
    add_non_empty_field(
        payload, EncounterTypeFields.PROGRAM_UUID.value, contract.programUuid
    )

    # Add optional fields only if they are not None
    if contract.entityEligibilityCheckRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_RULE.value] = (
            contract.entityEligibilityCheckRule
        )
    if contract.entityEligibilityCheckDeclarativeRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value] = (
            contract.entityEligibilityCheckDeclarativeRule
        )

    # Log the actual API payload to both standard and session loggers
    log_payload("EncounterType CREATE payload:", payload)

    result = await make_avni_request("POST", "/web/encounterType", auth_token, payload)

    if not result.success:
        return result.format_error("create encounter type")

    return format_creation_response(
        "Encounter type", contract.name, "uuid", result.data
    )


async def update_encounter_type(
    auth_token: str, contract: EncounterTypeUpdateContract
) -> str:
    """Update an existing encounter type in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: EncounterTypeUpdateContract with update details
    """
    payload = {
        EncounterTypeFields.NAME.value: contract.name,
        EncounterTypeFields.SUBJECT_TYPE_UUID.value: contract.subjectTypeUuid,
        EncounterTypeFields.ACTIVE.value: contract.active,
        EncounterTypeFields.VOIDED.value: contract.voided,
        EncounterTypeFields.IS_IMMUTABLE.value: contract.isImmutable,
    }

    # Only include programUuid if it's provided, not None, and not empty string
    add_non_empty_field(
        payload, EncounterTypeFields.PROGRAM_UUID.value, contract.programUuid
    )

    # Add optional fields only if they are not None
    if contract.entityEligibilityCheckRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_RULE.value] = (
            contract.entityEligibilityCheckRule
        )
    if contract.entityEligibilityCheckDeclarativeRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value] = (
            contract.entityEligibilityCheckDeclarativeRule
        )

    # Log the actual API payload to both standard and session loggers
    log_payload("EncounterType UPDATE payload:", payload)

    result = await make_avni_request(
        "PUT", f"/web/encounterType/{contract.id}", auth_token, payload
    )

    if not result.success:
        return result.format_error("update encounter type")

    return format_creation_response("Encounter type", contract.name, "id", result.data)


async def delete_encounter_type(
    auth_token: str, contract: EncounterTypeDeleteContract
) -> str:
    """Delete (void) an existing encounter type in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: EncounterTypeDeleteContract with ID to delete
    """
    # Log the delete operation
    logger.info(f"EncounterType DELETE: ID {contract.id}")

    result = await make_avni_request(
        "DELETE", f"/web/encounterType/{contract.id}", auth_token
    )

    if not result.success:
        return result.format_error("delete encounter type")

    return f"Encounter type with ID {contract.id} successfully deleted (voided)"


def register_encounter_tools() -> None:
    tool_registry.register_tool(create_encounter_type)
    tool_registry.register_tool(update_encounter_type)
    tool_registry.register_tool(delete_encounter_type)
