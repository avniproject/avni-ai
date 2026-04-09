const express = require("express");
const { WebSocketServer } = require("ws");
const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const app = express();
app.use(express.json({ limit: "50mb" }));

// Serve the UI
app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

const server = http.createServer(app);
const wss = new WebSocketServer({ server });

let activeWs = null;
let pendingUserReply = null; // resolve function for waitForUserReply

wss.on("connection", (ws) => {
  activeWs = ws;
  ws.on("message", (data) => {
    try {
      const msg = JSON.parse(data.toString());
      if (msg.type === "user_reply" && pendingUserReply) {
        pendingUserReply(msg.text);
        pendingUserReply = null;
      }
    } catch (_) {}
  });
  ws.on("close", () => {
    if (activeWs === ws) activeWs = null;
    // Unblock any pending wait
    if (pendingUserReply) {
      pendingUserReply("__stop__");
      pendingUserReply = null;
    }
  });
});

function waitForUserReply() {
  return new Promise((resolve) => {
    pendingUserReply = resolve;
    // Timeout after 5 minutes
    setTimeout(() => {
      if (pendingUserReply === resolve) {
        pendingUserReply = null;
        resolve("__stop__");
      }
    }, 5 * 60 * 1000);
  });
}

function emit(event) {
  if (activeWs && activeWs.readyState === 1) {
    activeWs.send(JSON.stringify(event));
  }
}

// -------------------------------------------------------
// Tool executor — calls avni-ai server endpoints
// -------------------------------------------------------
async function callServer(serverUrl, method, urlPath, opts = {}) {
  const url = `${serverUrl.replace(/\/$/, "")}${urlPath}`;
  const fetchOpts = { method, headers: { "Content-Type": "application/json" }, ...opts };
  if (opts.params) {
    const sp = new URLSearchParams(opts.params);
    const fullUrl = `${url}?${sp.toString()}`;
    delete fetchOpts.params;
    const r = await fetch(fullUrl, fetchOpts);
    return r.json().catch(() => ({ raw: r.statusText, status: r.status }));
  }
  const r = await fetch(url, fetchOpts);
  return r.json().catch(() => ({ raw: r.statusText, status: r.status }));
}

const TOOL_ROUTES = {
  get_srs_text:              { m: "GET",  p: "/get-srs-text",              via: "params" },
  store_entities:            { m: "POST", p: "/store-entities" },
  validate_entities:         { m: "POST", p: "/validate-entities" },
  generate_spec:             { m: "POST", p: "/generate-spec" },
  get_spec:                  { m: "GET",  p: "/get-spec",                  via: "params" },
  get_spec_section:          { m: "GET",  p: "/spec-section",              via: "params" },
  update_spec_section:       { m: "PUT",  p: "/spec-section" },
  get_entities_section:      { m: "GET",  p: "/entities-section",          via: "params" },
  update_entities_section:   { m: "PUT",  p: "/entities-section" },
  apply_entity_corrections:  { m: "POST", p: "/apply-entity-corrections" },
  generate_bundle:           { m: "POST", p: "/generate-bundle" },
  validate_bundle:           { m: "POST", p: "/validate-bundle" },
  validate_spec:             { m: "POST", p: "/validate-spec" },
  spec_to_entities:          { m: "POST", p: "/spec-to-entities" },
  bundle_to_spec:            { m: "POST", p: "/bundle-to-spec" },
  get_bundle_files:          { m: "GET",  p: "/bundle-files",              via: "params" },
  get_bundle_file:           { m: "GET",  p: "/bundle-file",               via: "params" },
  put_bundle_file:           { m: "PUT",  p: "/bundle-file" },
  upload_bundle:             { m: "POST", p: "/upload-bundle" },
  upload_status:             { m: "GET",  p: "/upload-status/{task_id}",   via: "path" },
  store_auth_token:          { m: "POST", p: "/store-auth-token" },
  download_bundle_b64:       { m: "GET",  p: "/download-bundle-b64",       via: "params" },
  patch_bundle:              { m: "POST", p: "/patch-bundle" },
  execute_python:            { m: "POST", p: "/execute-python" },
  get_existing_config:       { m: "GET",  p: "/api/existing-config",       via: "params" },
};

