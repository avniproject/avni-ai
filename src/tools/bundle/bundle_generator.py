import json
import logging
from pathlib import Path
from typing import Optional

from .models import (
    Bundle,
    AddressLevelTypeContract,
    EncounterTypeContract,
    FormMappingContract,
    ProgramContract,
    SubjectTypeContract,
    ParsedEncounter,
    ParsedEntities,
    ParsedLocationHierarchy,
    ParsedProgram,
    ParsedSubjectType,
)
from .models.subject_type import SubjectTypeEnum
from .uuid_registry import generate_uuid, get_standard_uuid

logger = logging.getLogger(__name__)


# ─── Constants ─────────────────────────────────────────────────────────────

PROGRAM_COLOURS: dict[str, str] = {
    "pregnancy": "#74b5de",
    "child": "#96d643",
    "maternal": "#74b5de",
    "nourish": "#e8a838",
    "enrich": "#9b59b6",
}
DEFAULT_COLOUR = "#3498db"

GENDER_UUIDS: dict[str, str] = {
    "Male": "924de7e5-47d9-401a-9178-3336fee5ee03",
    "Female": "710583d4-cb89-4986-aef2-b97b6aa222e5",
}

DEFAULT_RELATIONS = [
    ("Husband", "Male"), ("Wife", "Female"),
    ("Father", "Male"), ("Mother", "Female"),
    ("Son", "Male"), ("Daughter", "Female"),
    ("Brother", "Male"), ("Sister", "Female"),
    ("Grandfather", "Male"), ("Grandmother", "Female"),
    ("Son in law", "Male"), ("Daughter in law", "Female"),
    ("Father in law", "Male"), ("Mother in law", "Female"),
    ("Uncle", "Male"), ("Aunt", "Female"),
    ("Nephew", "Male"), ("Niece", "Female"),
    ("Grandson", "Male"), ("Granddaughter", "Female"),
    ("Brother in law", "Male"), ("Sister in law", "Female"),
]

DEFAULT_RELATIONSHIP_TYPES = [
    ("Husband", "Wife"), ("Father", "Son"), ("Father", "Daughter"),
    ("Mother", "Son"), ("Mother", "Daughter"), ("Brother", "Sister"),
    ("Grandfather", "Grandson"), ("Grandmother", "Granddaughter"),
]


# ─── Helpers ───────────────────────────────────────────────────────────────


def _get_program_colour(program_name: str) -> str:
    lower = program_name.lower()
    for keyword, colour in PROGRAM_COLOURS.items():
        if keyword in lower:
            return colour
    return DEFAULT_COLOUR


def _resolve_name(
    target: str,
    known: list[ParsedSubjectType] | list[ParsedProgram],
) -> Optional[str]:
    if not target:
        return None
    target_lower = target.strip().lower()
    for item in known:
        item_lower = item.name.strip().lower()
        if target_lower == item_lower:
            return item.name
        if target_lower in item_lower or item_lower in target_lower:
            return item.name
    return None


def _infer_eligibility_rule(program_name: str) -> Optional[list[dict]]:
    if program_name == "Pregnancy":
        return [{
            "actions": [{"actionType": "showProgram"}],
            "conditions": [{"compoundRule": {"rules": [{
                "lhs": {"type": "gender"},
                "rhs": {"type": "value", "value": "Female"},
                "operator": "equals",
            }]}}],
        }]
    if program_name == "Child":
        return [{
            "actions": [{"actionType": "hideProgram"}],
            "conditions": [{"compoundRule": {
                "rules": [{"lhs": {"type": "ageInYears"}, "rhs": {"type": "value", "value": 2}, "operator": "greaterThan"}],
                "conjunction": "and",
            }}],
        }]
    return None

def _generate_subject_types(parsed: list[ParsedSubjectType]) -> list[SubjectTypeContract]:
    result = []
    for st in parsed:
        subject_type = SubjectTypeEnum.from_raw(st.type)
        result.append(SubjectTypeContract(
            name=st.name,
            uuid=generate_uuid(),
            type=subject_type,
            group=subject_type in (SubjectTypeEnum.HOUSEHOLD, SubjectTypeEnum.GROUP),
            household=subject_type == SubjectTypeEnum.HOUSEHOLD,
            allow_middle_name=subject_type == SubjectTypeEnum.PERSON,
        ))
    return result


def _generate_programs(parsed_programs: list[ParsedProgram]) -> list[ProgramContract]:
    result = []
    for prog in parsed_programs:
        result.append(ProgramContract(
            name=prog.name,
            uuid=generate_uuid(),
            colour=_get_program_colour(prog.name),
            enrolment_eligibility_check_declarative_rule=_infer_eligibility_rule(prog.name),
        ))
    return result


def _generate_encounter_types(
    encounters: list[ParsedEncounter],
    program_encounters: list[ParsedEncounter],
) -> list[EncounterTypeContract]:
    seen: set[str] = set()
    result = []
    for enc in encounters + program_encounters:
        key = enc.name.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(EncounterTypeContract(
            name=enc.name,
            uuid=generate_uuid(),
        ))
    return result


