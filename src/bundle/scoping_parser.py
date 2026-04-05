"""
scoping_parser.py — Parse Avni scoping/modelling Excel files into validated EntitySpec.

Handles two kinds of sheets generically:

**Modelling sheets** (entity definitions):
  - Location Hierarchy   : Location Type | Count
  - Subject Types        : Subject Type Name | Type | Lowest Address Level | ...
  - Program              : Program Name | Target Subject Type | ...
  - Encounters           : Encounter Name | Subject Type | Encounter Type | ...
  - Program Encounters   : Encounter Name | Program name | Encounter Type | ...

**Form sheets** (columns A–R, detected by header signature):
  Page Name | Field Name | Data Type | Mandatory | User entered/System generated |
  Allow Negative | Allow Decimal | Max and Min Limit | Unit |
  Allow Current Date | Allow Future Date | Allow Past Date |
  Selection Type | OPTIONS | Unique option | Option condition |
  When to show | When NOT to show

**W3H sheet** (form-to-entity mapping):
  What | When | Who | How | Forms to be scheduled | Notes

Returns a validated EntitySpec (Pydantic model) or raises ValueError on failures.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import pandas as pd

from ..schemas.bundle_models import (
    AddressLevelSpec,
    EncounterTypeSpec,
    EntitySpec,
    FieldSpec,
    FormSpec,
    ProgramSpec,
    SectionSpec,
    SkipLogicSpec,
    SubjectTypeSpec,
)

logger = logging.getLogger(__name__)

_DEFAULT_SCOPING_DOC = (
    Path(__file__).resolve().parents[2]
    / "tests"
    / "resources"
    / "scoping"
    / "Durga India Modelling.xlsx"
)

_SUBJECT_TYPE_MAP = {
    "individual": "Person",
    "person": "Person",
    "group": "Group",
    "household": "Household",
}


def _clean(val: Any) -> str:
    """Return stripped string or empty string for NaN/None."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    return str(val).strip()


def parse_location_hierarchy(df: pd.DataFrame) -> list[AddressLevelSpec]:
    """
    Parse 'Location Hierarchy' sheet.
    Expected columns: Location Type | Count
    Rows are listed top-down (highest → lowest), so we assign descending levels.
    """
    levels: list[AddressLevelSpec] = []
    rows = [(str(r[0]).strip(), str(r[1]).strip()) for r in df.itertuples(index=False) if _clean(r[0])]

    total = len(rows)
    prev_name: str | None = None
    for i, (loc_type, _count) in enumerate(rows):
        level = total - i
        levels.append(
            AddressLevelSpec(
                name=loc_type,
                level=level,
                parent=prev_name,
            )
        )
        prev_name = loc_type

    return levels


def parse_subject_types(df: pd.DataFrame) -> list[SubjectTypeSpec]:
    """
    Parse 'Subject Types' sheet.
    Expected columns: Subject Type Name | Type | ...
    """
    subject_types: list[SubjectTypeSpec] = []
    seen: set[str] = set()

    for _, row in df.iterrows():
        name = _clean(row.get("Subject Type Name", ""))
        if not name or name in seen:
            continue
        seen.add(name)

        raw_type = _clean(row.get("Type", "Person")).lower()
        avni_type = _SUBJECT_TYPE_MAP.get(raw_type, "Person")

        subject_types.append(
            SubjectTypeSpec(
                name=name,
                type=avni_type,
                allowProfilePicture=False,
                uniqueName=False,
                lastNameOptional=True,
            )
        )

    return subject_types


def parse_programs(df: pd.DataFrame, subject_type_names: set[str]) -> list[ProgramSpec]:
    """
    Parse 'Program' sheet.
    Expected columns: Program Name | Target Subject Type | ...
    """
    programs: list[ProgramSpec] = []
    seen: set[str] = set()

    for _, row in df.iterrows():
        name = _clean(row.get("Program Name", ""))
        if not name or name in seen:
            continue
        seen.add(name)

        target = _clean(row.get("Target Subject Type", ""))
        if not target and subject_type_names:
            target = next(iter(subject_type_names))

        programs.append(
            ProgramSpec(
                name=name,
                target_subject_type=target,
                colour="#4A148C",
                allow_multiple_enrolments=False,
            )
        )

    return programs