async function executeTool(serverUrl, name, args) {
  const route = TOOL_ROUTES[name];
  if (!route) return { error: `Unknown tool: ${name}` };

  let urlPath = route.p;
  if (route.via === "path") {
    // Replace {task_id} etc
    urlPath = urlPath.replace(/\{(\w+)\}/g, (_, k) => args[k] || "");
  }

  const opts = {};
  if (route.via === "params") {
    opts.params = args;
  } else {
    opts.body = JSON.stringify(args);
  }

  return callServer(serverUrl, route.m, urlPath, opts);
}

// -------------------------------------------------------
// Build tool definitions from OpenAPI spec
// -------------------------------------------------------
function buildTools() {
  let yaml;
  try {
    yaml = require("./node_modules/js-yaml") || null;
  } catch (_) {
    yaml = null;
  }

  const specPath = path.join(__dirname, "..", "..", "dify", "avni-ai-tools-openapi.yaml");
  const raw = fs.readFileSync(specPath, "utf-8");

  // Simple YAML parser for OpenAPI — just enough to extract tool defs
  let spec;
  if (yaml) {
    spec = yaml.load(raw);
  } else {
    // Fallback: use a basic approach — parse JSON after converting simple YAML
    // Actually just load it with a regex-based extractor
    spec = parseSimpleYaml(raw);
  }

  if (!spec || !spec.paths) return [];

  const tools = [];
  for (const [urlPath, methods] of Object.entries(spec.paths)) {
    for (const [method, op] of Object.entries(methods)) {
      if (!["get", "post", "put"].includes(method)) continue;
      const opId = op.operationId;
      if (!opId) continue;

      let desc = op.summary || op.description || "";
      if (op.description && op.description !== desc) desc += "\n\n" + op.description;

      const props = {};
      const required = [];

      for (const param of op.parameters || []) {
        props[param.name] = {
          type: (param.schema && param.schema.type) || "string",
          description: param.description || "",
        };
        if (param.required) required.push(param.name);
      }

      const bodySchema =
        op.requestBody?.content?.["application/json"]?.schema || {};
      for (const [prop, pdef] of Object.entries(bodySchema.properties || {})) {
        const cleaned = { ...pdef };
        delete cleaned.required;
        props[prop] = cleaned;
      }
      if (bodySchema.required) required.push(...bodySchema.required);

      tools.push({
        name: opId,
        description: desc.trim().slice(0, 1024),
        input_schema: {
          type: "object",
          properties: props,
          required: [...new Set(required)],
        },
      });
    }
  }
  return tools;
}

// Minimal YAML parser (just enough for the OpenAPI spec structure)
function parseSimpleYaml(raw) {
  // Use js-yaml if available via dynamic require, otherwise return null
  try {
    const jsYaml = require("js-yaml");
    return jsYaml.load(raw);
  } catch (_) {}

  // Absolute fallback — won't work for complex YAML
  return null;
}

