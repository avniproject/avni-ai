#!/usr/bin/env bash
# Expose the local avni-ai FastMCP server to Anthropic infra so Managed Agents
# can reach it as an MCP `url` server. Requires `cloudflared` installed.
#
# Usage:
#   PORT=8023 ./scripts/spike/tunnel.sh
#
# The script prints the public URL it gets back from Cloudflare; copy it into
# AVNI_MCP_SERVER_URL=<that-url>/mcp before running the spike CLI.

set -euo pipefail

PORT="${PORT:-8023}"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared not installed; brew install cloudflared" >&2
  exit 1
fi

echo "starting Quick Tunnel against http://localhost:${PORT}"
echo "(Ctrl-C to stop; copy the *.trycloudflare.com URL printed below)"
exec cloudflared tunnel --url "http://localhost:${PORT}"
