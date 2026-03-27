import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment files in fallback order.
# Existing shell environment variables are never overridden.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
for _env_file in (".env", ".env.staging", ".env.production"):
    _env_path = _PROJECT_ROOT / _env_file
    if _env_path.exists():
        load_dotenv(dotenv_path=_env_path, override=False)

# Backward-compatible aliases and defaults used across runners/tests.
if not os.getenv("AVNI_MCP_SERVER_URL"):
    _avni_ai_server_url = os.getenv("AVNI_AI_SERVER_URL")
    if _avni_ai_server_url:
        os.environ["AVNI_MCP_SERVER_URL"] = _avni_ai_server_url

if not os.getenv("DIFY_API_KEY"):
    for _candidate in ("DIFY_SCHEDULING_API_KEY", "DIFY_STAGING_TEST_API_KEY"):
        _candidate_value = os.getenv(_candidate)
        if _candidate_value:
            os.environ["DIFY_API_KEY"] = _candidate_value
            break

if not os.getenv("DIFY_API_BASE_URL"):
    os.environ["DIFY_API_BASE_URL"] = "https://api.dify.ai/v1"

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_BASE_URL = os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1")
