"""
Hardcoded sector defaults for common implementation domains.

Provides pre-built entity structures, form fields, and vital-sign ranges
for MCH, Nutrition, Livelihoods, Education, and WASH sectors so that
the chat-SRS flow can bootstrap a working configuration without an LLM call.
"""

from __future__ import annotations

import re
from typing import Any

# ---------------------------------------------------------------------------
# Sector knowledge database
# ---------------------------------------------------------------------------

_SECTOR_DEFAULTS: dict[str, dict[str, Any]] = {
    "MCH": {
        "subject_types": [
            {"name": "Individual", "type": "Person"},
            {"name": "Household", "type": "Household"},
        ],
        "programs": [
            {
                "name": "Pregnancy",
                "colour": "#E91E63",
                "target_subject_type": "Individual",
            },
            {
                "name": "Child",
                "colour": "#4CAF50",
                "target_subject_type": "Individual",
            },
        ],
        "encounter_types": [
            {
                "name": "ANC",
                "is_program_encounter": True,
                "program_name": "Pregnancy",
                "schedule_days": 30,
                "max_days": 45,
            },
            {
                "name": "Delivery",
                "is_program_encounter": True,
                "program_name": "Pregnancy",
            },
            {
                "name": "PNC",
                "is_program_encounter": True,
                "program_name": "Pregnancy",
            },
            {
                "name": "HBNC",
                "is_program_encounter": True,
                "program_name": "Child",
            },
            {
                "name": "Immunization",
                "is_program_encounter": True,
                "program_name": "Child",
                "schedule_days": 30,
                "max_days": 45,
            },
            {
                "name": "Growth Monitoring",
                "is_program_encounter": True,
                "program_name": "Child",
                "schedule_days": 30,
                "max_days": 45,
            },
        ],
        "address_levels": [
            {"name": "State", "level": 4},
            {"name": "District", "level": 3, "parent": "State"},
            {"name": "Block", "level": 2, "parent": "District"},
            {"name": "Village", "level": 1, "parent": "Block"},
        ],
        "groups": [
            {"name": "Everyone", "admin": False},
            {"name": "Administrators", "admin": True},
        ],
    },
    "Nutrition": {
        "subject_types": [
            {"name": "Individual", "type": "Person"},
            {"name": "Household", "type": "Household"},
        ],
        "programs": [
            {
                "name": "Nutrition",
                "colour": "#FF9800",
                "target_subject_type": "Individual",
            },
        ],
        "encounter_types": [
            {
                "name": "Nutrition Assessment",
                "is_program_encounter": True,
                "program_name": "Nutrition",
                "schedule_days": 30,
                "max_days": 45,
            },
            {
                "name": "Counselling",
                "is_program_encounter": True,
                "program_name": "Nutrition",
            },
            {
                "name": "Supplementation",
                "is_program_encounter": True,
                "program_name": "Nutrition",
            },
            {
                "name": "Follow-up",
                "is_program_encounter": True,
                "program_name": "Nutrition",
                "schedule_days": 14,
                "max_days": 21,
            },
        ],
        "address_levels": [
            {"name": "State", "level": 4},
            {"name": "District", "level": 3, "parent": "State"},
            {"name": "Block", "level": 2, "parent": "District"},
            {"name": "Village", "level": 1, "parent": "Block"},
        ],
        "groups": [
            {"name": "Everyone", "admin": False},
            {"name": "Administrators", "admin": True},
        ],
    },
    "Livelihoods": {
        "subject_types": [
            {"name": "Individual", "type": "Person"},
            {"name": "Self Help Group", "type": "Group"},
        ],
        "programs": [
            {
                "name": "Livelihoods",
                "colour": "#795548",
                "target_subject_type": "Individual",
            },
        ],
        "encounter_types": [
            {
                "name": "Skill Assessment",
                "is_program_encounter": True,
                "program_name": "Livelihoods",
            },
            {
                "name": "Training",
                "is_program_encounter": True,
                "program_name": "Livelihoods",
            },
            {
                "name": "Placement Follow-up",
                "is_program_encounter": True,
                "program_name": "Livelihoods",
                "schedule_days": 30,
                "max_days": 45,
            },
            {
                "name": "SHG Meeting",
                "is_program_encounter": False,
                "subject_type": "Self Help Group",
            },
        ],
        "address_levels": [
            {"name": "State", "level": 4},
            {"name": "District", "level": 3, "parent": "State"},
            {"name": "Block", "level": 2, "parent": "District"},
            {"name": "Village", "level": 1, "parent": "Block"},
        ],
        "groups": [
            {"name": "Everyone", "admin": False},
            {"name": "Administrators", "admin": True},
        ],
    },
    "Education": {
        "subject_types": [
            {"name": "Student", "type": "Person"},
            {"name": "School", "type": "Individual"},
        ],
        "programs": [
            {
                "name": "Education",
                "colour": "#2196F3",
                "target_subject_type": "Student",
            },
        ],
        "encounter_types": [
            {
                "name": "Enrolment Assessment",
                "is_program_encounter": True,
                "program_name": "Education",
            },
            {
                "name": "Attendance Tracking",
                "is_program_encounter": True,
                "program_name": "Education",
                "schedule_days": 7,
                "max_days": 14,
            },
            {
                "name": "Learning Assessment",
                "is_program_encounter": True,
                "program_name": "Education",
                "schedule_days": 90,
                "max_days": 120,
            },
            {
                "name": "School Inspection",
                "is_program_encounter": False,
                "subject_type": "School",
            },
        ],
        "address_levels": [
            {"name": "State", "level": 4},
            {"name": "District", "level": 3, "parent": "State"},
            {"name": "Block", "level": 2, "parent": "District"},
            {"name": "Village", "level": 1, "parent": "Block"},
        ],
        "groups": [
            {"name": "Everyone", "admin": False},
            {"name": "Administrators", "admin": True},
        ],
    },
    "WASH": {
        "subject_types": [
            {"name": "Household", "type": "Household"},
            {"name": "Water Source", "type": "Individual"},
        ],
        "programs": [
            {
                "name": "WASH",
                "colour": "#00BCD4",
                "target_subject_type": "Household",
            },
        ],
        "encounter_types": [
            {
                "name": "Household Survey",
                "is_program_encounter": True,
                "program_name": "WASH",
            },
            {
                "name": "Water Quality Test",
                "is_program_encounter": False,
                "subject_type": "Water Source",
                "schedule_days": 30,
                "max_days": 45,
            },
            {
                "name": "Sanitation Inspection",
                "is_program_encounter": True,
                "program_name": "WASH",
                "schedule_days": 90,
                "max_days": 120,
            },
            {
                "name": "Follow-up Visit",
                "is_program_encounter": True,
                "program_name": "WASH",
                "schedule_days": 14,
                "max_days": 21,
            },
        ],
        "address_levels": [
            {"name": "State", "level": 4},
            {"name": "District", "level": 3, "parent": "State"},
            {"name": "Block", "level": 2, "parent": "District"},
            {"name": "Village", "level": 1, "parent": "Block"},
        ],
        "groups": [
            {"name": "Everyone", "admin": False},
            {"name": "Administrators", "admin": True},
        ],
    },
}

