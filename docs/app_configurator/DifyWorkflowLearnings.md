# Dify Workflow Learnings from Emulation Trial Runs

Learnings derived from running `tests/emulation/app_configurator_flow.py` against staging
(Apr 2026). Each section maps an observed issue to the required Dify v3 workflow fix.

---

## 1. `org_name` must always flow into `/generate-spec`

### Observed
The emulation passes `org_name` explicitly from `FlowState` to `POST /generate-spec`.
The Dify v3 workflow sends only `{ "conversation_id": "..." }` — `org_name` is absent from
the body, so the backend falls back to `""` and the spec YAML gets `org: Unknown Organization`.

### Required fix
The `generate-spec` HTTP node body must include `org_name`:

```json
{
  "conversation_id": "{{#sys.conversation_id#}}",
  "org_name": "{{#sys.inputs.org_name#}}"
}
```

`org_name` is already a Start node input variable — it just isn't threaded through to the
spec node. Add it.

---

## 2. `validate-entities` should use `conversation_id`, not inline entities

### Observed
The Ambiguity Checker node sends the full `entities_jsonl` object inline:
```json
{ "entities": {{#conversation.entities_jsonl#}} }
```
The emulation instead sends `{ "conversation_id": "..." }` and lets the server look up the
stored entities. This avoids the 15 MB Dify conversation-variable size limit and keeps the
HTTP body small.

### Required fix
Change the Ambiguity Checker body to:
```json
{ "conversation_id": "{{#sys.conversation_id#}}" }
```
The `/validate-entities` endpoint already supports both forms — no backend change needed.

---

## 3. Stale config cleanup: two strategies, both must be user-selectable

### Observed
On a re-run after a prior Durga upload, the patched bundle contained growing
`formMappings.json` (voided old + new each run = O(n²) growth) because the old void-all
approach didn't diff by UUID.

**Correct patch-bundle logic** (now fixed in backend):
- Only void formMappings whose UUID is **absent** from the new spec.
- Mappings present in both → replaced by the new version (Avni upserts by UUID).
- Stale `forms/*.json` (not in new spec) → set `isVoided: true`.

**But the Dify workflow has no cleanup path at all.** The user has no way to trigger a
"delete everything and start fresh" before uploading.

### Required fix
Add a **pre-upload cleanup decision** node after the human-input confirmation:

```
[Human Input: Yes/No]
    → Yes → [If-Else: user said "clean slate" or "delete everything"?]
                → true  → [HTTP: DELETE /api/implementation?deleteMetadata=true&deleteAdminConfig=true]
                              → [Continue to Spec Agent]
                → false → [Continue to Spec Agent directly]
```

The Orchestrator already routes `"delete everything"` / `"clean slate"` to ASSISTANT —
but that goes nowhere useful. Rewire it to trigger the delete-and-reconfigure path.

---

## 4. `DELETE /api/implementation` body is wrong — use query params

### Observed
`delete_config()` in the emulation was calling with `json={}` which httpx rejected.
The actual Avni endpoint (`/implementation/delete`) uses **query parameters**, not a body:

```
DELETE /api/implementation?deleteMetadata=true&deleteAdminConfig=true
```

### Required fix
If a Dify HTTP node calls `DELETE /api/implementation`, it must use query params:
```
URL: {{#conversation.avni_mcp_server_url#}}api/implementation
Params: deleteMetadata:true, deleteAdminConfig:true
Headers: avni-auth-token:{{#conversation.auth_token#}}
Method: DELETE
```
`deleteMetadata=true` deletes forms/concepts/mappings.
`deleteAdminConfig=true` deletes subject types/programs/encounter types.
Both must be `true` for a full wipe.

---

## 5. No programs extracted from Durga scoping doc → warnings on every run

### Observed
The scoping parser returns 0 programs for the Durga Excel:
```
Programs      : []
Encounter types: ['Session', 'Baseline for Women', ...]
```
Spec validation then warns "Encounter type 'X' has no form" for all 7 encounter types.
These are warnings (not errors) so the flow proceeds — but the config is incomplete.

