"""
Shared helpers for emulation flow tests.

Provides assertion utilities, a step recorder for tracking multi-step
flow outcomes, and a helper to load bundle ZIPs as base64.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import httpx


# ---------------------------------------------------------------------------
# Step result tracking
# ---------------------------------------------------------------------------


@dataclass
class StepResult:
    """Outcome of a single step in an emulated flow."""

    step_name: str
    ok: bool
    status_code: int = 0
    elapsed_ms: float = 0.0
    detail: str = ""
    response_body: Any = None


class StepRecorder:
    """Accumulates ``StepResult`` entries and provides a summary."""

    def __init__(self) -> None:
        self._results: List[StepResult] = []

    def record(self, result: StepResult) -> StepResult:
        """Append a result and return it for inline chaining."""
        self._results.append(result)
        return result

    @property
    def results(self) -> List[StepResult]:
        return list(self._results)

    def summary(self) -> dict[str, Any]:
        """Return a dict summarising pass/fail counts and failed step names."""
        passed = [r for r in self._results if r.ok]
        failed = [r for r in self._results if not r.ok]
        return {
            "total": len(self._results),
            "passed": len(passed),
            "failed": len(failed),
            "failed_steps": [r.step_name for r in failed],
        }

    def all_ok(self) -> bool:
        """True when every recorded step succeeded."""
        return all(r.ok for r in self._results)


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------


def assert_ok_response(
    resp: httpx.Response,
    *,
    step_name: str = "",
    expected_codes: tuple[int, ...] = (200, 201),
) -> StepResult:
    """Assert response status is acceptable; return a ``StepResult``."""
    ok = resp.status_code in expected_codes
    try:
        body = resp.json()
    except Exception:
        body = resp.text
    return StepResult(
        step_name=step_name or "http_call",
        ok=ok,
        status_code=resp.status_code,
        detail="" if ok else f"Unexpected status {resp.status_code}",
        response_body=body,
    )


def assert_entities_non_empty(
    entities: dict,
    *,
    min_subject_types: int = 1,
    min_programs: int = 0,
    min_encounter_types: int = 0,
) -> StepResult:
    """Verify that parsed entities meet minimum counts."""
    issues: List[str] = []

    subjects = entities.get("subject_types", [])
    if len(subjects) < min_subject_types:
        issues.append(
            f"subject_types: expected >= {min_subject_types}, got {len(subjects)}"
        )

    programs = entities.get("programs", [])
    if len(programs) < min_programs:
        issues.append(f"programs: expected >= {min_programs}, got {len(programs)}")

    encounters = entities.get("encounter_types", [])
    if len(encounters) < min_encounter_types:
        issues.append(
            f"encounter_types: expected >= {min_encounter_types}, got {len(encounters)}"
        )

    return StepResult(
        step_name="entities_non_empty",
        ok=len(issues) == 0,
        detail="; ".join(issues) if issues else "OK",
    )


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------


def load_bundle_zip_b64(path: Path) -> str:
    """Read a ZIP file from disk and return its contents as a base64 string."""
    raw = path.read_bytes()
    return base64.b64encode(raw).decode("ascii")
