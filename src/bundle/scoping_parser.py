"""
scoping_parser.py — Parse any combination of SRS/scoping/modelling files into
a validated AVNI EntitySpec.

Accepts: .xlsx (multi-sheet), .csv, .txt, .json — any number of files.
Each sheet/file is auto-classified by its content (column headers, data patterns)
into one of: location_hierarchy, subject_types, programs, encounters,
program_encounters, w3h_mapping, form_fields, or ignored.

The parser is content-driven, not name-driven — it works regardless of sheet
names or column header variations.
"""

from __future__ import annotations

import io
import json
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
    GroupSpec,
    ProgramSpec,
    SectionSpec,
    SkipLogicSpec,
    SubjectTypeSpec,
)

pd.set_option("future.no_silent_downcasting", True)

logger = logging.getLogger(__name__)

_DEFAULT_SCOPING_DOC = (
    Path(__file__).resolve().parents[2]
    / "tests"
    / "resources"
    / "scoping"
    / "Durga India Modelling.xlsx"
)

# ── Constants ────────────────────────────────────────────────────────────────

_SUBJECT_TYPE_MAP = {
    "individual": "Person",
    "person": "Person",
    "group": "Group",
    "household": "Household",
}

_DATA_TYPE_MAP: dict[str, str] = {
    "text": "Text",
    "string": "Text",
    "varchar": "Text",
    "numeric": "Numeric",
    "number": "Numeric",
    "integer": "Numeric",
    "int": "Numeric",
    "decimal": "Numeric",
    "float": "Numeric",
    "date": "Date",
    "datetime": "DateTime",
    "pre added options": "Coded",
    "coded": "Coded",
    "single select": "Coded",
    "single-select": "Coded",
    "multi select": "Coded",
    "multi-select": "Coded",
    "dropdown": "Coded",
    "radio": "Coded",
    "checkbox": "Coded",
    "boolean": "Coded",
    "bool": "Coded",
    "yes/no": "Coded",
    "subject": "Subject",
    "duration": "Duration",
    "notes": "Notes",
    "image": "ImageV2",
    "imagev2": "ImageV2",
    "photo": "ImageV2",
    "phone number": "PhoneNumber",
    "phonenumber": "PhoneNumber",
    "phone": "PhoneNumber",
    "mobile": "PhoneNumber",
    "location": "Location",
    "file": "File",
    "audio": "Audio",
    "video": "Video",
    "questiongroup": "QuestionGroup",
    "question group": "QuestionGroup",
    "repeatable": "QuestionGroup",
}

# Header patterns for auto-classification (lowercase, checked via substring)
_LOCATION_HEADERS = {"location type", "location", "address level", "hierarchy"}
_SUBJECT_HEADERS = {"subject type", "subject type name", "entity type", "type"}
_PROGRAM_HEADERS = {"program name", "program", "target subject"}
_ENCOUNTER_HEADERS = {"encounter name", "encounter type", "scheduled", "unscheduled"}
_FORM_HEADERS = {"field name", "data type", "mandatory", "page name"}
_W3H_HEADERS = {"what", "when", "who", "how"}


# ── Helpers ──────────────────────────────────────────────────────────────────


def _clean(val: Any) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    return str(val).strip()


# Regex to strip leading numbering prefixes from field/concept names:
# "1. Name" → "Name", "2) Age" → "Age", "A. Gender" → "Gender",
# "1.2 Weight" → "Weight", "1.2.3 Height" → "Height"
_NUMBER_PREFIX_RE = re.compile(
    r"^\s*"
    r"(?:"
    r"[0-9]+(?:\.[0-9]+)*"  # "1", "1.2", "1.2.3"
    r"|[A-Za-z]"  # single letter like "A", "B"
    r")"
    r"[\.\)\-:\s]\s*"  # followed by . ) - : or space
)


def _clean_field_name(val: Any) -> str:
    """Clean a field/concept name: strip whitespace and numbering prefixes."""
    name = _clean(val)
    if not name:
        return name
    # Strip leading number prefixes like "1. ", "2) ", "A. ", "1.2 "
    name = _NUMBER_PREFIX_RE.sub("", name)
    # Also strip trailing numbering artefacts
    return name.strip()


def _parse_yes_no(val: Any) -> bool:
    return _clean(val).lower() in ("yes", "y", "true", "1")


def _parse_options(val: Any) -> list[str]:
    raw = _clean(val)
    if not raw:
        return []
    if "\n" in raw:
        parts = raw.split("\n")
    elif ";" in raw:
        parts = raw.split(";")
    else:
        parts = raw.split(",")
    return [
        _NUMBER_PREFIX_RE.sub("", p.strip().rstrip(",")).strip()
        for p in parts
        if p.strip() and p.strip().lower() != "nan"
    ]


def _parse_min_max(val: Any) -> tuple[float | None, float | None]:
    raw = _clean(val)
    if not raw:
        return None, None
    m = re.match(r"(-?[\d.]+)\s*[-–to]+\s*(-?[\d.]+)", raw, re.IGNORECASE)
    if m:
        try:
            return float(m.group(1)), float(m.group(2))
        except ValueError:
            pass
    return None, None


