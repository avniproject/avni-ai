"""Fixtures shared by spike tests.

Keeps three things consistent across files:
  - a clarification handler that records what was asked and replies
    deterministically (so tests are not flaky)
  - an OrchestratorConfig builder that supplies safe defaults
  - the SpikeError import (re-exported via .helpers below for brevity)
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any
from unittest.mock import MagicMock

import pytest
import pytest_asyncio

from src.orchestrators.claude_agent.contracts import (
    ClarificationRequest,
    ClarificationResponse,
    OrchestratorConfig,
)


@pytest.fixture
def base_config(tmp_path) -> OrchestratorConfig:
    """A config that will not actually call out to anything.

    Tests override fields explicitly; the values here are pessimistic so an
    accidentally-real call surfaces immediately."""
    return OrchestratorConfig(
        avni_mcp_url="http://localhost:0/mcp",
        avni_auth_token="",
        anthropic_api_key="test-key",
        model_default="claude-opus-4-5",
        org_name="Test Org",
        scoping_doc_paths=(),
        conversation_id="cid-test",
    )


class RecordingClarificationHandler:
    """Replays a script of answers and records every question seen.

    Pass `answers=[...]` to drive multi-turn flows deterministically."""

    def __init__(self, answers: list[str] | None = None):
        self.requests: list[ClarificationRequest] = []
        self._answers = list(answers or [])

    async def __call__(self, req: ClarificationRequest) -> ClarificationResponse:
        self.requests.append(req)
        if self._answers:
            return ClarificationResponse(answer=self._answers.pop(0))
        # Default: pick the first option (mirrors --non-interactive)
        if req.options:
            return ClarificationResponse(answer=req.options[0])
        return ClarificationResponse(answer="ok")


@pytest.fixture
def recording_handler() -> RecordingClarificationHandler:
    return RecordingClarificationHandler()


@pytest_asyncio.fixture
async def fake_anthropic_client() -> AsyncIterator[MagicMock]:
    """A MagicMock shaped like the Anthropic SDK we touch.

    Every leaf the runner calls is a MagicMock that returns a small object
    with the fields the runner reads.  Tests customise behaviour by patching
    individual leaves (e.g. `client.beta.sessions.events.stream.return_value`)
    rather than re-constructing the whole tree.
    """
    client = MagicMock()

    # Defaults — enough for happy-path lifecycle tests.
    client.beta.files.upload.return_value = MagicMock(id="file_abc")
    client.beta.agents.create.return_value = MagicMock(id="agent_abc", version=1)
    client.beta.environments.create.return_value = MagicMock(id="env_abc")
    client.beta.sessions.create.return_value = MagicMock(id="sess_abc")
    client.beta.sessions.retrieve.return_value = MagicMock(status="idle")

    # Default event stream — empty: yields nothing, then context-exits.
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=iter([]))
    cm.__exit__ = MagicMock(return_value=False)
    client.beta.sessions.events.stream.return_value = cm

    yield client


def make_event(etype: str, **kwargs: Any) -> dict[str, Any]:
    """Tiny helper for building dict-shaped events the runner accepts."""
    return {"type": etype, **kwargs}
