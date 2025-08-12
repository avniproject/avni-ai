"""Tests for the main server functionality."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import create_server, server_instructions, openai_client


class TestServerInitialization:
    """Test server initialization and configuration."""

    def test_create_server_returns_fastmcp_instance(self):
        """Test that create_server returns a FastMCP instance."""
        server = create_server()
        assert server is not None
        assert hasattr(server, "run")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_server_requires_openai_key(self):
        """Test that server requires OpenAI API key."""
        assert openai_client is not None

    def test_server_instructions_exist(self):
        """Test that server has proper instructions."""
        assert server_instructions is not None
        assert "Avni platform" in server_instructions
        assert "health data management" in server_instructions


# class TestServerConfiguration:
#     """Test server configuration and environment handling."""
#
#     @patch.dict(os.environ, {}, clear=True)
#     def test_missing_openai_key_raises_error(self):
#         """Test that missing OpenAI key raises appropriate error."""
#         with pytest.raises(Exception):
#             # This should fail when trying to initialize OpenAI client
#             from openai import OpenAI
#             OpenAI()  # This will fail without API key
#
#     @patch.dict(os.environ, {
#         'OPENAI_API_KEY': 'test_key',
#         'AVNI_BASE_URL': 'https://test.avni.org'
#     })
#     def test_environment_variables_loaded(self):
#         """Test that environment variables are properly loaded."""
#         from config import BASE_URL
#         assert BASE_URL == 'https://test.avni.org'


# class TestToolRegistration:
#     """Test that all tools are properly registered."""
#
#     def test_all_tools_registered(self):
#         """Test that all expected tools are registered with the server."""
#         server = create_server()
#
#         # Check that tools are registered (this depends on how FastMCP exposes tools)
#         # You may need to adjust this based on the actual FastMCP API
#         assert hasattr(server, '_tools') or hasattr(server, 'tools')
#
#         # Expected tool categories
#         expected_tools = [
#             'create_organization',
#             'get_location_types',
#             'get_catchments',
#             'create_location_type',
#             'get_groups',
#             'create_user_group',
#             'create_subject_type',
#             'create_program'
#         ]
#
#         # This test might need adjustment based on how FastMCP exposes tool information
#         # For now, we'll just check that the server has some tools
#         # In a real implementation, you'd inspect server._tools or similar
#         pass  # TODO: Implement proper tool inspection when FastMCP API is clear
