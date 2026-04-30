"""Probe whether the configured ANTHROPIC_API_KEY has Managed Agents beta access.

Runs the minimum-cost authenticated call against each Managed Agents resource
(`skills.list`, `agents.list`, `environments.list`) and reports per-resource
status. Exit 0 = full access, 1 = no access / error.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from anthropic import Anthropic, APIStatusError

BETA = "managed-agents-2026-04-01"


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _probe(label: str, fn) -> tuple[bool, str]:
    try:
        result = fn()
        n = len(getattr(result, "data", []) or [])
        return True, f"{label}: OK (200) — {n} item(s)"
    except APIStatusError as e:
        body = ""
        try:
            body = str(e.response.json())[:200]
        except Exception:
            body = (e.response.text or "")[:200]
        return False, f"{label}: HTTP {e.status_code} — {body}"
    except Exception as e:
        return False, f"{label}: {type(e).__name__} — {e}"


def main() -> int:
    _load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 1
    print(f"Using key: {key[:10]}…{key[-4:]} (len={len(key)})")
    print(f"Beta header: {BETA}\n")

    client = Anthropic(api_key=key)

    probes = [
        ("skills.list      ", lambda: client.beta.skills.list(betas=[BETA])),
        ("agents.list      ", lambda: client.beta.agents.list(betas=[BETA])),
        ("environments.list", lambda: client.beta.environments.list(betas=[BETA])),
    ]

    all_ok = True
    for label, fn in probes:
        ok, msg = _probe(label, fn)
        all_ok = all_ok and ok
        print(msg)

    print()
    if all_ok:
        print("RESULT: API key has Managed Agents beta access ✅")
        return 0
    print("RESULT: Managed Agents beta access NOT confirmed ❌")
    return 1


if __name__ == "__main__":
    sys.exit(main())
