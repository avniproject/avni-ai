"""
flow_state.py — Pydantic model mirroring Dify conversation variables.

Each field in FlowState corresponds to a Dify conversation variable or
environment variable from App Configurator [Staging] v3.yml.

Dify conversation variables → FlowState fields (runtime state):
  auth_token            → auth_token
  avni_mcp_server_url   → avni_mcp_server_url
  entities_jsonl        → entities_jsonl
  spec_yaml             → spec_yaml
  existing_bundle_b64   → existing_bundle_b64
  bundle_zip_b64        → bundle_zip_b64
  upload_task_id        → upload_task_id
  loop                  → (emulated via cycle_count < max_cycles)

Config via env vars (no Dify equivalent — injected as HTTP node config):
  AVNI_AUTH_TOKEN       → auth_token
  AVNI_MCP_SERVER_URL   → avni_mcp_server_url
  AVNI_BASE_URL         → avni_base_url
  AVNI_ORG_NAME         → org_name
  SCOPING_DOC_PATH      → scoping_doc_path
  MAX_PEV_CYCLES        → max_cycles
  POLL_INTERVAL_SECS    → poll_interval_secs
  POLL_MAX_ATTEMPTS     → poll_max_attempts
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


PlanStatus = Literal[
    "idle",
    "extracting",
    "spec",
    "bundling",
    "uploading",
    "done",
    "failed",
]

UploadStatus = Literal["pending", "completed", "failed", "timeout", "unknown"]


class FlowState(BaseModel):
    """
    Typed state container for AppConfiguratorFlow.

    Mirrors Dify conversation variables so the Python emulation is structurally
    isomorphic to the Dify workflow. Fields settable via env vars are initialised
    by FlowState.from_env(); runtime fields are populated as the flow executes.
    """

    model_config = ConfigDict(extra="allow")

    # ── Config fields (set from env vars / constructor) ──────────────────────

    auth_token: str = Field(
        default="",
        description="Avni auth token for API calls. Dify conv var: auth_token. Env: AVNI_AUTH_TOKEN",
    )
    avni_mcp_server_url: str = Field(
        default="https://staging-ai.avniproject.org/",
        description="Avni AI server base URL. Dify conv var: avni_mcp_server_url. Env: AVNI_MCP_SERVER_URL",
    )
    avni_base_url: str = Field(
        default="https://staging.avniproject.org",
        description="Avni backend base URL (staging/prod). Env: AVNI_BASE_URL",
    )
    org_name: str = Field(
        default="",
        description="Org name for spec/bundle generation. Env: AVNI_ORG_NAME",
    )
    scoping_doc_path: str = Field(
        default="",
        description="Path to Excel scoping document. Env: SCOPING_DOC_PATH",
    )
    max_cycles: int = Field(
        default=3,
        description="Max PEV retry cycles. Env: MAX_PEV_CYCLES",
    )
    poll_interval_secs: float = Field(
        default=3.0,
        description="Seconds between upload status polls. Env: POLL_INTERVAL_SECS",
    )
    poll_max_attempts: int = Field(
        default=20,
        description="Max upload status poll attempts. Env: POLL_MAX_ATTEMPTS",
    )

    # ── Runtime state (populated as flow executes) ────────────────────────────

    entities_jsonl: dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted entities from scoping doc. Dify conv var: entities_jsonl",
    )
    spec_yaml: str = Field(
        default="",
        description="Approved YAML spec from Spec Agent. Dify conv var: spec_yaml",
    )
    existing_bundle_b64: str = Field(
        default="",
        description="Base64-encoded existing org bundle ZIP. Dify conv var: existing_bundle_b64",
    )
    bundle_zip_b64: str = Field(
        default="",
        description="Base64-encoded patched bundle ZIP ready for upload. Dify conv var: bundle_zip_b64",
    )
    upload_task_id: str = Field(
        default="",
        description="Async upload task ID for polling. Dify conv var: upload_task_id",
    )
    upload_status: UploadStatus = Field(
        default="unknown",
        description="Result of upload polling: pending/completed/failed/timeout/unknown",
    )
    upload_error: str = Field(
        default="",
        description="Last upload or bundle error message",
    )
    error_diagnosis: str = Field(
        default="",
        description="Structured diagnosis from Diagnose Agent on failed cycle",
    )
    cycle_count: int = Field(
        default=0,
        description="Current PEV cycle number (mirrors Dify loop counter)",
    )
    plan_status: PlanStatus = Field(
        default="idle",
        description="Overall flow state: idle/extracting/spec/bundling/uploading/done/failed",
    )
    spec_valid: bool = Field(
        default=False,
        description="Whether the last spec passed validation",
    )
    bundle_valid: bool = Field(
        default=False,
        description="Whether the last bundle passed validation",
    )

    # ── Factory ──────────────────────────────────────────────────────────────

    @classmethod
    def from_env(cls, **overrides: Any) -> "FlowState":
        """
        Create a FlowState from environment variables.

        Env vars read:
          AVNI_AUTH_TOKEN, AVNI_MCP_SERVER_URL, AVNI_BASE_URL,
          AVNI_ORG_NAME, SCOPING_DOC_PATH,
          MAX_PEV_CYCLES, POLL_INTERVAL_SECS, POLL_MAX_ATTEMPTS
        """
        from dotenv import load_dotenv

        _project_root = Path(__file__).resolve().parents[2]
        for _env_file in (".env", ".env.staging", ".env.production"):
            _env_path = _project_root / _env_file
            if _env_path.exists():
                load_dotenv(dotenv_path=_env_path, override=False)

        kwargs: dict[str, Any] = {
            "auth_token": os.environ.get("AVNI_AUTH_TOKEN", ""),
            "avni_mcp_server_url": os.environ.get(
                "AVNI_MCP_SERVER_URL",
                os.environ.get(
                    "AVNI_AI_SERVER_URL", "https://staging-ai.avniproject.org/"
                ),
            ),
            "avni_base_url": os.environ.get(
                "AVNI_BASE_URL", "https://staging.avniproject.org"
            ),
            "org_name": os.environ.get("AVNI_ORG_NAME", ""),
            "scoping_doc_path": os.environ.get("SCOPING_DOC_PATH", ""),
        }

        _max_cycles = os.environ.get("MAX_PEV_CYCLES")
        if _max_cycles:
            kwargs["max_cycles"] = int(_max_cycles)

        _poll_interval = os.environ.get("POLL_INTERVAL_SECS")
        if _poll_interval:
            kwargs["poll_interval_secs"] = float(_poll_interval)

        _poll_max = os.environ.get("POLL_MAX_ATTEMPTS")
        if _poll_max:
            kwargs["poll_max_attempts"] = int(_poll_max)

        kwargs.update(overrides)
        return cls(**kwargs)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def reset_cycle_state(self) -> None:
        """Clear per-cycle state before starting a new PEV cycle."""
        self.spec_yaml = ""
        self.bundle_zip_b64 = ""
        self.upload_task_id = ""
        self.upload_status = "unknown"
        self.upload_error = ""
        self.spec_valid = False
        self.bundle_valid = False

    def to_summary_dict(self) -> dict[str, Any]:
        """Return a compact summary for logging (excludes large b64 fields)."""
        return {
            "plan_status": self.plan_status,
            "cycle_count": self.cycle_count,
            "max_cycles": self.max_cycles,
            "spec_valid": self.spec_valid,
            "bundle_valid": self.bundle_valid,
            "upload_status": self.upload_status,
            "upload_task_id": self.upload_task_id,
            "upload_error": self.upload_error,
            "error_diagnosis": self.error_diagnosis[:200]
            if self.error_diagnosis
            else "",
            "spec_yaml_len": len(self.spec_yaml),
            "bundle_zip_b64_len": len(self.bundle_zip_b64),
            "existing_bundle_b64_len": len(self.existing_bundle_b64),
        }
