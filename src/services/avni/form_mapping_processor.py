import logging
from typing import Dict, Any, List, Optional

from ...clients.avni_client import AvniClient

logger = logging.getLogger(__name__)


class FormMappingProcessor:
    # TODO: Use proper objects instead of subject_type_uuid etc

    @staticmethod
    def find_registration_form_uuid(
        form_mappings: List[Dict], subject_type_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType") == "IndividualProfile"
                and not mapping.get("isVoided", False)
                and mapping.get("subjectTypeUUID") == subject_type_uuid
            ):
                return mapping.get("formUUID")
        return None

    @staticmethod
    def find_program_enrolment_form_uuid(
        form_mappings: List[Dict], program_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType") == "ProgramEnrolment"
                and not mapping.get("isVoided", False)
                and mapping.get("programUUID") == program_uuid
            ):
                return mapping.get("formUUID")
        return None

    @staticmethod
    def find_program_exit_form_uuid(
        form_mappings: List[Dict], program_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType") == "ProgramExit"
                and not mapping.get("isVoided", False)
                and mapping.get("programUUID") == program_uuid
            ):
                return mapping.get("formUUID")
        return None

    @staticmethod
    def find_program_encounter_form_uuid(
        form_mappings: List[Dict], encounter_type_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType") in ["ProgramEncounter", "Encounter"]
                and not mapping.get("isVoided", False)
                and mapping.get("encounterTypeUUID") == encounter_type_uuid
            ):
                return mapping.get("formUUID")
        return None

    @staticmethod
    def find_program_encounter_cancellation_form_uuid(
        form_mappings: List[Dict], encounter_type_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType")
                in ["ProgramEncounterCancellation", "IndividualEncounterCancellation"]
                and not mapping.get("isVoided", False)
                and mapping.get("encounterTypeUUID") == encounter_type_uuid
            ):
                return mapping.get("formUUID")
        return None

    @staticmethod
    def find_program_uuid_for_encounter_type(
        form_mappings: List[Dict], encounter_type_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType") == "ProgramEncounter"
                and not mapping.get("isVoided", False)
                and mapping.get("encounterTypeUUID") == encounter_type_uuid
            ):
                return mapping.get("programUUID")
        return None

    @staticmethod
    def find_subject_type_uuid_for_encounter_type(
        form_mappings: List[Dict], encounter_type_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType") in ["ProgramEncounter", "Encounter"]
                and not mapping.get("isVoided", False)
                and mapping.get("encounterTypeUUID") == encounter_type_uuid
            ):
                return mapping.get("subjectTypeUUID")
        return None

    @staticmethod
    def find_subject_type_uuid_for_program(
        form_mappings: List[Dict], program_uuid: str
    ) -> Optional[str]:
        for mapping in form_mappings:
            if (
                mapping.get("formType") == "ProgramEnrolment"
                and not mapping.get("isVoided", False)
                and mapping.get("programUUID") == program_uuid
            ):
                return mapping.get("subjectTypeUUID")
        return None

    @staticmethod
    def process_subject_types(
        subject_types: List[Dict], form_mappings: List[Dict]
    ) -> List[Dict]:
        processed_subject_types = []

        for subject_type in subject_types:
            processed_subject_type = subject_type.copy()

            # Only update if registrationFormUuid is null/None
            if not processed_subject_type.get("registrationFormUuid"):
                subject_type_uuid = processed_subject_type.get("uuid")
                if subject_type_uuid:
                    form_uuid = FormMappingProcessor.find_registration_form_uuid(
                        form_mappings, subject_type_uuid
                    )
                    if form_uuid:
                        processed_subject_type["registrationFormUuid"] = form_uuid
                        logger.info(
                            f"Updated subject type '{processed_subject_type.get('name')}' "
                            f"with registration form UUID: {form_uuid}"
                        )

            processed_subject_types.append(processed_subject_type)

        return processed_subject_types

    @staticmethod
    def process_programs(programs: List[Dict], form_mappings: List[Dict]) -> List[Dict]:
        processed_programs = []

        for program in programs:
            processed_program = program.copy()
            program_uuid = processed_program.get("uuid")

            if program_uuid:
                # Update program enrolment form UUID if null
                if not processed_program.get("programEnrolmentFormUuid"):
                    enrolment_form_uuid = (
                        FormMappingProcessor.find_program_enrolment_form_uuid(
                            form_mappings, program_uuid
                        )
                    )
                    if enrolment_form_uuid:
                        processed_program["programEnrolmentFormUuid"] = (
                            enrolment_form_uuid
                        )
                        logger.info(
                            f"Updated program '{processed_program.get('name')}' "
                            f"with enrolment form UUID: {enrolment_form_uuid}"
                        )

                # Update program exit form UUID if null
                if not processed_program.get("programExitFormUuid"):
                    exit_form_uuid = FormMappingProcessor.find_program_exit_form_uuid(
                        form_mappings, program_uuid
                    )
                    if exit_form_uuid:
                        processed_program["programExitFormUuid"] = exit_form_uuid
                        logger.info(
                            f"Updated program '{processed_program.get('name')}' "
                            f"with exit form UUID: {exit_form_uuid}"
                        )

                # Update subject type UUID if null
                if not processed_program.get("subjectTypeUuid"):
                    subject_type_uuid = (
                        FormMappingProcessor.find_subject_type_uuid_for_program(
                            form_mappings, program_uuid
                        )
                    )
                    if subject_type_uuid:
                        processed_program["subjectTypeUuid"] = subject_type_uuid
                        logger.info(
                            f"Updated program '{processed_program.get('name')}' "
                            f"with subject type UUID: {subject_type_uuid}"
                        )

            processed_programs.append(processed_program)

        return processed_programs

    @staticmethod
    def process_encounter_types(
        encounter_types: List[Dict], form_mappings: List[Dict]
    ) -> List[Dict]:
        processed_encounter_types = []

        for encounter_type in encounter_types:
            processed_encounter_type = encounter_type.copy()
            encounter_type_uuid = processed_encounter_type.get("uuid")

            if encounter_type_uuid:
                # Update program encounter form UUID if null
                if not processed_encounter_type.get("programEncounterFormUuid"):
                    encounter_form_uuid = (
                        FormMappingProcessor.find_program_encounter_form_uuid(
                            form_mappings, encounter_type_uuid
                        )
                    )
                    if encounter_form_uuid:
                        processed_encounter_type["programEncounterFormUuid"] = (
                            encounter_form_uuid
                        )
                        logger.info(
                            f"Updated encounter type '{processed_encounter_type.get('name')}' "
                            f"with encounter form UUID: {encounter_form_uuid}"
                        )

                # Update program encounter cancellation form UUID if null
                if not processed_encounter_type.get("programEncounterCancelFormUuid"):
                    cancellation_form_uuid = FormMappingProcessor.find_program_encounter_cancellation_form_uuid(
                        form_mappings, encounter_type_uuid
                    )
                    if cancellation_form_uuid:
                        processed_encounter_type["programEncounterCancelFormUuid"] = (
                            cancellation_form_uuid
                        )
                        logger.info(
                            f"Updated encounter type '{processed_encounter_type.get('name')}' "
                            f"with cancellation form UUID: {cancellation_form_uuid}"
                        )

                # Update program UUID if null
                if not processed_encounter_type.get("programUuid"):
                    program_uuid = (
                        FormMappingProcessor.find_program_uuid_for_encounter_type(
                            form_mappings, encounter_type_uuid
                        )
                    )
                    if program_uuid:
                        processed_encounter_type["programUuid"] = program_uuid
                        logger.info(
                            f"Updated encounter type '{processed_encounter_type.get('name')}' "
                            f"with program UUID: {program_uuid}"
                        )

                # Update subject type UUID if null
                if not processed_encounter_type.get("subjectTypeUuid"):
                    subject_type_uuid = (
                        FormMappingProcessor.find_subject_type_uuid_for_encounter_type(
                            form_mappings, encounter_type_uuid
                        )
                    )
                    if subject_type_uuid:
                        processed_encounter_type["subjectTypeUuid"] = subject_type_uuid
                        logger.info(
                            f"Updated encounter type '{processed_encounter_type.get('name')}' "
                            f"with subject type UUID: {subject_type_uuid}"
                        )

            processed_encounter_types.append(processed_encounter_type)

        return processed_encounter_types

    @staticmethod
    async def enrich_config_with_form_mappings(
        config: Dict[str, Any],
        auth_token: str,
        session_logger: logging.Logger,
    ) -> Dict[str, Any]:
        """
        Main method to enrich configuration data with form mapping information.

        Args:
            config: The complete existing configuration
            auth_token: Authentication token
            session_logger: Logger for session-specific logging

        Returns:
            Enriched configuration with form mappings applied
        """
        try:
            session_logger.info(
                "STEP 2.1: Fetching operational modules for form mappings"
            )
            session_logger.info(
                f"Config type: {type(config)}, Config keys: {config.keys() if isinstance(config, dict) else 'N/A'}"
            )

            # Validate input config is a dictionary
            if not isinstance(config, dict):
                session_logger.error(
                    f"Expected config to be a dictionary, got {type(config)}"
                )
                return config

            # Initialize AvniClient for form mapping operations
            avni_client = AvniClient()

            # Fetch operational modules to get form mappings
            result = await avni_client.call_avni_server(
                "GET", "/web/operationalModules", auth_token
            )

            if not result.success:
                session_logger.error(
                    f"Failed to fetch operational modules: {result.error}"
                )
                # Return original config if we can't fetch form mappings
                return config

            operational_modules = result.data or {}
            form_mappings = operational_modules.get("formMappings", [])

            session_logger.info(f"Found {len(form_mappings)} form mappings")

            if not form_mappings:
                session_logger.warning(
                    "No form mappings found, returning original config"
                )
                return config

            # Create enriched copy of config
            enriched_config = config.copy()

            # Process subject types
            subject_types_data = enriched_config.get("subjectTypes", {})
            if (
                "_embedded" in subject_types_data
                and "subjectType" in subject_types_data["_embedded"]
            ):
                session_logger.info("Processing subject types with form mappings")
                processed_subject_types = FormMappingProcessor.process_subject_types(
                    subject_types_data["_embedded"]["subjectType"], form_mappings
                )
                enriched_config["subjectTypes"]["_embedded"]["subjectType"] = (
                    processed_subject_types
                )

            # Process programs
            programs_data = enriched_config.get("programs", {})
            if "_embedded" in programs_data and "program" in programs_data["_embedded"]:
                session_logger.info("Processing programs with form mappings")
                processed_programs = FormMappingProcessor.process_programs(
                    programs_data["_embedded"]["program"], form_mappings
                )
                enriched_config["programs"]["_embedded"]["program"] = processed_programs

            # Process encounter types
            encounter_types_data = enriched_config.get("encounterTypes", {})
            if (
                "_embedded" in encounter_types_data
                and "encounterType" in encounter_types_data["_embedded"]
            ):
                session_logger.info("Processing encounter types with form mappings")
                processed_encounter_types = (
                    FormMappingProcessor.process_encounter_types(
                        encounter_types_data["_embedded"]["encounterType"],
                        form_mappings,
                    )
                )
                enriched_config["encounterTypes"]["_embedded"]["encounterType"] = (
                    processed_encounter_types
                )

            session_logger.info(
                "Successfully enriched configuration with form mappings"
            )
            return enriched_config

        except Exception as e:
            session_logger.error(f"Error enriching config with form mappings: {str(e)}")
            logger.error(f"Error enriching config with form mappings: {str(e)}")
            # Return original config on error to prevent breaking the pipeline
            return config