def parse_encounters(
    df: pd.DataFrame,
    subject_type_names: set[str],
    program_names: set[str],
    is_program_encounter: bool = False,
) -> list[EncounterTypeSpec]:
    """
    Parse 'Encounters' or 'Program Encounters' sheet.

    For 'Encounters':
      Columns: Encounter Name | Subject Type | Encounter Type (Scheduled/Unscheduled) | ...
    For 'Program Encounters':
      Columns: Encounter Name | Program name | Encounter Type (Scheduled/Unscheduled) | ...
    """
    encounter_types: list[EncounterTypeSpec] = []
    seen: set[str] = set()

    for _, row in df.iterrows():
        name = _clean(row.get("Encounter Name", ""))
        if not name or name in seen:
            continue
        seen.add(name)

        if is_program_encounter:
            program_name = _clean(row.get("Program name", row.get("Program Name", "")))
            subject_type = ""
        else:
            program_name = ""
            raw_subject = _clean(row.get("Subject Type", ""))
            subject_type = _resolve_subject_type(raw_subject, subject_type_names)

        enc_type_raw = _clean(
            row.get("Encounter Type (Scheduled/Unscheduled)", row.get("Encounter Type", "Scheduled"))
        ).lower()
        is_scheduled = "unscheduled" not in enc_type_raw

        encounter_types.append(
            EncounterTypeSpec(
                name=name,
                program_name=program_name,
                subject_type=subject_type,
                is_program_encounter=is_program_encounter or bool(program_name),
                is_scheduled=is_scheduled,
            )
        )

    return encounter_types


def _resolve_subject_type(raw: str, known: set[str]) -> str:
    """Fuzzy-match raw subject type name against known names."""
    if not raw:
        return ""
    raw_lower = raw.strip().lower()
    for name in known:
        if name.lower() == raw_lower or name.lower() in raw_lower or raw_lower in name.lower():
            return name
    return raw


# ── Data type mapping from scoping doc to Avni ──────────────────────────────

_SCOPING_DATA_TYPE_MAP: dict[str, str] = {
    "text": "Text",
    "numeric": "Numeric",
    "date": "Date",
    "pre added options": "Coded",
    "subject": "Subject",
    "duration": "Duration",
    "notes": "Notes",
    "image": "ImageV2",
    "phone number": "PhoneNumber",
    "location": "Location",
    "datetime": "DateTime",
    "file": "File",
    "audio": "Audio",
    "video": "Video",
}

# Sheets that are modelling/metadata — never form sheets
_MODELLING_SHEET_PREFIXES = (
    "location", "subject", "program", "encounter",
    "help", "project summary", "user persona", "w3h",
    "proposed process", "cost", "permissions", "report",
    "dashboard", "review", "question", "summary",
)


def _is_form_sheet(xf: pd.ExcelFile, sheet_name: str) -> bool:
    """
    Detect whether a sheet is a form sheet by checking its header row.
    Form sheets have 'Page Name' in col A and 'Field Name' in col B of row 1.
    """
    # Skip known modelling/metadata sheets
    lower = sheet_name.strip().lower()
    for prefix in _MODELLING_SHEET_PREFIXES:
        if lower.startswith(prefix):
            return False

    try:
        df = pd.read_excel(xf, sheet_name=sheet_name, header=None, nrows=2)
        if df.shape[0] < 2 or df.shape[1] < 3:
            return False
        # Row 1 (0-indexed) should contain the actual column headers
        row1 = [_clean(df.iloc[1, c]).lower() for c in range(min(3, df.shape[1]))]
        return row1[0].startswith("page name") and row1[1].startswith("field name")
    except Exception:
        return False


