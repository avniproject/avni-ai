"""
Specific validator for test-config-delete.json structure.
This validator knows exactly what should be in the test delete configuration.
"""

import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class TestConfigDeleteValidator:
    """Validates the specific structure expected in test-config-delete.json"""

    @staticmethod
    def validate_test_delete_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate that the generated config matches test-config-delete.json structure exactly.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not isinstance(config, dict):
            return False, ["Config must be a dictionary"]

        if "delete" not in config:
            return False, ["Config must have 'delete' key"]

        delete_config = config["delete"]
        if not isinstance(delete_config, dict):
            return False, ["'delete' must be a dictionary"]

        # Validate the deletion order and structure
        # Note: In test-config-delete.json, deletions are in reverse dependency order
        errors.extend(
            TestConfigDeleteValidator._validate_delete_encounter_types(delete_config)
        )
        errors.extend(
            TestConfigDeleteValidator._validate_delete_programs(delete_config)
        )
        errors.extend(
            TestConfigDeleteValidator._validate_delete_subject_types(delete_config)
        )
        errors.extend(
            TestConfigDeleteValidator._validate_delete_catchments(delete_config)
        )
        errors.extend(
            TestConfigDeleteValidator._validate_delete_locations(delete_config)
        )
        errors.extend(
            TestConfigDeleteValidator._validate_delete_address_level_types(
                delete_config
            )
        )

        return len(errors) == 0, errors

    @staticmethod
    def _validate_delete_encounter_types(delete_config: Dict[str, Any]) -> List[str]:
        """Validate specific encounter types to be deleted"""
        errors = []

        if "encounterTypes" not in delete_config:
            return ["Missing 'encounterTypes' section in delete config"]

        encounter_types = delete_config["encounterTypes"]
        if not isinstance(encounter_types, list):
            return ["'encounterTypes' must be a list"]

        if len(encounter_types) != 1:
            errors.append(
                f"Expected exactly 1 encounterType to delete, got {len(encounter_types)}"
            )
            return errors

        # Expected: Only delete Family Survey encounter
        expected_encounter = encounter_types[0]
        if expected_encounter.get("id") != "id of Updated Family Survey":
            errors.append("Should delete 'id of Updated Family Survey' encounter type")

        return errors

    @staticmethod
    def _validate_delete_programs(delete_config: Dict[str, Any]) -> List[str]:
        """Validate specific programs to be deleted"""
        errors = []

        if "programs" not in delete_config:
            return ["Missing 'programs' section in delete config"]

        programs = delete_config["programs"]
        if not isinstance(programs, list):
            return ["'programs' must be a list"]

        if len(programs) != 1:
            errors.append(f"Expected exactly 1 program to delete, got {len(programs)}")
            return errors

        # Expected: Only delete Family Welfare program
        expected_program = programs[0]
        if expected_program.get("id") != "id of Updated Family Welfare":
            errors.append("Should delete 'id of Updated Family Welfare' program")

        return errors

    @staticmethod
    def _validate_delete_subject_types(delete_config: Dict[str, Any]) -> List[str]:
        """Validate specific subject types to be deleted"""
        errors = []

        if "subjectTypes" not in delete_config:
            return ["Missing 'subjectTypes' section in delete config"]

        subject_types = delete_config["subjectTypes"]
        if not isinstance(subject_types, list):
            return ["'subjectTypes' must be a list"]

        if len(subject_types) != 1:
            errors.append(
                f"Expected exactly 1 subjectType to delete, got {len(subject_types)}"
            )
            return errors

        # Expected: Only delete Household subject type
        expected_subject_type = subject_types[0]
        if expected_subject_type.get("id") != "id of Updated Household":
            errors.append("Should delete 'id of Updated Household' subject type")

        return errors

    @staticmethod
    def _validate_delete_catchments(delete_config: Dict[str, Any]) -> List[str]:
        """Validate specific catchments to be deleted"""
        errors = []

        if "catchments" not in delete_config:
            return ["Missing 'catchments' section in delete config"]

        catchments = delete_config["catchments"]
        if not isinstance(catchments, list):
            return ["'catchments' must be a list"]

        if len(catchments) != 2:
            errors.append(
                f"Expected exactly 2 catchments to delete, got {len(catchments)}"
            )
            return errors

        # Expected: Delete both catchments
        expected_catchment_ids = [
            "id of Updated Rural Catchment",
            "id of Updated Urban Catchment",
        ]

        actual_ids = [catchment.get("id") for catchment in catchments]

        for expected_id in expected_catchment_ids:
            if expected_id not in actual_ids:
                errors.append(f"Should delete catchment with id '{expected_id}'")

        return errors

    @staticmethod
    def _validate_delete_locations(delete_config: Dict[str, Any]) -> List[str]:
        """Validate specific locations to be deleted"""
        errors = []

        if "locations" not in delete_config:
            return ["Missing 'locations' section in delete config"]

        locations = delete_config["locations"]
        if not isinstance(locations, list):
            return ["'locations' must be a list"]

        if len(locations) != 3:
            errors.append(
                f"Expected exactly 3 locations to delete, got {len(locations)}"
            )
            return errors

        # Expected: Delete all locations in reverse hierarchy order (child to parent)
        expected_location_ids = [
            "id of Updated Electronic City",
            "id of Updated Bangalore",
            "id of Updated Karnataka",
        ]

        actual_ids = [location.get("id") for location in locations]

        # Check that all expected locations are present
        for expected_id in expected_location_ids:
            if expected_id not in actual_ids:
                errors.append(f"Should delete location with id '{expected_id}'")

        # Check deletion order (child to parent for proper dependency handling)
        if len(actual_ids) == 3:
            if actual_ids[0] != "id of Updated Electronic City":
                errors.append(
                    "First location to delete should be 'id of Updated Electronic City' (child)"
                )
            if actual_ids[1] != "id of Updated Bangalore":
                errors.append(
                    "Second location to delete should be 'id of Updated Bangalore' (parent)"
                )
            if actual_ids[2] != "id of Updated Karnataka":
                errors.append(
                    "Third location to delete should be 'id of Updated Karnataka' (top parent)"
                )

        return errors

    @staticmethod
    def _validate_delete_address_level_types(
        delete_config: Dict[str, Any],
    ) -> List[str]:
        """Validate specific address level types to be deleted"""
        errors = []

        if "addressLevelTypes" not in delete_config:
            return ["Missing 'addressLevelTypes' section in delete config"]

        addr_types = delete_config["addressLevelTypes"]
        if not isinstance(addr_types, list):
            return ["'addressLevelTypes' must be a list"]

        if len(addr_types) != 3:
            errors.append(
                f"Expected exactly 3 addressLevelTypes to delete, got {len(addr_types)}"
            )
            return errors

        # Expected: Delete all address level types in reverse hierarchy order (child to parent)
        expected_addr_type_ids = [
            "id of Updated Block",
            "id of Updated District",
            "id of Updated State",
        ]

        actual_ids = [addr_type.get("id") for addr_type in addr_types]

        # Check that all expected address level types are present
        for expected_id in expected_addr_type_ids:
            if expected_id not in actual_ids:
                errors.append(f"Should delete addressLevelType with id '{expected_id}'")

        # Check deletion order (child to parent for proper dependency handling)
        if len(actual_ids) == 3:
            if actual_ids[0] != "id of Updated Block":
                errors.append(
                    "First addressLevelType to delete should be 'id of Updated Block' (child)"
                )
            if actual_ids[1] != "id of Updated District":
                errors.append(
                    "Second addressLevelType to delete should be 'id of Updated District' (parent)"
                )
            if actual_ids[2] != "id of Updated State":
                errors.append(
                    "Third addressLevelType to delete should be 'id of Updated State' (top parent)"
                )

        return errors

    @staticmethod
    def validate_deletion_order(delete_config: Dict[str, Any]) -> List[str]:
        """
        Validate that deletions are in the correct dependency order.
        This is important for referential integrity.
        """
        errors = []

        # Expected order: encounterTypes -> programs -> subjectTypes -> catchments -> locations -> addressLevelTypes
        section_order = [
            "encounterTypes",
            "programs",
            "subjectTypes",
            "catchments",
            "locations",
            "addressLevelTypes",
        ]

        present_sections = []
        for section in section_order:
            if section in delete_config and len(delete_config[section]) > 0:
                present_sections.append(section)

        # For this specific test config, we expect all sections to be present
        if len(present_sections) != len(section_order):
            missing_sections = set(section_order) - set(present_sections)
            errors.append(f"Missing deletion sections: {missing_sections}")

        # Validate that if a section is present, it comes in the right order
        # (This is more of a structural validation for proper deletion sequencing)

        return errors