def _resolve_subject_type(raw: str, known: set[str]) -> str:
    if not raw:
        return ""
    raw_lower = raw.strip().lower()
    # Also try cleaned version (strip "Registration" etc.)
    cleaned_lower = _clean_subject_name(raw).lower()
    # Exact match first
    for name in known:
        nl = name.lower()
        if nl == raw_lower or nl == cleaned_lower:
            return name
    # Substring match
    for name in known:
        nl = name.lower()
        if (
            nl in raw_lower
            or raw_lower in nl
            or nl in cleaned_lower
            or cleaned_lower in nl
        ):
            return name
    return _clean_subject_name(raw)


def _map_data_type(raw: str) -> str:
    lower = raw.strip().lower()
    return _DATA_TYPE_MAP.get(lower, "Text")


def _find_col(df: pd.DataFrame, *candidates: str) -> str | None:
    """Find a column in df by fuzzy matching against candidate names."""
    cols_lower = {str(c).strip().lower(): str(c) for c in df.columns}
    for cand in candidates:
        cand_lower = cand.lower()
        # Exact
        if cand_lower in cols_lower:
            return cols_lower[cand_lower]
        # Substring
        for col_lower, col_orig in cols_lower.items():
            if cand_lower in col_lower or col_lower in cand_lower:
                return col_orig
    return None


# ── Sheet Classification ─────────────────────────────────────────────────────


def _classify_sheet(df: pd.DataFrame, sheet_name: str = "") -> str:
    """
    Classify a DataFrame by its column headers into one of:
    location, subject_type, program, encounter, program_encounter,
    w3h, form, or unknown.

    Uses the FIRST column as the strongest signal — it's usually the primary
    entity name (e.g. "Encounter Name", "Subject Type Name", "Program Name").
    Falls back to sheet_name pattern matching when content headers are ambiguous.
    """
    if df.empty or df.shape[1] < 2:
        return "unknown"

    cols_lower = [str(c).strip().lower() for c in df.columns]
    cols_set = set(cols_lower)
    first_col = cols_lower[0] if cols_lower else ""

    # W3H — "what" as first column + "when"/"who"/"how"
    if first_col in ("what", "activity") and any(
        c in cols_set for c in ("when", "who", "how")
    ):
        return "w3h"

    # Form fields — "field name" or "page name" + "data type"
    has_field_name = any("field name" in c for c in cols_lower)
    has_data_type = any("data type" in c or "datatype" in c for c in cols_lower)
    if has_field_name and has_data_type:
        return "form"

    # Encounters — first col contains "encounter name" or "encounter type"
    if (
        "encounter name" in first_col
        or "encounter type" in first_col
        or first_col in ("encounter", "encounter type")
    ):
        # Program encounters have a "program" column too
        if any("program" in c for c in cols_lower[1:]):
            return "program_encounter"
        return "encounter"

    # Subject types — first col is "subject type name" or similar
    if "subject type name" in first_col or first_col == "subject type":
        return "subject_type"

    # Programs — first col is "program name" or standalone "program" with structural cols
    if "program name" in first_col or first_col == "program name":
        return "program"
    if first_col == "program" and any(
        "target" in c
        or "subject" in c
        or "enrolment" in c
        or "colour" in c
        or "color" in c
        for c in cols_lower
    ):
        return "program"

    # Location hierarchy — first col is "location type" or similar
    if "location" in first_col and (
        "type" in first_col or "hierarchy" in first_col or "level" in first_col
    ):
        return "location"
    if first_col == "location type":
        return "location"

    # ── Sheet-name fallback (when column headers are ambiguous) ─────────────
    if sheet_name:
        sn = sheet_name.strip().lower()
        if "program encounter" in sn:
            return "program_encounter"
        if sn in ("program", "programs"):
            return "program"
        if "encounter" in sn and "program" not in sn:
            return "encounter"
        if "subject type" in sn or sn in ("subject types", "subjects"):
            return "subject_type"
        if "location hierarchy" in sn or sn in (
            "location",
            "locations",
            "address levels",
        ):
            return "location"

    return "unknown"


# ── Entity Parsers ───────────────────────────────────────────────────────────


def parse_location_hierarchy(df: pd.DataFrame) -> list[AddressLevelSpec]:
    levels: list[AddressLevelSpec] = []
    rows = [(_clean(r[0]),) for r in df.itertuples(index=False) if _clean(r[0])]
    total = len(rows)
    prev_name: str | None = None
    for i, (loc_type,) in enumerate(rows):
        level = total - i
        levels.append(AddressLevelSpec(name=loc_type, level=level, parent=prev_name))
        prev_name = loc_type
    return levels


_SUBJECT_NAME_STRIP_SUFFIXES = [
    " registration",
    " enrolment",
    " enrollment",
    " form",
    " profile",
    " details",
    " entry",
]

# Header row values that should be filtered out
_HEADER_ROW_VALUES = {
    "subject type",
    "subject type name",
    "name",
    "entity name",
    "encounter name",
    "encounter",
    "program name",
    "program",
    "type",
    "entity type",
    "scheduled",
    "unscheduled",
}


def _clean_subject_name(raw: str) -> str:
    """Clean a subject type name: strip form-like suffixes.
    'Beneficiary Registration' → 'Beneficiary'
    'School Registration' → 'School'
    """
    name = raw.strip()
    lower = name.lower()
    for suffix in _SUBJECT_NAME_STRIP_SUFFIXES:
        if lower.endswith(suffix):
            name = name[: len(name) - len(suffix)].strip()
            break
    return name


