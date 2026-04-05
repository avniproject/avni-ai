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


# Stable namespace for all Avni deterministic UUIDs
_AVNI_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "avni.project.org")


def generate_deterministic_uuid(seed: str) -> str:
    """
    Produce a fully deterministic UUID v5 from *seed*.

    Same seed always yields the same UUID — this guarantees that
    re-running the generator produces identical bundles, enabling
    idempotent re-uploads (Avni upserts by UUID).
    """
    return str(uuid.uuid5(_AVNI_NAMESPACE, seed))


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
