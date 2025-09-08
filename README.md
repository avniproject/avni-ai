# Avni AI

**TODO** Move all MCP-Server code within a sub-folder of this repo.


## Avni MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with programmatic access to the Avni platform. This server enables LLMs like OpenAI GPT-4 to interact with Avni's system through standardized tool calling.

## 🚀 Features

- Works with OpenAI Responses API for automatic tool calling
- Built-in monitoring support at `/health`
- REST API endpoint at `/chat`
- Access to organizations, users, locations, and programs (WIP)
- Deployed with SSE transport and proper error handling

## 📋 Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## 🛠️ Installation

### 1. Install uv package manager

```bash
# macOS
brew install uv

# Other platforms
# See: https://docs.astral.sh/uv/getting-started/installation/
```

### 2. Clone and setup project

```bash
git clone https://github.com/avniproject/avni-mcp-server
cd avni-mcp-server
uv sync
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Avni Platform Configuration  
AVNI_BASE_URL=https://staging.avniproject.org
AVNI_MCP_SERVER_URL=https://staging-mcp.avniproject.org/sse

# Server Configuration
PORT=8023
```

### Environment-Specific URLs

**Staging:**
```env
AVNI_BASE_URL=https://staging.avniproject.org
AVNI_MCP_SERVER_URL=https://staging-mcp.avniproject.org/sse
```

## 🚀 Usage

### Development

```bash
# Run the server
uv run main.py

# Server will start on http://localhost:8023
# MCP endpoint: http://localhost:8023/sse/
# Health check: http://localhost:8023/health
# Chat endpoint: http://localhost:8023/chat
```

```bash
# Run linting
uv run ruff format .

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=.

# Run specific test
uv run pytest tests/test_tools.py
```

## 🛠️ Available Tools

### Organization Tools
- `create_organization` - Create new health organizations
- `list_organizations` - List existing organizations
- `get_organization` - Get organization details

### User Tools  
- `create_user` - Create new users
- `create_user_group` - Create user groups
- `list_users` - List existing users

### Location Tools
- `create_location` - Create geographic locations
- `create_catchment` - Create catchment areas
- `list_locations` - List existing locations

### Program Tools
- `create_program` - Create health programs
- `create_subject_type` - Create subject types
- `create_encounter_type` - Create encounter types

### Environment Variables Export

Ensure your deployment exports these variables:

```bash
export OPENAI_API_KEY={{ openai_api_key }}
export AVNI_BASE_URL={{ avni_base_url }}
export AVNI_MCP_SERVER_URL={{ avni_mcp_server_url }}
export PORT=8023
```

### Logs

```bash
# Check server logs
sudo journalctl -u avni-mcp-server -f

# Development debugging
uv run python main.py --log-level DEBUG
```

## 🔗 Related Links
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)

## Get tools list

curl -X POST https://staging-mcp.avniproject.org/mcp \
-H "Content-Type: application/json" \
-H "Accept: application/json, text/event-stream" \
-d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
