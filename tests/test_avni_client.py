"""Tests for Avni client functionality."""

from src.clients.avni_client import ApiResult


class TestApiResult:
    """Test ApiResult data class."""

    def test_success_result_creation(self):
        """Test creating successful ApiResult."""
        data = {"id": 1, "name": "test"}
        result = ApiResult.success_result(data)

        assert result.success is True
        assert result.data == data
        assert result.error is None

    def test_error_result_creation(self):
        """Test creating error ApiResult."""
        error_msg = "Something went wrong"
        result = ApiResult.error_result(error_msg)

        assert result.success is False
        assert result.data is None
        assert result.error == error_msg