def _is_header_row(name: str) -> bool:
    """Check if a parsed name is actually a header row value."""
    return name.strip().lower() in _HEADER_ROW_VALUES


def parse_subject_types(df: pd.DataFrame) -> list[SubjectTypeSpec]:
    subject_types: list[SubjectTypeSpec] = []
    seen: set[str] = set()

    name_col = _find_col(df, "Subject Type Name", "Subject Type", "Name", "Entity Name")
    type_col = _find_col(df, "Type", "Subject Type", "Entity Type")

    if not name_col:
        return []

    for _, row in df.iterrows():
        raw_name = _clean(row.get(name_col, ""))
        if not raw_name or _is_header_row(raw_name):
            continue

        name = _clean_subject_name(raw_name)
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())

        raw_type = _clean(row.get(type_col, "Person")).lower() if type_col else "person"
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
    programs: list[ProgramSpec] = []
    seen: set[str] = set()

    name_col = _find_col(df, "Program Name", "Program", "Name")
    target_col = _find_col(df, "Target Subject Type", "Target Subject", "Subject Type")

    if not name_col:
        return []

    for _, row in df.iterrows():
        name = _clean(row.get(name_col, ""))
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())

        target = _clean(row.get(target_col, "")) if target_col else ""
        if not target and subject_type_names:
            target = next(iter(subject_type_names))

        programs.append(
            ProgramSpec(name=name, target_subject_type=target, colour="#4A148C")
        )
    return programs


def parse_encounters(
    df: pd.DataFrame,
    subject_type_names: set[str],
    program_names: set[str],
    is_program_encounter: bool = False,
) -> list[EncounterTypeSpec]:
    encounter_types: list[EncounterTypeSpec] = []
    seen: set[str] = set()

    name_col = _find_col(df, "Encounter Name", "Encounter", "Name")
    if not name_col:
        return []

    sched_col = _find_col(
        df,
        "Encounter Type (Scheduled/Unscheduled)",
        "Encounter Type",
        "Scheduled",
        "Type",
    )

    if is_program_encounter:
        prog_col = _find_col(df, "Program name", "Program Name", "Program")
        st_col = None
    else:
        prog_col = None
        st_col = _find_col(df, "Subject Type", "Subject", "Entity")

    for _, row in df.iterrows():
        name = _clean(row.get(name_col, ""))
        if not name or name.lower() in seen:
            continue
        # Skip header rows that got parsed as data
        if _is_header_row(name):
            continue
        seen.add(name.lower())

        program_name = ""
        subject_type = ""

        if is_program_encounter and prog_col:
            raw_prog = _clean(row.get(prog_col, ""))
            if not _is_header_row(raw_prog):
                program_name = raw_prog
        elif st_col:
            raw_subject = _clean(row.get(st_col, ""))
            if not _is_header_row(raw_subject):
                subject_type = _resolve_subject_type(raw_subject, subject_type_names)

        enc_type_raw = ""
        if sched_col:
            enc_type_raw = _clean(row.get(sched_col, "")).lower()
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


# ── W3H Parser ───────────────────────────────────────────────────────────────


def parse_w3h(
    df: pd.DataFrame,
    subject_type_names: set[str],
    encounter_type_names: set[str],
    program_encounter_map: dict[str, str],
) -> dict[str, dict[str, str | None]]:
    """Parse W3H sheet to build form → entity mapping."""
    what_col = _find_col(df, "What", "Activity", "Form")
    if not what_col:
        what_col = str(df.columns[0]) if len(df.columns) > 0 else None
    if not what_col:
        return {}

    st_names_lower = {n.lower(): n for n in subject_type_names}
    enc_names_lower = {n.lower(): n for n in encounter_type_names}

    _REG_KEYWORDS = (
        "registration",
        "register",
        "details",
        "profile",
        "enrolment",
        "enrollment",
    )

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

        is_registration = any(kw in activity_lower for kw in _REG_KEYWORDS)

        if is_registration:
            entry["formType"] = "IndividualProfile"
            for st_lower, st_name in st_names_lower.items():
                if st_lower in activity_lower or activity_lower in st_lower:
                    entry["subjectType"] = st_name
                    break
            if not entry["subjectType"] and len(subject_type_names) == 1:
                entry["subjectType"] = next(iter(subject_type_names))
        else:
            matched_enc = None
            for enc_lower, enc_name in enc_names_lower.items():
                if (
                    enc_lower == activity_lower
                    or enc_lower in activity_lower
                    or activity_lower in enc_lower
                ):
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

        mapping[activity] = entry

    return mapping


# ── Form Sheet Parser ────────────────────────────────────────────────────────