def _generate_address_level_types(
    hierarchies: list[ParsedLocationHierarchy],
) -> list[AddressLevelTypeContract]:
    all_levels: dict[str, dict] = {}
    for h in hierarchies:
        for level in h.levels:
            if level.name not in all_levels:
                all_levels[level.name] = {
                    "level": level.level,
                    "parent": level.parent,
                }

    if not all_levels:
        logger.info("No location hierarchy found, using default: State -> District -> Block -> Village")
        state = AddressLevelTypeContract(name="State", uuid=generate_uuid(), level=4.0)
        district = AddressLevelTypeContract(name="District", uuid=generate_uuid(), level=3.0, parent={"uuid": state.uuid})
        block = AddressLevelTypeContract(name="Block", uuid=generate_uuid(), level=2.0, parent={"uuid": district.uuid})
        village = AddressLevelTypeContract(name="Village", uuid=generate_uuid(), level=1.0, parent={"uuid": block.uuid})
        return [state, district, block, village]

    # First pass: generate UUIDs for all levels
    uuid_by_name: dict[str, str] = {}
    for name in all_levels:
        uuid_by_name[name] = generate_uuid()

    # Second pass: build contracts with parent references
    result = []
    for name, data in sorted(all_levels.items(), key=lambda x: x[1]["level"]):
        parent = {"uuid": uuid_by_name[data["parent"]]} if data.get("parent") and data["parent"] in uuid_by_name else None
        result.append(AddressLevelTypeContract(
            name=name,
            uuid=uuid_by_name[name],
            level=float(data["level"]),
            parent=parent,
        ))
    return result


def _generate_form_mappings(
    entities: ParsedEntities,
    subject_types: list[SubjectTypeContract],
    programs: list[ProgramContract],
    encounter_types: list[EncounterTypeContract],
) -> list[FormMappingContract]:
    mappings: list[FormMappingContract] = []

    # Build lookup dicts: name -> uuid
    st_uuid_by_name = {st.name: st.uuid for st in subject_types}
    prog_uuid_by_name = {p.name: p.uuid for p in programs}
    et_uuid_by_name = {et.name: et.uuid for et in encounter_types}

    def _resolve_st_uuid(target: str) -> str:
        resolved = _resolve_name(target, entities.subject_types)
        name = resolved or (entities.subject_types[0].name if entities.subject_types else "Individual")
        return st_uuid_by_name.get(name, generate_uuid())

    def _resolve_prog_uuid(target: str) -> Optional[str]:
        resolved = _resolve_name(target, entities.programs)
        return prog_uuid_by_name.get(resolved) if resolved else None

    def _resolve_et_uuid(name: str) -> str:
        return et_uuid_by_name.get(name, generate_uuid())

    # Registration forms
    for st in entities.subject_types:
        form_name = st.form_link or st.name
        mappings.append(FormMappingContract(
            uuid=generate_uuid(),
            form_uuid=generate_uuid(),
            subject_type_uuid=st_uuid_by_name[st.name],
            form_type="IndividualProfile",
            form_name=form_name,
        ))

    # Program enrolment + exit forms
    for prog in entities.programs:
        st_uuid = _resolve_st_uuid(prog.target_subject_type)
        prog_uuid = prog_uuid_by_name[prog.name]

        enrol_form = prog.enrolment_form or f"{prog.name} Enrolment"
        mappings.append(FormMappingContract(
            uuid=generate_uuid(),
            form_uuid=generate_uuid(),
            subject_type_uuid=st_uuid,
            form_type="ProgramEnrolment",
            form_name=enrol_form,
            program_uuid=prog_uuid,
        ))

        if prog.exit_form:
            mappings.append(FormMappingContract(
                uuid=generate_uuid(),
                form_uuid=generate_uuid(),
                subject_type_uuid=st_uuid,
                form_type="ProgramExit",
                form_name=prog.exit_form,
                program_uuid=prog_uuid,
            ))

    # General encounter forms
    for enc in entities.encounters:
        st_uuid = _resolve_st_uuid(enc.subject_type)
        form_name = enc.forms_linked or enc.name
        mappings.append(FormMappingContract(
            uuid=generate_uuid(),
            form_uuid=generate_uuid(),
            subject_type_uuid=st_uuid,
            form_type="Encounter",
            form_name=form_name,
            encounter_type_uuid=_resolve_et_uuid(enc.name),
        ))

        if enc.encounter_type.lower() == "scheduled":
            cancel_form = enc.cancellation_form or f"{enc.name} Cancellation"
            mappings.append(FormMappingContract(
                uuid=generate_uuid(),
                form_uuid=generate_uuid(),
                subject_type_uuid=st_uuid,
                form_type="IndividualEncounterCancellation",
                form_name=cancel_form,
                encounter_type_uuid=_resolve_et_uuid(enc.name),
            ))

    # Program encounter forms
    for pe in entities.program_encounters:
        prog_uuid = _resolve_prog_uuid(pe.program_name or "")
        st_uuid = _resolve_st_uuid("")
        if pe.program_name:
            for prog in entities.programs:
                if _resolve_name(pe.program_name, [prog]):
                    st_uuid = _resolve_st_uuid(prog.target_subject_type)
                    break

        form_name = pe.forms_linked or pe.name
        mappings.append(FormMappingContract(
            uuid=generate_uuid(),
            form_uuid=generate_uuid(),
            subject_type_uuid=st_uuid,
            form_type="ProgramEncounter",
            form_name=form_name,
            program_uuid=prog_uuid,
            encounter_type_uuid=_resolve_et_uuid(pe.name),
        ))

        if pe.encounter_type.lower() == "scheduled":
            cancel_form = pe.cancellation_form or f"{pe.name} Cancellation"
            mappings.append(FormMappingContract(
                uuid=generate_uuid(),
                form_uuid=generate_uuid(),
                subject_type_uuid=st_uuid,
                form_type="ProgramEncounterCancellation",
                form_name=cancel_form,
                program_uuid=prog_uuid,
                encounter_type_uuid=_resolve_et_uuid(pe.name),
            ))

    return mappings