def _parse_yes_no(val: Any) -> bool:
    """Parse a Yes/No cell value to bool."""
    return _clean(val).lower() in ("yes", "y", "true", "1")


def _parse_options(val: Any) -> list[str]:
    """Parse options from a cell (newline, semicolon, or comma separated)."""
    raw = _clean(val)
    if not raw:
        return []
    # Split by newlines first, then semicolons, then commas
    if "\n" in raw:
        parts = raw.split("\n")
    elif ";" in raw:
        parts = raw.split(";")
    else:
        parts = raw.split(",")
    return [p.strip() for p in parts if p.strip()]


def _parse_min_max(val: Any) -> tuple[float | None, float | None]:
    """Parse a 'Min and Max Limit' cell like '0-100' or '18 to 99'."""
    raw = _clean(val)
    if not raw:
        return None, None
    # Try patterns: "0-100", "0 - 100", "0 to 100", "min:0,max:100"
    m = re.match(r"(-?[\d.]+)\s*[-–to]+\s*(-?[\d.]+)", raw, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1)), float(m.group(2))
        except ValueError:
            pass
    return None, None


def parse_w3h_sheet(
    xf: pd.ExcelFile,
    sheet_names_lower: dict[str, str],
    subject_type_names: set[str],
    encounter_type_names: set[str],
    program_encounter_map: dict[str, str],
) -> dict[str, dict[str, str | None]]:
    """
    Parse 'W3H' sheet to build form-to-entity mapping.

    Returns:
        { "Session": {"formType": "Encounter", "subjectType": "Participant",
                       "encounterType": "Session", "program": None},
          "Participant Details": {"formType": "IndividualProfile",
                                   "subjectType": "Participant", ...}, ... }
    """
    w3h_actual = None
    for lower_name, actual_name in sheet_names_lower.items():
        if lower_name.startswith("w3h"):
            w3h_actual = actual_name
            break

    if not w3h_actual:
        logger.info("No W3H sheet found — form-entity mapping will be deferred to Spec Agent")
        return {}

    try:
        df = pd.read_excel(xf, sheet_name=w3h_actual)
        df = df.dropna(how="all")
    except Exception as e:
        logger.warning("Failed to read W3H sheet: %s", e)
        return {}

    # Find 'What' column (usually col A)
    what_col = None
    for col in df.columns:
        if "what" in str(col).lower():
            what_col = col
            break
    if what_col is None and len(df.columns) > 0:
        what_col = df.columns[0]

    if what_col is None:
        return {}

    st_names_lower = {n.lower(): n for n in subject_type_names}
    enc_names_lower = {n.lower(): n for n in encounter_type_names}

    # Registration-related keywords
    _REG_KEYWORDS = ("registration", "register", "details", "profile", "enrolment", "enrollment")

    mapping: dict[str, dict[str, str | None]] = {}
    for _, row in df.iterrows():
        activity = _clean(row.get(what_col, ""))
        if not activity:
            continue

        activity_lower = activity.lower()
        entry: dict[str, str | None] = {
            "formType": None,
            "subjectType": None,
            "encounterType": None,
            "program": None,
        }

        # Check if this is a registration form
        is_registration = any(kw in activity_lower for kw in _REG_KEYWORDS)

        if is_registration:
            entry["formType"] = "IndividualProfile"
            # Try to match a subject type from the activity name
            for st_lower, st_name in st_names_lower.items():
                if st_lower in activity_lower or activity_lower in st_lower:
                    entry["subjectType"] = st_name
                    break
            # If no subject type matched and there's only one, use it
            if not entry["subjectType"] and len(subject_type_names) == 1:
                entry["subjectType"] = next(iter(subject_type_names))
        else:
            # Try to match an encounter type
            matched_enc = None
            for enc_lower, enc_name in enc_names_lower.items():
                if enc_lower == activity_lower or enc_lower in activity_lower or activity_lower in enc_lower:
                    matched_enc = enc_name
                    break
            if matched_enc:
                entry["encounterType"] = matched_enc
                prog = program_encounter_map.get(matched_enc)
                if prog:
                    entry["formType"] = "ProgramEncounter"
                    entry["program"] = prog
                else:
                    entry["formType"] = "Encounter"
                # Resolve subject type for the encounter
                for enc in []:
                    pass  # subject type resolution happens later
            else:
                # Unmatched — leave formType as None for Spec Agent
                logger.info("W3H activity '%s' not matched to any entity", activity)

        mapping[activity] = entry

    return mapping


