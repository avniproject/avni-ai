"""Tests for result utility functions."""

from src.clients.avni_client import ApiResult
from src.utils.result_utils import (
    format_error_message, 
    format_empty_message, 
    format_list_response,
    format_creation_response,
    format_update_response,
    format_deletion_response,
    format_validation_error,
)


class TestResultUtils:
    """Test result formatting utility functions."""

    def test_format_error_message(self):
        """Test error message formatting."""
        result = ApiResult.error_result("API key invalid")
        formatted = format_error_message(result, "create organization")

        assert formatted == "Failed to create organization: API key invalid"

    def test_format_empty_message(self):
        """Test empty result message formatting."""
        formatted = format_empty_message("location types")
        assert formatted == "No location types found."

    def test_format_update_response(self):
        """Test update response formatting."""
        data = {"id": 789}
        result = format_update_response("Location", "Test Location", "id", data)
        expected = "Location 'Test Location' updated successfully with ID 789"
        assert result == expected

    def test_format_list_response_basic(self):
        """Test basic list response formatting."""
        items = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]

        result = format_list_response(items)
        expected = "ID: 1, Name: Item 1\nID: 2, Name: Item 2"
        assert result == expected

    def test_format_list_response_with_extra_key(self):
        """Test list response formatting with extra key."""
        items = [
            {"id": 1, "name": "State", "level": 3.0},
            {"id": 2, "name": "District", "level": 2.0}
        ]

        result = format_list_response(items, extra_key="level")
        expected = "ID: 1, Name: State, Level: 3.0\nID: 2, Name: District, Level: 2.0"
        assert result == expected

    def test_format_list_response_empty_list(self):
        """Test formatting empty list."""
        result = format_list_response([])
        assert result == "No items found."

    def test_format_creation_response(self):
        """Test creation response formatting."""
        data = {"id": 123}
        result = format_creation_response("Organization", "Test Org", "id", data)

        expected = "Organization 'Test Org' created successfully with ID 123"
        assert result == expected

    def test_format_deletion_response(self):
        """Test deletion response formatting."""
        result = format_deletion_response("Catchment", 456)
        expected = "Catchment with ID 456 successfully deleted (voided)"
        assert result == expected

    def test_format_validation_error(self):
        """Test validation error formatting."""
        result = format_validation_error("create location type", "Invalid parentId '0': Cannot be zero")
        expected = "Failed to create location type: Invalid parentId '0': Cannot be zero"
        assert result == expected