def _match_sheet_to_w3h(
    sheet_name: str, w3h_mapping: dict[str, dict[str, str | None]]
) -> dict[str, str | None] | None:
    """Match a form sheet name to a W3H activity. Picks best scored match."""
    sheet_lower = sheet_name.strip().lower()

    # Exact match
    for activity, entry in w3h_mapping.items():
        if activity.lower() == sheet_lower:
            return entry

    # Scored matching
    sheet_tokens = set(sheet_lower.split())
    best_score = 0.0
    best_entry = None

    for activity, entry in w3h_mapping.items():
        act_lower = activity.lower()

        if act_lower in sheet_lower or sheet_lower in act_lower:
            score = min(len(act_lower), len(sheet_lower)) / max(
                len(act_lower), len(sheet_lower)
            )
            score += 1.0
        else:
            act_tokens = set(act_lower.split())
            if not sheet_tokens or not act_tokens:
                continue
            overlap = len(sheet_tokens & act_tokens)
            score = overlap / max(len(sheet_tokens), len(act_tokens))

        if score > best_score:
            best_score = score
            best_entry = entry

    if best_score >= 0.5:
        return best_entry
    return None


def parse_form_df(
    df: pd.DataFrame,
    sheet_name: str,
    entity_mapping: dict[str, str | None] | None,
    header_offset: int = 0,
) -> FormSpec | None:
    """
    Parse a form DataFrame into a FormSpec.
    header_offset=0: headers in row 0 (standard CSV/clean Excel)
    header_offset=1: headers in row 1 (scoping Excel with category row in row 0)
    """
    if header_offset == 1:
        # Re-read with row 1 as header
        if df.shape[0] < 3:
            return None
        # Use raw positional access — row 0 = categories, row 1 = headers, row 2+ = data
        data_start = 2
    else:
        data_start = 0

    # Find columns by fuzzy matching on the header row
    if header_offset == 1:
        header_row = {str(df.iloc[1, c]).strip().lower(): c for c in range(df.shape[1])}
    else:
        header_row = {str(c).strip().lower(): i for i, c in enumerate(df.columns)}

    def _col_idx(*names: str) -> int | None:
        for n in names:
            n_lower = n.lower()
            for h, idx in header_row.items():
                if n_lower == h or n_lower in h or h in n_lower:
                    return idx
        return None

    page_idx = _col_idx("page name", "page", "section")
    field_idx = _col_idx("field name", "field", "question", "name")
    dtype_idx = _col_idx("data type", "datatype", "type")
    mand_idx = _col_idx("mandatory")
    options_idx = _col_idx("options", "option")
    selection_idx = _col_idx("selection type", "selection")
    min_max_idx = _col_idx("max and min", "min and max", "limit", "range")
    unit_idx = _col_idx("unit")
    skip_idx = _col_idx("when to show", "skip logic", "condition", "visibility")

    if field_idx is None:
        return None

    current_section = "General Information"
    fields: list[FieldSpec] = []

    for row_idx in range(data_start, df.shape[0]):
        row = df.iloc[row_idx]
        field_name = (
            _clean_field_name(row.iloc[field_idx]) if field_idx is not None else ""
        )
        if not field_name:
            continue

        if page_idx is not None:
            page = _clean(row.iloc[page_idx])
            if page:
                current_section = page

        raw_dtype = (
            _clean(row.iloc[dtype_idx]).lower() if dtype_idx is not None else "text"
        )
        avni_dtype = _map_data_type(raw_dtype)

        # Detect dtype column displacement:
        # Case A — dtype cell contains comma/newline-separated values (options bled in):
        #   treat field as Coded and carry those values forward as options candidate.
        _dtype_displaced_options: list[str] | None = None
        if dtype_idx is not None and avni_dtype == "Text" and raw_dtype:
            if "," in raw_dtype or "\n" in raw_dtype or ";" in raw_dtype:
                _dtype_displaced_options = _parse_options(row.iloc[dtype_idx])
                if _dtype_displaced_options:
                    avni_dtype = "Coded"
                    # Try to recover the real type from adjacent columns
                    for scan_idx in range(
                        dtype_idx + 1, min(dtype_idx + 3, row.shape[0])
                    ):
                        candidate_type = _clean(row.iloc[scan_idx]).lower()
                        if candidate_type in _DATA_TYPE_MAP:
                            avni_dtype = _DATA_TYPE_MAP[candidate_type]
                            _dtype_displaced_options = (
                                None  # not displaced options after all
                            )
                            break

        # Case B — dtype cell has an unrecognised single token but an adjacent cell has a
        #   valid type keyword (one-column right-shift of the whole row):
        if (
            dtype_idx is not None
            and avni_dtype == "Text"
            and raw_dtype
            and "," not in raw_dtype
        ):
            for scan_idx in range(dtype_idx + 1, min(dtype_idx + 3, row.shape[0])):
                candidate_type = _clean(row.iloc[scan_idx]).lower()
                if candidate_type in _DATA_TYPE_MAP:
                    avni_dtype = _DATA_TYPE_MAP[candidate_type]
                    break

        mandatory = _parse_yes_no(row.iloc[mand_idx]) if mand_idx is not None else False

        options = None
        _displaced_type_keyword: str | None = None  # type keyword found in options col
        if options_idx is not None:
            raw_options_val = _clean(row.iloc[options_idx]).lower()
            if raw_options_val in _DATA_TYPE_MAP:
                # Column displacement detected: the options cell contains a type keyword.
                # Record it for selection_type inference and scan adjacent columns for
                # the actual options.
                _displaced_type_keyword = raw_options_val
                for scan_idx in range(
                    options_idx + 1, min(options_idx + 4, row.shape[0])
                ):
                    candidate = _parse_options(row.iloc[scan_idx])
                    if candidate:
                        options = candidate
                        break
            else:
                options = _parse_options(row.iloc[options_idx]) or None

        # Use dtype-displaced options as fallback when options column had nothing
        if not options and _dtype_displaced_options:
            options = _dtype_displaced_options

        # If boolean/yes-no type detected, auto-add options
        if (
            avni_dtype == "Coded"
            and not options
            and raw_dtype in ("boolean", "bool", "yes/no")
        ):
            options = ["Yes", "No"]

        selection_type = None
        if selection_idx is not None:
            sel_raw = _clean(row.iloc[selection_idx]).lower()
            if "multi" in sel_raw:
                selection_type = "MultiSelect"
            elif "single" in sel_raw:
                selection_type = "SingleSelect"
        # Infer selection type from displaced keyword when no explicit selection column
        if selection_type is None and _displaced_type_keyword:
            if "multi" in _displaced_type_keyword:
                selection_type = "MultiSelect"
            elif "single" in _displaced_type_keyword:
                selection_type = "SingleSelect"

        min_val, max_val = None, None
        if min_max_idx is not None:
            min_val, max_val = _parse_min_max(row.iloc[min_max_idx])

        unit = _clean(row.iloc[unit_idx]) if unit_idx is not None else None
        if not unit:
            unit = None

        skip_logic = None
        if skip_idx is not None:
            when_to_show = _clean(row.iloc[skip_idx])
            if when_to_show:
                skip_logic = SkipLogicSpec(
                    dependsOn=when_to_show, condition="raw", value=when_to_show
                )

        fields.append(
            FieldSpec(
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
            )
        )

    if not fields:
        return None

    form_type = "Encounter"
    subject_type = None
    program = None
    encounter_type = None

    if entity_mapping:
        form_type = entity_mapping.get("formType") or "Encounter"
        subject_type = entity_mapping.get("subjectType")
        program = entity_mapping.get("program")
        encounter_type = entity_mapping.get("encounterType")

    # Build sections
    sections: list[SectionSpec] = []
    cur_name: str | None = None
    cur_fields: list[FieldSpec] = []
    for f in fields:
        sec_name = f.group or "General Information"
        if sec_name != cur_name:
            if cur_fields:
                sections.append(
                    SectionSpec(
                        name=cur_name or "General Information", fields=cur_fields
                    )
                )
            cur_name = sec_name
            cur_fields = [f]
        else:
            cur_fields.append(f)
    if cur_fields:
        sections.append(
            SectionSpec(name=cur_name or "General Information", fields=cur_fields)
        )

    return FormSpec(
        name=sheet_name.strip(),
        formType=form_type,
        subjectType=subject_type,
        program=program,
        encounterType=encounter_type,
        fields=fields,
        sections=sections,
    )