def _match_sheet_to_w3h(
    sheet_name: str, w3h_mapping: dict[str, dict[str, str | None]]
) -> dict[str, str | None] | None:
    """Try to match a form sheet name to a W3H activity entry."""
    sheet_lower = sheet_name.strip().lower()
    # Exact match
    for activity, entry in w3h_mapping.items():
        if activity.lower() == sheet_lower:
            return entry
    # Fuzzy: sheet name contained in activity or vice versa
    for activity, entry in w3h_mapping.items():
        act_lower = activity.lower()
        if act_lower in sheet_lower or sheet_lower in act_lower:
            return entry
    # Token overlap — at least 50% of tokens must match
    sheet_tokens = set(sheet_lower.split())
    for activity, entry in w3h_mapping.items():
        act_tokens = set(activity.lower().split())
        if not sheet_tokens or not act_tokens:
            continue
        overlap = len(sheet_tokens & act_tokens)
        if overlap / max(len(sheet_tokens), len(act_tokens)) >= 0.5:
            return entry
    return None


def parse_form_sheet(
    xf: pd.ExcelFile,
    sheet_name: str,
    entity_mapping: dict[str, str | None] | None,
) -> FormSpec | None:
    """
    Parse a single form sheet (columns A–R) into a FormSpec.
    Row 0 = category headers (skip), Row 1 = column headers, Row 2+ = data.
    """
    try:
        df = pd.read_excel(xf, sheet_name=sheet_name, header=None)
    except Exception as e:
        logger.warning("Failed to read form sheet '%s': %s", sheet_name, e)
        return None

    if df.shape[0] < 3:  # Need at least header + 1 data row
        return None

    # Data rows start at row index 2 (row 0 = category, row 1 = headers)
    current_section = "General Information"
    fields: list[FieldSpec] = []

    for row_idx in range(2, df.shape[0]):
        row = df.iloc[row_idx]
        field_name = _clean(row.iloc[1]) if df.shape[1] > 1 else ""
        if not field_name:
            continue

        # Column A: Page Name (section name) — carries forward if empty
        page_name = _clean(row.iloc[0]) if df.shape[1] > 0 else ""
        if page_name:
            current_section = page_name

        # Column C: Data Type
        raw_dtype = _clean(row.iloc[2]).lower().strip() if df.shape[1] > 2 else "text"
        avni_dtype = _SCOPING_DATA_TYPE_MAP.get(raw_dtype, "Text")

        # Column D: Mandatory
        mandatory = _parse_yes_no(row.iloc[3]) if df.shape[1] > 3 else False

        # Columns F-L: numeric/date key-values
        kv: dict[str, Any] = {}
        if df.shape[1] > 5 and _parse_yes_no(row.iloc[5]):
            kv["allowNegativeValue"] = True
        if df.shape[1] > 6 and _parse_yes_no(row.iloc[6]):
            kv["allowDecimalValue"] = True
        if df.shape[1] > 10 and _parse_yes_no(row.iloc[10]):
            kv["allowFutureDate"] = True

        # Column H: Min/Max
        min_val, max_val = None, None
        if df.shape[1] > 7:
            min_val, max_val = _parse_min_max(row.iloc[7])

        # Column I: Unit
        unit = _clean(row.iloc[8]) if df.shape[1] > 8 else None
        if not unit:
            unit = None

        # Column M: Selection type (Single Select / Multi Select)
        selection_type = None
        if df.shape[1] > 12:
            sel_raw = _clean(row.iloc[12]).lower()
            if "multi" in sel_raw:
                selection_type = "MultiSelect"
            elif "single" in sel_raw:
                selection_type = "SingleSelect"

        # For Coded data type, override based on selection type
        if avni_dtype == "Coded" and selection_type:
            pass  # Keep Coded, selection_type stored separately

        # Column N: Options
        options = None
        if df.shape[1] > 13:
            options = _parse_options(row.iloc[13]) or None

        # Columns Q/R: Skip logic (when to show / when not to show)
        skip_logic = None
        if df.shape[1] > 16:
            when_to_show = _clean(row.iloc[16])
            if when_to_show:
                skip_logic = SkipLogicSpec(
                    dependsOn=when_to_show,
                    condition="raw",
                    value=when_to_show,
                )

        field = FieldSpec(
            name=field_name,
            dataType=avni_dtype,
            mandatory=mandatory,
            group=current_section,
            unit=unit,
            min=min_val,
            max=max_val,
            options=options,
            selectionType=selection_type,
            skipLogic=skip_logic,
            keyValues=kv if kv else None,
        )
        fields.append(field)

    if not fields:
        logger.info("Form sheet '%s' has no data rows — skipping", sheet_name)
        return None

    # Build FormSpec from entity mapping (if available) or leave unlinked
    form_type = "Encounter"  # default
    subject_type = None
    program = None
    encounter_type = None

    if entity_mapping:
        form_type = entity_mapping.get("formType") or "Encounter"
        subject_type = entity_mapping.get("subjectType")
        program = entity_mapping.get("program")
        encounter_type = entity_mapping.get("encounterType")

    # Build sections from grouped fields
    sections: list[SectionSpec] = []
    current_sec_name = None
    current_sec_fields: list[FieldSpec] = []
    for f in fields:
        sec_name = f.group or "General Information"
        if sec_name != current_sec_name:
            if current_sec_fields:
                sections.append(SectionSpec(name=current_sec_name or "General Information", fields=current_sec_fields))
            current_sec_name = sec_name
            current_sec_fields = [f]
        else:
            current_sec_fields.append(f)
    if current_sec_fields:
        sections.append(SectionSpec(name=current_sec_name or "General Information", fields=current_sec_fields))

    form_spec = FormSpec(
        name=sheet_name.strip(),
        formType=form_type,
        subjectType=subject_type,
        program=program,
        encounterType=encounter_type,
        fields=fields,
        sections=sections,
    )

    logger.info(
        "Parsed form sheet '%s': %d fields, %d sections, formType=%s",
        sheet_name, len(fields), len(sections), form_type,
    )
    return form_spec