// -------------------------------------------------------
// Agent loop — calls Claude API, executes tools
// -------------------------------------------------------
async function runAgent(config) {
  const {
    anthropicApiKey,
    authToken,
    serverUrl,
    srsText,
    orgName = "test_org",
  } = config;

  const conversationId = crypto.randomUUID();
  emit({ type: "info", message: `Conversation ID: ${conversationId}` });
  emit({ type: "info", message: `Server: ${serverUrl}` });

  // Step 0: Store auth token
  emit({ type: "step_start", step: "pre-0", name: "store_auth_token", phase: "setup" });
  const authResult = await callServer(serverUrl, "POST", "/store-auth-token", {
    body: JSON.stringify({ conversation_id: conversationId, auth_token: authToken }),
  });
  emit({
    type: "step_end", step: "pre-0", name: "store_auth_token",
    args: { conversation_id: conversationId, auth_token: "***" },
    result: authResult, success: !!authResult.ok,
    size_bytes: JSON.stringify(authResult).length,
  });

  // Step 0b: Store SRS text
  if (srsText) {
    emit({ type: "step_start", step: "pre-1", name: "store_srs_text", phase: "setup" });
    const srsResult = await callServer(serverUrl, "POST", "/store-srs-text", {
      body: JSON.stringify({ conversation_id: conversationId, srs_text: srsText }),
    });
    emit({
      type: "step_end", step: "pre-1", name: "store_srs_text",
      args: { conversation_id: conversationId, srs_text: `[${srsText.length} chars]` },
      result: srsResult, success: !!srsResult.ok,
      size_bytes: JSON.stringify(srsResult).length,
    });
  }

  // Build system prompt
  const promptPath = path.join(__dirname, "..", "..", "bundle-agent-prompt.txt");
  const promptBody = fs.readFileSync(promptPath, "utf-8");

  const system = `You are the AVNI SRS Bundle Generator Agent. You help users create complete AVNI configuration bundles from SRS specifications.

Conversation ID: ${conversationId}

IMPORTANT: Use conversation_id (= ${conversationId}) for ALL tool calls that need it.

CRITICAL TOOL-CALL RULES (these override any conflicting instructions below):

RULE 1 — FIRST TOOL CALL IS ALWAYS get_srs_text: At the very start of EVERY new SRS processing task, your first tool call MUST be get_srs_text(conversation_id). Do not show a plan, do not ask the user anything, do not say "let me retrieve" — just call the tool immediately. If it returns ok (200), use the srs_text field as your SRS input. If it returns 404 (no file uploaded), only then ask the user to paste the SRS text. After retrieving the text, call store_entities, then validate_entities, then generate_spec, then get_spec IN SEQUENCE without pausing. Only after get_spec returns do you show spec_yaml and ask for approval.

RULE 2 — generate_bundle uses conversation_id ONLY: When the user approves the spec, call generate_bundle(conversation_id) without any entities field. Entities are already in the server store from RULE 1.

RULE 3 — validate_bundle uses conversation_id ONLY: Call validate_bundle(conversation_id). Do NOT pass bundle_zip_b64.

RULE 4 — upload_bundle uses conversation_id ONLY: Call upload_bundle(conversation_id). Do NOT pass bundle_zip_b64.

RULE 5 — SKIP STEP 0 ("ASK FIRST"): The user has already told you whether this is a new or existing org in their first message. Do NOT ask again. Read the user's message for "new org" or "existing org" and proceed directly to Step 1 (get_srs_text). This overrides the "ASK FIRST" instruction in the prompt below.

RULE 6 — COMPLETE THE FULL PIPELINE: You must complete ALL phases in a single conversation:
  Phase 1: get_srs_text → extract entities → store_entities → validate_entities → (fix errors autonomously) → generate_spec → get_spec → show spec → wait for approval
  Phase 2 (if user requests changes): get_entities_section → update_entities_section → validate_entities → generate_spec → get_spec → show updated spec
  Phase 3 (after approval): generate_bundle → validate_bundle → (fix errors via Bundle Fix Loop) → upload_bundle → upload_status (poll until completed/failed)
  Do NOT stop early. Do NOT end the conversation until upload is complete or has permanently failed.

RULE 7 — GROUPS ARE REQUIRED: Always include groups in extracted entities: groups: [{name: "Everyone", hasAllPrivileges: true}]. The bundle generator does NOT auto-create groups.

${promptBody}`;

  const tools = buildTools();
  emit({ type: "info", message: `Loaded ${tools.length} tools from OpenAPI spec` });

  if (tools.length === 0) {
    emit({ type: "error", message: "Failed to load tools from OpenAPI spec. Install js-yaml: npm install js-yaml" });
    emit({ type: "done", success: false });
    return;
  }

  const messages = [
    { role: "user", content: srsText
      ? `I've uploaded an SRS document (scoping sheet + modelling sheet). This is a NEW org — name: "${orgName}". Do NOT ask if new/existing — I'm telling you: it's new. Start by calling get_srs_text to retrieve the document, then extract entities, store, validate, generate spec, and show me the spec for approval. I will review and approve or request corrections.`
      : `Generate a bundle for a simple MCH (Maternal & Child Health) program with Individual subject type, MCH program, ANC Visit encounter type, and a registration form + ANC form with basic fields. This is a NEW org — name: "${orgName}". Proceed: extract entities, store, validate, generate spec, show me for approval.` },
  ];

  let turn = 0;
  const maxTurns = 25;
  let totalInputTokens = 0;
  let totalOutputTokens = 0;
  let waitingForUser = false;

  while (turn < maxTurns) {
    turn++;
    emit({ type: "turn_start", turn, maxTurns });

    let response;
    try {
      const apiStart = Date.now();

      // Emit a heartbeat every 10s so the UI knows the API call is alive
      const heartbeat = setInterval(() => {
        const elapsed = Math.round((Date.now() - apiStart) / 1000);
        emit({ type: "info", message: `Claude API thinking... ${elapsed}s elapsed` });
      }, 10000);

      const apiRes = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": anthropicApiKey,
          "anthropic-version": "2023-06-01",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 16384,
          system,
          messages,
          tools,
        }),
      });

      clearInterval(heartbeat);

      if (!apiRes.ok) {
        const errText = await apiRes.text();
        emit({ type: "error", message: `Claude API error ${apiRes.status}: ${errText.slice(0, 500)}` });
        emit({ type: "done", success: false });
        return;
      }

      response = await apiRes.json();
      const apiDuration = Date.now() - apiStart;

      totalInputTokens += response.usage?.input_tokens || 0;
      totalOutputTokens += response.usage?.output_tokens || 0;

      emit({
        type: "turn_api", turn, duration_ms: apiDuration,
        input_tokens: response.usage?.input_tokens,
        output_tokens: response.usage?.output_tokens,
        stop_reason: response.stop_reason,
      });
    } catch (err) {
      emit({ type: "error", message: `Claude API call failed: ${err.message}` });
      emit({ type: "done", success: false });
      return;
    }

    // Process response content
    const textParts = [];
    const toolCalls = [];

    for (const block of response.content || []) {
      if (block.type === "text") {
        textParts.push(block.text);
      } else if (block.type === "tool_use") {
        toolCalls.push(block);
      }
    }

    if (textParts.length > 0) {
      emit({ type: "agent_message", turn, text: textParts.join("\n") });
    }

    messages.push({ role: "assistant", content: response.content });

    if (response.stop_reason === "end_turn" || toolCalls.length === 0) {
      const agentText = textParts.join(" ").toLowerCase();

      // Auto-respond ONLY to questions that have a fixed answer
      let autoReply = null;
      if (agentText.includes("new org") && agentText.includes("existing")) {
        autoReply = `This is a new org. Org name: ${orgName}. Proceed immediately with entity extraction.`;
      } else if (agentText.includes("auth token") || agentText.includes("provide a token")) {
        autoReply = "Auth token is already stored server-side via conversation_id. Proceed.";
      }

      if (autoReply) {
        emit({ type: "auto_reply", text: autoReply, trigger: textParts.join(" ").slice(0, 200) });
        messages.push({ role: "user", content: autoReply });
        continue;
      }

      // No auto-reply — wait for user input from the UI via WebSocket
      emit({
        type: "waiting_for_user",
        message: "Agent is waiting for your response. Type a reply below.",
        agent_said: textParts.join("\n"),
      });

      // Wait for user reply via WebSocket
      const userReply = await waitForUserReply();
      if (!userReply || userReply === "__stop__") {
        emit({
          type: "done", success: false, turns: turn,
          total_input_tokens: totalInputTokens,
          total_output_tokens: totalOutputTokens,
          reason: "User stopped or no reply",
        });
        return;
      }
      emit({ type: "user_reply", text: userReply });
      messages.push({ role: "user", content: userReply });
      continue;
    }

    // Execute tool calls
    const toolResults = [];
    for (const tc of toolCalls) {
      const stepId = `${turn}-${tc.name}`;
      emit({
        type: "step_start", step: stepId, name: tc.name,
        phase: guessPhase(tc.name), args: tc.input,
      });

      const start = Date.now();
      let result;
      try {
        result = await executeTool(serverUrl, tc.name, tc.input);
      } catch (err) {
        result = { error: err.message };
      }
      const duration = Date.now() - start;

      const resultStr = JSON.stringify(result);
      const success = !result.error && result.status !== 404;
      const difyWouldTruncate = resultStr.length > 65536;

      emit({
        type: "step_end", step: stepId, name: tc.name,
        args: tc.input, result,
        success, duration_ms: duration,
        size_bytes: resultStr.length,
        dify_would_truncate: difyWouldTruncate,
      });

      toolResults.push({
        type: "tool_result",
        tool_use_id: tc.id,
        content: resultStr,
      });
    }

    messages.push({ role: "user", content: toolResults });
  }

  emit({ type: "error", message: `Agent exceeded ${maxTurns} turns — possible infinite loop` });
  emit({ type: "done", success: false, turns: turn });
}

