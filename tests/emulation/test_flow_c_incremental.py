"""
Flow C — Incremental update of an existing organisation.

Emulates the flow for modifying an existing AVNI configuration starting
from a reference bundle ZIP:
  load bundle ZIP -> bundle-to-spec -> spec-to-entities -> store-entities
  -> generate-spec -> patch-bundle -> validate-bundle
  -> generate-rule(visitSchedule+decision) -> generate-report-cards -> inspect-config

Only runs for orgs that have a ``bundle_zip`` defined in the org registry.
Uses ``load_bundle_zip_b64`` helper to load the reference bundle.
"""

from __future__ import annotations

import base64
import json
import zipfile
import io

import pytest
import httpx

from .flow_helpers import (
    StepRecorder,
    StepResult,
    assert_ok_response,
    load_bundle_zip_b64,
)
from .org_registry import OrgConfig


def _zip_b64_to_bundle_dict(zip_b64: str) -> dict:
    """Decode a b64 ZIP and parse the contained JSON files into a bundle dict."""
    zip_bytes = base64.b64decode(zip_b64)
    bundle: dict = {}
    forms: list = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in zf.namelist():
            if not name.endswith(".json"):
                continue
            try:
                parsed = json.loads(zf.read(name))
            except Exception:
                continue
            if name.startswith("forms/"):
                forms.append(parsed)
            else:
                key = name.replace(".json", "")
                bundle[key] = parsed
    if forms:
        bundle["forms"] = forms
    return bundle