# ─── Operational & relationship generators ─────────────────────────────────


def _generate_operational_encounter_types(encounter_types: list[EncounterTypeContract]) -> list[dict]:
    return [
        {
            "encounterType": {"uuid": et.uuid, "name": et.name},
            "uuid": generate_uuid(),
            "name": et.name,
            "voided": False,
        }
        for et in encounter_types
    ]


def _generate_operational_programs(programs: list[ProgramContract]) -> list[dict]:
    return [
        {
            "program": {"uuid": p.uuid, "name": p.name},
            "uuid": generate_uuid(),
            "name": p.name,
            "voided": False,
            "programSubjectLabel": p.name,
        }
        for p in programs
    ]


def _generate_operational_subject_types(subject_types: list[SubjectTypeContract]) -> list[dict]:
    return [
        {
            "subjectType": {"uuid": st.uuid, "name": st.name},
            "uuid": generate_uuid(),
            "name": st.name,
            "voided": False,
        }
        for st in subject_types
    ]


def _generate_individual_relations() -> list[dict]:
    # Build relation UUIDs once so relationship types can reference them
    relation_uuids: dict[str, str] = {}
    for name, _ in DEFAULT_RELATIONS:
        relation_uuids[name] = generate_uuid()

    relations = [
        {
            "id": None,
            "name": name,
            "uuid": relation_uuids[name],
            "voided": False,
            "genders": [{"uuid": GENDER_UUIDS[gender], "name": gender, "voided": False}],
        }
        for name, gender in DEFAULT_RELATIONS
    ]
    return relations, relation_uuids


def _generate_relationship_types(relation_uuids: dict[str, str]) -> list[dict]:
    return [
        {
            "uuid": generate_uuid(),
            "name": f"{from_rel}-{to_rel}",
            "individualAIsToBRelation": {
                "name": from_rel,
                "uuid": relation_uuids[from_rel],
            },
            "individualBIsToARelation": {
                "name": to_rel,
                "uuid": relation_uuids[to_rel],
            },
            "voided": False,
        }
        for from_rel, to_rel in DEFAULT_RELATIONSHIP_TYPES
    ]


def _generate_organisation_config(org_name: str) -> dict:
    return {
        "uuid": generate_uuid(),
        "settings": {
            "languages": ["en"],
            "myDashboardFilters": [],
            "searchFilters": [],
            "enableMessaging": False,
        },
    }


# ─── Main entry point ─────────────────────────────────────────────────────


def generate_bundle(entities: ParsedEntities, org_name: str) -> Bundle:
    logger.info(f"Generating bundle for org: {org_name}")

    subject_types = _generate_subject_types(entities.subject_types)
    programs = _generate_programs(entities.programs)
    encounter_types = _generate_encounter_types(entities.encounters, entities.program_encounters)
    address_level_types = _generate_address_level_types(entities.location_hierarchies)
    form_mappings = _generate_form_mappings(entities, subject_types, programs, encounter_types)
    individual_relations, relation_uuids = _generate_individual_relations()

    bundle = Bundle(
        subject_types=subject_types,
        programs=programs,
        encounter_types=encounter_types,
        address_level_types=address_level_types,
        form_mappings=form_mappings,
        operational_encounter_types=_generate_operational_encounter_types(encounter_types),
        operational_programs=_generate_operational_programs(programs),
        operational_subject_types=_generate_operational_subject_types(subject_types),
        individual_relations=individual_relations,
        relationship_types=_generate_relationship_types(relation_uuids),
        organisation_config=_generate_organisation_config(org_name),
    )

    logger.info(
        f"Bundle generated: {len(subject_types)} subject types, "
        f"{len(programs)} programs, {len(encounter_types)} encounter types, "
        f"{len(address_level_types)} address level types, {len(form_mappings)} form mappings"
    )

    return bundle


def export_bundle_to_directory(bundle: Bundle, output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    assets = bundle.to_asset_dict()
    for filename, data in assets.items():
        file_path = output_dir / f"{filename}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    logger.info(f"Wrote {len(assets)} files to {output_dir}")
    return output_dir
