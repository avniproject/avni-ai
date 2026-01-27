# Avni AI

A Function Tool Calling server that provides AI assistants with programmatic access to the Avni platform. This server enables LLMs like OpenAI GPT-4 to interact with Avni's system through standardized tool calling.

## 🚀 Features

- Built-in monitoring support at `/health`
- Deployed with HTTP transport and proper error handling
- Comprehensive admin tools for managing Avni entities:
  - Address Level Types
  - Locations
  - Catchments
  - Users
  - Programs
  - Subject Types
  - Encounters
  - Implementations
- Async configuration processing with status tracking

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
git clone https://github.com/avniproject/avni-ai
cd avni-ai
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

**Production:**
```env
AVNI_BASE_URL=https://avniproject.org
AVNI_AI_SERVER_URL=https://mcp.avniproject.org/
```

## 🚀 Usage

### Development

```bash
# Run the server
uv run avni-ai-server

# Server will start on http://localhost:8023
# Health check: http://localhost:8023/health
# Config processing: http://localhost:8023/process-config-async
```

### Testing

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

### Production Deployment

Ensure your deployment exports these variables:

```bash
export OPENAI_API_KEY={{ openai_api_key }}
export AVNI_BASE_URL={{ avni_base_url }}
export AVNI_AI_SERVER_URL={{ avni_ai_server_url }}
export PORT=8023
```

### Logs

```bash
# Check server logs (systemd service)
sudo journalctl -u avni-ai -f

# Development debugging
uv run avni-ai-server --log-level DEBUG
```

## 🔧 Available Tools

The server provides MCP tools for:

### Admin Tools
- **Address Level Types**: Create, search, and manage address level types
- **Locations**: Create, search, and manage location hierarchy
- **Catchments**: Create and manage catchment areas
- **Users**: Search and manage user accounts

### App Designer Tools
- **Programs**: Create and manage programs
- **Subject Types**: Create and manage subject types
- **Encounters**: Create and manage encounter types

### Implementation Tools
- **Implementations**: Manage organization implementations

## 📚 API Endpoints

- `GET /health` - Health check endpoint
- `POST /process-config-async` - Process configuration asynchronously
- `GET /process-config-status/{task_id}` - Get async processing status

## 🔗 Related Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
- [Avni Platform](https://avniproject.org/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
