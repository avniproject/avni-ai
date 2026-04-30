"""
Upload `avni-skills` directories to Anthropic as custom skills.

Walks a checkout of github.com/avniproject/avni-skills, picks the directories
the spike actually uses (set in `SPIKE_SKILLS`), packages each as a tar+SKILL.md
upload via the Skills API, and writes the resulting `skill_id`s into the
manifest at src/orchestrators/claude_agent/skills.json.

Run once after cloning avni-skills locally; rerun whenever upstream skills
change. Idempotent: deletes any old skill with the same name first.

Usage:
    export ANTHROPIC_API_KEY=...
    uv run python scripts/spike/upload_avni_skills.py \\
        --avni-skills /path/to/avni-skills

Skips skills already uploaded if their name matches; pass `--force` to replace.
"""

from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import os
import sys
from pathlib import Path

logger = logging.getLogger("upload_avni_skills")

SPIKE_SKILLS = (
    "srs-bundle-generator",
    "project-scoping",
    "implementation-engineer",
    "support-engineer",
    "support-patterns",
    "architecture-patterns",
)
"""Skill subdirectories from avni-skills that the spike attaches to agents.
Mirrors agent_definition.py's intent — keep in sync."""

MANIFEST_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "src"
    / "orchestrators"
    / "claude_agent"
    / "skills.json"
)
BETA = "managed-agents-2026-04-01"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--avni-skills",
        required=True,
        type=Path,
        help="Local checkout of avniproject/avni-skills.",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Re-upload even if a skill with the same name already exists.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would happen without uploading.",
    )
    return p


def _ensure_skill_md(skill_dir: Path) -> Path:
    """Validate the skill has a SKILL.md and return its path."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(
            f"{skill_md} missing — Anthropic skills must contain SKILL.md"
        )
    return skill_md


def _read_skill_name(skill_md: Path) -> str:
    """Pull `name:` out of the SKILL.md frontmatter and normalize.

    Anthropic enforces folder-name == normalized-frontmatter-name. They
    normalize as: lowercase + spaces → hyphens. e.g. `AVNI Support Engineer`
    → `avni-support-engineer`. Matching that here keeps uploads idempotent.
    """
    text = skill_md.read_text()
    if not text.startswith("---"):
        raise ValueError(f"{skill_md}: missing YAML frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError(f"{skill_md}: unterminated frontmatter")
    raw_name = ""
    for line in text[3:end].splitlines():
        line = line.strip()
        if line.startswith("name:"):
            raw_name = line.split(":", 1)[1].strip().strip('"').strip("'")
            break
    if not raw_name:
        raise ValueError(f"{skill_md}: no `name:` in frontmatter")
    return raw_name.lower().replace(" ", "-")


# Files we never want to ship into a skill upload — keep the wire payload
# clean and avoid leaking host artefacts. Lockfiles + node_modules are common
# in the avni-skills repo because some skills bundle helper scripts.
_SKIP_DIRS = frozenset({"node_modules", ".git", "__pycache__", ".venv", "output"})
_SKIP_FILES = frozenset({".DS_Store", "package-lock.json", "yarn.lock"})


def _collect_skill_files(
    skill_dir: Path, top_folder: str
) -> list[tuple[str, bytes, str]]:
    """Walk a skill dir and return (filename, bytes, content_type) tuples.

    The Skills API requires every uploaded path to begin with the same
    top-level folder, with `SKILL.md` directly inside it (e.g.
    `<top_folder>/SKILL.md`). Bare top-level files return
    `SKILL.md file must be exactly in the top-level folder.`
    """
    files: list[tuple[str, bytes, str]] = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(skill_dir)
        if any(part in _SKIP_DIRS for part in rel.parts[:-1]):
            continue
        if rel.name in _SKIP_FILES:
            continue
        ctype = mimetypes.guess_type(rel.name)[0] or "application/octet-stream"
        files.append((f"{top_folder}/{rel.as_posix()}", path.read_bytes(), ctype))
    return files


def _load_manifest() -> dict[str, str]:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return {}


def _save_manifest(manifest: dict[str, str]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def _delete_existing(client, name: str) -> None:
    """Best-effort: list skills, delete any whose display_title matches."""
    try:
        page = client.beta.skills.list(betas=[BETA])
        for sk in page.data:
            if getattr(sk, "display_title", "") == name:
                logger.info("deleting existing skill %s (%s)", name, sk.id)
                client.beta.skills.delete(sk.id, betas=[BETA])
    except Exception as e:  # noqa: BLE001  — best effort
        logger.warning("could not list/delete existing skills: %s", e)


def _index_existing(client) -> dict[str, str]:
    """Return display_title → skill_id for everything already on the org.

    Anthropic rejects new skills whose display_title collides; re-using the
    existing id keeps the manifest correct without `--force` deletions.
    """
    try:
        page = client.beta.skills.list(betas=[BETA])
        return {
            getattr(sk, "display_title", ""): sk.id
            for sk in page.data
            if getattr(sk, "display_title", "")
        }
    except Exception as e:  # noqa: BLE001
        logger.warning("could not list existing skills: %s", e)
        return {}


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = _build_parser().parse_args(argv)

    if not args.avni_skills.exists():
        logger.error("avni-skills checkout not found at %s", args.avni_skills)
        return 1

    manifest = _load_manifest()

    if args.dry_run:
        for name in SPIKE_SKILLS:
            d = args.avni_skills / name
            print(
                f"DRY: would upload {name} from {d} ({'exists' if d.exists() else 'missing'})"
            )
        return 0

    if not os.environ.get("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY not set")
        return 1
    from anthropic import Anthropic

    client = Anthropic()
    existing = _index_existing(client)

    for name in SPIKE_SKILLS:
        d = args.avni_skills / name
        if not d.exists():
            logger.warning("skill dir missing: %s — skipping", d)
            continue
        skill_md = _ensure_skill_md(d)
        canonical = _read_skill_name(skill_md)

        if canonical in existing and not args.force:
            manifest[name] = existing[canonical]
            logger.info(
                "skill %s already exists as %s (%s); reusing",
                name,
                canonical,
                existing[canonical],
            )
            continue
        if args.force:
            _delete_existing(client, canonical)

        files = _collect_skill_files(d, top_folder=canonical)
        logger.info(
            "uploading %s as %s (%d files)", name, canonical, len(files)
        )
        created = client.beta.skills.create(
            display_title=canonical,
            files=files,
            betas=[BETA],
        )
        manifest[name] = created.id
        logger.info("uploaded %s -> %s", canonical, created.id)

    _save_manifest(manifest)
    print(f"\nmanifest written: {MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
