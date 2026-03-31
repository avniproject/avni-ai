"""
Canonical ZIP ordering for Avni bundles.

Mirrors the exact file insertion order from BundleService.java createBundle()
and srs-bundle-generator/scripts/zip_bundle.js so that the Avni server
processes files in the correct sequence on upload.

Python's zipfile module preserves insertion order, so we use it directly
with deflate compression.
"""

import io
import json
import zipfile
from typing import Dict, Any, List

# ── Canonical order (mirrors zip_bundle.js / BundleService.java) ──────────

CANONICAL_ORDER: List[str] = [
    # 1. Address hierarchy
    "addressLevelTypes.json",
    # addressLevels.json and catchments.json only when includeLocations=true
    # 2. Subject types
    "subjectTypes.json",
    "operationalSubjectTypes.json",
    # 3. Encounter types
    "encounterTypes.json",
    "operationalEncounterTypes.json",
    # 4. Programs
    "programs.json",
    "operationalPrograms.json",
    # 5. Concepts
    "concepts.json",
    # 6. Forms — all forms/*.json inserted here (sorted alphabetically)
    "__FORMS__",
    # 7. Form mappings
    "formMappings.json",
    # 8. Organisation config
    "organisationConfig.json",
    # 9. Identity sources (skipped when no locations)
    # "identifierSource.json",
    # 10. Relations
    "individualRelation.json",
    "relationshipType.json",
    # 11. Checklists
    "checklistDetail.json",
    # 12. Groups & privileges
    "groups.json",
    "groupRole.json",
    "groupPrivilege.json",
    # 13. Media/video
    "video.json",
    # 14. Dashboards
    "reportCard.json",
    "reportDashboard.json",
    "groupDashboards.json",
    # 15. Documentation
    "documentations.json",
    # 16. Task management
    "taskType.json",
    "taskStatus.json",
    # 17. Translations
    "translations.json",
    # 18. Rule dependency
    "ruleDependency.json",
]


def _resolve_order(file_map: Dict[str, bytes]) -> List[str]:
    """Resolve CANONICAL_ORDER against actual files, expanding __FORMS__."""
    ordered: List[str] = []
    form_names = sorted(k for k in file_map if k.startswith("forms/"))

    for entry in CANONICAL_ORDER:
        if entry == "__FORMS__":
            ordered.extend(form_names)
        elif entry in file_map:
            ordered.append(entry)

    # Append any files not in the canonical order (e.g. validation_report.json)
    seen = set(ordered)
    for name in sorted(file_map.keys()):
        if name not in seen:
            ordered.append(name)

    return ordered


def create_canonical_zip(file_map: Dict[str, bytes]) -> bytes:
    """Create an in-memory ZIP with files in canonical BundleService order.

    Args:
        file_map: dict mapping ZIP entry names (e.g. "concepts.json",
                  "forms/MyForm.json") to their raw bytes content.

    Returns:
        The ZIP file as bytes, ready for upload.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in _resolve_order(file_map):
            zf.writestr(name, file_map[name])
    return buf.getvalue()


def unzip_to_map(zip_bytes: bytes) -> Dict[str, bytes]:
    """Unzip bytes into a dict of {filename: raw_bytes}.

    Args:
        zip_bytes: raw ZIP file bytes.

    Returns:
        dict mapping each ZIP entry name to its uncompressed content.
    """
    file_map: Dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            file_map[info.filename] = zf.read(info.filename)
    return file_map


def patch_bundle_zip(
    existing_zip_bytes: bytes,
    patches: Dict[str, Any],
) -> bytes:
    """Apply fractional JSON patches to an existing bundle ZIP.

    Args:
        existing_zip_bytes: the original bundle ZIP bytes.
        patches: dict mapping ZIP entry names to new JSON content.
                 For top-level files: {"concepts.json": [...]}
                 For forms: {"forms/MyForm.json": {...}}
                 If a value is None, the file is removed from the bundle.

    Returns:
        New ZIP bytes with patches applied, in canonical order.
    """
    file_map = unzip_to_map(existing_zip_bytes)

    for name, content in patches.items():
        if content is None:
            file_map.pop(name, None)
        else:
            if isinstance(content, (dict, list)):
                file_map[name] = json.dumps(content, indent=2).encode("utf-8")
            elif isinstance(content, str):
                file_map[name] = content.encode("utf-8")
            elif isinstance(content, bytes):
                file_map[name] = content
            else:
                file_map[name] = json.dumps(content, indent=2).encode("utf-8")

    return create_canonical_zip(file_map)
