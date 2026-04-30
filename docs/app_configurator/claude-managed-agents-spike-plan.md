# Spike: Claude Managed Agents as an Alternative Orchestrator for the Avni App Configurator

> **Tracks:** [avniproject/avni-ai#45](https://github.com/avniproject/avni-ai/issues/45)
> **Author:** Siddharth Harsh Raj · 2026-04-30
> **Status:** Plan only — no prototype code yet
> **Decision sought from spike:** adopt / hybrid / reject

---

## 0. TL;DR

The spike will build a minimal end-to-end prototype that ingests a real scoping document (Yenepoya or Kshamata SRS), holds a multi-turn clarification conversation, and emits an Avni bundle byte-identical to what the current Dify v3 flow produces.

Recommended target runtime: **Anthropic Claude Managed Agents** (hosted REST API, beta header `managed-agents-2026-04-01`) — it is the product the issue names, gives us a managed sandbox per session, and lets us reuse the existing FastMCP server **as a remote MCP server** without writing a new tool-execution layer.

We will keep the existing `avni-ai` FastMCP server as the single source of bundle-generation logic. The spike does **not** rewrite generators, validators, or the spec layer; it only swaps the orchestrator that drives them. The deliverable is a head-to-head comparison vs. Dify on latency, cost/run, tool-call accuracy, failure modes, dev ergonomics, observability, and the surgical-edit / Plan-Emulate-Verify (PEV) loop already documented in `PlanEmulateValidateSelf-HealingAgenticFlow.md`.

If Managed Agents access is blocked (it's still in beta), the same prototype will run on the **Claude Agent SDK** (Python in-process library) using identical agents, skills, and prompts — that fallback is wired into the plan from day one so the spike is never blocked on access.

---

## 1. What we're spiking and why

### 1.1 The problem with the current Dify flow

`docs/app_configurator/avni-ai-iterative-dev-plan.md`, `DifyWorkflowLearnings.md`, and `dify-agent-restructure-bundle-patch-plan.md` document what `App Configurator [Staging] v2` looks like today: a 42-node `advanced-chat` workflow with three agent nodes (Spec / Review / Error) wrapped around explicit HTTP-request nodes that call `avni-ai` endpoints. The pain points the issue calls out are real and reproducible:

| # | Dify pain point | Where it bites |
|---|---|---|
| 1 | Sub-workflow imports add 200–500 ms each (HTTP call to self) | Every `/generate-bundle` round-trip |
| 2 | Auth token is injected as an in-memory conversation variable | All authed calls — fragile across restarts |
| 3 | Prompt-length workarounds: prompt injected as a variable into the agent node | Spec Agent system prompt is 4 KB+ |
| 4 | Agent nodes only support non-auth tools natively | Forces explicit HTTP nodes for everything authed |
| 5 | YAML-based config vs. page-wise code → developer adoption friction | New contributors can't navigate the YAML |
| 6 | Entity extractor comprehensiveness / skipped content (e.g. Durga Excel: 0 programs extracted) | Empty bundles, warnings on every run |
| 7 | Sticky bugs uncovered in emulation runs (`org_name` not threaded, `validate-entities` body too large, no clean-slate path, wrong DELETE body, timeout/`No` re-loop, polling exit silent, `spec_yaml` not persisted) | Documented in `DifyWorkflowLearnings.md` §1–9 |

These aren't all Dify's fault — some are wiring bugs we own — but they each cost a developer-day to find and another to fix because the orchestrator is a YAML-defined visual graph rather than testable code.

### 1.2 What Claude Managed Agents (and the Agent SDK) gives us

From the docs ([Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview), [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)):

| Primitive | Managed Agents (hosted) | Agent SDK (in-process) |
|---|---|---|
| Runtime | Anthropic-hosted container per session | Python/TS library inside our process |
| Built-in tools | `bash`, `read`, `write`, `edit`, `glob`, `grep`, `web_fetch`, `web_search` (toolset `agent_toolset_20260401`) | Same set, plus `Monitor`, `AskUserQuestion`, `Agent` (sub-agent) |
| Custom tools | JSON-schema definitions; agent emits a tool-use event, host executes, posts back result | In-process Python/TS functions |
| MCP servers | `mcp_servers: [{type:"url", name, url}]` + `mcp_toolset` + `vault_ids` for auth | `mcp_servers={...}` config (stdio, SSE, or HTTP) |
| Skills | Pre-built (`anthropic`, e.g. `xlsx`, `pdf`, `docx`, `pptx`) **and** custom skills uploaded by `skill_id`, max 20 per session | Filesystem `.claude/skills/*/SKILL.md`, auto-discovered |
| File ingestion | Files API → mount paths in session container (`/workspace/...`), max 100 per session, read-only | Files live on the host filesystem |
| Sessions | Server-side event log; user → session events stream via SSE; pause / interrupt / resume / archive | JSONL on host filesystem |
| Sub-agents | `callable_agents` (research preview) | `agents={"name": AgentDefinition(...)}` |
| Auth for MCP | Vaults — Anthropic refreshes OAuth tokens | Whatever the host process has |
| Observability | Server-side event log, `session.error` events, beta endpoints (rate limit: 600 reads / 300 writes per minute per org) | OpenTelemetry / your own logging |

Three properties are decisive for this spike:

1. **MCP-as-tooling.** Our `avni-ai` FastMCP server already speaks streamable HTTP (`fastmcp.FastMCP(stateless_http=True)`, see `src/main.py:106`). One agent definition + one `mcp_toolset` entry exposes all 50+ existing endpoints to the agent, with no glue code. We do not re-implement bundle generation; we point Claude at it.
2. **Skills with progressive disclosure.** `avni-skills` is already a Skills repo (the `srs-bundle-generator` directory is a `SKILL.md` + scripts + training data). Either:
   - Upload as **custom skills** to Anthropic and reference by `skill_id` (Managed Agents path), or
   - Symlink into `.claude/skills/` (Agent SDK path).
   No copy-paste from `avni-skills` into prompts is needed.
3. **Built-in multi-turn + clarification.** `AskUserQuestion` is a first-class tool: the agent asks multiple-choice questions and the host pauses execution until the user answers, eliminating the bespoke human-input + No/timeout routing nodes that misbehave today (`DifyWorkflowLearnings.md` §6).

### 1.3 Why not just stick with Dify for this slice?

Dify is the production system today. We are not migrating off it. The spike's job is to test whether a code-first orchestrator removes enough friction in the seven pain points above to be worth keeping in our toolkit (hybrid: Dify for the production conversational chat, Claude Managed Agent for batched / API-driven SRS-to-bundle runs), or whether it's a wholesale better runtime for the App Configurator path. The decision is made *after* the comparison matrix in §6 is filled in; the plan does not pre-commit.

---

## 2. Scope

### 2.1 In scope (issue success criteria)

- [ ] Prototype ingests **at least one** real scoping doc (Yenepoya or Kshamata SRS, both available in `tests/`/`examples/` already used by `tests/emulation/app_configurator_flow.py`) and produces a valid Avni bundle.
- [ ] Agent holds **multi-turn** clarification with the user — minimum two clarification rounds covered (one entity-level, one form-field level).
- [ ] Agent reuses **existing `avni-ai` tools** rather than reimplementing bundle generation, validation, or upload logic.
- [ ] `avni-skills` is loaded as Skills / system prompts — **no copy-paste**.
- [ ] Documented comparison vs. current Dify flow on:
  1. End-to-end latency (median, p95)
  2. Cost per run (tokens × model price)
  3. Tool-call accuracy (right tool, right arguments, on first try)
  4. Failure modes & recovery
  5. Developer ergonomics (LOC, time-to-first-run, time-to-modify-a-prompt)
  6. Observability (what's loggable, traceable)
  7. Surgical edits / PEV loop fidelity (matched against `PlanEmulateValidateSelf-HealingAgenticFlow.md`)

### 2.2 Out of scope (issue + extra guardrails)

- Production migration off Dify
- UI / chat frontend beyond what's needed to demo multi-turn (CLI is fine)
- Performance tuning — prototype only
- Re-implementing bundle generators, validators, or `/upload-bundle`
- Any changes to `avni-server` contracts

### 2.3 Deliverables (issue, expanded)

1. **Working prototype** in branch `spike/claude-managed-agents` of `avni-ai`, under `src/orchestrators/claude_agent/`. Self-contained — toggleable via `AVNI_ORCHESTRATOR=claude` env var so it can be A/B-run against the same backend.
2. **Comparison writeup** at `docs/app_configurator/claude-managed-agents-spike-results.md` with the seven-axis matrix populated from real runs.
3. **Demo recording or transcript** of a multi-turn run on Yenepoya or Kshamata, plus a recording of the Dify run on the same input, for side-by-side review.
4. **Recommendation memo** (last section of the writeup): adopt / hybrid / reject, with explicit rationale tied to the matrix numbers and the seven Dify pain points from §1.1.

---

## 3. Architecture

### 3.1 Big picture

```
                     ┌──────────────────────────────────────┐
                     │       Spike CLI (Python)             │
                     │  - reads scoping doc paths           │
                     │  - prints agent stream to terminal   │
                     │  - records run metrics → JSON        │
                     └───────────────────┬──────────────────┘
                                         │
                       ┌─────────────────┴───────────────────┐
                       ▼                                     ▼
        ┌────────────────────────────┐        ┌────────────────────────────┐
        │  Path A: Managed Agents     │        │  Path B: Agent SDK (local) │
        │  REST + SSE                 │        │  Python in-process         │
        │  (preferred)                │        │  (fallback / parity test)  │
        │                             │        │                            │
        │  Files API uploads          │        │  cwd= /tmp/avni-spike      │
        │  agent_toolset_20260401     │        │  with .claude/skills/      │
        │  mcp_toolset → avni-ai MCP  │        │  mcp_servers={             │
        │  custom skills (avni-skills)│        │    "avni-ai": {url=...}    │
        │  vault_ids → auth-token     │        │  }                         │
        │                             │        │  AskUserQuestion           │
        └─────────────┬───────────────┘        └─────────────┬──────────────┘
                      │                                      │
                      └──────────────────┬───────────────────┘
                                         ▼
                      ┌──────────────────────────────────────┐
                      │    avni-ai FastMCP server (HTTP)     │
                      │  src/main.py — same endpoints as Dify│
                      │   /parse-srs-file, /validate-entities│
                      │   /generate-spec, /validate-spec     │
                      │   /spec-to-entities, /generate-bundle│
                      │   /validate-bundle, /upload-bundle   │
                      │   /upload-status/{task_id}, …        │
                      └──────────────────┬───────────────────┘
                                         ▼
                      ┌──────────────────────────────────────┐
                      │   avni-server (staging)              │
                      │   /api/importMetaData                │
                      └──────────────────────────────────────┘
```

Crucial property: the **green box (`avni-ai` FastMCP server) is unchanged**. Both the Dify production flow and the spike's two paths point at the same endpoints. Any bundle-generation regressions surface in both flows identically — we are measuring orchestrator quality, not generator quality.

### 3.2 Agents (one per stage — same contracts as Dify v3)

The Dify v3 plan in `avni-ai-iterative-dev-plan.md` already names three agents — **Spec Agent**, **Review Agent**, **Error Agent**. We mirror the same three, so the comparison is apples-to-apples.

| Agent | System prompt source | Tools (via `mcp_toolset`) | Skills attached | Iter cap |
|---|---|---|---|---|
| **Spec Agent** | `src/orchestrators/claude_agent/prompts/spec_agent.md` (mirrors Dify v3 system prompt) | `parse-srs-file`, `store-entities`, `validate-entities`, `apply-entity-corrections`, `generate-spec`, `validate-spec`, `bundle-to-spec`, `enrich-spec`, `api/existing-config`, `knowledge-search` | `srs-bundle-generator`, `project-scoping`, `implementation-engineer` | 5 |
| **Review Agent** | `prompts/review_agent.md` | `validate-bundle`, `bundle-to-spec`, `download-bundle-b64`, `bundle-files`, `bundle-file`, `execute-python` | `architecture-patterns`, `backend-architecture` | 3 |
| **Error Agent** | `prompts/error_agent.md` | `upload-status`, `api/existing-config`, `execute-python`, `generate-bundle`, `validate-bundle` | `support-engineer`, `support-patterns` | 3 |

A fourth orchestrator agent — **Coordinator** — sits above these and decides which sub-agent to call. In Managed Agents this is a `callable_agents` tree (research-preview feature; if access is unavailable we fall back to a single agent with all tools and rely on system-prompt routing, which the [Autoolize playbook](https://autoolize.com/blog/claude-agent-sdk-production-playbook/) recommends as Pattern 1: router + specialist).

### 3.3 Skills wiring (zero copy-paste)

`avni-skills` already ships `SKILL.md` files with frontmatter (`name`, `description`, `version`). We expose them three ways:

- **Managed Agents (custom skills):** `scripts/spike/upload_avni_skills.py` walks `avni-skills/`, packages each subdir as a custom skill via the Skills upload endpoint, and writes the resulting `skill_id`s to `src/orchestrators/claude_agent/skills.json`. The agent definition references those IDs.
- **Agent SDK (filesystem):** prototype's `cwd` is set to a temp dir containing `.claude/skills/` symlinked from a checkout of `avniproject/avni-skills`. `setting_sources=["project"]` to pick them up. (See [Skills in the SDK](https://code.claude.com/docs/en/agent-sdk/skills).)
- **Anthropic pre-built skills:** add `xlsx` and `pdf` as `{"type":"anthropic","skill_id":"xlsx"}` so the agent can read scoping spreadsheets and form PDFs out of the box (instead of forcing every agent to learn `openpyxl`).

### 3.4 Tool surface — exclusively MCP, never re-implemented

The Dify flow today calls `avni-ai` two ways: explicit HTTP nodes and Dify "tools" registered from OpenAPI. In the spike we go through MCP only. Concretely:

```python
# src/orchestrators/claude_agent/agent_definition.py
spec_agent = client.beta.agents.create(
    name="Avni Spec Agent",
    model="claude-opus-4-7",       # opus for spec reasoning
    system=open("prompts/spec_agent.md").read(),
    mcp_servers=[
        {
          "type": "url",
          "name": "avni-ai",
          "url": os.environ["AVNI_AI_MCP_URL"],   # e.g. https://avni-ai.staging/.../mcp
        }
    ],
    tools=[
        {"type": "agent_toolset_20260401",
         "default_config": {"enabled": False},
         "configs": [{"name": n, "enabled": True} for n in ["bash", "read", "write", "glob"]]},
        {"type": "mcp_toolset", "mcp_server_name": "avni-ai"},
        # AskUserQuestion is automatic in Managed Agents — surfaced as a session event.
    ],
    skills=[
        {"type": "anthropic", "skill_id": "xlsx"},
        {"type": "anthropic", "skill_id": "pdf"},
        {"type": "custom", "skill_id": SKILLS["srs-bundle-generator"], "version": "latest"},
        {"type": "custom", "skill_id": SKILLS["project-scoping"], "version": "latest"},
        {"type": "custom", "skill_id": SKILLS["implementation-engineer"], "version": "latest"},
    ],
)
```

**Auth** for the avni-server endpoints (`/upload-bundle`, `download-bundle-b64`, `DELETE /api/implementation`) is handled via the existing `/store-auth-token` endpoint. The spike CLI POSTs the auth token before sending the first user event, indexed by `conversation_id`. This is the same pattern as production Dify and avoids leaking auth into the agent's prompt or arguments. (The vaults primitive is for OAuth-style MCP auth, not symmetric tokens, so we don't need it here.)

### 3.5 File ingestion

```python
# scripts/spike/run_one.py — sketch
file_ids = []
for path in args.scoping_docs:               # XLS, PDF, images
    with open(path, "rb") as f:
        meta = client.beta.files.upload(file=f).id
        file_ids.append(meta)

session = client.beta.sessions.create(
    agent=spec_agent.id,
    environment_id=env.id,
    resources=[
        {"type": "file", "file_id": fid, "mount_path": f"/workspace/{Path(p).name}"}
        for fid, p in zip(file_ids, args.scoping_docs)
    ],
)
```

The agent then sees `/workspace/Yenepoya_SRS.xlsx`. Its first action is the `xlsx` Anthropic skill, *or* a `parse-srs-file` MCP call against `avni-ai` — we let the system prompt prefer the latter so the parser logic stays in `avni-ai/src/handlers/extraction_handlers.py` (single source of truth for extraction rules).

### 3.6 Multi-turn clarification

```
user.message → (agent reasoning) → agent emits AskUserQuestion event
                                      ↓
                          Spike CLI prints the multi-choice options
                                      ↓
                            User picks one (or types free text)
                                      ↓
                          CLI sends user.message back to session
                                      ↓
                                  Agent continues
```

Two clarification points are mandatory in the demo run:
1. **Entity-level:** "I extracted 3 subject types but Encounter X has no subject_type linked. Which subject type should it belong to: Individual / Household / Mother?" (mirrors Durga bug from `DifyWorkflowLearnings.md` §5.)
2. **Form-field level:** "Field `Number of children` has no validation. Should it be: non-negative integer / non-negative decimal / range 0–20?" (this is exactly the LLM-reasoner enrichment step in `avni-ai-iterative-dev-plan.md` Phase 1.)

Both surface naturally if the system prompt instructs the agent to call `AskUserQuestion` on any spec-validator warning that has `severity:>=info` and is human-disambiguable.

### 3.7 PEV (Plan-Emulate-Verify) loop fidelity

`PlanEmulateValidateSelf-HealingAgenticFlow.md` describes the self-healing loop the team values: agent generates a plan, emulates the bundle, validates, fixes, retries. Mapping that onto the spike:

| PEV step | Spike implementation |
|---|---|
| **Plan** | Spec Agent calls `/generate-spec` → YAML spec |
| **Emulate** | `/spec-to-entities` → `/generate-bundle` (in memory) → bundle b64 |
| **Verify** | Review Agent calls `/validate-bundle` + `/bundle-to-spec` (round-trip diff) + `/execute-python` for ad-hoc invariants |
| **Fix** | Spec Agent receives the validator's structured errors and revises the YAML, max 3 retries |
| **Commit** | `/upload-bundle` after Review Agent approves |
| **Heal** | On `upload-status: failed`, Error Agent gets `/upload-status` payload + last spec, attempts a targeted fix, retries once, else escalates to user via `AskUserQuestion` |

The retry caps and the structured-error contract are the same as the Dify Spec Agent's `iter ≤ 5` limit — gives a fair benchmark.

---

## 4. Tooling decisions and rationale

### 4.1 Why Managed Agents over the Agent SDK as the primary path

| Decision factor | Managed Agents | Agent SDK | Winner |
|---|---|---|---|
| Issue requirement | Issue says "Claude Managed Agents" | — | Managed Agents |
| Server-side session log + replay | ✅ Anthropic-hosted, queryable via REST | ❌ Local JSONL only | Managed Agents |
| Long-running async jobs (bundle uploads can take minutes) | ✅ Pause / resume / interrupt built in | ⚠️ Have to manage subprocess lifecycle | Managed Agents |
| Sandbox isolation per run | ✅ Container per session | ⚠️ Process inherits whatever cwd has | Managed Agents |
| Beta access risk | ❌ Beta header required, may be gated | ✅ GA library | Agent SDK |
| Local dev iteration speed | ⚠️ Round-trip via API for every change | ✅ Pure Python, hot reload | Agent SDK |
| Multi-tenancy (future SaaS) | ✅ Already isolated per session | ⚠️ Build it yourself | Managed Agents |

**Conclusion:** Managed Agents is the primary build target. The Agent SDK gets a thin parity adapter so the same `agent_definition.py` config can run both. This costs us roughly half a day extra and de-risks the spike from beta-gate or rate-limit issues, **and** gives us the parity test that proves our orchestrator code isn't accidentally relying on hosted-only features. The community is converging on this pattern: prototype with the SDK, production on Managed Agents (Anthropic's [own positioning](https://code.claude.com/docs/en/agent-sdk/overview#agent-sdk-vs-managed-agents) recommends exactly this).

### 4.2 Why MCP over OpenAPI tool definitions

Dify already supports OpenAPI tool registration. We could replicate that. We don't, because:
- MCP is a single config block on the agent definition — OpenAPI per-tool is per-tool registration overhead.
- MCP carries auth via vaults / per-session headers cleanly. OpenAPI in Dify forced us to inject the auth token into a conversation variable (Dify pain point #2).
- `avni-ai` is *already* an MCP server — `FastMCP(name="Avni AI Server", stateless_http=True)` (`src/main.py:106`). Zero new code.

### 4.3 Why we keep `avni-ai`'s endpoints, not push logic into the agent

The whole `enhancements_to_be_made.md` design — JSONL → spec → bundle, with deterministic validators in between — is built so that the LLM does inference and the Python deterministically generates. That contract holds in this spike too:

- Generators stay deterministic (`generator.py`, `spec_generator.py`, `spec_parser.py`, `spec_validator.py`).
- LLM is restricted to: clarification, entity correction suggestions, field-property inference, NL-to-spec-edit translation, error diagnosis.
- This is **TECH-01** from `TechApproachEvaluation.md` ("Use LLM for understanding, code for execution") and the Autoolize Pattern 5 ("structured output, not free-text" — agent emits tool calls; tools return structured JSON; agent reads JSON; agent emits next tool call).

### 4.4 Cost & latency expectations (going-in priors)

From benchmarks we can find publicly:
- Claude Opus 4.7 at $15/M input / $75/M output — premium model.
- Sonnet 4.6 at $3/M input / $15/M output — 5× cheaper.
- Per the Autoolize playbook, router (Haiku 4.5) → specialist (Sonnet 4.6) gets roughly 40 % cost reduction vs. one big Opus agent. For a Yenepoya-sized run we expect ~30–80 K input + ~5–15 K output tokens once skills are progressively loaded.
- Cost expectation per full run: **$0.20–$0.60** on Sonnet, **$1–$3** on Opus.
- Latency: Managed Agents adds container provisioning (~5–10 s on cold sessions) but amortises over a multi-turn conversation. Dify cold-start is comparable. We will measure, not assume.

These are the priors going in; the comparison matrix in §6 will replace them with measured numbers.

---

## 5. Milestones and execution plan

10 working days end-to-end, single engineer. Each milestone has a hard exit criterion so we can stop and report if any one fails.

### M0 — Access + scaffolding (Day 1, half day)

- [ ] Confirm Managed Agents beta access on the Anthropic account: `curl https://api.anthropic.com/v1/agents -H 'anthropic-beta: managed-agents-2026-04-01'`. If 403, switch to SDK-only path immediately.
- [ ] Create branch `spike/claude-managed-agents`.
- [ ] Add `src/orchestrators/claude_agent/` skeleton: `agent_definition.py`, `prompts/`, `skills/`, `cli.py`.
- [ ] Add a feature flag `AVNI_ORCHESTRATOR` (`dify` | `claude` — default `dify`).

**Exit:** `python -m src.orchestrators.claude_agent.cli --help` runs.

### M1 — Skills upload + agent definition (Day 1.5–2)

- [ ] `scripts/spike/upload_avni_skills.py` — packages `srs-bundle-generator`, `project-scoping`, `implementation-engineer`, `support-engineer` from a local `avni-skills` checkout, uploads each as a custom skill, persists `skill_id`s.
- [ ] `agent_definition.py` — three agents (Spec / Review / Error) created and versioned; environment created with Python 3.11 + the standard toolset.
- [ ] Smoke run: a session that does nothing but `bash echo "hello"` succeeds.

**Exit:** all three agents materialise as version 1; smoke session returns idle → running → idle.

### M2 — MCP wiring + scoping doc ingestion (Day 3)

- [ ] Stand up `avni-ai` FastMCP server reachable from Anthropic infra. Two options:
  - **Cloudflare tunnel** to local dev box (`cloudflared tunnel --url http://localhost:8023`) — simplest, no infra.
  - **Use existing staging URL** `https://avni-ai.staging…/mcp` (preferred if it exposes HTTP MCP — confirm).
- [ ] Configure agents' `mcp_servers: [{type:"url", name:"avni-ai", url: <tunnel>}]`.
- [ ] Spike CLI uploads Yenepoya `.xlsx` via Files API and mounts at `/workspace/Yenepoya_SRS.xlsx`.
- [ ] First user event: "Read the file at /workspace/Yenepoya_SRS.xlsx and call avni-ai's parse-srs-file tool. Confirm what entity counts you found."

**Exit:** transcript shows agent calling `parse-srs-file`, returning entity counts that match `tests/emulation/app_configurator_flow.py` baseline (i.e. matches the Dify entity extractor output for the same input within ±1 entity per type).

### M3 — Multi-turn spec loop (Day 4–5)

- [ ] Spec Agent system prompt — port from Dify v3, with the `org_name` threading and `validate-entities` `conversation_id` fixes from `DifyWorkflowLearnings.md` baked in.
- [ ] First clarification (entity-level missing subject_type) — agent emits `AskUserQuestion`, CLI displays options, user replies, agent continues.
- [ ] Second clarification (form-field property) — agent uses `enrich-spec` and asks before committing if confidence is < threshold.
- [ ] Loop terminates with `validate-spec` returning `valid:true` and the agent printing the YAML spec.

**Exit:** end-to-end transcript with two clarifications and a valid spec, no errors, ≤ 5 agent iterations per loop.

### M4 — Bundle generation + Review + Upload (Day 6)

- [ ] `spec-to-entities` → `generate-bundle` → Review Agent invoked.
- [ ] Review Agent uses `validate-bundle` and `bundle-to-spec` round-trip; `execute-python` for one structural sanity check (e.g., "no formMappings reference a missing form UUID").
- [ ] On approval, `upload-bundle` → polling via `upload-status` → success.
- [ ] On `validate-bundle` failure, Spec Agent corrects (max 3 retries — PEV self-heal).

**Exit:** A bundle is uploaded to staging avni-server and visible in the App Designer. The same bundle, byte-compared via `canonical_zip.py`, equals what the Dify v3 flow produces on the same input (modulo timestamps). Determinism check.

### M5 — Error Agent + intentional failure (Day 7)

- [ ] Inject a known failure mode (e.g. encounter type with no program *and* no subject_type) into the Yenepoya input.
- [ ] Error Agent reads `upload-status` failure payload, identifies cause, emits a fix proposal, retries.
- [ ] On second failure, escalates to the user via `AskUserQuestion`.

**Exit:** transcript shows one auto-recovery and one user-escalation, both reproducibly.

### M6 — Agent SDK parity adapter (Day 7.5–8)

- [ ] `src/orchestrators/claude_agent/sdk_runner.py` — same `agent_definition.py` config, but invoked via `claude_agent_sdk.query` with `mcp_servers={"avni-ai": {...}}` and `setting_sources=["project"]` for filesystem skills.
- [ ] One identical run (Yenepoya input) on both paths.

**Exit:** outputs match within tolerance (same final spec YAML; same uploaded bundle hash). Parity confirmed.

### M7 — Comparison runs + matrix (Day 9)

Two SRSs (Yenepoya + Kshamata) × two paths (Dify, Claude) × three runs each = 12 runs. Capture per run:

- Wall-clock latency (start → upload-status:completed)
- Total tokens in / out, cost at posted prices
- Number of tool calls; tool-call retries; tool-call failures
- Bundle hash + bundle-to-spec round-trip correctness
- Where the agent asked clarifying questions (count, depth)

Median over the 3 runs, with p95 from the 6 runs per (path, doc) pair.

**Exit:** `claude-managed-agents-spike-results.md` matrix populated with real numbers, not estimates.

### M8 — Recommendation memo + demo (Day 10)

- [ ] Recommendation: adopt / hybrid / reject, with explicit rationale tied to the matrix and the seven Dify pain points.
- [ ] 5-minute screencast of the Yenepoya run on both paths, side-by-side.
- [ ] Open a draft PR (do not merge) so reviewers can comment on the prototype code.

**Exit:** PR opened, demo posted to the team channel referenced in the issue.

---

## 6. Comparison matrix template (filled in M7)

The deliverable doc will contain this table fully populated; here are the axes and how each is measured.

| Dimension | Dify v3 | Claude Managed Agents | How measured |
|---|---|---|---|
| **End-to-end latency (median, p95)** | s | s | Stopwatch from first user event to upload-status `completed` |
| **Cost per full run** | USD | USD | Token counts × posted prices; for Dify, sum of LLM nodes' token reports |
| **Tool-call accuracy (right tool, first try)** | % | % | Manual tag of each tool call: correct / wrong tool / wrong args / unnecessary |
| **Tool-call retries on transient errors** | count | count | Count of tool calls flagged as retries by orchestrator logs |
| **Failure modes encountered** | list | list | Free-form, then bucketed (auth / parsing / validation / upload / hallucination) |
| **Self-heal success on injected failure** | yes/no | yes/no | Run M5 scenario on each |
| **Surgical edit (e.g. "rename field X to Y")** | turns | turns | Round-trip count from user request to bundle re-uploaded |
| **PEV loop fidelity** | matches doc? | matches doc? | Compare actual run trace to `PlanEmulateValidateSelf-HealingAgenticFlow.md` |
| **Developer ergonomics (LOC orchestration)** | lines | lines | Count: Dify YAML lines for App Configurator [Staging] v2; Python lines under `src/orchestrators/claude_agent/` excluding prompts |
| **Time-to-first-run from clone** | min | min | Stopwatch a clean clone + setup (excluding access provisioning) |
| **Time-to-modify-a-prompt** | min | min | Change one sentence in spec agent's prompt, rerun: how long? |
| **Observability — replayable session log** | yes/no | yes/no | Can we reproduce a failed run's exact trace from logs alone? |
| **Multi-tenancy story** | how? | how? | Describe what we'd need for SaaS isolation |

---

## 7. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Managed Agents beta access denied / rate-limited | Medium | Blocks primary path | M6 SDK parity adapter — same config runs both. Build the SDK path on Day 1 too if needed. |
| `avni-ai` MCP server not reachable from Anthropic infra | Medium | Blocks tool calls | Cloudflare tunnel as fallback; if Anthropic blocks tunnel egress, run agent locally via SDK path |
| Custom skills upload format changes mid-spike (beta) | Low | Breaks skills | Pin to a known-good version of `anthropic-beta`; if upload fails, switch to SDK filesystem skills (no upload needed) |
| Agent calls wrong tool / hallucinates a non-existent endpoint | Medium | Bundle generation breaks | Tool-loop guardrails per Autoolize Pattern 2: `MAX_TOOL_CALLS=15`, same-args-twice abort, structured-error-on-422 |
| Auth-token leakage into prompts/logs | Low | Security incident | Token never enters conversation; only `/store-auth-token` POST from CLI, indexed by `conversation_id`. Verify by grepping all session events for the literal token before sharing logs |
| Beta API behaviour drift between weeks | Medium | Inconsistent measurements | Pin model to `claude-opus-4-7`/`claude-sonnet-4-6`, pin beta header, do all measurements within 48 hours of each other |
| Claude SaaS PII / India deployment concerns | Low (staging only) | Procurement | Spike runs against staging-only data. Production decision lives in §8. |

---

## 8. What the recommendation will weigh (decision criteria)

**Adopt** Claude Managed Agents as the primary orchestrator for the App Configurator if **all** of the following hold post-spike:

- Bundle correctness on real SRSs ≥ Dify's
- Median latency within 30 % of Dify's, or strictly faster
- Cost per run ≤ 1.5× Dify's at the chosen model tier
- ≥ 4 of the 7 Dify pain points are objectively eliminated (sub-workflow overhead, auth handling, prompt-length workarounds, agent-only-non-auth-tools, YAML adoption friction, entity-extractor comprehensiveness, the bug pile from `DifyWorkflowLearnings.md`)
- Surgical-edit and PEV-loop UX is measurably better
- Self-hosting / data-residency story is acceptable for production roadmap

**Hybrid** (use Dify for chat-driven UX in the Avni webapp, Managed Agents for batched / API-driven SRS-to-bundle automation) if:

- Bundle correctness equal but latency is materially worse on one path
- Multi-tenancy story isn't ready for production but works fine for a backend SaaS pipeline
- Team appetite for two orchestrators is acceptable (we already maintain two: production webapp + emulation harness)

**Reject** (stay on Dify, harden it instead) if:

- Bundle correctness regresses
- Cost > 2× without a quality justification
- Beta surface area is too unstable to commit to a year out
- Ergonomics gain doesn't justify a second runtime

---

## 9. Referenced sources

### Internal docs (this repo)

- [Spike issue (avniproject/avni-ai#45)](https://github.com/avniproject/avni-ai/issues/45)
- `docs/app_configurator/avni-ai-iterative-dev-plan.md` — current architecture, two-stage flow, agent definitions
- `docs/app_configurator/enhancements_to_be_made.md` — JSONL + YAML spec design, validation contracts
- `docs/app_configurator/DifyWorkflowLearnings.md` — nine concrete Dify v3 bugs from emulation runs
- `docs/app_configurator/dify-agent-restructure-bundle-patch-plan.md` — agent restructuring plan
- `docs/app_configurator/PlanEmulateValidateSelf-HealingAgenticFlow.md` — PEV loop design
- `docs/app_configurator/TechApproachEvaluation.md` — A/B/C/D approach scoring (A=79 %, D=53 %)
- `docs/app_configurator/RevisedImplementationPlan.md` — JSONL intermediate, MongoDB asset store, story split
- `src/main.py` — FastMCP server, every endpoint already exposed
- `tests/emulation/app_configurator_flow.py` — emulation harness used as reference run
- [`avniproject/avni-skills` srs-bundle-generator skill](https://github.com/avniproject/avni-skills/tree/main/srs-bundle-generator)

### Anthropic primary docs

- [Claude Managed Agents — Overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Managed Agents — Agent setup](https://platform.claude.com/docs/en/managed-agents/agent-setup)
- [Managed Agents — Sessions](https://platform.claude.com/docs/en/managed-agents/sessions)
- [Managed Agents — Tools](https://platform.claude.com/docs/en/managed-agents/tools)
- [Managed Agents — MCP connector](https://platform.claude.com/docs/en/managed-agents/mcp-connector)
- [Managed Agents — Files](https://platform.claude.com/docs/en/managed-agents/files)
- [Managed Agents — Skills](https://platform.claude.com/docs/en/managed-agents/skills)
- [Claude Agent SDK — Overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Claude Agent SDK — Skills](https://code.claude.com/docs/en/agent-sdk/skills)
- [Claude Agent SDK — User input & AskUserQuestion](https://code.claude.com/docs/en/agent-sdk/user-input)

### Engineering blogs / case studies surveyed

- [Autoolize — Claude Agent SDK in production: a studio's playbook](https://autoolize.com/blog/claude-agent-sdk-production-playbook/) — router+specialist, tool-loop guardrails, eval gates, skill-token-economy heuristics
- [ML6 — Inside the Claude Agents SDK: Lessons from the AI Engineer Summit](https://www.ml6.eu/en/blog/inside-the-claude-agents-sdk-lessons-from-the-ai-engineer-summit) — harness > raw model on CORE-Bench, "bash is all you need" composability
- [Digital Applied — Claude Agent SDK: Production Patterns Guide 2026](https://www.digitalapplied.com/blog/claude-agent-sdk-production-patterns-guide) — state persistence, circuit breakers, structured-output completion signals
- [LangChain Docs — Comparison with Claude Agent SDK (DeepAgents)](https://docs.langchain.com/oss/python/deepagents/comparison) — provider lock-in, multi-tenancy, deployment trade-offs
- [Anthropic — Claude Managed Agents: get to production 10× faster](https://claude.com/blog/claude-managed-agents)
- [Claude — Eight trends defining how software gets built in 2026](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026)
- [Jimmy Song — Open Source AI Agent Platform Comparison (2026)](https://jimmysong.io/blog/open-source-ai-agent-workflow-comparison/) — n8n / Dify / LangGraph / Coze / RAGFlow positioning

---

## 10. Appendix A — Repo layout for the spike

```
src/orchestrators/claude_agent/
├── __init__.py
├── agent_definition.py        # creates Spec / Review / Error agents (idempotent)
├── cli.py                     # `python -m … cli run --doc Yenepoya.xlsx`
├── prompts/
│   ├── spec_agent.md          # ported from Dify v3
│   ├── review_agent.md
│   └── error_agent.md
├── skills.json                # local cache of uploaded skill_ids
├── sdk_runner.py              # parity adapter for claude_agent_sdk
└── managed_runner.py          # Managed Agents runner

scripts/spike/
├── upload_avni_skills.py      # packages avni-skills → uploads as custom skills
├── tunnel.sh                  # cloudflared one-liner for local FastMCP exposure
├── run_one.py                 # single end-to-end run, emits metrics JSON
└── compare_runs.py            # joins Dify + Claude metrics into the matrix CSV

tests/spike/
├── test_parity.py             # SDK vs Managed Agents on the same input
└── test_pev_loop.py           # injects M5 failure scenario
```

## 11. Appendix B — Spec Agent system prompt skeleton (excerpt)

```text
You are the Avni Spec Agent. Your only job is to take a parsed scoping document
and produce a validated YAML spec (see avni-ai-iterative-dev-plan.md §"YAML
Spec Format") that the deterministic generator can convert into an Avni bundle.

You have these MCP tools (all under server "avni-ai"):
  parse-srs-file, store-entities, validate-entities, apply-entity-corrections,
  generate-spec, validate-spec, bundle-to-spec, enrich-spec,
  api/existing-config, knowledge-search

Hard rules:
  1. Never invent fields, UUIDs, or values. If a field is missing or ambiguous,
     call AskUserQuestion with multiple-choice options.
  2. Never re-implement bundle generation logic. Always call the avni-ai MCP tool.
  3. Always thread `org_name` through to /generate-spec.
  4. After every /validate-spec call: if errors, fix the YAML and revalidate.
     Stop after 5 iterations and escalate via AskUserQuestion.
  5. If any encounter type has no program, it MUST have a subject_type set.

Outputs:
  - On success, emit the final spec_yaml as a code block and stop.
  - On give-up, emit a structured error with your last spec attempt and the
    validator's last response.
```

(Full prompts ship in `prompts/`.)