function guessPhase(toolName) {
  if (["get_srs_text", "store_entities", "validate_entities"].includes(toolName)) return "extract";
  if (["generate_spec", "get_spec", "validate_spec", "get_spec_section", "update_spec_section"].includes(toolName)) return "spec";
  if (["generate_bundle", "validate_bundle", "get_bundle_files", "get_bundle_file", "put_bundle_file"].includes(toolName)) return "bundle";
  if (["upload_bundle", "upload_status"].includes(toolName)) return "upload";
  if (["get_entities_section", "update_entities_section", "apply_entity_corrections"].includes(toolName)) return "correction";
  return "other";
}

// -------------------------------------------------------
// Direct pipeline — deterministic scoping parser, no LLM
// -------------------------------------------------------
async function runDirect(config) {
  const { authToken, serverUrl, srsText, orgName = "test_org", filePaths } = config;
  const conversationId = crypto.randomUUID();
  emit({ type: "info", message: `Mode: DETERMINISTIC PIPELINE (scoping parser, no LLM)` });
  emit({ type: "info", message: `Conversation ID: ${conversationId}` });
  emit({ type: "info", message: `Server: ${serverUrl}` });

  // Step 0: Store auth token
  await runStep("store_auth_token", "setup", { conversation_id: conversationId },
    () => callServer(serverUrl, "POST", "/store-auth-token", {
      body: JSON.stringify({ conversation_id: conversationId, auth_token: authToken })
    }));

  // Step 1: Parse scoping docs (deterministic — no LLM)
  let entities = null;
  let specYaml = null;
  let audit = null;

  if (filePaths && filePaths.length > 0) {
    // Use scoping parser endpoint
    emit({ type: "info", message: `Parsing ${filePaths.length} file(s) with scoping parser...` });
    const parseResult = await runStep("parse_scoping_docs", "extract",
      { file_paths: filePaths, org_name: orgName },
      () => callServer(serverUrl, "POST", "/parse-scoping-docs", {
        body: JSON.stringify({ file_paths: filePaths, org_name: orgName })
      }));

    if (!parseResult || parseResult.error) {
      emit({ type: "done", success: false }); return;
    }

    entities = parseResult.entities;
    specYaml = parseResult.spec_yaml;
    audit = parseResult.audit;

    // Show audit
    if (audit) {
      const auditLines = [
        `**Files parsed:** ${audit.files_parsed?.length || 0}`,
        `**Entities:** ${JSON.stringify(audit.entity_counts)}`,
        `**Warnings:** ${audit.warnings?.length || 0}`,
        `**Errors:** ${audit.errors?.length || 0}`,
      ];
      if (audit.warnings?.length > 0) {
        auditLines.push("", "Warnings:");
        audit.warnings.forEach(w => auditLines.push(`  - ${w}`));
      }
      if (audit.errors?.length > 0) {
        auditLines.push("", "Errors:");
        audit.errors.forEach(e => auditLines.push(`  - ${e}`));
      }
      emit({ type: "agent_message", turn: 0, text: auditLines.join("\n") });
    }

    // Show spec
    if (specYaml) {
      emit({ type: "agent_message", turn: 0, text: "Consolidated Spec (source of truth):\n```yaml\n" + specYaml.slice(0, 5000) + (specYaml.length > 5000 ? "\n... (truncated)" : "") + "\n```" });
    }
  } else if (srsText) {
    // Fallback: use Claude for extraction from pasted text
    emit({ type: "info", message: "No Excel files — using Claude to extract entities from pasted SRS text..." });
    entities = await extractEntitiesWithClaude(config, srsText, orgName);
    if (!entities) { emit({ type: "done", success: false }); return; }
    emit({ type: "agent_message", turn: 0, text: "Extracted entities:\n```json\n" + JSON.stringify(entities, null, 2).slice(0, 3000) + "\n```" });
  } else {
    emit({ type: "error", message: "No input — upload Excel files or paste SRS text" });
    emit({ type: "done", success: false }); return;
  }

  // Step 2: Store → Validate → Spec → Bundle → Validate → Upload
  const pipeline = [
    { name: "store_entities", phase: "extract",
      fn: () => callServer(serverUrl, "POST", "/store-entities", {
        body: JSON.stringify({ conversation_id: conversationId, entities })
      })},
    { name: "validate_entities", phase: "extract",
      fn: () => callServer(serverUrl, "POST", "/validate-entities", {
        body: JSON.stringify({ conversation_id: conversationId })
      })},
    { name: "generate_spec", phase: "spec",
      fn: () => callServer(serverUrl, "POST", "/generate-spec", {
        body: JSON.stringify({ conversation_id: conversationId, org_name: orgName })
      })},
    { name: "get_spec", phase: "spec",
      fn: () => callServer(serverUrl, "GET", "/get-spec", { params: { conversation_id: conversationId } })
    },
    { name: "generate_bundle", phase: "bundle",
      fn: () => callServer(serverUrl, "POST", "/generate-bundle", {
        body: JSON.stringify({ conversation_id: conversationId, org_name: orgName })
      })},
    { name: "validate_bundle", phase: "bundle",
      fn: () => callServer(serverUrl, "POST", "/validate-bundle", {
        body: JSON.stringify({ conversation_id: conversationId })
      })},
    { name: "get_bundle_files", phase: "bundle",
      fn: () => callServer(serverUrl, "GET", "/bundle-files", { params: { conversation_id: conversationId } })
    },
    { name: "upload_bundle", phase: "upload",
      fn: () => callServer(serverUrl, "POST", "/upload-bundle", {
        body: JSON.stringify({ conversation_id: conversationId })
      })},
  ];

  for (const step of pipeline) {
    const result = await runStep(step.name, step.phase,
      { conversation_id: conversationId }, step.fn);

    if (step.name === "validate_entities" && result) {
      const msg = result.has_errors
        ? `Validation: ${result.error_count} errors, ${result.warning_count} warnings\n${result.issues_summary}`
        : `Validation passed (${result.warning_count} warnings)`;
      emit({ type: "agent_message", turn: 0, text: msg });
    }
    if (step.name === "get_spec" && result?.spec_yaml) {
      emit({ type: "agent_message", turn: 0, text: "Server-generated Spec:\n```yaml\n" + result.spec_yaml.slice(0, 3000) + (result.spec_yaml.length > 3000 ? "\n..." : "") + "\n```" });
    }
    if (step.name === "generate_bundle" && result?.summary) {
      emit({ type: "agent_message", turn: 0, text: "Bundle: " + JSON.stringify(result.summary) });
    }
    if (step.name === "validate_bundle") {
      emit({ type: "agent_message", turn: 0, text: result?.valid ? "Bundle validation: PASSED" : "Bundle validation: FAILED\n" + JSON.stringify(result?.errors) });
    }
    if (step.name === "get_bundle_files" && result?.files) {
      emit({ type: "agent_message", turn: 0, text: "Bundle files:\n" + result.files.map(f => `  ${f.name} (${f.size_bytes}B)`).join("\n") });
    }
    if (step.name === "upload_bundle" && result?.error) {
      emit({ type: "info", message: "Upload failed (likely expired auth token). Bundle was generated and validated — update token and retry." });
    }

    if (result?.error && step.name !== "upload_bundle") {
      emit({ type: "done", success: false, conversation_id: conversationId, server_url: serverUrl });
      return;
    }
  }

  emit({ type: "done", success: true, conversation_id: conversationId, server_url: serverUrl });
}

