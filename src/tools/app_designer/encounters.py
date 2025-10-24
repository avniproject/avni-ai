import logging
from src.clients import AvniClient
from src.utils.session_context import log_payload
from src.utils.result_utils import format_error_message, format_empty_message, format_creation_response, format_update_response, format_deletion_response
from src.schemas.encounter_type_contract import (
    EncounterTypeContract,
    EncounterTypeUpdateContract,
    EncounterTypeDeleteContract,
)
from src.schemas.field_names import EncounterTypeFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


def add_non_empty_field(payload: dict, field_name: str, value) -> None:
    if value is not None and value != "":
        payload[field_name] = value


async def create_encounter_type(
    auth_token: str, contract: EncounterTypeContract
) -> str:
    payload = {
        EncounterTypeFields.NAME.value: contract.name,
        EncounterTypeFields.UUID.value: contract.uuid,
        EncounterTypeFields.SUBJECT_TYPE_UUID.value: contract.subjectTypeUuid,
        EncounterTypeFields.ACTIVE.value: contract.active,
        EncounterTypeFields.VOIDED.value: contract.voided,
        EncounterTypeFields.IS_IMMUTABLE.value: contract.isImmutable,
    }

    add_non_empty_field(
        payload, EncounterTypeFields.PROGRAM_UUID.value, contract.programUuid
    )

    if contract.entityEligibilityCheckRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_RULE.value] = (
            contract.entityEligibilityCheckRule
        )
    if contract.entityEligibilityCheckDeclarativeRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value] = (
            contract.entityEligibilityCheckDeclarativeRule
        )

    log_payload("EncounterType CREATE payload:", payload)

    result = await AvniClient().call_avni_server("POST", "/web/encounterType", auth_token, payload)

    if not result.success:
        return format_error_message(result, "create encounter type")

    return format_creation_response(
        "Encounter type", contract.name, EncounterTypeFields.UUID.value, result.data
    )


async def update_encounter_type(
    auth_token: str, contract: EncounterTypeUpdateContract
) -> str:
    payload = {
        EncounterTypeFields.NAME.value: contract.name,
        EncounterTypeFields.SUBJECT_TYPE_UUID.value: contract.subjectTypeUuid,
        EncounterTypeFields.ACTIVE.value: contract.active,
        EncounterTypeFields.VOIDED.value: contract.voided,
        EncounterTypeFields.IS_IMMUTABLE.value: contract.isImmutable,
    }

    add_non_empty_field(
        payload, EncounterTypeFields.PROGRAM_UUID.value, contract.programUuid
    )

    if contract.entityEligibilityCheckRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_RULE.value] = (
            contract.entityEligibilityCheckRule
        )
    if contract.entityEligibilityCheckDeclarativeRule is not None:
        payload[EncounterTypeFields.ENTITY_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value] = (
            contract.entityEligibilityCheckDeclarativeRule
        )

    log_payload("EncounterType UPDATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "PUT", f"/web/encounterType/{contract.id}", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "update encounter type")

    return format_update_response("Encounter type", contract.name, EncounterTypeFields.ID.value, result.data)


async def delete_encounter_type(
    auth_token: str, contract: EncounterTypeDeleteContract
) -> str:
    result = await AvniClient().call_avni_server(
        "DELETE", f"/web/encounterType/{contract.id}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete encounter type")

    return format_deletion_response("Encounter type", contract.id)


def register_encounter_tools() -> None:
    tool_registry.register_tool(create_encounter_type)
    tool_registry.register_tool(update_encounter_type)
    tool_registry.register_tool(delete_encounter_type)
