"""Tests for scripts/spike/upload_avni_skills.py — packaging logic only.

The actual skill upload to Anthropic is mocked; we don't network-call.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_HERE = Path(__file__).resolve().parent.parent.parent
_SPEC_PATH = _HERE / "scripts" / "spike" / "upload_avni_skills.py"
_spec = importlib.util.spec_from_file_location("upload_avni_skills", _SPEC_PATH)
upload_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(upload_mod)  # type: ignore[union-attr]


@pytest.fixture
def fake_avni_skills(tmp_path: Path) -> Path:
    """Build a tiny tree shaped like avni-skills/."""
    root = tmp_path / "avni-skills"
    root.mkdir()
    skill = root / "srs-bundle-generator"
    skill.mkdir()
    (skill / "SKILL.md").write_text("---\nname: srs-bundle-generator\n---\n# x\n")
    (skill / "scripts").mkdir()
    (skill / "scripts" / "gen.js").write_text("console.log('hi')")
    return root


def test_ensure_skill_md_finds_file(fake_avni_skills):
    skill = fake_avni_skills / "srs-bundle-generator"
    p = upload_mod._ensure_skill_md(skill)
    assert p.name == "SKILL.md"


def test_ensure_skill_md_raises_when_missing(tmp_path):
    d = tmp_path / "no-skill"
    d.mkdir()
    with pytest.raises(FileNotFoundError):
        upload_mod._ensure_skill_md(d)


def test_collect_skill_files_prefixes_top_folder(fake_avni_skills):
    """Anthropic enforces that every uploaded path starts with the same
    top-level folder; SKILL.md must sit directly inside it. Verify our
    packager honours that — the API rejects anything else."""
    skill = fake_avni_skills / "srs-bundle-generator"
    files = upload_mod._collect_skill_files(skill, top_folder="srs-bundle-generator")
    names = [f[0] for f in files]
    assert "srs-bundle-generator/SKILL.md" in names
    assert "srs-bundle-generator/scripts/gen.js" in names
    assert all(n.startswith("srs-bundle-generator/") for n in names)


def test_collect_skill_files_skips_noise(tmp_path):
    skill = tmp_path / "noisy-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("---\nname: noisy-skill\n---\n# x\n")
    (skill / ".DS_Store").write_bytes(b"\x00")
    (skill / "package-lock.json").write_text("{}")
    (skill / "node_modules").mkdir()
    (skill / "node_modules" / "junk.js").write_text("// no")
    files = upload_mod._collect_skill_files(skill, top_folder="noisy-skill")
    names = [f[0] for f in files]
    assert names == ["noisy-skill/SKILL.md"]


def test_read_skill_name_normalizes(tmp_path):
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text(
        "---\nname: AVNI Implementation Engineer\ndescription: x\n---\n# body\n"
    )
    assert upload_mod._read_skill_name(skill_md) == "avni-implementation-engineer"


def test_read_skill_name_rejects_missing_frontmatter(tmp_path):
    skill_md = tmp_path / "SKILL.md"
    skill_md.write_text("# no frontmatter\n")
    with pytest.raises(ValueError):
        upload_mod._read_skill_name(skill_md)


def test_load_save_manifest_roundtrip(tmp_path, monkeypatch):
    manifest_path = tmp_path / "skills.json"
    monkeypatch.setattr(upload_mod, "MANIFEST_PATH", manifest_path)
    assert upload_mod._load_manifest() == {}
    upload_mod._save_manifest({"a": "skill_1", "b": "skill_2"})
    parsed = json.loads(manifest_path.read_text())
    assert parsed == {"a": "skill_1", "b": "skill_2"}


def test_dry_run_does_not_call_anthropic(fake_avni_skills, monkeypatch, capsys):
    monkeypatch.setattr(upload_mod, "SPIKE_SKILLS", ("srs-bundle-generator",))
    rc = upload_mod.main(["--avni-skills", str(fake_avni_skills), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "DRY" in out and "srs-bundle-generator" in out


def test_main_returns_error_when_skills_dir_missing(tmp_path):
    rc = upload_mod.main(["--avni-skills", str(tmp_path / "nope")])
    assert rc == 1


def test_main_uploads_each_skill_and_writes_manifest(
    fake_avni_skills, tmp_path, monkeypatch
):
    """End-to-end with a mocked Anthropic client.

    Reaches into the module's `Anthropic` import path to stub the network."""
    manifest_path = tmp_path / "skills.json"
    monkeypatch.setattr(upload_mod, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(upload_mod, "SPIKE_SKILLS", ("srs-bundle-generator",))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")

    fake_client = MagicMock()
    # Empty list → nothing to reuse; new upload path is taken.
    fake_client.beta.skills.list.return_value = MagicMock(data=[])
    fake_client.beta.skills.create.return_value = MagicMock(id="skill_xyz")

    class _AnthropicStub:
        def __new__(cls, *a, **kw):
            return fake_client

    # Patch the import inside the module's main(); the import is local.
    import sys

    fake_anthropic_pkg = MagicMock()
    fake_anthropic_pkg.Anthropic = _AnthropicStub
    monkeypatch.setitem(sys.modules, "anthropic", fake_anthropic_pkg)

    rc = upload_mod.main(["--avni-skills", str(fake_avni_skills)])
    assert rc == 0
    parsed = json.loads(manifest_path.read_text())
    assert parsed == {"srs-bundle-generator": "skill_xyz"}
    fake_client.beta.skills.create.assert_called_once()


def test_main_reuses_existing_skill_by_display_title(
    fake_avni_skills, tmp_path, monkeypatch
):
    """If the org already has a skill whose display_title matches the
    canonical (normalized) name, the script must reuse its id rather than
    re-uploading — Anthropic rejects display_title collisions."""
    manifest_path = tmp_path / "skills.json"
    monkeypatch.setattr(upload_mod, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(upload_mod, "SPIKE_SKILLS", ("srs-bundle-generator",))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")

    existing = MagicMock()
    existing.id = "skill_existing"
    existing.display_title = "srs-bundle-generator"
    fake_client = MagicMock()
    fake_client.beta.skills.list.return_value = MagicMock(data=[existing])

    class _AnthropicStub:
        def __new__(cls, *a, **kw):
            return fake_client

    import sys

    fake_anthropic_pkg = MagicMock()
    fake_anthropic_pkg.Anthropic = _AnthropicStub
    monkeypatch.setitem(sys.modules, "anthropic", fake_anthropic_pkg)

    rc = upload_mod.main(["--avni-skills", str(fake_avni_skills)])
    assert rc == 0
    parsed = json.loads(manifest_path.read_text())
    assert parsed == {"srs-bundle-generator": "skill_existing"}
    fake_client.beta.skills.create.assert_not_called()
