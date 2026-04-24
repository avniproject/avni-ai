# Handover — Avni App Configurator (Dify + avni-ai)

**Branch:** `app-configurator-dev`
**Date:** 2026-04-23
**Tracking issue:** [avniproject/avni-ai#45 — Spike: Evaluate Claude Managed Agents as alternative orchestrator](https://github.com/avniproject/avni-ai/issues/45)

## TL;DR

- We built a chat-first Avni configurator as a Dify agentic workflow calling a FastAPI/FastMCP tool service (this repo).
- Spec → bundle → upload works end-to-end for simple programs. Complex configuration (rules, reports, skip-logic, formElement specials) is brittle, and the Dify orchestration has become difficult to debug and extend.
- Next we would attempt re-architecting the orchestration using Claude-managed agents. The tool service, prompts, knowledge base, and domain learnings are assets we keep; the Dify workflow is not.
- This doc tells the next owner what to keep, what to throw away, and what's half-built.

---

## 1. What we built

- **avni-ai** (this repo) — stateless FastAPI/FastMCP server exposing ~55 endpoints: parsers, entity/spec/bundle stores, bundle generator, validators, knowledge search, form/rule/report generators, admin tooling. Code under `src/`. OpenAPI contract at `dify/avni-ai-tools-openapi.yaml`.
- **Dify workflow** — `dify/Avni [Staging] Sub-Agentic Assistant.yml`. Visual orchestrator, chat UI, conversation state, agent nodes, human gates. Staging URL: https://cloud.dify.ai/app/0b859aeb-9c7b-4881-b9fc-3769e64de168/workflow
- **Knowledge base** — `dify/knowledge_base/AI_ASSISTANT_KNOWLEDGE_BASE/`. Markdown reference material the RAG node searches.
- **Extracted prompts** — `prompts/*.txt`. Seven sub-agent system prompts already lifted out as plain text (see §5).

End-to-end flow, one line: user message → Orchestrator classifies → dispatcher selects one of six sub-agents → agent calls tool endpoints → validator gate → loop or exit → answer.

---

## 2. Why we're switching away from Dify

Concrete pain points. Framed as "lessons for the next orchestration choice," not Dify-bashing.

1. **Control flow is a state machine smeared across YAML.** `active_phase`, `agent_loop_active`, `spec_awaiting_user_input`, `last_gate_status`, `agent_memory` — all exist only because Dify can't hold control flow in code. Every new routing rule adds an IF/ELSE node plus an Assigner. Debugging means reading a ~5000-line graph.
2. **Agent nodes cannot call auth'd tools.** We store the Avni auth token server-side keyed by `conversation_id` (`src/auth_store.py`) and every tool resolves it itself. Every sub-agent lost native auth and gained a silent dependency.
3. **No sub-workflow imports.** Reused logic is copy-pasted across graphs, or called back via HTTP-to-self (200–500 ms overhead per call).
4. **Prompt-length + editing UI.** Long system prompts get injected as variables. The prompt editor is cramped; diffing revisions is manual.
5. **Dify's built-in doc extractor skipped content.** We moved parsing server-side (`src/bundle/scoping_parser.py`).
6. **YAML-config vs. code-file friction.** For developers used to code files, editing a large visual graph is fighting the tool.
7. **Loops + human-in-the-loop interact badly.** The `spec_awaiting_user_input` short-circuit lives in three places (agent prompt, classifier IF/ELSE, assigner). Drift between them is the top source of "agent stuck" incidents — see the `stuck_*.json` dumps at the repo root.
8. **Limited observability.** We built `/agent-log` because Dify's built-in run view doesn't survive across turns.

Call-it-as-it-is, from the cohort notes: *"Untangling knots within the Agentic workflow is getting increasingly difficult."*

---

## 3. What to keep — tool service maturity grading

Grade each endpoint before assuming it works. Source of truth: `dify/avni-ai-tools-openapi.yaml`, handlers in `src/handlers/`.

### Solid — keep as-is

- **Auth store** — `store_auth_token` (`src/auth_store.py`). TTL store, trivial.
- **SRS parser** — `parse_srs_file` (`src/bundle/scoping_parser.py`). Deterministic parse of Excel scoping docs → entities. Battle-tested on MCH, APF, Goonj, CSJ, Kshamata, Yenepoya.
- **Handle-not-payload store + sectional access** — `store_entities`, `get_entities_section`, `update_entities_section`, `get_spec`, `get_spec_section`, `update_spec_section`, `get_bundle_files`, `get_bundle_file`, `put_bundle_file`. Biggest single token-saver.
- **Spec generator** — `generate_spec` (`src/bundle/spec_generator.py`).
- **Bundle generator** — `generate_bundle` (`src/bundle/generator.py`). NOOP guard prevents wiping downstream edits unless `force=true`.
- **Validators** — `validate_entities`, `validate_spec`, `validate_bundle` (`src/bundle/validators.py`, `src/bundle/spec_validator.py`).
- **Spec ↔ bundle converters** — `spec_to_entities`, `bundle_to_spec`. Round-trip for patching.
- **Patching** — `patch_bundle`, `put_bundle_file`. Surgical edits.
- **Upload + status** — `upload_bundle`, `upload_status/{task_id}`. Async with blocking-wait.
- **Existing config fetch** — `get_existing_config`, `download_bundle_b64` (`src/services/avni/config_fetcher.py`). Section-filterable, item-capped.
- **Knowledge search** — `knowledge_search`. RAG over markdown KB.
- **Ambiguity flow** — `enrich_spec`, `apply_ambiguity_answers`, `resolve_ambiguities`, `get_ambiguities`.
- **Activity log** — `append_agent_log`, `get_agent_logs` (`src/handlers/log_handlers.py`). Per-conversation trace, 24h TTL.
- **State diff** — `entity_diff`. Per-turn diff vs last-uploaded baseline. Drives dispatcher short-circuits.
- **Pipeline gate** — `validate_pipeline_step` (`src/handlers/pipeline_gate.py`). Read-only validator after each writer. Works today — re-examine whether a Claude-driven orchestrator still needs an HTTP-level gate.
- **Silo + sandbox** — `execute_python`, `read_silo_file`. Per-conversation Python sandbox; useful for bulk ops.

### Partial / rough edges — happy-path only, brittle elsewhere

- **Rules generation** — `generate_rule`, `validate_rule` (`src/handlers/rules_handlers.py`). Known correctness gaps: visit scheduling wrong or missing (#40), skip logic requires a manual "Validate & Generate" re-prompt (#42).
- **Reports** — `generate_report_cards` (`src/handlers/reports_handlers.py`). Report cards + dashboards produced, but layout, grouping, and custom queries are thin.
- **Skip logic** — `generate_skip_logic`. Often returns rules that fail `validate_rule` without the explicit re-prompt.
- **Form generation** — `generate_form` (`src/handlers/form_designer_handlers.py`). Form JSON works, but **formElement specials** are inconsistent: `keyValues` (units, `highNormal`/`lowNormal`, `highAbsolute`/`lowAbsolute`), `validFormat` regex, `durationOptions`, `QuestionGroup`/`RepeatableQuestionGroup` nesting. `AvniFormElementValidatorPrompt.md` at repo root is a post-hoc validator attempt; not wired everywhere.
- **Bundle-config agent path** — surgical form edits via `put_bundle_file` work, but the agent sometimes regenerates whole forms it could have patched.
- **Chat SRS / guided flow** — `chat_srs_init_session`, `chat_srs_update_section`, `chat_srs_build_entities`. Sector defaults in `src/utils/sector_templates.py`. Not on the main path.
- **Admin agent endpoints** — `src/tools/admin/*`. CRUD works individually; agent-driven flows are ad-hoc.

### Stub / aspirational — referenced but thin

- **Inspector** — `src/handlers/inspector_handlers.py`. Mostly calls existing-config + bundle-file. Prompt promises more than the tools deliver.
- **Bulk admin** — `src/handlers/bulk_admin_handlers.py`. Lightly exercised.
- **DSPy evaluation framework** — `src/dspy/`. Early experiment, not in the hot path.

Rule of thumb: when in doubt, run the endpoint and read the handler. Don't trust the prompt.

---

## 4. What to discard

- The Dify workflow YAML as orchestrator. Keep it only as a reference for routing rules and per-agent tool manifests.
- All `conversation_variables` in that YAML — they are workarounds for the lack of in-code state.
- IF/ELSE, Assigner, fail-branch, and loop-break nodes — replace with plain Python.
- `agent_memory` — Dify-specific short-term memory hack.
- The HTTP-call-to-self sub-workflow pattern.
- Dify's "agent node" abstraction in general — model sub-agents as Anthropic SDK calls with tool manifests.

---

## 5. Prompts + tool manifests — extraction checklist

Already extracted to `prompts/`:

| File | Role | Dify node ID | Lines |
|---|---|---|---|
| `prompts/orchestrator.txt` | Top-level classifier: RAG / ASSISTANT / BUNDLE_SETUP / OUT_OF_SCOPE | `1757492907627` | 181 |
| `prompts/spec-agent.txt` | Parse SRS → entities → YAML spec, drive gap-fix dialog | agent `1800000000110` | 97 |
| `prompts/bundle-config-agent.txt` | Form-level surgical edits on the generated bundle | agent `1800000000210` | 239 |
| `prompts/rules-agent.txt` | Form / visit-schedule / skip-logic rule generation and validation | agent `1800000000310` | 346 |
| `prompts/reports-agent.txt` | Report cards, dashboards | agent `1800000000410` | 243 |
| `prompts/config-inspector-agent.txt` | Read-only audit of generated config | agent `1800000000510` | 269 |
| `prompts/admin-agent.txt` | Location hierarchy, users, catchments | agent `1800000000610` | 275 |

Before porting: diff each file against the current Dify YAML (these text copies may be stale). For each agent also extract from the YAML: model, temperature, memory window size, and the **tool list** — the tool list is the real design artifact, not every agent sees every endpoint.

Worth porting verbatim from the orchestrator prompt: the HARD OVERRIDE rule, the misrouting-trap list, and the decision tree. These are earned judgment from many iterations.

---

## 6. Architectural learnings that carry forward

Generic patterns. They work regardless of orchestration tool.

- **Handles, not payloads.** Heavy state (entities, spec YAML, bundle ZIP) lives server-side keyed by `conversation_id`. Tools return a summary and a handle; the LLM never sees the bytes.
- **Sectional retrieval + surgical edits.** `get_spec_section`/`update_spec_section`, `get_bundle_file`/`put_bundle_file`. One section, one edit. Small context, preserves other work.
- **Deterministic rails around LLM judgment.** Parse, validate, and generate in code whenever the schema is known. LLM fills only the fuzzy middle.
- **Sub-agent archetypes.** Classifier → Planner → Synthesizer → Patcher → Inspector. Each has a narrow job, clear I/O contract, bounded iterations.
- **Read-only validation gate after every writer.** `validate_pipeline_step` runs after each sub-agent. Agents see gate errors as `[GATE ERROR]` on the next turn.
- **Per-turn state diff.** `entity_diff` lets the dispatcher skip Rules/Reports on unchanged state.
- **Noop + force guards.** `generate_bundle` refuses to wipe downstream edits unless `force=true`. Apply this anywhere a cheap regeneration could destroy surgical work.
- **Traceable activity log.** `append_agent_log`/`get_agent_logs` per conversation. Keep even with Claude agents — useful for post-hoc incident reconstruction.

---

## 7. Avni domain gotchas

- **FormatContract must be an object, not a string.** Server silently rejects bundles with string FormatContracts. See `src/schemas/`.
- **Parser workarounds for oddly-formatted SRS.** Yenepoya and Kshamata use unified modelling sheets with odd header offsets — `scoping_parser.py` has explicit handling. New SRS styles need parser-level fixes, not agent retries.
- **YAML spec is the intermediate format.** Every round-trip goes entities → spec → bundle. Don't build tools that shortcut this — it breaks validators and diffing.
- **Concepts are global.** Adding a concept in one form mutates the shared concepts list; patching a form without also patching `concepts.json` produces a broken bundle.
- **FormMappings are fragile.** `src/services/avni/form_mapping_processor.py` handles program/encounter/subject form wiring. Changes here break in non-obvious ways.
- **Bundle canonicalization.** `src/bundle/canonical_zip.py` normalizes ZIP byte layout for stable diffs. Keep this.
- **Deterministic UUIDs.** `src/bundle/uuid_utils.py` + `full_uuid_remap.py` manage stable UUIDs across regenerations; bypassing them silently breaks reconciliation.

Longer-form design notes: `docs/app_configurator/` — especially `DifyWorkflowLearnings.md`, `TechApproachEvaluation.md`, `avni-ai-overhaul-plan.md`.
