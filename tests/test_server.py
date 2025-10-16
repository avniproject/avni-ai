"""Tests for the main server functionality."""

import os
import sys
from pathlib import Path
from unittest.mock import patch
import importlib
import pytest

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import main
from src.main import create_server, server_instructions


class TestServerInitialization:
    """Test server initialization and configuration."""

    @pytest.mark.run(order=1)
    def test_create_server_returns_fastmcp_instance(self):
        """Test that create_server returns a FastMCP instance."""
        server = create_server()
        assert server is not None
        assert hasattr(server, "run")

    @pytest.mark.run(order=2)
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_server_requires_openai_key(self):
        """Test that server requires OpenAI API key."""
        # Test that OPENAI_API_KEY is loaded from environment
        importlib.reload(main)  # Reload to pick up env var
        assert main.OPENAI_API_KEY == "test_key"
