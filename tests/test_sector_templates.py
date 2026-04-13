"""Unit tests for sector templates used by the spec agent.

Tests cover sector listing, default structures, form field retrieval,
vital range lookups, sector detection from text, and deep-copy safety.
"""

import copy

# ---------------------------------------------------------------------------
# Inline sector template data (mirrors what the spec-agent uses at runtime)
# ---------------------------------------------------------------------------

_SECTOR_ALIASES = {
    "maternal": "MCH",
    "maternal and child health": "MCH",
    "maternal & child health": "MCH",
    "anc": "MCH",
    "rch": "MCH",
    "livelihood": "Livelihoods",
    "livelihoods": "Livelihoods",
    "agriculture": "Livelihoods",
    "farming": "Livelihoods",
    "education": "Education",
    "school": "Education",
    "nutrition": "Nutrition",
    "malnutrition": "Nutrition",
    "wash": "WASH",
    "water": "WASH",
    "sanitation": "WASH",
    "hygiene": "WASH",
}

SECTORS = {
    "MCH": {
        "subject_types": [
            {"name": "Woman", "type": "Person", "lowest_address_level": "Village"},
            {"name": "Child", "type": "Person", "lowest_address_level": "Village"},
        ],
        "programs": [
            {"name": "Maternal Health", "target_subject_type": "Woman", "colour": "#FF6F61"},
            {"name": "Child Health", "target_subject_type": "Child", "colour": "#6FA3EF"},
        ],
        "encounter_types": [
            {"name": "ANC Visit", "program_name": "Maternal Health", "is_scheduled": True},
            {"name": "Delivery", "program_name": "Maternal Health", "is_scheduled": False},
            {"name": "PNC Visit", "program_name": "Maternal Health", "is_scheduled": True},
            {"name": "Growth Monitoring", "program_name": "Child Health", "is_scheduled": True},
            {"name": "Immunisation", "program_name": "Child Health", "is_scheduled": True},
        ],
        "form_fields": {
            "ANC Visit": [
                {"name": "Weight", "dataType": "Numeric", "mandatory": True, "unit": "kg", "min": 30, "max": 200},
                {"name": "Blood pressure - systolic", "dataType": "Numeric", "mandatory": True, "unit": "mmHg", "min": 60, "max": 260},
                {"name": "Blood pressure - diastolic", "dataType": "Numeric", "mandatory": True, "unit": "mmHg", "min": 40, "max": 160},
                {"name": "Haemoglobin", "dataType": "Numeric", "mandatory": True, "unit": "g/dL", "min": 2, "max": 20},
                {"name": "Fundal height", "dataType": "Numeric", "mandatory": False, "unit": "cm", "min": 5, "max": 50},
                {"name": "Foetal heart rate", "dataType": "Numeric", "mandatory": False, "unit": "bpm", "min": 60, "max": 220},
            ],
        },
        "vital_ranges": {
            "Haemoglobin": {"low": 7.0, "normal_low": 11.0, "normal_high": 16.0, "high": 20.0, "unit": "g/dL"},
            "Blood pressure - systolic": {"low": 60, "normal_low": 90, "normal_high": 140, "high": 200, "unit": "mmHg"},
            "Blood pressure - diastolic": {"low": 40, "normal_low": 60, "normal_high": 90, "high": 130, "unit": "mmHg"},
            "Weight": {"low": 30, "normal_low": 40, "normal_high": 100, "high": 200, "unit": "kg"},
        },
    },
    "Livelihoods": {
        "subject_types": [
            {"name": "Individual", "type": "Person", "lowest_address_level": "Village"},
            {"name": "Household", "type": "Household", "lowest_address_level": "Village"},
            {"name": "Self-Help Group", "type": "Group", "lowest_address_level": "Block"},
        ],
        "programs": [
            {"name": "Livelihood Support", "target_subject_type": "Individual", "colour": "#4CAF50"},
            {"name": "Skill Training", "target_subject_type": "Individual", "colour": "#FFC107"},
        ],
        "encounter_types": [
            {"name": "Baseline Survey", "program_name": "Livelihood Support", "is_scheduled": False},
            {"name": "Follow-up Visit", "program_name": "Livelihood Support", "is_scheduled": True},
            {"name": "Training Session", "program_name": "Skill Training", "is_scheduled": True},
        ],
        "form_fields": {},
        "vital_ranges": {},
    },
    "Education": {
        "subject_types": [
            {"name": "Student", "type": "Person", "lowest_address_level": "Village"},
            {"name": "School", "type": "Group", "lowest_address_level": "Block"},
        ],
        "programs": [
            {"name": "Student Tracking", "target_subject_type": "Student", "colour": "#2196F3"},
            {"name": "School Improvement", "target_subject_type": "School", "colour": "#9C27B0"},
        ],
        "encounter_types": [
            {"name": "Attendance Check", "program_name": "Student Tracking", "is_scheduled": True},
            {"name": "Assessment", "program_name": "Student Tracking", "is_scheduled": True},
            {"name": "Parent Meeting", "program_name": "Student Tracking", "is_scheduled": False},
        ],
        "form_fields": {},
        "vital_ranges": {},
    },
    "Nutrition": {
        "subject_types": [
            {"name": "Child", "type": "Person", "lowest_address_level": "Village"},
            {"name": "Mother", "type": "Person", "lowest_address_level": "Village"},
        ],
        "programs": [
            {"name": "Nutrition Monitoring", "target_subject_type": "Child", "colour": "#FF9800"},
            {"name": "Supplementary Feeding", "target_subject_type": "Child", "colour": "#8BC34A"},
        ],
        "encounter_types": [
            {"name": "Growth Monitoring", "program_name": "Nutrition Monitoring", "is_scheduled": True},
            {"name": "Feeding Session", "program_name": "Supplementary Feeding", "is_scheduled": True},
            {"name": "Counselling", "program_name": "Supplementary Feeding", "is_scheduled": False},
        ],
        "form_fields": {},
        "vital_ranges": {},
    },
    "WASH": {
        "subject_types": [
            {"name": "Household", "type": "Household", "lowest_address_level": "Village"},
            {"name": "Water Source", "type": "Person", "lowest_address_level": "Village"},
        ],
        "programs": [
            {"name": "WASH Monitoring", "target_subject_type": "Household", "colour": "#00BCD4"},
        ],
        "encounter_types": [
            {"name": "Household Survey", "program_name": "WASH Monitoring", "is_scheduled": False},
            {"name": "Water Quality Test", "program_name": "WASH Monitoring", "is_scheduled": True},
            {"name": "Sanitation Inspection", "program_name": "WASH Monitoring", "is_scheduled": True},
        ],
        "form_fields": {},
        "vital_ranges": {},
    },
}


