# Avni AI
A Model Context Protocol (MCP) server that provides AI assistants with programmatic access to the Avni platform. This server enables LLMs like OpenAI GPT-4 to interact with Avni's system through standardized tool calling.

## 🚀 Features

- Built-in monitoring support at `/health`
- Deployed with HTTP transport and proper error handling

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
AVNI_AI_SERVER_URL=https://staging-mcp.avniproject.org/

# Server Configuration
PORT=8023
```

### Environment-Specific URLs

**Staging:**
```env
AVNI_BASE_URL=https://staging.avniproject.org
AVNI_AI_SERVER_URL=https://staging-mcp.avniproject.org/
```

## 🚀 Usage

### Development

```bash
# Run the server
uv run avni-mcp-server

# Server will start on http://localhost:8023
# MCP endpoint: http://localhost:8023/mcp (no longer used, as we call tools in code now)
# Health check: http://localhost:8023/health
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
sudo journalctl -u avni-ai -f

# Development debugging
uv run python main.py --log-level DEBUG
```

## 🔗 Related Links
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