// Helper: run one step with emit
async function runStep(name, phase, args, fn) {
  emit({ type: "step_start", step: name, name, phase });
  const start = Date.now();
  let result;
  try { result = await fn(); } catch (e) { result = { error: e.message }; }
  const duration = Date.now() - start;
  const resultStr = JSON.stringify(result);
  const success = !result.error && result.status !== 404 && result.status !== 401;
  emit({ type: "step_end", step: name, name, phase, args, result, success,
    duration_ms: duration, size_bytes: resultStr.length,
    dify_would_truncate: resultStr.length > 65536 });
  return result;
}

async function extractEntitiesWithClaude(config, srsText, orgName) {
  const { anthropicApiKey } = config;

  // Truncate SRS to avoid massive payloads — 30K chars is plenty for extraction
  const maxSrsChars = 30000;
  let trimmedSrs = srsText;
  if (srsText.length > maxSrsChars) {
    trimmedSrs = srsText.slice(0, maxSrsChars) + `\n\n... (truncated from ${srsText.length} chars)`;
    emit({ type: "info", message: `SRS text truncated: ${srsText.length} → ${maxSrsChars} chars for extraction` });
  }

  emit({ type: "step_start", step: "claude_extract", name: "claude_extract_entities", phase: "extract" });
  const start = Date.now();

  const heartbeat = setInterval(() => {
    emit({ type: "info", message: `Claude extracting entities... ${Math.round((Date.now() - start) / 1000)}s` });
  }, 10000);

  // 90 second timeout
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 90000);

  try {
    const apiRes = await fetch("https://api.anthropic.com/v1/messages", {
      signal: controller.signal,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": anthropicApiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 4096,
        messages: [{ role: "user", content: `Extract AVNI entities from this SRS document. Return ONLY a JSON object (no markdown, no explanation) with this exact structure:
{
  "subject_types": [{"name": "...", "type": "Person|Group|Household"}],
  "programs": [{"name": "...", "target_subject_type": "...", "colour": "#hex"}],
  "encounter_types": [{"name": "...", "program_name": "..." or null, "subject_type": "...", "is_program_encounter": bool, "is_scheduled": bool}],
  "address_levels": [{"name": "...", "level": int, "parent": "..." or null}],
  "groups": [{"name": "Everyone", "hasAllPrivileges": true}],
  "forms": [{"name": "...", "formType": "IndividualProfile|ProgramEnrolment|ProgramExit|ProgramEncounter|Encounter", "subjectType": "...", "program": "..." or null, "encounterType": "..." or null, "fields": [{"name": "...", "dataType": "Text|Numeric|Coded|Date|DateTime|PhoneNumber|ImageV2|Notes|Duration", "mandatory": bool, "options": ["..."] for Coded only}]}]
}

Rules:
- FormType: IndividualProfile=registration, ProgramEnrolment=enrolment, ProgramEncounter=visit in program, Encounter=general visit
- Only Coded fields get options array
- Always include groups: [{"name": "Everyone", "hasAllPrivileges": true}]
- Address levels: topmost=highest level number
- Org name: ${orgName}

SRS Document:
${trimmedSrs}` }],
      }),
    });

    clearInterval(heartbeat);
    clearTimeout(timeout);

    if (!apiRes.ok) {
      const err = await apiRes.text();
      emit({ type: "step_end", step: "claude_extract", name: "claude_extract_entities", phase: "extract",
        result: { error: err.slice(0, 500) }, success: false, duration_ms: Date.now() - start, size_bytes: 0 });
      return null;
    }

    const resp = await apiRes.json();
    const text = resp.content?.find(b => b.type === "text")?.text || "";

    // Parse JSON from response (strip markdown if present)
    let jsonStr = text;
    const jsonMatch = text.match(/```(?:json)?\s*([\s\S]*?)```/);
    if (jsonMatch) jsonStr = jsonMatch[1];
    jsonStr = jsonStr.trim();

    const entities = JSON.parse(jsonStr);

    emit({ type: "step_end", step: "claude_extract", name: "claude_extract_entities", phase: "extract",
      args: { srs_text_length: srsText.length }, result: { ok: true, entity_counts: {
        subject_types: entities.subject_types?.length || 0,
        programs: entities.programs?.length || 0,
        encounter_types: entities.encounter_types?.length || 0,
        forms: entities.forms?.length || 0,
      }}, success: true, duration_ms: Date.now() - start,
      size_bytes: JSON.stringify(entities).length });

    return entities;
  } catch (err) {
    clearInterval(heartbeat);
    clearTimeout(timeout);
    const msg = err.name === "AbortError" ? "Entity extraction timed out after 90 seconds. SRS may be too large." : err.message;
    emit({ type: "step_end", step: "claude_extract", name: "claude_extract_entities", phase: "extract",
      result: { error: msg }, success: false, duration_ms: Date.now() - start, size_bytes: 0 });
    emit({ type: "error", message: `Entity extraction failed: ${msg}` });
    return null;
  }
}