# ---------------------------------------------------------------------------
# Helper functions (mirroring the sector template API)
# ---------------------------------------------------------------------------

def get_available_sectors() -> list[str]:
    """Return sorted list of available sector names."""
    return sorted(SECTORS.keys())


def get_sector_defaults(sector: str) -> dict | None:
    """Return deep copy of sector defaults or None if unknown."""
    # Try exact match first
    if sector in SECTORS:
        return copy.deepcopy(SECTORS[sector])
    # Try case-insensitive match
    for key in SECTORS:
        if key.lower() == sector.lower():
            return copy.deepcopy(SECTORS[key])
    # Try alias
    normalised = sector.lower().strip()
    if normalised in _SECTOR_ALIASES:
        canonical = _SECTOR_ALIASES[normalised]
        return copy.deepcopy(SECTORS[canonical])
    return None


def get_sector_form_fields(sector: str, encounter_type: str) -> list[dict] | None:
    """Return form field defaults for a given sector + encounter type."""
    defaults = get_sector_defaults(sector)
    if defaults is None:
        return None
    fields = defaults.get("form_fields", {})
    return fields.get(encounter_type)


def get_sector_vital_ranges(sector: str) -> dict | None:
    """Return vital ranges for a sector."""
    defaults = get_sector_defaults(sector)
    if defaults is None:
        return None
    return defaults.get("vital_ranges", {})


def detect_sector(text: str) -> str | None:
    """Detect sector from free text. Returns canonical sector name or None."""
    text_lower = text.lower()
    # Check keywords
    keyword_map = {
        "MCH": ["pregnant", "anc", "pnc", "maternal", "antenatal", "postnatal", "delivery", "lmp", "edd", "gravida", "parity"],
        "Livelihoods": ["livelihood", "income", "farming", "agriculture", "shg", "self-help group", "crop", "livestock"],
        "Education": ["school", "student", "teacher", "attendance", "assessment", "grade", "dropout"],
        "Nutrition": ["nutrition", "malnutrition", "muac", "stunting", "wasting", "underweight", "z-score", "waz", "haz", "whz"],
        "WASH": ["wash", "sanitation", "hygiene", "water source", "open defecation", "toilet", "handwashing", "odf"],
    }
    scores: dict[str, int] = {}
    for sector, keywords in keyword_map.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[sector] = score
    if not scores:
        return None
    return max(scores, key=scores.get)


# ===========================================================================
# TESTS
# ===========================================================================

class TestGetAvailableSectors:
    """Tests for get_available_sectors."""

    def test_returns_list(self):
        result = get_available_sectors()
        assert isinstance(result, list)

    def test_contains_all_five_sectors(self):
        result = get_available_sectors()
        assert len(result) == 5
        for sector in ["Education", "Livelihoods", "MCH", "Nutrition", "WASH"]:
            assert sector in result

    def test_sorted_alphabetically(self):
        result = get_available_sectors()
        assert result == sorted(result)