# ---------------------------------------------------------------------------
# Sector-specific form fields
# ---------------------------------------------------------------------------

_SECTOR_FORM_FIELDS: dict[str, dict[str, list[dict[str, Any]]]] = {
    "MCH": {
        "ANC": [
            {"name": "Weight", "dataType": "Numeric", "unit": "kg", "mandatory": True},
            {
                "name": "BP Systolic",
                "dataType": "Numeric",
                "unit": "mmHg",
                "mandatory": True,
            },
            {
                "name": "BP Diastolic",
                "dataType": "Numeric",
                "unit": "mmHg",
                "mandatory": True,
            },
            {
                "name": "Hemoglobin",
                "dataType": "Numeric",
                "unit": "g/dL",
                "mandatory": True,
            },
            {
                "name": "Urine Albumin",
                "dataType": "Coded",
                "options": ["Nil", "Trace", "+1", "+2", "+3", "+4"],
                "mandatory": False,
            },
            {
                "name": "Fetal Heart Rate",
                "dataType": "Numeric",
                "unit": "bpm",
                "mandatory": False,
            },
            {
                "name": "Danger Signs",
                "dataType": "Coded",
                "options": [
                    "None",
                    "Vaginal Bleeding",
                    "Severe Headache",
                    "Blurred Vision",
                    "Convulsions",
                    "Swollen Hands/Face",
                    "High Fever",
                    "Loss of Consciousness",
                    "Difficulty Breathing",
                    "Severe Abdominal Pain",
                    "Reduced Fetal Movement",
                ],
                "mandatory": True,
            },
        ],
        "Delivery": [
            {
                "name": "Delivery Type",
                "dataType": "Coded",
                "options": ["Normal", "Assisted", "C-Section"],
                "mandatory": True,
            },
            {
                "name": "Delivery Place",
                "dataType": "Coded",
                "options": [
                    "Home",
                    "Sub-centre",
                    "PHC",
                    "CHC",
                    "District Hospital",
                    "Private Hospital",
                ],
                "mandatory": True,
            },
            {"name": "Delivery Date", "dataType": "Date", "mandatory": True},
            {
                "name": "Delivery Outcome",
                "dataType": "Coded",
                "options": ["Live Birth", "Still Birth", "Abortion"],
                "mandatory": True,
            },
            {
                "name": "Birth Weight",
                "dataType": "Numeric",
                "unit": "grams",
                "mandatory": True,
            },
            {
                "name": "Baby Gender",
                "dataType": "Coded",
                "options": ["Male", "Female"],
                "mandatory": True,
            },
        ],
        "PNC": [
            {
                "name": "Mother Condition",
                "dataType": "Coded",
                "options": ["Healthy", "Mild Concern", "Serious Concern"],
                "mandatory": True,
            },
            {
                "name": "Temperature",
                "dataType": "Numeric",
                "unit": "F",
                "mandatory": True,
            },
            {
                "name": "BP Systolic",
                "dataType": "Numeric",
                "unit": "mmHg",
                "mandatory": True,
            },
            {
                "name": "BP Diastolic",
                "dataType": "Numeric",
                "unit": "mmHg",
                "mandatory": True,
            },
            {
                "name": "Breastfeeding Status",
                "dataType": "Coded",
                "options": ["Exclusive", "Partial", "None"],
                "mandatory": True,
            },
        ],
        "HBNC": [
            {
                "name": "Baby Weight",
                "dataType": "Numeric",
                "unit": "kg",
                "mandatory": True,
            },
            {
                "name": "Temperature",
                "dataType": "Numeric",
                "unit": "F",
                "mandatory": True,
            },
            {
                "name": "Breastfeeding Status",
                "dataType": "Coded",
                "options": ["Exclusive", "Partial", "None"],
                "mandatory": True,
            },
            {
                "name": "Umbilical Cord Condition",
                "dataType": "Coded",
                "options": ["Clean", "Red", "Pus Discharge"],
                "mandatory": True,
            },
            {
                "name": "Danger Signs",
                "dataType": "Coded",
                "options": [
                    "None",
                    "Not Feeding Well",
                    "Convulsions",
                    "Fast Breathing",
                    "Chest Indrawing",
                    "High Temperature",
                    "Low Temperature",
                    "Jaundice",
                    "Umbilical Infection",
                ],
                "mandatory": True,
            },
        ],
        "Immunization": [
            {
                "name": "Vaccine Given",
                "dataType": "Coded",
                "options": [
                    "BCG",
                    "OPV-0",
                    "OPV-1",
                    "OPV-2",
                    "OPV-3",
                    "Hep-B Birth Dose",
                    "Hep-B 1",
                    "Hep-B 2",
                    "Hep-B 3",
                    "Pentavalent 1",
                    "Pentavalent 2",
                    "Pentavalent 3",
                    "Rotavirus 1",
                    "Rotavirus 2",
                    "Rotavirus 3",
                    "IPV",
                    "Measles 1",
                    "Measles 2",
                    "JE 1",
                    "JE 2",
                    "Vitamin A",
                    "DPT Booster 1",
                    "DPT Booster 2",
                    "TT",
                ],
                "mandatory": True,
            },
            {"name": "Vaccination Date", "dataType": "Date", "mandatory": True},
            {
                "name": "Adverse Reaction",
                "dataType": "Coded",
                "options": [
                    "None",
                    "Mild Fever",
                    "Swelling",
                    "Rash",
                    "Severe Reaction",
                ],
                "mandatory": False,
            },
        ],
        "Growth Monitoring": [
            {"name": "Weight", "dataType": "Numeric", "unit": "kg", "mandatory": True},
            {"name": "Height", "dataType": "Numeric", "unit": "cm", "mandatory": True},
            {"name": "MUAC", "dataType": "Numeric", "unit": "cm", "mandatory": False},
            {
                "name": "Nutritional Status",
                "dataType": "Coded",
                "options": ["Normal", "Moderately Underweight", "Severely Underweight"],
                "mandatory": False,
            },
        ],
    },
    "Nutrition": {
        "Nutrition Assessment": [
            {"name": "Weight", "dataType": "Numeric", "unit": "kg", "mandatory": True},
            {"name": "Height", "dataType": "Numeric", "unit": "cm", "mandatory": True},
            {"name": "MUAC", "dataType": "Numeric", "unit": "cm", "mandatory": True},
            {
                "name": "Nutritional Status",
                "dataType": "Coded",
                "options": ["Normal", "MAM", "SAM"],
                "mandatory": True,
            },
            {
                "name": "Oedema",
                "dataType": "Coded",
                "options": ["None", "Mild", "Moderate", "Severe"],
                "mandatory": True,
            },
            {
                "name": "Hemoglobin",
                "dataType": "Numeric",
                "unit": "g/dL",
                "mandatory": False,
            },
        ],
        "Counselling": [
            {
                "name": "Counselling Topic",
                "dataType": "Coded",
                "options": [
                    "Breastfeeding",
                    "Complementary Feeding",
                    "Hygiene",
                    "Diet Diversity",
                    "Micronutrients",
                ],
                "mandatory": True,
            },
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
        "Supplementation": [
            {
                "name": "Supplement Type",
                "dataType": "Coded",
                "options": ["IFA", "Vitamin A", "Zinc", "ORS", "RUTF", "Other"],
                "mandatory": True,
            },
            {"name": "Quantity Given", "dataType": "Numeric", "mandatory": True},
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
        "Follow-up": [
            {"name": "Weight", "dataType": "Numeric", "unit": "kg", "mandatory": True},
            {"name": "MUAC", "dataType": "Numeric", "unit": "cm", "mandatory": False},
            {
                "name": "Improvement Status",
                "dataType": "Coded",
                "options": ["Improved", "Same", "Deteriorated"],
                "mandatory": True,
            },
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
    },
    "Livelihoods": {
        "Skill Assessment": [
            {
                "name": "Education Level",
                "dataType": "Coded",
                "options": [
                    "No Formal Education",
                    "Primary",
                    "Secondary",
                    "Higher Secondary",
                    "Graduate",
                    "Post Graduate",
                ],
                "mandatory": True,
            },
            {
                "name": "Current Occupation",
                "dataType": "Coded",
                "options": [
                    "Agriculture",
                    "Daily Wage",
                    "Self Employed",
                    "Unemployed",
                    "Student",
                    "Other",
                ],
                "mandatory": True,
            },
            {
                "name": "Skill Area",
                "dataType": "Coded",
                "options": [
                    "Tailoring",
                    "Computer",
                    "Driving",
                    "Electrical",
                    "Plumbing",
                    "Beautician",
                    "Other",
                ],
                "mandatory": True,
            },
            {
                "name": "Monthly Income",
                "dataType": "Numeric",
                "unit": "INR",
                "mandatory": False,
            },
        ],
        "Training": [
            {"name": "Training Name", "dataType": "Text", "mandatory": True},
            {"name": "Training Start Date", "dataType": "Date", "mandatory": True},
            {"name": "Training End Date", "dataType": "Date", "mandatory": False},
            {
                "name": "Training Status",
                "dataType": "Coded",
                "options": ["Ongoing", "Completed", "Dropped Out"],
                "mandatory": True,
            },
        ],
        "Placement Follow-up": [
            {
                "name": "Employment Status",
                "dataType": "Coded",
                "options": ["Employed", "Self Employed", "Seeking", "Not Interested"],
                "mandatory": True,
            },
            {
                "name": "Monthly Income",
                "dataType": "Numeric",
                "unit": "INR",
                "mandatory": False,
            },
            {"name": "Employer Name", "dataType": "Text", "mandatory": False},
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
        "SHG Meeting": [
            {"name": "Meeting Date", "dataType": "Date", "mandatory": True},
            {"name": "Members Present", "dataType": "Numeric", "mandatory": True},
            {
                "name": "Savings Collected",
                "dataType": "Numeric",
                "unit": "INR",
                "mandatory": False,
            },
            {
                "name": "Loans Disbursed",
                "dataType": "Numeric",
                "unit": "INR",
                "mandatory": False,
            },
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
    },
    "Education": {
        "Enrolment Assessment": [
            {
                "name": "Class",
                "dataType": "Coded",
                "options": [
                    "1",
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                ],
                "mandatory": True,
            },
            {
                "name": "Medium of Instruction",
                "dataType": "Coded",
                "options": ["Hindi", "English", "Regional Language"],
                "mandatory": True,
            },
            {
                "name": "Previous Year Result",
                "dataType": "Coded",
                "options": ["Pass", "Fail", "Not Applicable"],
                "mandatory": False,
            },
        ],
        "Attendance Tracking": [
            {"name": "Days Present", "dataType": "Numeric", "mandatory": True},
            {"name": "Days Absent", "dataType": "Numeric", "mandatory": True},
            {
                "name": "Reason for Absence",
                "dataType": "Coded",
                "options": [
                    "Illness",
                    "Family Work",
                    "Migration",
                    "Lack of Interest",
                    "Other",
                ],
                "mandatory": False,
            },
        ],
        "Learning Assessment": [
            {
                "name": "Reading Level",
                "dataType": "Coded",
                "options": [
                    "Cannot Read",
                    "Letters",
                    "Words",
                    "Sentences",
                    "Paragraph",
                    "Story",
                ],
                "mandatory": True,
            },
            {
                "name": "Math Level",
                "dataType": "Coded",
                "options": [
                    "Cannot Recognise Numbers",
                    "Numbers 1-9",
                    "Numbers 10-99",
                    "Subtraction",
                    "Division",
                ],
                "mandatory": True,
            },
            {"name": "Score", "dataType": "Numeric", "mandatory": False},
        ],
        "School Inspection": [
            {"name": "Teachers Present", "dataType": "Numeric", "mandatory": True},
            {"name": "Students Present", "dataType": "Numeric", "mandatory": True},
            {
                "name": "Infrastructure Status",
                "dataType": "Coded",
                "options": ["Good", "Average", "Poor"],
                "mandatory": True,
            },
            {
                "name": "Midday Meal Status",
                "dataType": "Coded",
                "options": ["Served", "Not Served", "Not Applicable"],
                "mandatory": True,
            },
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
    },
    "WASH": {
        "Household Survey": [
            {
                "name": "Water Source",
                "dataType": "Coded",
                "options": [
                    "Piped",
                    "Hand Pump",
                    "Well",
                    "River/Pond",
                    "Tanker",
                    "Other",
                ],
                "mandatory": True,
            },
            {
                "name": "Toilet Type",
                "dataType": "Coded",
                "options": ["Flush", "Pit Latrine", "No Toilet"],
                "mandatory": True,
            },
            {
                "name": "Handwashing Practice",
                "dataType": "Coded",
                "options": ["With Soap", "Without Soap", "No Handwashing"],
                "mandatory": True,
            },
            {
                "name": "Waste Disposal",
                "dataType": "Coded",
                "options": ["Collected", "Open Dumping", "Burning", "Composting"],
                "mandatory": False,
            },
        ],
        "Water Quality Test": [
            {
                "name": "pH Level",
                "dataType": "Numeric",
                "mandatory": True,
            },
            {
                "name": "Turbidity",
                "dataType": "Numeric",
                "unit": "NTU",
                "mandatory": True,
            },
            {
                "name": "Chlorine Residual",
                "dataType": "Numeric",
                "unit": "mg/L",
                "mandatory": False,
            },
            {
                "name": "Coliform Test",
                "dataType": "Coded",
                "options": ["Absent", "Present"],
                "mandatory": True,
            },
            {
                "name": "Result",
                "dataType": "Coded",
                "options": ["Safe", "Unsafe"],
                "mandatory": True,
            },
        ],
        "Sanitation Inspection": [
            {
                "name": "Toilet Functional",
                "dataType": "Coded",
                "options": ["Yes", "No"],
                "mandatory": True,
            },
            {
                "name": "Drainage Condition",
                "dataType": "Coded",
                "options": ["Good", "Blocked", "No Drainage"],
                "mandatory": True,
            },
            {
                "name": "Cleanliness Score",
                "dataType": "Numeric",
                "mandatory": True,
            },
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
        "Follow-up Visit": [
            {
                "name": "Issue Status",
                "dataType": "Coded",
                "options": ["Resolved", "Partially Resolved", "Not Resolved"],
                "mandatory": True,
            },
            {
                "name": "Action Taken",
                "dataType": "Text",
                "mandatory": False,
            },
            {"name": "Notes", "dataType": "Text", "mandatory": False},
        ],
    },
}

# ---------------------------------------------------------------------------
# Vital-sign ranges: {parameter: [absolute_low, normal_low, normal_high, absolute_high]}
# ---------------------------------------------------------------------------

_SECTOR_VITALS: dict[str, dict[str, list[int | float]]] = {
    "MCH": {
        "BP Systolic": [80, 100, 139, 220],
        "BP Diastolic": [40, 60, 90, 120],
        "Hemoglobin": [2, 11, 14, 18],
        "Weight": [30, 45, 80, 150],
        "Birth Weight": [500, 2500, 4000, 6000],
        "Fetal Heart Rate": [60, 110, 160, 200],
        "Temperature": [95, 97, 99, 105],
        "MUAC": [5, 12.5, 25, 40],
    },
    "Nutrition": {
        "Weight": [0.5, 2.5, 80, 150],
        "Height": [30, 45, 180, 220],
        "MUAC": [5, 11.5, 25, 40],
        "Hemoglobin": [2, 11, 14, 18],
    },
    "Livelihoods": {
        "Monthly Income": [0, 0, 50000, 500000],
    },
    "Education": {
        "Score": [0, 0, 100, 100],
        "Days Present": [0, 0, 31, 31],
        "Days Absent": [0, 0, 31, 31],
    },
    "WASH": {
        "pH Level": [0, 6.5, 8.5, 14],
        "Turbidity": [0, 0, 5, 1000],
        "Chlorine Residual": [0, 0.2, 2.0, 10],
        "Cleanliness Score": [0, 0, 10, 10],
    },
}

# ---------------------------------------------------------------------------
# Keyword map for auto-detection
# ---------------------------------------------------------------------------

_SECTOR_KEYWORDS: dict[str, list[str]] = {
    "MCH": [
        "maternal",
        "child health",
        "mch",
        "pregnancy",
        "antenatal",
        "anc",
        "pnc",
        "postnatal",
        "delivery",
        "newborn",
        "neonatal",
        "hbnc",
        "immunization",
        "immunisation",
        "vaccine",
        "growth monitoring",
        "breastfeeding",
        "reproductive",
        "rch",
        "mother",
        "infant",
        "obstetric",
        "gynec",
        "fetal",
        "prenatal",
    ],
    "Nutrition": [
        "nutrition",
        "malnutrition",
        "underweight",
        "stunting",
        "wasting",
        "sam",
        "mam",
        "muac",
        "supplementary feeding",
        "therapeutic feeding",
        "rutf",
        "ors",
        "icds",
        "anganwadi",
        "mid-day meal",
        "midday meal",
        "poshan",
    ],
    "Livelihoods": [
        "livelihood",
        "livelihoods",
        "self help group",
        "shg",
        "income generation",
        "skill development",
        "skill training",
        "vocational",
        "employment",
        "microfinance",
        "micro-finance",
        "enterprise",
        "placement",
    ],
    "Education": [
        "education",
        "school",
        "student",
        "attendance",
        "learning",
        "teacher",
        "classroom",
        "enrollment",
        "enrolment",
        "literacy",
        "numeracy",
        "aser",
        "reading level",
    ],
    "WASH": [
        "wash",
        "water",
        "sanitation",
        "hygiene",
        "toilet",
        "latrine",
        "handwashing",
        "hand washing",
        "drinking water",
        "water quality",
        "open defecation",
        "odf",
        "sewage",
        "drainage",
        "swachh",
    ],
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_available_sectors() -> list[str]:
    """Return the list of supported sector names."""
    return sorted(_SECTOR_DEFAULTS.keys())


def get_sector_defaults(sector: str) -> dict:
    """
    Return the default entity structure for *sector*.

    Returns an empty dict if the sector is not recognised.
    """
    return _SECTOR_DEFAULTS.get(sector, {})


def get_sector_form_fields(sector: str, encounter_name: str) -> list[dict]:
    """
    Return pre-built form field definitions for a given sector and encounter type.

    Returns an empty list if the sector or encounter is not recognised.
    """
    sector_fields = _SECTOR_FORM_FIELDS.get(sector, {})
    return sector_fields.get(encounter_name, [])


def get_sector_vital_ranges(sector: str) -> dict:
    """
    Return vital-sign ranges for a sector.

    Each key maps to ``[absolute_low, normal_low, normal_high, absolute_high]``.
    Returns an empty dict if the sector is not recognised.
    """
    return _SECTOR_VITALS.get(sector, {})


def detect_sector(description: str) -> str | None:
    """
    Attempt to detect the sector from a free-text description using keyword matching.

    Returns the best matching sector name, or ``None`` if no sector matches.
    """
    if not description:
        return None

    text = description.lower()
    scores: dict[str, int] = {}

    for sector, keywords in _SECTOR_KEYWORDS.items():
        score = 0
        for kw in keywords:
            # Use word-boundary matching for short keywords to avoid false positives
            if len(kw) <= 3:
                if re.search(rf"\b{re.escape(kw)}\b", text):
                    score += 2
            else:
                if kw in text:
                    score += 1
        if score > 0:
            scores[sector] = score

    if not scores:
        return None

    # Return the sector with the highest score
    return max(scores, key=scores.get)  # type: ignore[arg-type]
