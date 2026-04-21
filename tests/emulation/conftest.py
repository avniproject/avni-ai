"""
Shared fixtures for emulation tests.

Provides an async HTTP client, conversation id management, org
parametrization, auth-token handling, store cleanup, and a step recorder.
"""

from __future__ import annotations

import functools
import os
import uuid

import httpx
import pytest
import pytest_asyncio
from httpx import ASGITransport

from src.main import app

from .flow_helpers import StepRecorder
from .org_registry import ALL_ORGS, OrgConfig

# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------


def _get_auth_token() -> str:
    """Read AVNI_AUTH_TOKEN from the environment (supports .env via dotenv)."""
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass
    return os.environ.get("AVNI_AUTH_TOKEN", "")


def requires_auth(fn):
    """Decorator that skips a test when AVNI_AUTH_TOKEN is not set."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        token = _get_auth_token()
        if not token:
            pytest.skip("AVNI_AUTH_TOKEN not configured; skipping authenticated test.")
        return fn(*args, **kwargs)

    return wrapper


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def client():
    """Async HTTP client wired to the ASGI app (no running server needed)."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as c:
        yield c


@pytest_asyncio.fixture
async def staging_client():
    """HTTP client that hits AVNI_AI_BASE_URL when set, else the in-process ASGI app.

    Used by the LLM-driven emulation tests that want to replay the Dify flow against
    the real staging avni-ai so we catch drift between tests and production.
    """
    base_url = os.environ.get("AVNI_AI_BASE_URL", "").strip()
    if base_url:
        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as c:
            yield c
    else:
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://testserver", timeout=60.0
        ) as c:
            yield c


@pytest_asyncio.fixture
def conversation_id() -> str:
    """Unique conversation id per test."""
    return f"emu-{uuid.uuid4().hex[:12]}"


@pytest.fixture(
    params=ALL_ORGS,
    ids=[o.org_id for o in ALL_ORGS],
)
def org_config(request) -> OrgConfig:
    """Parametrized fixture — yields one ``OrgConfig`` per registered org."""
    return request.param


@pytest.fixture
def auth_token() -> str:
    """Return the current auth token from the environment, or empty string."""
    return _get_auth_token()


@pytest_asyncio.fixture(autouse=True)
async def _clear_stores():
    """Clear in-memory stores between tests so state does not leak."""
    from src.handlers.entity_handlers import get_entity_store
    from src.handlers.spec_handlers import get_spec_store
    from src.handlers.bundle_handlers import get_bundle_store

    for store in (get_entity_store(), get_spec_store(), get_bundle_store()):
        store._store.clear()
    yield
    for store in (get_entity_store(), get_spec_store(), get_bundle_store()):
        store._store.clear()


@pytest.fixture
def recorder() -> StepRecorder:
    """Fresh ``StepRecorder`` for the current test."""
    return StepRecorder()
