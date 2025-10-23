"""
Specific validator for test-config-update.json structure.
This validator knows exactly what should be in the test update configuration.
"""

import logging
from typing import Dict, Any, List
from .validation_result import ValidationResult

logger = logging.getLogger(__name__)


class TestConfigUpdateValidator:
    """Validates the specific structure expected in test-config-update.json"""

    @staticmethod
    def validate_test_update_config(config: Dict[str, Any]) -> ValidationResult:
        """
        Validate that the generated config matches test-config-update.json structure exactly.

        Returns:
            ValidationResult with validation status and any errors
        """
        if not isinstance(config, dict):
            return ValidationResult.failure(["Config must be a dictionary"])

        if "update" not in config:
            return ValidationResult.failure(["Config must have 'update' key"])

        update_config = config["update"]
        if not isinstance(update_config, dict):
            return ValidationResult.failure(["'update' must be a dictionary"])

        result = ValidationResult.success()

        # Validate address level types - expecting exactly 3 updated ones
        result.add_errors(
            TestConfigUpdateValidator._validate_updated_address_level_types(
                update_config
            )
        )

        # Validate locations - expecting exactly 3 updated ones
        result.add_errors(
            TestConfigUpdateValidator._validate_updated_locations(update_config)
        )

        # Validate catchments - expecting exactly 2 updated ones
        result.add_errors(
            TestConfigUpdateValidator._validate_updated_catchments(update_config)
        )

        # Validate subject types - expecting exactly 2 updated ones
        result.add_errors(
            TestConfigUpdateValidator._validate_updated_subject_types(update_config)
        )

        # Validate programs - expecting exactly 2 updated ones
        result.add_errors(
            TestConfigUpdateValidator._validate_updated_programs(update_config)
        )

        # Validate encounter types - expecting exactly 3 updated ones
        result.add_errors(
            TestConfigUpdateValidator._validate_updated_encounter_types(update_config)
        )

        return result

    @staticmethod
    def _validate_updated_address_level_types(
        update_config: Dict[str, Any],
    ) -> List[str]:
        """Validate specific updated address level types"""
        errors = []

        if "addressLevelTypes" not in update_config:
            return ["Missing 'addressLevelTypes' section"]

        addr_types = update_config["addressLevelTypes"]
        if not isinstance(addr_types, list):
            return ["'addressLevelTypes' must be a list"]

        if len(addr_types) != 3:
            errors.append(
                f"Expected exactly 3 updated addressLevelTypes, got {len(addr_types)}"
            )
            return errors

        # Expected updated structure:
        expected_types = [
            {"name": "Updated State", "level": 3.0, "parentId": None},
            {
                "name": "Updated District",
                "level": 2.0,
                "parentId": "id of Updated State",
            },
            {
                "name": "Updated Block",
                "level": 1.0,
                "parentId": "id of Updated District",
            },
        ]

        for i, (actual, expected) in enumerate(zip(addr_types, expected_types)):
            if actual.get("name") != expected["name"]:
                errors.append(
                    f"addressLevelTypes[{i}] name should be '{expected['name']}', got '{actual.get('name')}'"
                )

            if actual.get("level") != expected["level"]:
                errors.append(
                    f"addressLevelTypes[{i}] level should be {expected['level']}, got {actual.get('level')}"
                )

            if actual.get("parentId") != expected["parentId"]:
                errors.append(
                    f"addressLevelTypes[{i}] parentId should be {expected['parentId']}, got {actual.get('parentId')}"
                )

        return errors

    @staticmethod
    def _validate_updated_locations(update_config: Dict[str, Any]) -> List[str]:
        """Validate specific updated locations"""
        errors = []

        if "locations" not in update_config:
            return ["Missing 'locations' section"]

        locations = update_config["locations"]
        if not isinstance(locations, list):
            return ["'locations' must be a list"]

        if len(locations) != 3:
            errors.append(f"Expected exactly 3 updated locations, got {len(locations)}")
            return errors

        # Expected updated structure - note the different field structure for updates
        expected_locations = [
            {"title": "Updated Karnataka", "level": 3, "parentId": None},
            {
                "title": "Updated Bangalore",
                "level": 2,
                "parentId": "id of Updated Karnataka",
            },
            {
                "title": "Updated Electronic City",
                "level": 1,
                "parentId": "id of Updated Bangalore",
            },
        ]

        for i, (actual, expected) in enumerate(zip(locations, expected_locations)):
            if actual.get("title") != expected["title"]:
                errors.append(
                    f"locations[{i}] title should be '{expected['title']}', got '{actual.get('title')}'"
                )

            if actual.get("level") != expected["level"]:
                errors.append(
                    f"locations[{i}] level should be {expected['level']}, got {actual.get('level')}"
                )

            if actual.get("parentId") != expected["parentId"]:
                errors.append(
                    f"locations[{i}] parentId should be {expected['parentId']}, got '{actual.get('parentId')}'"
                )

        return errors

    @staticmethod
    def _validate_updated_catchments(update_config: Dict[str, Any]) -> List[str]:
        """Validate specific updated catchments"""
        errors = []

        if "catchments" not in update_config:
            return ["Missing 'catchments' section"]

        catchments = update_config["catchments"]
        if not isinstance(catchments, list):
            return ["'catchments' must be a list"]

        if len(catchments) != 2:
            errors.append(
                f"Expected exactly 2 updated catchments, got {len(catchments)}"
            )
            return errors

        # Expected updated structure:
        expected_catchments = [
            {"name": "Updated Urban Catchment", "deleteFastSync": False},
            {"name": "Updated Rural Catchment", "deleteFastSync": False},
        ]

        for i, (actual, expected) in enumerate(zip(catchments, expected_catchments)):
            if actual.get("name") != expected["name"]:
                errors.append(
                    f"catchments[{i}] name should be '{expected['name']}', got '{actual.get('name')}'"
                )

            if actual.get("deleteFastSync") != expected["deleteFastSync"]:
                errors.append(
                    f"catchments[{i}] deleteFastSync should be {expected['deleteFastSync']}"
                )

        return errors

    @staticmethod
    def _validate_updated_subject_types(update_config: Dict[str, Any]) -> List[str]:
        """Validate specific updated subject types"""
        errors = []

        if "subjectTypes" not in update_config:
            return ["Missing 'subjectTypes' section"]

        subject_types = update_config["subjectTypes"]
        if not isinstance(subject_types, list):
            return ["'subjectTypes' must be a list"]

        if len(subject_types) != 2:
            errors.append(
                f"Expected exactly 2 updated subjectTypes, got {len(subject_types)}"
            )
            return errors

        # Find Updated Individual and Household subject types
        individual_st = None
        household_st = None

        for st in subject_types:
            if st.get("name") == "Updated Individual":
                individual_st = st
            elif st.get("name") == "Updated Household":
                household_st = st

        # Validate Updated Individual
        if individual_st is None:
            errors.append("Missing 'Updated Individual' subject type")
        else:
            # Check for updated properties - only validate what we requested
            if (
                individual_st.get("allowMiddleName") is not True
            ):  # Changed from false to true
                errors.append(
                    "Updated Individual allowMiddleName should be true (updated)"
                )
            # Don't validate allowProfilePicture or enableApproval - we didn't request these changes

        # Validate Updated Household
        if household_st is None:
            errors.append("Missing 'Updated Household' subject type")
        else:
            # Only validate basic rename - we didn't request specific property changes for Household
            # Don't validate allowProfilePicture, displayPlannedEncounters, enableApproval, or group roles
            pass

        return errors

    @staticmethod
    def _validate_updated_programs(update_config: Dict[str, Any]) -> List[str]:
        """Validate specific updated programs"""
        errors = []

        if "programs" not in update_config:
            return ["Missing 'programs' section"]

        programs = update_config["programs"]
        if not isinstance(programs, list):
            return ["'programs' must be a list"]

        if len(programs) != 2:
            errors.append(f"Expected exactly 2 updated programs, got {len(programs)}")
            return errors

        # Find programs by name
        health_program = None
        family_program = None

        for prog in programs:
            if prog.get("name") == "Updated Health Program":
                health_program = prog
            elif prog.get("name") == "Updated Family Welfare":
                family_program = prog

        if health_program is None:
            errors.append("Missing 'Updated Health Program'")
        else:
            # Only validate changes we explicitly requested
            if (
                health_program.get("colour") != "#FF9800"
            ):  # Changed color - we requested this
                errors.append(
                    "Updated Health Program colour should be '#FF9800' (updated)"
                )
            if (
                health_program.get("allowMultipleEnrolments") is not True
            ):  # Changed to true - we requested this
                errors.append(
                    "Updated Health Program allowMultipleEnrolments should be true (updated)"
                )
            # Don't validate manualEligibilityCheckRequired - we didn't request this change

        if family_program is None:
            errors.append("Missing 'Updated Family Welfare'")
        else:
            # Only validate changes we explicitly requested
            if (
                family_program.get("colour") != "#9C27B0"
            ):  # Changed color - we requested this
                errors.append(
                    "Updated Family Welfare colour should be '#9C27B0' (updated)"
                )
            # Don't validate showGrowthChart or allowMultipleEnrolments - we didn't request these changes

        return errors

    @staticmethod
    def _validate_updated_encounter_types(update_config: Dict[str, Any]) -> List[str]:
        """Validate specific updated encounter types"""
        errors = []

        if "encounterTypes" not in update_config:
            return ["Missing 'encounterTypes' section"]

        encounter_types = update_config["encounterTypes"]
        if not isinstance(encounter_types, list):
            return ["'encounterTypes' must be a list"]

        if len(encounter_types) != 3:
            errors.append(
                f"Expected exactly 3 updated encounterTypes, got {len(encounter_types)}"
            )
            return errors

        # Find encounters by name
        registration_enc = None
        health_checkup_enc = None
        family_survey_enc = None

        for enc in encounter_types:
            if enc.get("name") == "Updated Registration":
                registration_enc = enc
            elif enc.get("name") == "Updated Health Checkup":
                health_checkup_enc = enc
            elif enc.get("name") == "Updated Family Survey":
                family_survey_enc = enc

        if registration_enc is None:
            errors.append("Missing 'Updated Registration' encounter type")
        else:
            if registration_enc.get("isImmutable") is not True:  # Changed to true
                errors.append(
                    "Updated Registration isImmutable should be true (updated)"
                )

        if health_checkup_enc is None:
            errors.append("Missing 'Updated Health Checkup' encounter type")

        if family_survey_enc is None:
            errors.append("Missing 'Updated Family Survey' encounter type")

        return errors