// -------------------------------------------------------
// Parse Excel files using the Python scoping parser
// -------------------------------------------------------
app.post("/api/parse", async (req, res) => {
  const { file_paths, org_name, server_url } = req.body;
  if (!file_paths || !file_paths.length) {
    return res.status(400).json({ error: "No file_paths provided" });
  }
  try {
    const result = await callServer(server_url || "http://localhost:8023", "POST", "/parse-scoping-docs", {
      body: JSON.stringify({ file_paths, org_name: org_name || "" }),
    });
    res.json(result);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// -------------------------------------------------------
// Download bundle ZIP from server-side store
// -------------------------------------------------------
app.get("/api/download-bundle", async (req, res) => {
  const { conversation_id, server_url } = req.query;
  if (!conversation_id || !server_url) {
    return res.status(400).json({ error: "Missing conversation_id or server_url" });
  }
  try {
    const stored = await callServer(server_url, "GET", "/bundle-files", { params: { conversation_id } });
    if (stored.error) return res.status(404).json(stored);

    // Fetch the b64 ZIP from the bundle store via a direct internal call
    const resp = await fetch(`${server_url.replace(/\/$/, "")}/download-bundle-zip?conversation_id=${conversation_id}`);
    if (resp.ok) {
      const buf = await resp.arrayBuffer();
      res.set({ "Content-Type": "application/zip", "Content-Disposition": "attachment; filename=bundle.zip" });
      return res.send(Buffer.from(buf));
    }
    // Fallback — not all servers have that endpoint, so we'll reconstruct from bundle store
    return res.status(404).json({ error: "Bundle download not available via this endpoint" });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// -------------------------------------------------------
// API endpoints
// -------------------------------------------------------
app.post("/api/run", (req, res) => {
  const config = req.body;
  const mode = config.mode || "direct";
  res.json({ ok: true, message: `Run started (${mode}) — watch WebSocket for events` });

  const runner = mode === "agent" ? runAgent : runDirect;
  runner(config).catch((err) => {
    emit({ type: "error", message: `Run crashed: ${err.message}\n${err.stack}` });
    emit({ type: "done", success: false });
  });
});

// -------------------------------------------------------
// Start
// -------------------------------------------------------
const PORT = process.env.PORT || 3456;
server.listen(PORT, () => {
  console.log(`Agent Debugger running at http://localhost:${PORT}`);
});
