"""
Deterministic UUID generation and registry lookup for AVNI bundles.
Ports the JS generateDeterministicUUID + uuid_registry.json logic.
"""

import json
import uuid
from pathlib import Path

_TRAINING_DATA_DIR = Path(__file__).resolve().parent.parent / "training_data"


def _load_uuid_registry() -> dict[str, str]:
    registry_path = _TRAINING_DATA_DIR / "uuid_registry.json"
    if registry_path.exists():
        return json.loads(registry_path.read_text(encoding="utf-8"))
    return {}


# Module-level singleton — loaded once
UUID_REGISTRY: dict[str, str] = _load_uuid_registry()


def _java_string_hash(seed: str) -> int:
    """Replicate JS hash: hash = ((hash << 5) - hash) + charCode; hash &= hash."""
    h = 0
    for ch in seed:
        h = ((h << 5) - h) + ord(ch)
        h &= 0xFFFFFFFF  # keep 32-bit
        if h >= 0x80000000:
            h -= 0x100000000
    return h


def generate_deterministic_uuid(seed: str) -> str:
    """
    Produce a UUID whose first 8 hex chars are derived from *seed*
    and the remainder is a random UUID v4 tail.  This matches the JS:
        const hex = Math.abs(hash).toString(16).padStart(8, '0');
        return `${hex.substring(0, 8)}-${uuidv4().substring(9)}`;
    """
    h = abs(_java_string_hash(seed))
    prefix = format(h, "x").zfill(8)[:8]
    tail = str(uuid.uuid4())[9:]  # everything after first 8+dash
    return f"{prefix}-{tail}"


def lookup_answer_uuid(name: str) -> str | None:
    """Case-insensitive lookup in the standard UUID registry."""
    cleaned = name.strip()
    # Exact match
    if cleaned in UUID_REGISTRY:
        return UUID_REGISTRY[cleaned]
    # Case-insensitive fallback
    lower = cleaned.lower()
    for key, val in UUID_REGISTRY.items():
        if key.lower() == lower:
            return val
    return None
