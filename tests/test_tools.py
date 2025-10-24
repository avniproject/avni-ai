"""Tests for utility functions."""

# This file can be used for testing other utility functions in the future
# All formatting-related tests have been moved to test_result_utils.py


# @pytest.mark.asyncio
# class TestAvniClient:
#     """Test Avni API client functionality."""
#
#     @patch('avni_mcp_server.client.httpx.AsyncClient')
#     async def test_make_avni_request_success(self, mock_client):
#         """Test successful API request."""
#         # Mock response
#         mock_response = MagicMock()
#         mock_response.json.return_value = {"id": 1, "name": "test"}
#         mock_response.raise_for_status.return_value = None
#
#         # Mock client
#         mock_client_instance = MagicMock()
#         mock_client_instance.get.return_value = mock_response
#         mock_client.return_value.__aenter__.return_value = mock_client_instance
#
#         # Test the request
#         result = await make_avni_request("GET", "/test", api_key="test_key")
#
#         assert result.success is True
#         assert result.data == {"id": 1, "name": "test"}
#         assert result.error is None
#
#     @patch('avni_mcp_server.client.httpx.AsyncClient')
#     async def test_make_avni_request_http_error(self, mock_client):
#         """Test API request with HTTP error."""
#         # Mock client to raise HTTP error
#         mock_client_instance = MagicMock()
#         mock_client_instance.get.side_effect = Exception("HTTP 401")
#         mock_client.return_value.__aenter__.return_value = mock_client_instance
#
#         result = await make_avni_request("GET", "/test", api_key="test_key")
#
#         assert result.success is False
#         assert "HTTP 401" in result.error
#
#     async def test_make_avni_request_no_api_key(self):
#         """Test API request without API key."""
#         result = await make_avni_request("GET", "/test", api_key=None)
#
#         assert result.success is False
#         assert "API key is required" in result.error
#
#     # @patch('avni_mcp_server.client.httpx.AsyncClient')
#     # async def test_make_avni_request_post_with_data(self, mock_client):
#     #     """Test POST request with data."""
#     #     # Mock response
#     #     mock_response = MagicMock()
#     #     mock_response.json.return_value = {"id": 1, "status": "created"}
#     #     mock_response.raise_for_status.return_value = None
#     #
#     #     # Mock client
#     #     mock_client_instance = MagicMock()
#     #     mock_client_instance.post.return_value = mock_response
#     #     mock_client.return_value.__aenter__.return_value = mock_client_instance
#     #
#     #     # Test POST request
#     #     test_data = {"name": "Test Organization"}
#     #     result = await make_avni_request("POST", "/organizations", test_data, api_key="test_key")
#     #
#     #     assert result.success is True
#     #     assert result.data == {"id": 1, "status": "created"}
#     #
#     #     # Verify POST was called with correct parameters
#     #     mock_client_instance.post.assert_called_once()


# class TestToolIntegration:
#     """Integration tests for tool functionality."""
#
#     @pytest.fixture
#     def api_key_context(self):
#         """Fixture to set up API key context for tests."""
#         test_key = "test_api_key_for_tools"
#         set_api_key(test_key)
#         yield test_key
#         # Cleanup
#         from context import api_key_context
#         api_key_context.set(None)
#
#     @patch('avni_mcp_server.tools.organization.make_avni_request')
#     async def test_create_organization_tool(self, mock_request, api_key_context):
#         """Test create organization tool."""
#         # Mock successful response
#         mock_request.return_value = ApiResult.success_result({"id": 123})
#
#         # Import and test the tool
#         from tools.organization import create_organization
#         # Note: This would be registered as an MCP tool, so direct testing might differ
#         # This is a simplified test - actual implementation might need to test via MCP interface
#
#         # For now, we'll test that the mock was configured correctly
#         assert mock_request is not None