def parse_form_sheets(
    xf: pd.ExcelFile,
    sheet_names_lower: dict[str, str],
    subject_type_names: set[str],
    encounter_type_names: set[str],
    program_encounter_map: dict[str, str],
) -> list[FormSpec]:
    """
    Detect and parse all form sheets in the scoping document.

    Uses W3H sheet for form-entity mapping, falls back to unlinked forms
    for the Dify Spec Agent to resolve.
    """
    # Stage 1: Parse W3H for form-entity mapping
    w3h_mapping = parse_w3h_sheet(
        xf, sheet_names_lower, subject_type_names,
        encounter_type_names, program_encounter_map,
    )
    logger.info("W3H mapping: %d activities mapped", len(w3h_mapping))

    # Stage 2: Find and parse form sheets
    forms: list[FormSpec] = []
    for sheet_name in xf.sheet_names:
        if not _is_form_sheet(xf, sheet_name):
            continue

        # Match sheet to W3H entity mapping
        entity_mapping = _match_sheet_to_w3h(sheet_name, w3h_mapping)
        if entity_mapping:
            logger.info("Matched form sheet '%s' to W3H entity", sheet_name)
        else:
            logger.info("Form sheet '%s' has no W3H match — unlinked (Spec Agent will resolve)", sheet_name)

        form = parse_form_sheet(xf, sheet_name, entity_mapping)
        if form:
            forms.append(form)

    logger.info("Parsed %d form sheets total", len(forms))
    return forms