# ── File Loaders ─────────────────────────────────────────────────────────────


def _load_xlsx(path: Path) -> list[tuple[str, pd.DataFrame]]:
    """Load all sheets from an Excel file. Returns [(sheet_name, df), ...]."""
    xf = pd.ExcelFile(path)
    sheets = []
    for name in xf.sheet_names:
        try:
            df = pd.read_excel(xf, sheet_name=name, header=None)
            if not df.empty:
                sheets.append((name, df))
        except Exception as e:
            logger.warning("Failed to read sheet '%s' in %s: %s", name, path, e)
    return sheets


def _load_csv(path: Path) -> list[tuple[str, pd.DataFrame]]:
    """Load a CSV file as a single 'sheet'."""
    try:
        df = pd.read_csv(path)
        return [(path.stem, df)]
    except Exception as e:
        logger.warning("Failed to read CSV %s: %s", path, e)
        return []


def _load_txt(path: Path) -> list[tuple[str, pd.DataFrame]]:
    """Load a text file. Try JSON first, then CSV, then as single-column text."""
    text = path.read_text(encoding="utf-8", errors="replace")

    # Try JSON
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "text" in data:
            # Dify-extracted format: {"text": ["sheet1 content", "sheet2 content"]}
            sheets = []
            for i, t in enumerate(data["text"]):
                # Try to parse as markdown tables
                df = _parse_markdown_tables(t)
                if df is not None and not df.empty:
                    sheets.append((f"text_{i}", df))
            if sheets:
                return sheets
        elif isinstance(data, dict):
            # Direct entities dict
            return [("json_data", pd.DataFrame([data]))]
        elif isinstance(data, list):
            return [("json_data", pd.DataFrame(data))]
    except (json.JSONDecodeError, ValueError):
        pass

    # Try CSV
    try:
        df = pd.read_csv(io.StringIO(text))
        if df.shape[1] > 1:
            return [(path.stem, df)]
    except Exception:
        pass

    # Plain text — return as single column
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        return [(path.stem, pd.DataFrame({"content": lines}))]
    return []


def _parse_markdown_tables(text: str) -> pd.DataFrame | None:
    """Extract the first markdown table from text and return as DataFrame."""
    lines = text.split("\n")
    table_lines = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and "|" in stripped[1:]:
            if "---" in stripped:
                continue  # separator row
            in_table = True
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            table_lines.append(cells)
        elif in_table:
            break  # end of table

    if len(table_lines) < 2:
        return None

    headers = table_lines[0]
    data = table_lines[1:]
    # Pad rows to match header length
    data = [row + [""] * (len(headers) - len(row)) for row in data]
    return pd.DataFrame(data, columns=headers)


