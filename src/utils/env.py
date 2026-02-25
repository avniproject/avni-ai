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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_BASE_URL = os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1")
