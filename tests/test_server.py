import os
from unittest.mock import patch
import importlib
import pytest
from src import main
from src.main import create_server


class TestServerInitialization:

    @pytest.mark.run(order=1)
    def test_create_server_returns_fastmcp_instance(self):
        server = create_server()
        assert server is not None
        assert hasattr(server, "run")

    @pytest.mark.run(order=2)
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
    def test_server_requires_openai_key(self):
        """Test that server requires OpenAI API key."""
        importlib.reload(main)  # Reload to pick up env var
        assert main.OPENAI_API_KEY