def _load_file(path: Path) -> list[tuple[str, pd.DataFrame]]:
    """Load any supported file format."""
    suffix = path.suffix.lower()
    if suffix in (".xlsx", ".xls"):
        return _load_xlsx(path)
    elif suffix == ".csv":
        return _load_csv(path)
    elif suffix in (".txt", ".json"):
        return _load_txt(path)
    else:
        logger.warning("Unsupported file type: %s", path)
        return []


# ── Post-processing ──────────────────────────────────────────────────────────


def _resolve_form_subject_types(
    forms: list[FormSpec],
    encounter_types: list[EncounterTypeSpec],
    subject_types: list[SubjectTypeSpec],
) -> None:
    """Fill missing encounterType and subjectType on forms. Mutates in place."""
    enc_to_subject: dict[str, str] = {}
    enc_to_program: dict[str, str] = {}
    for et in encounter_types:
        if et.subject_type:
            enc_to_subject[et.name.lower()] = et.subject_type
        if et.program_name:
            enc_to_program[et.name.lower()] = et.program_name

    for form in forms:
        # Step 1: Match form to encounter type by name if not set
        if not form.encounterType and form.formType in (
            "Encounter",
            "ProgramEncounter",
            "IndividualEncounterCancellation",
            "ProgramEncounterCancellation",
        ):
            form_lower = form.name.lower()
            # Strip " Cancellation" suffix for matching
            match_name = form_lower.replace(" cancellation", "").strip()
            for et in encounter_types:
                if et.name.lower() == match_name:
                    form.encounterType = et.name
                    break

        # Step 2: Resolve subjectType from encounterType
        if not form.subjectType and form.encounterType:
            subject = enc_to_subject.get(form.encounterType.lower())
            if subject:
                form.subjectType = subject

        # Step 3: Resolve subjectType for registration forms by name match
        if not form.subjectType and form.formType == "IndividualProfile":
            for st in subject_types:
                if (
                    st.name.lower() in form.name.lower()
                    or form.name.lower() in st.name.lower()
                ):
                    form.subjectType = st.name
                    break

        # Step 4: Resolve program from encounterType
        if not form.program and form.encounterType:
            prog = enc_to_program.get(form.encounterType.lower())
            if prog:
                form.program = prog

        # Step 5: Fallback — single subject type
        if not form.subjectType and len(subject_types) == 1:
            form.subjectType = subject_types[0].name


# ── Main Entry Point ─────────────────────────────────────────────────────────