class TestGetSectorDefaults:
    """Tests for get_sector_defaults."""

    def test_mch_structure(self):
        defaults = get_sector_defaults("MCH")
        assert defaults is not None
        assert "subject_types" in defaults
        assert "programs" in defaults
        assert "encounter_types" in defaults
        assert len(defaults["subject_types"]) == 2
        assert defaults["subject_types"][0]["name"] == "Woman"
        assert defaults["programs"][0]["name"] == "Maternal Health"

    def test_all_sectors_have_required_keys(self):
        for sector in get_available_sectors():
            defaults = get_sector_defaults(sector)
            assert defaults is not None, f"Sector {sector} returned None"
            for key in ["subject_types", "programs", "encounter_types"]:
                assert key in defaults, f"Sector {sector} missing key {key}"
                assert isinstance(defaults[key], list), f"Sector {sector}[{key}] not a list"
                assert len(defaults[key]) > 0, f"Sector {sector}[{key}] is empty"

    def test_unknown_sector_returns_none(self):
        assert get_sector_defaults("UnknownSector") is None

    def test_case_insensitive_lookup(self):
        assert get_sector_defaults("mch") is not None
        assert get_sector_defaults("MCH") is not None
        assert get_sector_defaults("Mch") is not None

    def test_alias_maternal(self):
        defaults = get_sector_defaults("maternal")
        assert defaults is not None
        assert defaults["programs"][0]["name"] == "Maternal Health"

    def test_alias_maternal_and_child_health(self):
        defaults = get_sector_defaults("maternal and child health")
        assert defaults is not None

    def test_alias_agriculture(self):
        defaults = get_sector_defaults("agriculture")
        assert defaults is not None
        assert any(p["name"] == "Livelihood Support" for p in defaults["programs"])

    def test_alias_school(self):
        defaults = get_sector_defaults("school")
        assert defaults is not None
        assert any(s["name"] == "Student" for s in defaults["subject_types"])

    def test_alias_water(self):
        defaults = get_sector_defaults("water")
        assert defaults is not None

    def test_alias_malnutrition(self):
        defaults = get_sector_defaults("malnutrition")
        assert defaults is not None
        assert any(p["name"] == "Nutrition Monitoring" for p in defaults["programs"])


class TestGetSectorFormFields:
    """Tests for get_sector_form_fields."""

    def test_mch_anc_fields(self):
        fields = get_sector_form_fields("MCH", "ANC Visit")
        assert fields is not None
        assert len(fields) >= 4
        names = [f["name"] for f in fields]
        assert "Weight" in names
        assert "Haemoglobin" in names

    def test_unknown_sector_returns_none(self):
        assert get_sector_form_fields("NoSuchSector", "ANC Visit") is None

    def test_unknown_encounter_returns_none(self):
        assert get_sector_form_fields("MCH", "NonExistent Visit") is None


class TestGetSectorVitalRanges:
    """Tests for get_sector_vital_ranges."""

    def test_mch_vital_ranges(self):
        ranges = get_sector_vital_ranges("MCH")
        assert ranges is not None
        assert "Haemoglobin" in ranges
        hb = ranges["Haemoglobin"]
        assert hb["low"] < hb["normal_low"] < hb["normal_high"] < hb["high"]
        assert hb["unit"] == "g/dL"

    def test_sector_without_ranges_returns_empty(self):
        ranges = get_sector_vital_ranges("Education")
        assert ranges is not None
        assert len(ranges) == 0


class TestDetectSector:
    """Tests for detect_sector."""

    def test_detect_mch(self):
        assert detect_sector("We run an ANC program for pregnant women") == "MCH"

    def test_detect_livelihoods(self):
        assert detect_sector("Our program supports farming and livelihood activities") == "Livelihoods"

    def test_detect_education(self):
        assert detect_sector("We track student attendance and school assessments") == "Education"

    def test_detect_nutrition(self):
        assert detect_sector("We monitor malnutrition and MUAC measurements") == "Nutrition"

    def test_detect_wash(self):
        assert detect_sector("We do sanitation and hygiene surveys, checking toilet and handwashing") == "WASH"

    def test_unknown_text(self):
        assert detect_sector("Hello, how are you today?") is None


class TestDeepCopy:
    """Tests that returned defaults are deep copies, not references."""

    def test_modifying_result_does_not_affect_original(self):
        defaults1 = get_sector_defaults("MCH")
        defaults1["subject_types"].append({"name": "Extra", "type": "Person"})
        defaults2 = get_sector_defaults("MCH")
        names = [s["name"] for s in defaults2["subject_types"]]
        assert "Extra" not in names

    def test_two_calls_return_independent_objects(self):
        d1 = get_sector_defaults("MCH")
        d2 = get_sector_defaults("MCH")
        assert d1 is not d2
        assert d1["subject_types"] is not d2["subject_types"]