def parse_scoping_doc(xlsx_path: str | Path | None = None) -> EntitySpec:
    """
    Parse the Avni modelling workbook and return a validated EntitySpec.

    Args:
        xlsx_path: Path to the .xlsx file. Defaults to SCOPING_DOC_PATH env var
                   or the bundled Durga India Modelling.xlsx test fixture.

    Returns:
        EntitySpec — validated Pydantic model.

    Raises:
        FileNotFoundError: if the file doesn't exist.
        ValueError: if the parsed entities fail Pydantic cross-ref validation.
    """
    import os

    if xlsx_path is None:
        xlsx_path = os.environ.get("SCOPING_DOC_PATH", str(_DEFAULT_SCOPING_DOC))

    path = Path(xlsx_path)
    if not path.exists():
        raise FileNotFoundError(f"Scoping document not found: {path}")

    logger.info("Parsing scoping document: %s", path)
    xf = pd.ExcelFile(path)
    sheet_names_lower = {s.strip().lower(): s for s in xf.sheet_names}

    def _read(key: str) -> pd.DataFrame:
        """Read sheet by case-insensitive key prefix match."""
        for lower_name, actual_name in sheet_names_lower.items():
            if lower_name.startswith(key.lower()):
                df = pd.read_excel(xf, sheet_name=actual_name)
                return df.dropna(how="all")
        return pd.DataFrame()

    loc_df = _read("location")
    st_df = _read("subject")
    prog_df = _read("program")
    enc_df = _read("encounter")
    prog_enc_df = _read("program encounter")

    address_levels = parse_location_hierarchy(loc_df) if not loc_df.empty else []
    subject_types = parse_subject_types(st_df) if not st_df.empty else []
    subject_type_names = {st.name for st in subject_types}

    programs = parse_programs(prog_df, subject_type_names) if not prog_df.empty else []
    program_names = {p.name for p in programs}

    enc_types: list[EncounterTypeSpec] = []
    if not enc_df.empty:
        enc_types.extend(parse_encounters(enc_df, subject_type_names, program_names, is_program_encounter=False))
    if not prog_enc_df.empty:
        enc_types.extend(parse_encounters(prog_enc_df, subject_type_names, program_names, is_program_encounter=True))

    if not address_levels:
        logger.warning("No location hierarchy found in scoping doc — using default State/District/Village")
        address_levels = [
            AddressLevelSpec(name="State", level=3, parent=None),
            AddressLevelSpec(name="District", level=2, parent="State"),
            AddressLevelSpec(name="Village", level=1, parent="District"),
        ]

    # Build encounter → program lookup for form-entity mapping
    encounter_type_names = {et.name for et in enc_types}
    program_encounter_map: dict[str, str] = {}
    for et in enc_types:
        if et.program_name:
            program_encounter_map[et.name] = et.program_name

    # Parse form sheets (columns A–R) with W3H mapping
    forms = parse_form_sheets(
        xf, sheet_names_lower, subject_type_names,
        encounter_type_names, program_encounter_map,
    )

    logger.info(
        "Parsed: %d address levels, %d subject types, %d programs, %d encounter types, %d forms",
        len(address_levels),
        len(subject_types),
        len(programs),
        len(enc_types),
        len(forms),
    )

    return EntitySpec(
        subject_types=subject_types,
        programs=programs,
        encounter_types=enc_types,
        address_levels=address_levels,
        groups=[],
        forms=forms,
    )


def load_durga_entities(xlsx_path: str | Path | None = None) -> dict:
    """
    Parse the Durga India scoping document and return a plain dict
    suitable for use with the AppConfiguratorFlow emulation.

    This is the replacement for load_sample_entities() — it reads real
    Durga data instead of hardcoded Maternal Health placeholders.
    """
    entity_spec = parse_scoping_doc(xlsx_path)
    return entity_spec.to_entities_dict()
