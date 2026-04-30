# Real run runbook — Claude Managed Agents spike

Ordered checklist for the live end-to-end test. Each block is copy-pasteable
from the avni-ai repo root.

## 0. One-time prerequisites
- [x] `ANTHROPIC_API_KEY` set in `.env` and has Managed Agents beta access
      (verified by `scripts/spike/check_managed_agents_access.py`).
- [x] Skills uploaded; `src/orchestrators/claude_agent/skills.json` present.
- [ ] `cloudflared` installed locally (`brew install cloudflared`).
- [ ] avni-server staging URL + auth token to hand.
- [ ] One Yenepoya/Kshamata SRS file (`.xlsx`/`.pdf`) on disk.

## 1. Start the FastMCP server
```bash
# Terminal 1 — keep open
set -a && source .env && set +a
PORT=8023 .venv/bin/python -m src.main
```
Confirm `GET http://localhost:8023/health` returns
`{"status":"healthy","service":"Avni AI Server"}`.

## 2. Expose to Anthropic via Cloudflare Quick Tunnel
```bash
# Terminal 2 — keep open
PORT=8023 ./scripts/spike/tunnel.sh
```
Copy the printed `https://<random>.trycloudflare.com` URL. The MCP endpoint is
that URL plus `/mcp`.

## 3. Set runtime env
```bash
# In Terminal 3 (or just export for the run)
export AVNI_MCP_SERVER_URL="https://<random>.trycloudflare.com/mcp"
export AVNI_AUTH_TOKEN="<staging avni-server bearer>"
export AVNI_ORG_NAME="Yenepoya"        # or "Kshamata"
export AVNI_CLAUDE_MODEL="claude-opus-4-5"
```

## 4. Sanity-ping the tunnel
```bash
curl -fsS "$AVNI_MCP_SERVER_URL/../health" | jq .
```
A `healthy` body confirms Anthropic infra will reach the MCP server.

## 5. Run the spike — Managed Agents
```bash
.venv/bin/python -m src.orchestrators.claude_agent.cli \
  --runner managed \
  --doc /path/to/srs.xlsx \
  --org-name "$AVNI_ORG_NAME" \
  --mcp-url "$AVNI_MCP_SERVER_URL" \
  --out runs/managed.json \
  -v
```
Trace + transcript land in `runs/managed.json`.

## 6. Run the spike — Agent SDK (parity)
```bash
.venv/bin/python -m src.orchestrators.claude_agent.cli \
  --runner sdk \
  --doc /path/to/srs.xlsx \
  --org-name "$AVNI_ORG_NAME" \
  --mcp-url "$AVNI_MCP_SERVER_URL" \
  --out runs/sdk.json \
  -v
```

## 7. Aggregate the comparison
```bash
.venv/bin/python scripts/spike/compare_runs.py \
  --managed runs/managed.json \
  --sdk runs/sdk.json \
  --out docs/app_configurator/claude-managed-agents-spike-results.md
```

## 8. (Optional) Inject a failure for M5
Pass `--inject-failure` to run_one.py / cli.py to force the runner into the
ERROR_AGENT path. The runner detects an upload failure (or a synthesised one)
and hands off to ERROR_AGENT for diagnosis.

## Troubleshooting
- `store-auth-token returned HTTP 401` — wrong staging token; refresh.
- `permission_denied` from Anthropic — beta access flag missing.
- `tool not in spike allowlist` (SDK only) — extend `_build_options` allowlist.
- Stuck event stream — `cloudflared` logs in Terminal 2 will show drops; the
  managed runner already auto-resubscribes on `httpx.HTTPError`.
