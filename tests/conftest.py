"""Pytest configuration and shared fixtures."""

import pytest
import os
from unittest.mock import patch


@pytest.fixture(scope="session")
def test_environment():
    """Set up test environment variables."""
    test_env = {
        "AVNI_BASE_URL": "https://test.avni.org",
        "OPENAI_API_KEY": "test_openai_key_12345",
    }

    with patch.dict(os.environ, test_env):
        yield test_env


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for tests."""
    with patch("avni.openai_client") as mock_client:
        yield mock_client


@pytest.fixture
def sample_avni_response():
    """Sample Avni API response data."""
    return {
        "success_response": {"id": 1, "name": "Test Organization", "status": "active"},
        "error_response": {"error": "Invalid API key", "code": 401},
        "list_response": [
            {"id": 1, "name": "Item 1", "level": 1.0},
            {"id": 2, "name": "Item 2", "level": 2.0},
        ],
    }