### Required fix (two parts)
**A. Scoping parser**: The Durga Excel models encounter types directly on subject types
(no program layer). The parser should detect this and model them as `IndividualEncounterType`
(subject-linked, not program-linked). Currently they're being extracted but their
`subject_type` link may be missing.

**B. Dify Spec Agent prompt**: Add an explicit rule:
> "If encounter types have no associated program, they must have a `subject_type` field
> set to the relevant subject type name. Do not leave both `program_name` and `subject_type`
> empty."

---

## 6. Human-input `Yes/No` confirmation is a blocking gate — needs timeout handling

### Observed
The emulation has a simple `choice = input("Choice [1]:")` which is synchronous.
The Dify v3 workflow uses a `human-input` node with `Yes/No` buttons. Both the `__timeout`
path and the `No` path currently route back to the Spec Agent (same target), which means:
- Timeout → silently re-runs the spec agent without user knowing
- `No` → also re-runs the spec agent without asking the user what to change

### Required fix
- **Timeout** → answer node: "Your session timed out. Please restart the configuration."
  Then set `setup_mode_active = false`.
- **No** → answer node: "What would you like to change? Please describe the corrections
  needed." Then route to Spec Agent with the user's correction in context.

The `No` path needs the user's correction text — the human-input node should capture a
free-text response or route to a clarification LLM before re-entering the Spec Agent.

---

## 7. Upload polling loop exits without telling the user the outcome

### Observed
The polling loop checks status every 3s. On success (`status=completed`), it logs
"Upload COMPLETED successfully!" but the Dify loop's success path exits to an answer node
that says "Upload Done" without showing the Avni URL or next steps.

### Required fix
The upload-done answer node should include:
- Confirmation that the org is now live
- Direct link: `https://staging.avniproject.org/` (parameterised by `AVNI_BASE_URL`)
- Next steps: "You can now log in to Avni and verify your configuration"

---

## 8. `spec_yaml` conversation variable is set but `existing_bundle_b64` is not persisted

### Observed
The emulation stores `spec_yaml` and `existing_bundle_b64` in `FlowState` across cycles.
In the Dify v3 workflow, `existing_bundle_b64` is downloaded fresh every cycle (correct),
but `spec_yaml` is also regenerated every cycle from scratch — the Spec Agent doesn't
carry forward the approved spec from a prior cycle for the Diagnose/retry path.

### Required fix
After the Spec Agent succeeds, save `spec_yaml` to the conversation variable:
```yaml
# Assigner node after spec-extractor-001
- variable: conversation.spec_yaml
  value: {{#spec-extractor-001.spec_yaml#}}
```
On retry, pass the previous `spec_yaml` to the Diagnose Agent as context so it can
produce targeted corrections rather than starting from scratch.

---

## 9. `store-entities` sends `avni-auth-token` header unnecessarily

### Observed
The Store Entities HTTP node includes `avni-auth-token:{{#conversation.auth_token#}}` in
headers. The `/store-entities` endpoint doesn't require auth — it stores to an in-memory
dict keyed by `conversation_id`. Sending auth is harmless but misleading.

### Required fix (cosmetic / correctness)
Remove the `avni-auth-token` header from the Store Entities and Ambiguity Checker nodes.
Auth is only needed for: `download-bundle-b64`, `upload-bundle`, `DELETE /api/implementation`.

---

## Summary: Priority Order for Dify v3 Updates

| # | Change | Impact | Effort |
|---|--------|--------|--------|
| 1 | Thread `org_name` into `/generate-spec` body | Config correctness | Low |
| 3 | Add delete-config path before spec agent | Stale config cleanup | Medium |
| 4 | Fix DELETE /api/implementation to use query params | Delete-config works | Low |
| 6 | Fix `No` and timeout paths from human-input | UX correctness | Medium |
| 5 | Fix encounter types with no program in Durga | Config completeness | Medium |
| 7 | Enrich upload-done answer with next steps | UX | Low |
| 8 | Persist `spec_yaml` for retry context | Retry quality | Low |
| 2 | Switch validate-entities to use conversation_id | Scalability | Low |
| 9 | Remove unnecessary auth from store-entities | Cosmetic | Low |