def parse_scoping_docs(
    file_paths: list[str | Path],
) -> tuple["EntitySpec", list[dict]]:
    """
    Parse one or more SRS/scoping/modelling files of any supported format
    and consolidate into a validated EntitySpec.

    Accepts .xlsx, .csv, .txt, .json files in any combination.
    Each sheet/file is auto-classified by its content and parsed accordingly.
    All results are merged with deduplication.

    Returns:
        (EntitySpec, misc_sheets) where misc_sheets is a list of dicts for
        sheets that could not be classified, each containing:
        {name, file, columns, rows (first 20 non-empty rows as list-of-dicts)}
    """
    all_address: list[AddressLevelSpec] = []
    all_subjects: list[SubjectTypeSpec] = []
    all_programs: list[ProgramSpec] = []
    all_encounters: list[EncounterTypeSpec] = []
    all_forms: list[FormSpec] = []
    w3h_dfs: list[pd.DataFrame] = []
    form_sheets: list[tuple[str, pd.DataFrame, int]] = []  # (name, df, header_offset)
    misc_sheets: list[dict] = []

    seen: dict[str, set[str]] = {
        "address": set(),
        "subject": set(),
        "program": set(),
        "encounter": set(),
        "form": set(),
    }

    # Phase 1: Load all files and classify each sheet
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        logger.info("Loading file: %s", path)
        sheets = _load_file(path)

        for sheet_name, df in sheets:
            if df.empty or df.shape[1] < 2:
                continue

            # Try classifying with row 0 as headers
            df_with_header = df.copy()
            df_with_header.columns = [
                str(df.iloc[0, c]).strip() if df.shape[0] > 0 else f"col{c}"
                for c in range(df.shape[1])
            ]
            df_with_header = df_with_header.iloc[1:].reset_index(drop=True)
            df_with_header = df_with_header.dropna(how="all")

            classification = _classify_sheet(df_with_header, sheet_name)

            # If unknown, try with row 1 as headers (scoping doc pattern)
            if classification == "unknown" and df.shape[0] >= 3:
                df_alt = df.copy()
                df_alt.columns = [
                    str(df.iloc[1, c]).strip() if df.shape[0] > 1 else f"col{c}"
                    for c in range(df.shape[1])
                ]
                alt_class = _classify_sheet(df_alt, sheet_name)
                if alt_class in ("form", "form_offset1"):
                    classification = "form_offset1"
                elif alt_class != "unknown":
                    classification = alt_class
                    df_with_header = (
                        df_alt.iloc[2:].reset_index(drop=True).dropna(how="all")
                    )

            if classification == "form_offset1":
                classification = "form"

            logger.info("  Sheet '%s': classified as %s", sheet_name, classification)

            subject_type_names = {st.name for st in all_subjects}
            program_names = {p.name for p in all_programs}

            if classification == "location":
                for al in parse_location_hierarchy(df_with_header):
                    if al.name.lower() not in seen["address"]:
                        all_address.append(al)
                        seen["address"].add(al.name.lower())

            elif classification == "subject_type":
                for st in parse_subject_types(df_with_header):
                    if st.name.lower() not in seen["subject"]:
                        all_subjects.append(st)
                        seen["subject"].add(st.name.lower())

            elif classification == "program":
                for prog in parse_programs(df_with_header, subject_type_names):
                    if prog.name.lower() not in seen["program"]:
                        all_programs.append(prog)
                        seen["program"].add(prog.name.lower())

            elif classification in ("encounter", "program_encounter"):
                is_prog = classification == "program_encounter"
                for et in parse_encounters(
                    df_with_header, subject_type_names, program_names, is_prog
                ):
                    if et.name.lower() not in seen["encounter"]:
                        all_encounters.append(et)
                        seen["encounter"].add(et.name.lower())

            elif classification == "w3h":
                w3h_dfs.append(df_with_header)

            elif classification == "form":
                form_sheets.append((sheet_name, df, 1))  # offset=1 for scoping format

            else:
                # Unknown — capture for agent inspection
                cols = [str(c) for c in df_with_header.columns.tolist()]
                rows = (
                    df_with_header.head(3)
                    .dropna(how="all")
                    .fillna("")
                    .infer_objects(copy=False)
                    .to_dict(orient="records")
                )
                misc_sheets.append(
                    {
                        "name": sheet_name,
                        "file": path.name,
                        "columns": cols,
                        "rows": rows,
                    }
                )

    # Default address levels if none found
    if not all_address:
        logger.warning(
            "No location hierarchy found — using default State/District/Village"
        )
        all_address = [
            AddressLevelSpec(name="State", level=3, parent=None),
            AddressLevelSpec(name="District", level=2, parent="State"),
            AddressLevelSpec(name="Village", level=1, parent="District"),
        ]

    # Phase 2: Build consolidated context
    subject_type_names = {st.name for st in all_subjects}
    encounter_type_names = {et.name for et in all_encounters}
    program_encounter_map: dict[str, str] = {
        et.name: et.program_name for et in all_encounters if et.program_name
    }

    # Phase 3: Parse W3H for form-entity mapping
    w3h_mapping: dict[str, dict[str, str | None]] = {}
    for w3h_df in w3h_dfs:
        w3h_mapping.update(
            parse_w3h(
                w3h_df, subject_type_names, encounter_type_names, program_encounter_map
            )
        )
    logger.info("W3H mapping: %d activities", len(w3h_mapping))

    # Phase 4: Parse form sheets using consolidated context
    for sheet_name, df, offset in form_sheets:
        if sheet_name.lower() in seen["form"]:
            continue

        entity_mapping = _match_sheet_to_w3h(sheet_name, w3h_mapping)
        form = parse_form_df(df, sheet_name, entity_mapping, header_offset=offset)
        if form:
            all_forms.append(form)
            seen["form"].add(sheet_name.lower())

    # Phase 5a: Resolve missing subject_type on encounters via programs
    prog_to_subject: dict[str, str] = {}
    for prog in all_programs:
        if prog.target_subject_type:
            prog_to_subject[prog.name.lower()] = prog.target_subject_type
    for et in all_encounters:
        if not et.subject_type and et.program_name:
            resolved = prog_to_subject.get(et.program_name.lower())
            if resolved:
                et.subject_type = resolved
        # If still no subject_type and only one subject type exists, use it
        if not et.subject_type and len(all_subjects) == 1:
            et.subject_type = all_subjects[0].name

    # Phase 5b: Resolve missing subjectType on forms
    _resolve_form_subject_types(all_forms, all_encounters, all_subjects)

    # Phase 6: Always include default group
    groups = [GroupSpec(name="Everyone", has_all_privileges=True)]

    logger.info(
        "Consolidated: %d addresses, %d subjects, %d programs, "
        "%d encounters, %d forms, %d groups from %d file(s)",
        len(all_address),
        len(all_subjects),
        len(all_programs),
        len(all_encounters),
        len(all_forms),
        len(groups),
        len(file_paths),
    )

    return EntitySpec(
        subject_types=all_subjects,
        programs=all_programs,
        encounter_types=all_encounters,
        address_levels=all_address,
        groups=groups,
        forms=all_forms,
    ), misc_sheets


# ── Consolidation + Audit ────────────────────────────────────────────────────