@pytest.mark.asyncio(loop_scope="function")
class TestFlowCIncremental:
    """Incremental update pipeline for orgs with reference bundle ZIPs."""

    async def test_incremental_e2e(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_config: OrgConfig,
        recorder: StepRecorder,
    ):
        # Skip orgs without a bundle_zip
        if not org_config.bundle_zip:
            pytest.skip(f"No bundle_zip for {org_config.org_id}")

        bundle_path = org_config.bundle_zip_path()
        if not bundle_path.exists():
            pytest.skip(f"Bundle ZIP not found: {bundle_path}")

        # ------------------------------------------------------------------
        # Step 1: Load bundle ZIP as base64
        # ------------------------------------------------------------------
        zip_b64 = load_bundle_zip_b64(bundle_path)
        assert len(zip_b64) > 0, "Bundle ZIP must not be empty"
        recorder.record(
            StepResult(
                step_name="load-bundle-zip",
                ok=True,
                detail=f"Loaded {len(zip_b64)} b64 chars from {bundle_path.name}",
            )
        )

        # Parse bundle dict for bundle-to-spec
        bundle_dict = _zip_b64_to_bundle_dict(zip_b64)
        assert len(bundle_dict) > 0, "Bundle dict must have at least one section"

        # ------------------------------------------------------------------
        # Step 2: bundle-to-spec
        # ------------------------------------------------------------------
        resp = await client.post(
            "/bundle-to-spec",
            json={
                "bundle": bundle_dict,
                "org_name": org_config.org_name,
            },
        )
        step = assert_ok_response(resp, step_name="bundle-to-spec")
        recorder.record(step)
        assert step.ok, f"bundle-to-spec failed: {step.detail}"
        spec_yaml = resp.json().get("spec_yaml", "")
        assert len(spec_yaml) > 0, "bundle-to-spec must return non-empty spec_yaml"

        # ------------------------------------------------------------------
        # Step 3: spec-to-entities
        # ------------------------------------------------------------------
        resp = await client.post(
            "/spec-to-entities",
            json={"spec_yaml": spec_yaml},
        )
        step = assert_ok_response(resp, step_name="spec-to-entities")
        recorder.record(step)
        assert step.ok, f"spec-to-entities failed: {step.detail}"
        entities = resp.json().get("entities", {})
        assert len(entities.get("subject_types", [])) >= org_config.min_subject_types

        # ------------------------------------------------------------------
        # Step 4: store-entities
        # ------------------------------------------------------------------
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        step = assert_ok_response(resp, step_name="store-entities")
        recorder.record(step)
        assert step.ok, f"store-entities failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 5: generate-spec (from stored entities)
        # ------------------------------------------------------------------
        resp = await client.post(
            "/generate-spec",
            json={
                "conversation_id": conversation_id,
                "org_name": org_config.org_name,
            },
        )
        step = assert_ok_response(resp, step_name="generate-spec")
        recorder.record(step)
        assert step.ok, f"generate-spec failed: {step.detail}"

        # Retrieve the generated spec for patching.
        # Use get-spec but fall back to the original (non-truncated) spec_yaml
        # from bundle-to-spec if get-spec truncates it (large orgs exceed 8000 chars).
        resp_spec = await client.get(
            "/get-spec",
            params={"conversation_id": conversation_id},
        )
        new_spec_yaml = resp_spec.json().get("spec_yaml", spec_yaml)
        if resp_spec.json().get("truncated"):
            new_spec_yaml = spec_yaml  # use the full spec from bundle-to-spec

        # ------------------------------------------------------------------
        # Step 6: patch-bundle
        # ------------------------------------------------------------------
        resp = await client.post(
            "/patch-bundle",
            json={
                "existing_bundle_b64": zip_b64,
                "spec_yaml": new_spec_yaml,
            },
        )
        step = assert_ok_response(resp, step_name="patch-bundle")
        recorder.record(step)
        assert step.ok, f"patch-bundle failed: {step.detail}"
        patch_body = resp.json()
        assert patch_body.get("success") is True, (
            f"patch-bundle not successful: {patch_body}"
        )
        assert patch_body.get("files_patched", 0) > 0, "patch-bundle must patch files"

        # ------------------------------------------------------------------
        # Step 7: validate-bundle (using the patched bundle)
        # ------------------------------------------------------------------
        patched_b64 = patch_body.get("patched_bundle_b64", "")
        if patched_b64:
            patched_dict = _zip_b64_to_bundle_dict(patched_b64)
            resp = await client.post(
                "/validate-bundle",
                json={"bundle": patched_dict},
            )
        else:
            # Fall back to validating the original bundle
            resp = await client.post(
                "/validate-bundle",
                json={"bundle": bundle_dict},
            )
        step = assert_ok_response(resp, step_name="validate-bundle")
        recorder.record(step)
        assert step.ok, f"validate-bundle failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 8: generate-rule (visitSchedule + decision)
        # ------------------------------------------------------------------
        enc_types = entities.get("encounter_types", [])
        enc_name = enc_types[0].get("name", "Follow-up") if enc_types else "Follow-up"

        # visitSchedule
        resp = await client.post(
            "/generate-rule",
            json={
                "rule_type": "visitSchedule",
                "params": {
                    "schedule_days": 30,
                    "max_days": 45,
                    "encounter_name": enc_name,
                },
            },
        )
        step = assert_ok_response(resp, step_name="generate-rule(visitSchedule)")
        recorder.record(step)
        assert step.ok, f"generate-rule(visitSchedule) failed: {step.detail}"
        assert resp.json().get("ok") is True

        # decision
        resp = await client.post(
            "/generate-rule",
            json={
                "rule_type": "decision",
                "params": {
                    "concept_name": "Risk Level",
                },
            },
        )
        step = assert_ok_response(resp, step_name="generate-rule(decision)")
        recorder.record(step)
        assert step.ok, f"generate-rule(decision) failed: {step.detail}"
        assert resp.json().get("ok") is True

        # ------------------------------------------------------------------
        # Step 9: generate-report-cards
        # ------------------------------------------------------------------
        resp = await client.post(
            "/generate-report-cards",
            json={
                "org_name": org_config.org_name,
                "card_types": ["scheduledVisits", "overdueVisits", "total"],
            },
        )
        step = assert_ok_response(resp, step_name="generate-report-cards")
        recorder.record(step)
        assert step.ok, f"generate-report-cards failed: {step.detail}"
        assert resp.json().get("card_count", 0) >= 3

        # ------------------------------------------------------------------
        # Step 10: inspect-config
        # ------------------------------------------------------------------
        resp = await client.post(
            "/inspect-config",
            json={"entities": entities},
        )
        step = assert_ok_response(resp, step_name="inspect-config")
        recorder.record(step)
        assert step.ok, f"inspect-config failed: {step.detail}"
        assert resp.json().get("ok") is True
        assert resp.json().get("completeness_score", 0) > 0

        # ------------------------------------------------------------------
        # Final summary
        # ------------------------------------------------------------------
        assert recorder.all_ok(), (
            f"Flow C failed for {org_config.org_id}: {recorder.summary()}"
        )
