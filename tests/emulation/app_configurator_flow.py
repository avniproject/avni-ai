"""
App Configurator Flow Emulation

Emulates the Dify App Configurator workflow against the staging backend,
implementing the iterative PEV (Planner-Executor-Verifier) self-healing loop.

FlowState mirrors Dify conversation variables from App Configurator [Staging] v3.yml:
  auth_token, avni_mcp_server_url, entities_jsonl, spec_yaml,
  existing_bundle_b64, bundle_zip_b64, upload_task_id

Config env vars (no direct Dify equiv — injected as HTTP node config):
  AVNI_AUTH_TOKEN, AVNI_MCP_SERVER_URL, AVNI_BASE_URL, AVNI_ORG_NAME,
  SCOPING_DOC_PATH, MAX_PEV_CYCLES, POLL_INTERVAL_SECS, POLL_MAX_ATTEMPTS

Usage:
    export AVNI_MCP_SERVER_URL="https://staging-ai.avniproject.org/"
    export AVNI_AUTH_TOKEN="<your-staging-token>"
    python -m tests.emulation.app_configurator_flow
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from uuid import uuid4

import httpx

from src.schemas.flow_state import FlowState
from src.bundle.scoping_parser import load_durga_entities

logger = logging.getLogger(__name__)


@dataclass
class CycleResult:
    """Result of a single PEV cycle."""

    cycle: int
    phase_failed: str  # "spec", "bundle_patch", "bundle_validate", "upload", "poll", ""
    status: str  # "completed", "failed", "bundle_invalid", "timeout", "error"
    errors: list[str] = field(default_factory=list)
    spec_yaml: str = ""
    bundle_size: int = 0
    upload_task_id: str = ""
    upload_result: dict | None = None


@dataclass
class FlowResult:
    """Result of the complete emulation run."""

    success: bool
    total_cycles: int
    cycles: list[CycleResult] = field(default_factory=list)
    final_error: str = ""


class AppConfiguratorFlow:
    """
    Emulates the Dify App Configurator workflow against the staging backend.

    Implements the PEV (Planner-Executor-Verifier) loop:
      - PLAN: Spec Agent generates/fixes YAML spec from entities
      - EXECUTE: Patch existing bundle with spec, validate, upload
      - VERIFY: Poll upload status, check result
      - On failure: diagnose, loop back to PLAN

    State is held in self.state (FlowState), mirroring Dify conversation variables.
    Auth-required endpoints use state.auth_token header.
    """

    def __init__(self, state: FlowState):
        self.state = state
        self.client = httpx.Client(timeout=120.0)
        self.conversation_id: str = str(uuid4())

    @classmethod
    def from_env(cls, **overrides) -> "AppConfiguratorFlow":
        """Create instance from environment variables via FlowState.from_env()."""
        state = FlowState.from_env(**overrides)
        if not state.auth_token:
            raise ValueError("AVNI_AUTH_TOKEN not set. Add it to .env or export it.")
        return cls(state=state)

    # ── HTTP helpers ──────────────────────────────────────────────

    def _url(self, path: str) -> str:
        return f"{self.state.avni_mcp_server_url.rstrip('/')}/{path.lstrip('/')}"

    def _auth_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "avni-auth-token": self.state.auth_token,
        }

    def _no_auth_headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json"}

    def post(self, path: str, body: dict, *, auth: bool = False) -> dict:
        """POST JSON to a backend endpoint. Returns parsed JSON response."""
        headers = self._auth_headers() if auth else self._no_auth_headers()
        url = self._url(path)
        logger.info("POST %s (auth=%s, body_keys=%s)", path, auth, list(body.keys()))
        resp = self.client.post(url, json=body, headers=headers)
        logger.info("  -> %d (%d bytes)", resp.status_code, len(resp.content))
        if resp.status_code >= 400:
            logger.error("  -> ERROR: %s", resp.text[:500])
        resp.raise_for_status()
        return resp.json()

    def get(
        self, path: str, *, auth: bool = False, params: dict | None = None
    ) -> httpx.Response:
        """GET from a backend endpoint. Returns raw httpx.Response."""
        headers = self._auth_headers() if auth else self._no_auth_headers()
        url = self._url(path)
        logger.info("GET %s (auth=%s)", path, auth)
        resp = self.client.get(url, headers=headers, params=params)
        logger.info("  -> %d (%d bytes)", resp.status_code, len(resp.content))
        if resp.status_code >= 400:
            logger.error("  -> ERROR: %s", resp.text[:500])
        return resp

    # ── Phase A: Entity Setup ────────────────────────────────────

    def store_and_validate_entities(self) -> dict:
        """
        Store entities server-side and run structural validation.
        Returns the validation result dict.
        """
        if not self.state.entities_jsonl:
            raise ValueError(
                "No entities loaded. Set state.entities_jsonl before calling run()."
            )

        logger.info("=== Phase A: Store & Validate Entities ===")
        logger.info(
            "  subject_types=%d, programs=%d, encounter_types=%d, forms=%d",
            len(self.state.entities_jsonl.get("subject_types", [])),
            len(self.state.entities_jsonl.get("programs", [])),
            len(self.state.entities_jsonl.get("encounter_types", [])),
            len(self.state.entities_jsonl.get("forms", [])),
        )

        # A1: Store entities server-side (requires auth for Dify, but endpoint itself doesn't)
        self.post(
            "/store-entities",
            {
                "conversation_id": self.conversation_id,
                "entities": self.state.entities_jsonl,
            },
        )
        logger.info("  Entities stored with conversation_id=%s", self.conversation_id)

        # A2: Validate entities (deterministic structural check)
        validation = self.post(
            "/validate-entities",
            {"conversation_id": self.conversation_id},
        )
        logger.info(
            "  Validation: %d errors, %d warnings",
            validation.get("error_count", 0),
            validation.get("warning_count", 0),
        )
        if validation.get("issues_summary"):
            logger.info("  Summary:\n%s", validation["issues_summary"])

        return validation

    # ── Phase C: Spec Generation (Planner) ───────────────────────

    def run_spec_agent(self) -> bool:
        """
        Simulate the Spec Agent's ReAct loop:
        1. If error_diagnosis is present, apply corrections first
        2. Generate spec from entities
        3. Validate spec
        4. If validation errors, attempt auto-correction and regenerate (up to 3 internal retries)

        Returns True if spec is ready (even with warnings), False if hard failure.
        """
        logger.info("=== Phase C: Spec Agent (cycle %d) ===", self.state.cycle_count)

        # If retrying after a failed cycle, apply corrections based on diagnosis
        if self.state.error_diagnosis:
            logger.info("  Applying corrections from previous failure diagnosis...")
            corrections = self._derive_corrections_from_diagnosis(
                self.state.error_diagnosis
            )
            if corrections:
                self.post(
                    "/apply-entity-corrections",
                    {
                        "conversation_id": self.conversation_id,
                        "corrections": corrections,
                    },
                )
                logger.info("  Applied %d corrections", len(corrections))
            self.state.error_diagnosis = ""  # Clear after applying

        # Internal ReAct loop: generate → validate → correct → retry
        for attempt in range(1, 4):
            logger.info("  Spec generation attempt %d/3", attempt)

            # Generate spec from entities
            resp = self.post(
                "/generate-spec",
                {
                    "conversation_id": self.conversation_id,
                    "org_name": self.state.org_name,
                },
            )
            self.state.spec_yaml = resp.get("spec_yaml", "")
            if not self.state.spec_yaml:
                logger.error("  generate-spec returned empty spec_yaml")
                self.state.spec_valid = False
                return False

            logger.info(
                "  Generated spec: %d chars, %d lines",
                len(self.state.spec_yaml),
                self.state.spec_yaml.count("\n"),
            )

            # Validate spec
            validation = self.post(
                "/validate-spec",
                {"spec_yaml": self.state.spec_yaml},
            )
            errors = validation.get("errors", [])
            warnings = validation.get("warnings", [])
            suggestions = validation.get("suggestions", [])

            logger.info(
                "  Spec validation: valid=%s, %d errors, %d warnings, %d suggestions",
                validation.get("valid"),
                len(errors),
                len(warnings),
                len(suggestions),
            )

            if validation.get("valid", False):
                self.state.spec_valid = True
                if warnings:
                    logger.info("  Warnings (proceeding anyway):")
                    for w in warnings:
                        logger.info("    - %s", w)
                return True

            # Spec has errors — try to auto-correct
            logger.warning("  Spec validation errors:")
            for e in errors:
                logger.warning("    - %s", e)

            if attempt < 3:
                corrections = self._derive_corrections_from_spec_errors(errors)
                if corrections:
                    self.post(
                        "/apply-entity-corrections",
                        {
                            "conversation_id": self.conversation_id,
                            "corrections": corrections,
                        },
                    )
                    logger.info(
                        "  Applied %d auto-corrections, retrying...", len(corrections)
                    )
                else:
                    logger.warning(
                        "  Could not derive corrections, proceeding with current spec"
                    )
                    return True  # Proceed with warnings/minor errors

        # Exhausted internal retries — proceed anyway (bundle validation will catch issues)
        logger.warning(
            "  Spec agent exhausted 3 internal retries. Proceeding with current spec."
        )
        return True

    # ── Phase D: Bundle Generation & Upload (Executor) ───────────

    def run_bundle_generation(self) -> CycleResult:
        """
        Execute the bundle generation pipeline:
        D1: Download existing org bundle
        D2: Patch bundle with spec
        D3: Upload patched bundle
        D4: Poll upload status

        Returns CycleResult with outcome.
        """
        logger.info(
            "=== Phase D: Bundle Generation & Upload (cycle %d) ===",
            self.state.cycle_count,
        )

        cycle = CycleResult(cycle=self.state.cycle_count, phase_failed="", status="")

        # D1: Download existing org bundle
        try:
            logger.info("  D1: Downloading existing org bundle...")
            resp = self.get(
                "/download-bundle-b64",
                auth=True,
                params={"includeLocations": "false"},
            )
            resp.raise_for_status()
            data = resp.json()
            self.state.existing_bundle_b64 = data.get("bundle_zip_b64", "")
            logger.info(
                "  Downloaded existing bundle: %d bytes (b64 len=%d)",
                data.get("size_bytes", 0),
                len(self.state.existing_bundle_b64),
            )
        except Exception as e:
            logger.error("  D1 FAILED: %s", e)
            cycle.phase_failed = "download"
            cycle.status = "error"
            cycle.errors = [f"Download existing bundle failed: {e}"]
            return cycle

        # D2: Patch bundle with spec
        try:
            logger.info("  D2: Patching bundle with spec...")
            patch_resp = self.post(
                "/patch-bundle",
                {
                    "existing_bundle_b64": self.state.existing_bundle_b64,
                    "spec_yaml": self.state.spec_yaml,
                },
            )
            self.state.bundle_zip_b64 = patch_resp.get("patched_bundle_b64", "")
            self.state.bundle_valid = patch_resp.get("success", False)
            files_patched = patch_resp.get("files_patched", 0)
            validation = patch_resp.get("validation", {})
            cycle.bundle_size = patch_resp.get("size_bytes", 0)

            logger.info(
                "  Patched bundle: %d files patched, %d bytes",
                files_patched,
                cycle.bundle_size,
            )

            # Check inline validation from patch-bundle
            if validation:
                val_errors = validation.get("errors", [])
                val_warnings = validation.get("warnings", [])
                if val_errors:
                    logger.warning("  Patch validation errors: %s", val_errors)
                if val_warnings:
                    logger.info("  Patch validation warnings: %s", val_warnings)

        except httpx.HTTPStatusError as e:
            logger.error(
                "  D2 FAILED: HTTP %d: %s",
                e.response.status_code,
                e.response.text[:500],
            )
            cycle.phase_failed = "bundle_patch"
            cycle.status = "error"
            cycle.errors = [f"Patch bundle failed: HTTP {e.response.status_code}"]
            return cycle
        except Exception as e:
            logger.error("  D2 FAILED: %s", e)
            cycle.phase_failed = "bundle_patch"
            cycle.status = "error"
            cycle.errors = [f"Patch bundle failed: {e}"]
            return cycle

        if not self.state.bundle_zip_b64:
            self.state.bundle_valid = False
            cycle.phase_failed = "bundle_patch"
            cycle.status = "error"
            cycle.errors = ["Patch bundle returned empty patched_bundle_b64"]
            return cycle

        # D3: Upload bundle
        try:
            logger.info("  D3: Uploading bundle to Avni...")
            upload_resp = self.post(
                "/upload-bundle",
                {"bundle_zip_b64": self.state.bundle_zip_b64},
                auth=True,
            )
            self.state.upload_task_id = upload_resp.get("task_id", "")
            cycle.upload_task_id = self.state.upload_task_id
            self.state.plan_status = "uploading"
            logger.info("  Upload started: task_id=%s", self.state.upload_task_id)
        except httpx.HTTPStatusError as e:
            logger.error(
                "  D3 FAILED: HTTP %d: %s",
                e.response.status_code,
                e.response.text[:500],
            )
            cycle.phase_failed = "upload"
            cycle.status = "error"
            cycle.errors = [
                f"Upload bundle failed: HTTP {e.response.status_code}: {e.response.text[:200]}"
            ]
            return cycle
        except Exception as e:
            logger.error("  D3 FAILED: %s", e)
            cycle.phase_failed = "upload"
            cycle.status = "error"
            cycle.errors = [f"Upload bundle failed: {e}"]
            return cycle

        # D4: Poll upload status
        logger.info(
            "  D4: Polling upload status (max %d attempts, %ds interval)...",
            self.state.poll_max_attempts,
            self.state.poll_interval_secs,
        )
        for poll_attempt in range(1, self.state.poll_max_attempts + 1):
            time.sleep(self.state.poll_interval_secs)
            try:
                status_resp = self.get(f"/upload-status/{self.state.upload_task_id}")
                status_data = status_resp.json()
                status = status_data.get("status", "unknown")
                progress = status_data.get("progress", "")
                logger.info(
                    "  Poll %d/%d: status=%s progress=%s",
                    poll_attempt,
                    self.state.poll_max_attempts,
                    status,
                    progress,
                )

                if status == "completed":
                    self.state.upload_status = "completed"
                    self.state.plan_status = "done"
                    cycle.status = "completed"
                    cycle.upload_result = status_data
                    logger.info("  Upload COMPLETED successfully!")
                    return cycle

                if status == "failed":
                    error = status_data.get("error", "Unknown error")
                    self.state.upload_status = "failed"
                    self.state.upload_error = error
                    cycle.phase_failed = "poll"
                    cycle.status = "failed"
                    cycle.errors = [f"Upload failed: {error}"]
                    cycle.upload_result = status_data
                    logger.error("  Upload FAILED: %s", error)
                    return cycle

            except Exception as e:
                logger.warning("  Poll %d error: %s", poll_attempt, e)

        # Polling exhausted
        self.state.upload_status = "timeout"
        cycle.phase_failed = "poll"
        cycle.status = "timeout"
        cycle.errors = [
            f"Upload polling timed out after {self.state.poll_max_attempts} attempts"
        ]
        logger.error("  Upload polling TIMED OUT")
        return cycle

    # ── Phase E: Diagnosis ───────────────────────────────────────

    def diagnose(self, cycle_result: CycleResult) -> str:
        """
        Analyze a failed cycle and produce an error diagnosis string.
        In the real Dify flow, the Diagnose Agent would do this via LLM reasoning.
        In the emulation, we produce a structured diagnosis for the Spec Agent.
        """
        logger.info("=== Phase E: Diagnosis ===")

        diagnosis_parts = [
            f"Cycle {cycle_result.cycle} failed at phase '{cycle_result.phase_failed}'.",
            f"Status: {cycle_result.status}.",
        ]
        if cycle_result.errors:
            diagnosis_parts.append("Errors:")
            for e in cycle_result.errors:
                diagnosis_parts.append(f"  - {e}")

        diagnosis = "\n".join(diagnosis_parts)
        logger.info("  Diagnosis:\n%s", diagnosis)
        return diagnosis

    # ── Main PEV Loop ────────────────────────────────────────────

    def run(self) -> FlowResult:
        """
        Execute the full PEV (Planner-Executor-Verifier) self-healing loop.

        Returns FlowResult with overall outcome and per-cycle details.
        """
        logger.info("=" * 60)
        logger.info("App Configurator Flow Emulation")
        logger.info("  Server: %s", self.state.avni_mcp_server_url)
        logger.info("  Conversation: %s", self.conversation_id)
        logger.info("  Max cycles: %d", self.state.max_cycles)
        logger.info("  State: %s", self.state.to_summary_dict())
        logger.info("=" * 60)

        self.state.plan_status = "extracting"
        result = FlowResult(success=False, total_cycles=0)

        # Phase A: One-time entity setup
        try:
            validation = self.store_and_validate_entities()
            if validation.get("has_errors"):
                logger.warning(
                    "Entity validation has errors, but proceeding (Spec Agent will handle)."
                )
        except Exception as e:
            logger.error("Phase A failed: %s", e)
            self.state.plan_status = "failed"
            self.state.upload_error = str(e)
            result.final_error = f"Entity setup failed: {e}"
            return result

        # PEV Loop
        while self.state.cycle_count < self.state.max_cycles:
            self.state.cycle_count += 1
            result.total_cycles = self.state.cycle_count
            logger.info("\n" + "=" * 60)
            logger.info(
                "PEV CYCLE %d/%d", self.state.cycle_count, self.state.max_cycles
            )
            logger.info("=" * 60)

            # PLAN: Generate/fix spec
            self.state.plan_status = "spec"
            try:
                spec_ok = self.run_spec_agent()
                if not spec_ok:
                    cycle_result = CycleResult(
                        cycle=self.state.cycle_count,
                        phase_failed="spec",
                        status="error",
                        errors=["Spec generation failed completely"],
                    )
                    result.cycles.append(cycle_result)
                    self.state.error_diagnosis = self.diagnose(cycle_result)
                    continue
            except Exception as e:
                logger.error("Spec Agent failed with exception: %s", e)
                cycle_result = CycleResult(
                    cycle=self.state.cycle_count,
                    phase_failed="spec",
                    status="error",
                    errors=[str(e)],
                )
                result.cycles.append(cycle_result)
                self.state.error_diagnosis = self.diagnose(cycle_result)
                continue

            # EXECUTE: Bundle generation, validation, upload, polling
            self.state.plan_status = "bundling"
            try:
                cycle_result = self.run_bundle_generation()
                cycle_result.spec_yaml = self.state.spec_yaml
                result.cycles.append(cycle_result)
            except Exception as e:
                logger.error("Bundle generation failed with exception: %s", e)
                cycle_result = CycleResult(
                    cycle=self.state.cycle_count,
                    phase_failed="bundle_patch",
                    status="error",
                    errors=[str(e)],
                )
                result.cycles.append(cycle_result)
                self.state.error_diagnosis = self.diagnose(cycle_result)
                continue

            # VERIFY: Check result
            if cycle_result.status == "completed":
                logger.info("\n" + "=" * 60)
                logger.info("SUCCESS after %d cycle(s)!", self.state.cycle_count)
                logger.info("=" * 60)
                result.success = True
                return result

            # Failed — diagnose and retry
            self.state.error_diagnosis = self.diagnose(cycle_result)
            if self.state.cycle_count < self.state.max_cycles:
                logger.info(
                    "Cycle %d failed. Retrying... (%d cycles remaining)",
                    self.state.cycle_count,
                    self.state.max_cycles - self.state.cycle_count,
                )
            else:
                logger.error(
                    "Cycle %d failed. No more retries available.",
                    self.state.cycle_count,
                )

        # Exhausted all cycles
        self.state.plan_status = "failed"
        result.final_error = (
            f"Failed after {self.state.max_cycles} cycles. "
            f"Last diagnosis: {self.state.error_diagnosis}"
        )
        logger.error("\n" + "=" * 60)
        logger.error("FAILED after %d cycles", self.state.max_cycles)
        logger.error("  Last error: %s", self.state.error_diagnosis)
        logger.error("=" * 60)
        return result

    # ── Correction Helpers ───────────────────────────────────────

    def _derive_corrections_from_diagnosis(self, diagnosis: str) -> list[dict]:
        """
        Parse an error diagnosis string and derive entity corrections.
        This is a simplified heuristic — the real Dify Diagnose Agent
        would use LLM reasoning to produce corrections.
        """
        corrections = []
        # In the emulation, we return empty corrections.
        # The real Diagnose Agent in Dify would analyze the error
        # and produce specific corrections like:
        #   {"entity_type": "subject_type", "name": "Individual", "type": "Person"}
        #   {"entity_type": "encounter_type", "name": "Bad Encounter", "_delete": true}
        logger.info("  Deriving corrections from diagnosis (heuristic)...")
        logger.info(
            "  (No automatic corrections in emulation — Dify Diagnose Agent handles this)"
        )
        return corrections

    def _derive_corrections_from_spec_errors(self, errors: list[str]) -> list[dict]:
        """
        Parse spec validation errors and derive entity corrections.
        Simple heuristic mapping of common error patterns.
        """
        corrections = []
        for error in errors:
            error_lower = error.lower()

            # Missing subject type reference
            if "subject type" in error_lower and "not found" in error_lower:
                # Extract referenced name if possible
                logger.info("  Detected missing subject type reference: %s", error)

            # Missing program reference
            if "program" in error_lower and "not found" in error_lower:
                logger.info("  Detected missing program reference: %s", error)

            # Duplicate name
            if "duplicate" in error_lower:
                logger.info("  Detected duplicate: %s", error)

        if not corrections:
            logger.info("  No auto-corrections derived from spec errors")

        return corrections

    # ── Utilities ────────────────────────────────────────────────

    def health_check(self) -> bool:
        """Check if the staging server is reachable."""
        try:
            resp = self.get("/health")
            data = resp.json()
            logger.info("Health check: %s", data)
            return data.get("status") == "healthy"
        except Exception as e:
            logger.error("Health check failed: %s", e)
            return False

    def delete_config(
        self, delete_metadata: bool = True, delete_admin_config: bool = True
    ) -> bool:
        """
        Wipe the entire org configuration via DELETE /api/implementation.

        Passes deleteMetadata and deleteAdminConfig as query parameters.
        Use this before uploading a completely new config to ensure no stale
        MCH or placeholder data persists.  Requires auth.

        Returns True on success, False on failure.
        """
        logger.info(
            "=== DELETE CONFIG: wiping existing org configuration "
            "(deleteMetadata=%s, deleteAdminConfig=%s) ===",
            delete_metadata,
            delete_admin_config,
        )
        try:
            headers = self._auth_headers()
            url = self._url("/api/implementation")
            params = {
                "deleteMetadata": str(delete_metadata).lower(),
                "deleteAdminConfig": str(delete_admin_config).lower(),
            }
            resp = self.client.delete(url, headers=headers, params=params)
            logger.info("  DELETE /api/implementation -> %d", resp.status_code)
            if resp.status_code in (200, 204):
                logger.info("  Config deleted successfully.")
                return True
            logger.error("  Delete failed: %s", resp.text[:300])
            return False
        except Exception as e:
            logger.error("  delete_config failed: %s", e)
            return False

    def print_summary(self, result: FlowResult) -> None:
        """Print a human-readable summary of the flow result."""
        print("\n" + "=" * 60)
        print("FLOW RESULT SUMMARY")
        print("=" * 60)
        print(f"  Success: {result.success}")
        print(f"  Total cycles: {result.total_cycles}")
        for cr in result.cycles:
            status_icon = "OK" if cr.status == "completed" else "FAIL"
            print(f"  Cycle {cr.cycle}: [{status_icon}] status={cr.status}")
            if cr.phase_failed:
                print(f"    Failed at: {cr.phase_failed}")
            if cr.errors:
                for e in cr.errors:
                    print(f"    Error: {e}")
            if cr.bundle_size:
                print(f"    Bundle size: {cr.bundle_size} bytes")
        if result.final_error:
            print(f"  Final error: {result.final_error}")
        print("=" * 60)


def load_sample_entities() -> dict:
    """
    Load entities from the Durga India Modelling.xlsx scoping document.

    Replaces the old hardcoded Maternal Health placeholder data.
    Reads the real Durga entities: Cohort, Participant, Work With Women/Men programs,
    Session/Baseline/Endline encounter types, and Karnataka/City location hierarchy.

    Path controlled by SCOPING_DOC_PATH env var (defaults to the bundled test fixture).
    """
    return load_durga_entities()


if __name__ == "__main__":
    import os
    import sys
    from dotenv import load_dotenv

    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # ── Interactive prompts for missing env vars ──────────────────
    def _prompt(env_key: str, prompt_text: str, secret: bool = False) -> str:
        val = os.environ.get(env_key, "").strip()
        if val:
            return val
        if secret:
            import getpass

            val = getpass.getpass(f"{prompt_text}: ").strip()
        else:
            val = input(f"{prompt_text}: ").strip()
        if val:
            os.environ[env_key] = val
        return val

    server_url = _prompt(
        "AVNI_MCP_SERVER_URL",
        "Avni MCP server URL [https://staging-ai.avniproject.org/]",
    )
    if not server_url:
        server_url = "https://staging-ai.avniproject.org/"
        os.environ["AVNI_MCP_SERVER_URL"] = server_url

    auth_token = _prompt(
        "AVNI_AUTH_TOKEN", "Auth token (avni-auth-token header)", secret=True
    )
    if not auth_token:
        print("ERROR: AVNI_AUTH_TOKEN is required.")
        sys.exit(1)

    org_name = _prompt("AVNI_ORG_NAME", "Organisation name (e.g. 'Durga India')")
    scoping_doc = _prompt(
        "SCOPING_DOC_PATH",
        "Path to scoping Excel file [tests/resources/scoping/Durga India Modelling.xlsx]",
    )
    if not scoping_doc:
        os.environ["SCOPING_DOC_PATH"] = ""

    flow = AppConfiguratorFlow.from_env()

    # ── Health check ──────────────────────────────────────────────
    if not flow.health_check():
        print("ERROR: Server is not reachable. Check AVNI_MCP_SERVER_URL.")
        sys.exit(1)

    # ── Load entities from scoping document ───────────────────────
    print("\nParsing scoping document...")
    flow.state.entities_jsonl = load_sample_entities()
    entities = flow.state.entities_jsonl
    print(f"  Subject types : {[s['name'] for s in entities.get('subject_types', [])]}")
    print(f"  Programs      : {[p['name'] for p in entities.get('programs', [])]}")
    print(
        f"  Encounter types: {[e['name'] for e in entities.get('encounter_types', [])]}"
    )
    print(
        f"  Address levels: {[a['name'] for a in entities.get('address_levels', [])]}"
    )

    # ── Confirm before proceeding ─────────────────────────────────
    print("\nOptions:")
    print("  [1] Run PEV flow (void old forms via patch-bundle, upload new config)")
    print("  [2] Delete entire org config first, then run PEV flow")
    print("  [q] Quit")
    choice = input("Choice [1]: ").strip() or "1"

    if choice == "q":
        sys.exit(0)

    if choice == "2":
        print("\nDeleting existing org configuration...")
        ok = flow.delete_config()
        if not ok:
            print(
                "WARNING: delete_config failed — proceeding with patch-bundle void approach instead."
            )

    # ── Run the full PEV loop ─────────────────────────────────────
    result = flow.run()
    flow.print_summary(result)

    sys.exit(0 if result.success else 1)