def consolidate_and_audit(
    file_paths: list[str | Path],
    org_name: str = "",
) -> dict[str, Any]:
    """
    Parse input files, consolidate into a YAML spec (source of truth),
    and produce an audit report.

    Returns:
        {
            "spec_yaml": str,          # The consolidated YAML — edit this, then generate bundle
            "audit": {
                "files_parsed": [...],
                "entity_counts": {...},
                "warnings": [...],
                "errors": [...],
                "coverage": {...},     # What's present vs missing
            },
            "entities": dict,          # Raw entities dict for direct use
        }
    """
    from .spec_generator import entities_to_spec

    entity_spec, misc_sheets = parse_scoping_docs(file_paths)
    entities = entity_spec.to_entities_dict()
    if misc_sheets:
        entities["misc_sheets"] = misc_sheets

    # Generate the YAML spec — this is the source of truth
    spec_yaml = entities_to_spec(entities, org_name=org_name)

    # Build audit report — include cross-ref warnings from EntitySpec validation
    warnings: list[str] = list(entity_spec.validation_warnings)
    errors: list[str] = []

    # Check completeness
    form_encounter_links = {
        f.get("encounterType") for f in entities["forms"] if f.get("encounterType")
    }

    # Every subject type should have a registration form
    for st in entities["subject_types"]:
        has_reg = any(
            f.get("formType") == "IndividualProfile"
            and f.get("subjectType") == st["name"]
            for f in entities["forms"]
        )
        if not has_reg:
            warnings.append(f"Subject type '{st['name']}' has no registration form")

    # Every encounter type should have a form linked
    for et in entities["encounter_types"]:
        if et["name"] not in form_encounter_links:
            warnings.append(f"Encounter type '{et['name']}' has no form linked to it")

    # Forms with no subjectType — this is a critical issue
    for f in entities["forms"]:
        if not f.get("subjectType"):
            errors.append(
                f"Form '{f['name']}' has no subjectType — bundle generation will produce broken formMappings"
            )

    # Forms with 0 or very few fields
    for f in entities["forms"]:
        field_count = len(f.get("fields", []))
        if field_count == 0:
            errors.append(f"Form '{f['name']}' has 0 fields — will be empty")
        elif field_count <= 2:
            warnings.append(
                f"Form '{f['name']}' has only {field_count} field(s) — may be incomplete"
            )

    # Coded fields without options
    for f in entities["forms"]:
        for field in f.get("fields", []):
            if field.get("dataType") == "Coded" and not field.get("options"):
                warnings.append(
                    f"Coded field '{field['name']}' in form '{f['name']}' has no options"
                )

    # Groups check
    if not entities["groups"]:
        errors.append("No groups defined — bundle will fail without at least one group")

    # Coverage summary
    coverage = {
        "has_address_levels": len(entities["address_levels"]) > 0,
        "has_subject_types": len(entities["subject_types"]) > 0,
        "has_encounter_types": len(entities["encounter_types"]) > 0,
        "has_forms": len(entities["forms"]) > 0,
        "has_groups": len(entities["groups"]) > 0,
        "has_programs": len(entities["programs"]) > 0,
        "all_encounters_have_forms": all(
            et["name"] in form_encounter_links for et in entities["encounter_types"]
        ),
        "all_subjects_have_registration": all(
            any(
                f.get("formType") == "IndividualProfile"
                and f.get("subjectType") == st["name"]
                for f in entities["forms"]
            )
            for st in entities["subject_types"]
        ),
    }

    audit = {
        "files_parsed": [str(p) for p in file_paths],
        "entity_counts": {
            "address_levels": len(entities["address_levels"]),
            "subject_types": len(entities["subject_types"]),
            "programs": len(entities["programs"]),
            "encounter_types": len(entities["encounter_types"]),
            "forms": len(entities["forms"]),
            "groups": len(entities["groups"]),
            "total_fields": sum(len(f.get("fields", [])) for f in entities["forms"]),
            "misc_sheets": len(misc_sheets),
        },
        "warnings": warnings,
        "errors": errors,
        "coverage": coverage,
    }

    return {
        "spec_yaml": spec_yaml,
        "audit": audit,
        "entities": entities,
    }


# ── Backward-compatible wrappers ─────────────────────────────────────────────


def _is_form_sheet(excel_file: Any, sheet_name: str) -> bool:
    """Backward-compatible helper: returns True if the sheet classifies as a form."""
    try:
        df_raw = excel_file.parse(sheet_name, header=None)
        if df_raw.empty or df_raw.shape[1] < 2:
            return False
        # Try row 0 as header
        df = df_raw.copy()
        df.columns = [
            str(df_raw.iloc[0, c]).strip() if df_raw.shape[0] > 0 else f"col{c}"
            for c in range(df_raw.shape[1])
        ]
        df = df.iloc[1:].reset_index(drop=True).dropna(how="all")
        if _classify_sheet(df, sheet_name) == "form":
            return True
        # Try row 1 as header (scoping doc pattern)
        if df_raw.shape[0] >= 3:
            df_alt = df_raw.copy()
            df_alt.columns = [
                str(df_raw.iloc[1, c]).strip() if df_raw.shape[0] > 1 else f"col{c}"
                for c in range(df_raw.shape[1])
            ]
            if _classify_sheet(df_alt, sheet_name) in ("form", "form_offset1"):
                return True
        return False
    except Exception:
        return False


def parse_scoping_doc(xlsx_path: str | Path | None = None) -> EntitySpec:
    """Parse a single file. Backward-compatible wrapper."""
    import os

    if xlsx_path is None:
        xlsx_path = os.environ.get("SCOPING_DOC_PATH", str(_DEFAULT_SCOPING_DOC))
    entity_spec, _ = parse_scoping_docs([xlsx_path])
    return entity_spec


def load_durga_entities(xlsx_path: str | Path | None = None) -> dict:
    """Parse and return plain dict for AppConfiguratorFlow."""
    entity_spec = parse_scoping_doc(xlsx_path)
    return entity_spec.to_entities_dict()
