"""
Main bundle generator — orchestrates concept + form generation
and produces a complete AVNI bundle from an entities config.
Ported from srs-bundle-generator/generators/bundle.js.
"""

from __future__ import annotations

import io
import json
import logging
import zipfile
from typing import Any

from .concepts import ConceptGenerator
from .forms import FormGenerator
from .uuid_utils import generate_deterministic_uuid

logger = logging.getLogger(__name__)


class BundleGenerator:
    def __init__(self, org_name: str) -> None:
        # Guard against unresolved Dify template literals (e.g. "{{#n-start.org_name#}}")
        if not org_name or org_name.startswith("{{#"):
            org_name = "MyOrg"
        self.org_name = org_name
        self.concept_generator = ConceptGenerator()
        self.form_generator = FormGenerator()
        self.bundle: dict[str, Any] = {
            "concepts": [],
            "forms": [],
            "subjectTypes": [],
            "programs": [],
            "encounterTypes": [],
            "formMappings": [],
            "groups": [],
            "groupPrivileges": [],
            "addressLevelTypes": [],
            "operationalSubjectTypes": {"operationalSubjectTypes": []},
            "operationalPrograms": {"operationalPrograms": []},
            "operationalEncounterTypes": {"operationalEncounterTypes": []},
            "organisationConfig": {},
            "reportCards": [],
            "reportDashboards": [],
            "groupDashboards": [],
        }
        self.validation: dict[str, list] = {"errors": [], "warnings": []}
        self.confidence: dict[str, Any] = {}
        self.flags: list[dict] = []  # auto-resolved decisions for user review

    # ── Entity processors ───────────────────────────────────────────

    def process_subject_types(self, subject_types: list[dict]) -> None:
        for st in subject_types:
            self.bundle["subjectTypes"].append(
                {
                    "name": st["name"],
                    "uuid": generate_deterministic_uuid(f"subjectType:{st['name']}"),
                    "active": True,
                    "type": st.get("type", "Person"),
                    "subjectSummaryRule": "",
                    "programEligibilityCheckRule": "",
                    "allowEmptyLocation": False,
                    "allowMiddleName": False,
                    "lastNameOptional": True,
                    "validFirstNameFormat": {
                        "regex": "[A-Za-z0-9\\s]+",
                        "descriptionKey": "alphanumericAndSpaces",
                    },
                    "iconFileS3Key": None,
                    "settings": None,
                }
            )

    def process_programs(self, programs: list[dict]) -> None:
        for prog in programs:
            self.bundle["programs"].append(
                {
                    "name": prog["name"],
                    "uuid": generate_deterministic_uuid(f"program:{prog['name']}"),
                    "colour": prog.get("colour", "#3949AB"),
                    "programSubjectLabel": prog.get("subjectLabel", prog["name"]),
                    "enrolmentSummaryRule": "",
                    "enrolmentEligibilityCheckRule": "",
                    "active": True,
                    "manualEnrolmentEligibilityCheckRule": "",
                    "manualEligibilityCheckRequired": False,
                    "allowMultipleEnrolments": False,
                }
            )

    def process_encounter_types(self, encounter_types: list[dict]) -> None:
        for et in encounter_types:
            self.bundle["encounterTypes"].append(
                {
                    "name": et["name"],
                    "uuid": generate_deterministic_uuid(f"encounterType:{et['name']}"),
                    "encounterEligibilityCheckRule": "",
                    "active": True,
                    "immutable": False,
                    "programEncounter": et.get("programEncounter", True),
                }
            )

    def process_groups(self, groups: list[dict]) -> None:
        for group in groups:
            self.bundle["groups"].append(
                {
                    "name": group["name"],
                    "uuid": generate_deterministic_uuid(f"group:{group['name']}"),
                    "hasAllPrivileges": group.get("admin", False),
                }
            )

    def process_address_levels(self, address_levels: list[dict]) -> None:
        # Sort by level descending (topmost = highest number)
        sorted_levels = sorted(
            address_levels, key=lambda a: a.get("level", 0), reverse=True
        )
        # Build name→uuid map for parent resolution
        name_to_uuid: dict[str, str] = {}
        for al in sorted_levels:
            al_uuid = generate_deterministic_uuid(f"addressLevelType:{al['name']}")
            name_to_uuid[al["name"]] = al_uuid

        for al in sorted_levels:
            al_uuid = name_to_uuid[al["name"]]
            entry: dict[str, Any] = {
                "name": al["name"],
                "uuid": al_uuid,
                "level": float(al.get("level", 1)),
            }
            parent_name = al.get("parent")
            if parent_name and parent_name in name_to_uuid:
                entry["parent"] = {"uuid": name_to_uuid[parent_name]}
            self.bundle["addressLevelTypes"].append(entry)

    # ── Operational configs ────────────────────────────────────────

    def _generate_operational_configs(self) -> None:
        """Generate operational wrappers for subject types, programs, encounter types."""
        for st in self.bundle["subjectTypes"]:
            self.bundle["operationalSubjectTypes"]["operationalSubjectTypes"].append(
                {
                    "uuid": generate_deterministic_uuid(
                        f"operationalSubjectType:{st['name']}"
                    ),
                    "name": st["name"],
                    "subjectType": {"uuid": st["uuid"], "voided": False},
                    "voided": False,
                }
            )
        for prog in self.bundle["programs"]:
            self.bundle["operationalPrograms"]["operationalPrograms"].append(
                {
                    "uuid": generate_deterministic_uuid(
                        f"operationalProgram:{prog['name']}"
                    ),
                    "name": prog["name"],
                    "program": {"uuid": prog["uuid"], "voided": False},
                    "programSubjectLabel": prog.get("programSubjectLabel", ""),
                    "voided": False,
                }
            )
        for et in self.bundle["encounterTypes"]:
            self.bundle["operationalEncounterTypes"][
                "operationalEncounterTypes"
            ].append(
                {
                    "uuid": generate_deterministic_uuid(
                        f"operationalEncounterType:{et['name']}"
                    ),
                    "name": et["name"],
                    "encounterType": {"uuid": et["uuid"], "voided": False},
                    "voided": False,
                }
            )

    # ── Forms ───────────────────────────────────────────────────────

    def process_forms(self, forms: list[dict]) -> None:
        for form_spec in forms:
            fields = form_spec.get("fields", [])

            # Generate concepts from the fields
            concepts = self.concept_generator.generate_from_fields(fields)

            # Build concept lookup for form generator
            concept_map: dict[str, dict] = {}
            for c in concepts:
                concept_map[c["name"]] = {
                    "uuid": c["uuid"],
                    "dataType": c["dataType"],
                    "answers": c.get("answers"),
                }

            # Generate form
            form = self.form_generator.generate_form(
                name=form_spec["name"],
                form_type=form_spec.get("formType", "Encounter"),
                fields=fields,
                concepts=concept_map,
            )
            self.bundle["forms"].append(form)

            # Auto-generate cancellation form for encounter types
            if form_spec.get("formType") in ("ProgramEncounter", "Encounter"):
                cancel_form = self.form_generator.generate_cancellation_form(
                    form_spec["name"], form_spec["formType"]
                )
                self.bundle["forms"].append(cancel_form)

                # Register cancellation form concepts so they aren't orphaned
                for group in cancel_form.get("formElementGroups", []):
                    for elem in group.get("formElements", []):
                        concept = elem.get("concept", {})
                        if concept.get("name") and concept.get("uuid"):
                            self.concept_generator.generated_concepts.append(
                                {
                                    "name": concept["name"],
                                    "uuid": concept["uuid"],
                                    "dataType": concept.get("dataType", "Text"),
                                    "active": True,
                                }
                            )

                # Generate form mapping for the cancellation form
                cancel_form_type = (
                    "ProgramEncounterCancellation"
                    if form_spec["formType"] == "ProgramEncounter"
                    else "IndividualEncounterCancellation"
                )
                cancel_spec = {
                    **form_spec,
                    "name": cancel_form["name"],
                    "formType": cancel_form_type,
                }
                self._generate_form_mapping(cancel_spec, cancel_form["uuid"])

            # Generate form mapping for main form
            self._generate_form_mapping(form_spec, form["uuid"])

        # Store all concepts
        self.bundle["concepts"] = self.concept_generator.generated_concepts

    def _generate_form_mapping(self, form_spec: dict, form_uuid: str) -> None:
        form_type = form_spec.get("formType", "Encounter")
        mapping: dict[str, Any] = {
            "uuid": generate_deterministic_uuid(f"mapping:{form_spec['name']}"),
            "formUUID": form_uuid,
            "formType": form_type,
            "formName": form_spec["name"],
            "enableApproval": False,
        }
        # Resolve references
        st = next(
            (
                s
                for s in self.bundle["subjectTypes"]
                if s["name"] == form_spec.get("subjectType")
            ),
            None,
        )
        prog = next(
            (
                p
                for p in self.bundle["programs"]
                if p["name"] == form_spec.get("program")
            ),
            None,
        )
        et = next(
            (
                e
                for e in self.bundle["encounterTypes"]
                if e["name"] == form_spec.get("encounterType")
            ),
            None,
        )

        # Fallback: if no subject type resolved, use the first available one
        # (Avni requires subjectTypeUUID on every formMapping)
        if not st and self.bundle["subjectTypes"]:
            st = self.bundle["subjectTypes"][0]
            self.flags.append(
                {
                    "type": "defaulted",
                    "entity": "formMapping",
                    "name": form_spec["name"],
                    "field": "subjectType",
                    "resolved_to": st["name"],
                    "reason": f"No subject type specified for form '{form_spec['name']}', defaulted to '{st['name']}'",
                }
            )
            logger.warning(
                "formMapping '%s': no subjectType specified, defaulting to '%s'",
                form_spec["name"],
                st["name"],
            )

        # Fallback: if program encounter but no program, try to find a program
        # that targets the same subject type, or fall back to the first program
        if (
            not prog
            and form_type
            in (
                "ProgramEnrolment",
                "ProgramExit",
                "ProgramEncounter",
                "ProgramEncounterCancellation",
            )
            and self.bundle["programs"]
        ):
            # Try matching by subject type
            if st:
                prog = next(
                    (
                        p
                        for p in self.bundle["programs"]
                        if p.get("programSubjectLabel") == st["name"]
                    ),
                    None,
                )
            # Fall back to first program
            if not prog:
                prog = self.bundle["programs"][0]
            self.flags.append(
                {
                    "type": "defaulted",
                    "entity": "formMapping",
                    "name": form_spec["name"],
                    "field": "program",
                    "resolved_to": prog["name"],
                    "reason": f"No program specified for form '{form_spec['name']}' (type {form_type}), defaulted to '{prog['name']}'",
                }
            )
            logger.warning(
                "formMapping '%s': no program specified for %s, defaulting to '%s'",
                form_spec["name"],
                form_type,
                prog["name"],
            )

        # Auto-create missing encounter type when the form type requires one
        needs_et = form_type in (
            "Encounter",
            "IndividualEncounterCancellation",
            "ProgramEncounter",
            "ProgramEncounterCancellation",
        )
        if needs_et and not et:
            et_name = form_spec.get("encounterType") or form_spec["name"]
            # Strip cancellation suffix to get base encounter type name
            et_name = et_name.replace(" Cancellation", "").strip()
            # Check if it already exists (may have been auto-created for a paired form)
            et = next(
                (e for e in self.bundle["encounterTypes"] if e["name"] == et_name),
                None,
            )
            if not et:
                is_program = form_type in (
                    "ProgramEncounter",
                    "ProgramEncounterCancellation",
                )
                et = {
                    "name": et_name,
                    "uuid": generate_deterministic_uuid(f"encounterType:{et_name}"),
                    "encounterEligibilityCheckRule": "",
                    "active": True,
                    "immutable": False,
                    "programEncounter": is_program,
                }
                self.bundle["encounterTypes"].append(et)
                # Also create operational wrapper
                self.bundle["operationalEncounterTypes"][
                    "operationalEncounterTypes"
                ].append(
                    {
                        "uuid": generate_deterministic_uuid(
                            f"operationalEncounterType:{et_name}"
                        ),
                        "name": et_name,
                        "encounterType": {"uuid": et["uuid"], "voided": False},
                        "voided": False,
                    }
                )
                self.flags.append(
                    {
                        "type": "auto_created",
                        "entity": "encounterType",
                        "name": et_name,
                        "reason": f"Form '{form_spec['name']}' (type {form_type}) requires encounter type '{et_name}' but it was not in the entities. Auto-created it. Void if not needed.",
                    }
                )
                logger.info(
                    "formMapping '%s': auto-created encounter type '%s' "
                    "(form type %s requires encounterTypeUUID)",
                    form_spec["name"],
                    et_name,
                    form_type,
                )

        if st:
            mapping["subjectTypeUUID"] = st["uuid"]
        if prog:
            mapping["programUUID"] = prog["uuid"]
        if et:
            mapping["encounterTypeUUID"] = et["uuid"]

        # Deduplicate: Avni rejects duplicate formType+subjectType+program+encounterType
        dup_key = (
            f"{form_type}|{mapping.get('subjectTypeUUID', '')}|"
            f"{mapping.get('programUUID', '')}|{mapping.get('encounterTypeUUID', '')}"
        )
        for existing in self.bundle["formMappings"]:
            existing_key = (
                f"{existing.get('formType', '')}|{existing.get('subjectTypeUUID', '')}|"
                f"{existing.get('programUUID', '')}|{existing.get('encounterTypeUUID', '')}"
            )
            if dup_key == existing_key:
                self.flags.append(
                    {
                        "type": "deduplicated",
                        "entity": "formMapping",
                        "name": form_spec["name"],
                        "reason": (
                            f"Skipped duplicate form mapping '{form_spec['name']}' — "
                            f"same formType+subjectType+program+encounterType as "
                            f"'{existing.get('formName', '?')}'. Void if the wrong one was kept."
                        ),
                    }
                )
                logger.warning(
                    "formMapping '%s': skipped duplicate (same key as '%s')",
                    form_spec["name"],
                    existing.get("formName", "?"),
                )
                return

        self.bundle["formMappings"].append(mapping)

    # ── Auto-derive forms ─────────────────────────────────────────

    def _auto_derive_forms(self, entities: dict) -> list[dict]:
        """
        When no explicit forms are provided, derive form specs from
        subject types, programs, and encounter types so the bundle
        has valid form structures and form mappings.
        """
        forms: list[dict] = []
        encounter_types = entities.get("encounterTypes", [])
        programs = entities.get("programs", [])

        # Build lookup: program name → target subject type
        prog_to_st: dict[str, str] = {}
        for p in programs:
            target = p.get("target_subject_type") or p.get("targetSubjectType", "")
            if target:
                prog_to_st[p["name"]] = target

        # Registration form for each subject type
        for st in entities.get("subjectTypes", []):
            forms.append(
                {
                    "name": f"{st['name']} Registration",
                    "formType": "IndividualProfile",
                    "subjectType": st["name"],
                    "fields": [],
                }
            )

        # Enrolment + exit forms for each program
        for prog in programs:
            st_name = prog_to_st.get(prog["name"], "")
            forms.append(
                {
                    "name": f"{prog['name']} Enrolment",
                    "formType": "ProgramEnrolment",
                    "subjectType": st_name,
                    "program": prog["name"],
                    "fields": [],
                }
            )
            forms.append(
                {
                    "name": f"{prog['name']} Exit",
                    "formType": "ProgramExit",
                    "subjectType": st_name,
                    "program": prog["name"],
                    "fields": [],
                }
            )

        # Form for each encounter type
        for et in encounter_types:
            is_program = et.get(
                "is_program_encounter", et.get("programEncounter", False)
            )
            program_name = et.get("program_name", et.get("program", ""))
            st_name = et.get("subject_type", et.get("subjectType", ""))

            # If program encounter, resolve subject type from program
            if is_program and program_name and not st_name:
                st_name = prog_to_st.get(program_name, "")

            form_type = "ProgramEncounter" if is_program else "Encounter"
            forms.append(
                {
                    "name": f"{et['name']}",
                    "formType": form_type,
                    "subjectType": st_name,
                    "program": program_name if is_program else None,
                    "encounterType": et["name"],
                    "fields": [],
                }
            )

        return forms

    # ── Phase 7: Org config, reports, privileges ────────────────────

    # Standard report card type UUIDs (from production bundles)
    STANDARD_CARD_TYPES: dict[str, dict] = {
        "scheduledVisits": {
            "uuid": "27020b32-c21b-43a4-81bd-7b88ad3a6ef0",
            "color": "#388e3c",
            "label": "Scheduled visits",
        },
        "overdueVisits": {
            "uuid": "9f88bee5-2ab9-4ac4-ae19-d07e9715bdb5",
            "color": "#d32f2f",
            "label": "Overdue visits",
        },
        "total": {
            "uuid": "1fbcadf3-bf1a-439e-9e13-24adddfbf6c0",
            "color": "#ffffff",
            "label": "Total",
        },
        "recentRegistrations": {
            "uuid": "88a7514c-48c0-4d5d-a421-d074e43bb36c",
            "color": "#ffffff",
            "label": "Recent registrations",
            "recentDuration": '{"value":"1","unit":"days"}',
        },
        "recentEnrolments": {
            "uuid": "a5efc04c-317a-4823-a203-e62603454a65",
            "color": "#ffffff",
            "label": "Recent enrolments",
            "recentDuration": '{"value":"1","unit":"days"}',
        },
        "recentVisits": {
            "uuid": "77b5b3fa-de35-4f24-996b-2842492ea6e0",
            "color": "#ffffff",
            "label": "Recent visits",
            "recentDuration": '{"value":"1","unit":"days"}',
        },
    }

    def _generate_organisation_config(self) -> None:
        """Generate default organisationConfig."""
        search_filters = []
        for st in self.bundle["subjectTypes"]:
            for filter_type in ("Name", "Age", "Address", "SearchAll"):
                search_filters.append(
                    {
                        "type": filter_type,
                        "widget": "Default",
                        "titleKey": filter_type,
                        "subjectTypeUUID": st["uuid"],
                    }
                )
        self.bundle["organisationConfig"] = {
            "uuid": generate_deterministic_uuid(f"organisationConfig:{self.org_name}"),
            "settings": {
                "languages": ["en"],
                "customRegistrationLocations": [],
                "saveDrafts": True,
                "showHierarchicalLocation": False,
                "lowestAddressLevelType": [],
                "searchFilters": search_filters,
                "myDashboardFilters": [],
                "searchResultFields": [],
            },
        }

    def _generate_report_cards(self) -> None:
        """Generate standard report cards using known type UUIDs.

        Card names are org-scoped to avoid colliding with Avni's server-default
        card names (report_card_name_unique constraint).
        """
        self._report_card_uuid_by_type: dict[str, str] = {}
        for card_type, card_meta in self.STANDARD_CARD_TYPES.items():
            card_uuid = generate_deterministic_uuid(
                f"reportCard:{self.org_name}:{card_type}"
            )
            self._report_card_uuid_by_type[card_type] = card_uuid
            card: dict[str, Any] = {
                "uuid": card_uuid,
                "name": f"{self.org_name}: {card_meta['label']}",
                "color": card_meta["color"],
                "nested": False,
                "count": 1,
                "standardReportCardType": card_meta["uuid"],
                "standardReportCardInputSubjectTypes": [],
                "standardReportCardInputPrograms": [],
                "standardReportCardInputEncounterTypes": [],
                "voided": False,
            }
            if "recentDuration" in card_meta:
                card["standardReportCardInputRecentDuration"] = card_meta[
                    "recentDuration"
                ]
            self.bundle["reportCards"].append(card)

    def _generate_report_dashboard(self) -> None:
        """Generate a default dashboard with three sections.

        Uses self._report_card_uuid_by_type (keyed by card_type string) instead of
        name-based lookup, so org-scoped card names don't break the mapping.
        """
        dashboard_uuid = generate_deterministic_uuid(
            f"reportDashboard:{self.org_name}:Default Dashboard"
        )
        card_uuid_by_type = getattr(self, "_report_card_uuid_by_type", {})

        def _section(name: str, display_order: float, card_types: list[str]) -> dict:
            section_uuid = generate_deterministic_uuid(
                f"dashboardSection:{self.org_name}:{name}"
            )
            mappings = []
            for idx, card_type in enumerate(card_types, 1):
                card_uuid = card_uuid_by_type.get(card_type)
                if card_uuid:
                    mappings.append(
                        {
                            "uuid": generate_deterministic_uuid(
                                f"sectionCardMapping:{self.org_name}:{name}:{card_type}"
                            ),
                            "displayOrder": float(idx),
                            "dashboardSectionUUID": section_uuid,
                            "reportCardUUID": card_uuid,
                            "voided": False,
                        }
                    )
            return {
                "uuid": section_uuid,
                "name": name,
                "description": "",
                "viewType": "Tile",
                "displayOrder": display_order,
                "dashboardUUID": dashboard_uuid,
                "dashboardSectionCardMappings": mappings,
                "voided": False,
            }

        self.bundle["reportDashboards"].append(
            {
                "uuid": dashboard_uuid,
                "name": "Default Dashboard",
                "sections": [
                    _section(
                        "Visit Details", 1.0, ["scheduledVisits", "overdueVisits"]
                    ),
                    _section(
                        "Recent Statistics",
                        2.0,
                        ["recentRegistrations", "recentEnrolments", "recentVisits"],
                    ),
                    _section("Registration Overview", 3.0, ["total"]),
                ],
                "voided": False,
            }
        )

    def _generate_group_dashboards(self) -> None:
        """Map each group to the default dashboard."""
        if not self.bundle["reportDashboards"]:
            return
        dashboard_uuid = self.bundle["reportDashboards"][0]["uuid"]
        dashboard_name = self.bundle["reportDashboards"][0]["name"]
        for group in self.bundle["groups"]:
            self.bundle["groupDashboards"].append(
                {
                    "uuid": generate_deterministic_uuid(
                        f"groupDashboard:{self.org_name}:{group['name']}:{dashboard_name}"
                    ),
                    "voided": False,
                    "dashboardUUID": dashboard_uuid,
                    "groupUUID": group["uuid"],
                    "groupName": group["name"],
                    "dashboardName": dashboard_name,
                    "dashboardDescription": None,
                    "groupOneOfTheDefaultGroups": group["name"].lower() == "everyone",
                    "primaryDashboard": True,
                    "secondaryDashboard": False,
                }
            )

    # Privilege type UUIDs (from Avni production bundles — stable across orgs)
    PRIVILEGE_TYPES: list[tuple[str, str]] = [
        ("ViewSubject", "67410e50-8b40-4735-bfb4-135b13580027"),
        ("RegisterSubject", "46c3aa38-1ef5-4639-a406-d0b4f9bcb420"),
        ("EditSubject", "db791f27-0c04-4060-8938-6f18fb4069ee"),
        ("VoidSubject", "088a30ca-9ce2-4ab3-a517-e249cc43a4bf"),
        ("AssignSubject", "cac5adae-8d99-4cef-a00b-af7d66e31a09"),
        ("ViewVisit", "9f2a3495-93b7-47c3-8560-d572b6a9fc61"),
        ("ScheduleVisit", "867d5de9-0bf3-434c-9cb1-bd09a05250af"),
        ("PerformVisit", "e3352a23-f478-4166-af11-e949cc69e1cc"),
        ("EditVisit", "85ce5ed4-1490-4980-8c64-63fb423b5f14"),
        ("CancelVisit", "51fa8342-3228-4945-88eb-4b41970fa425"),
        ("VoidVisit", "305d8287-731b-4094-8139-71bc171b242e"),
        ("ApproveSubject", "37ae14f9-e6ac-4d24-951a-e457b0cdcf00"),
        ("ApproveEncounter", "7d725125-6b48-44d2-a53b-bf847ae8a3d0"),
        ("RejectSubject", "8a2e92c2-8af2-4f1c-896e-317c0bb4095f"),
        ("RejectEncounter", "ca4428e7-dc4c-4dad-8190-451d8ccd7402"),
        ("ViewEditEntitiesOnDataEntryApp", "a5899d5a-7a9b-4cba-88dd-20167411787c"),
        ("EditEncounterType", "c814bcf3-4739-48d8-8dae-375df72ee468"),
        ("EditProgram", "fc03c90d-6dd4-4067-9096-4e1b3c800270"),
        ("EditSubjectType", "e491db17-da8a-4ecd-82b1-9cd9921d7c72"),
        ("EditConcept", "f042823e-dbed-44dc-b3d7-a4dd342d883e"),
        ("EditOrganisationConfiguration", "df745841-79e6-4d6e-a04d-f2379449a318"),
        ("UploadMetadataAndData", "2ebe6ce5-77fa-491c-a629-f1fc46d87557"),
        ("DownloadBundle", "ee51fb36-8712-4125-8693-5c524bd75327"),
        ("EditOfflineDashboardAndReportCard", "d8ce88f8-c965-42c9-bed1-1f3a188b25b4"),
        ("EditUserConfiguration", "31c16b7d-825a-4bfa-b961-128846beb3ef"),
        ("EditUserGroup", "78902b7a-7970-4557-9ffa-ce8e93d20e9a"),
    ]

    def _generate_group_privileges(self) -> None:
        """
        Generate privilege matrix: each group × each privilege type.
        Groups with hasAllPrivileges=True get allow=True for all.
        Others default to allow=False (admin can enable in UI).
        """
        for group in self.bundle["groups"]:
            allow_all = group.get("hasAllPrivileges", False)
            for priv_type, priv_uuid in self.PRIVILEGE_TYPES:
                self.bundle["groupPrivileges"].append(
                    {
                        "uuid": generate_deterministic_uuid(
                            f"groupPrivilege:{self.org_name}:{group['name']}:{priv_type}"
                        ),
                        "groupUUID": group["uuid"],
                        "privilegeUUID": priv_uuid,
                        "allow": allow_all,
                        "privilegeType": priv_type,
                        "notEveryoneGroup": group["name"].lower() != "everyone",
                        "voided": False,
                    }
                )

    # ── Validation ──────────────────────────────────────────────────

    def validate(self) -> bool:
        errors: list[str] = []
        warnings: list[str] = []

        # Check form mapping references
        for m in self.bundle["formMappings"]:
            if not m.get("subjectTypeUUID"):
                warnings.append(f'Form mapping "{m["formName"]}" missing subject type')
            if "Program" in m.get("formType", "") and not m.get("programUUID"):
                errors.append(
                    f'Form mapping "{m["formName"]}" missing program reference'
                )

        # Duplicate concept names
        seen_names: set[str] = set()
        for c in self.bundle["concepts"]:
            lower = c["name"].lower()
            if lower in seen_names:
                errors.append(f"Duplicate concept name: {c['name']}")
            seen_names.add(lower)

        # Missing answer UUIDs
        for c in self.bundle["concepts"]:
            if c["dataType"] == "Coded":
                for a in c.get("answers", []):
                    if not a.get("uuid"):
                        errors.append(
                            f'Missing UUID for answer "{a["name"]}" in concept "{c["name"]}"'
                        )

        self.validation = {"errors": errors, "warnings": warnings}
        return len(errors) == 0

    # ── Confidence ──────────────────────────────────────────────────

    def calculate_confidence(self) -> dict:
        concept_conf = self.concept_generator.get_confidence()
        n_forms = len(self.bundle["forms"])
        n_errors = len(self.validation.get("errors", []))
        form_conf = round((n_forms - n_errors) / n_forms, 2) if n_forms > 0 else 0
        overall = round((concept_conf + form_conf) / 2, 2)
        self.confidence = {
            "concepts": concept_conf,
            "forms": form_conf,
            "overall": overall,
            "flaggedItems": len(self.validation.get("warnings", []))
            + len(self.validation.get("errors", [])),
        }
        return self.confidence

    # ── Main entry ──────────────────────────────────────────────────

    def generate(self, entities: dict) -> dict:
        logger.info("Generating bundle for: %s", self.org_name)

        # Normalise snake_case keys to camelCase (idempotent — camelCase passes through)
        _key_map = {
            "subject_types": "subjectTypes",
            "encounter_types": "encounterTypes",
            "address_levels": "addressLevels",
        }
        entities = {_key_map.get(k, k): v for k, v in entities.items()}

        # Validate through EntitySpec before generating — catches duplicates and bad cross-refs
        from ..schemas.bundle_models import EntitySpec as _EntitySpec

        _reverse_map = {
            "subjectTypes": "subject_types",
            "encounterTypes": "encounter_types",
            "addressLevels": "address_levels",
        }
        _norm = {_reverse_map.get(k, k): v for k, v in entities.items()}
        try:
            _EntitySpec(
                subject_types=_norm.get("subject_types", []),
                programs=_norm.get("programs", []),
                encounter_types=_norm.get("encounter_types", []),
                address_levels=_norm.get("address_levels", []),
                groups=_norm.get("groups", []),
            )
        except ValueError as exc:
            logger.warning(
                "BundleGenerator.generate: EntitySpec validation failed: %s", exc
            )
            raise

        # Process in server-expected order
        if entities.get("addressLevels"):
            self.process_address_levels(entities["addressLevels"])
        if entities.get("subjectTypes"):
            self.process_subject_types(entities["subjectTypes"])
        if entities.get("programs"):
            self.process_programs(entities["programs"])
        if entities.get("encounterTypes"):
            self.process_encounter_types(entities["encounterTypes"])

        # Generate operational configs (must come after core entity processing)
        self._generate_operational_configs()

        # Auto-derive forms if none provided
        forms = entities.get("forms", [])
        if not forms:
            forms = self._auto_derive_forms(entities)
            logger.info("Auto-derived %d forms from entities", len(forms))
        self.process_forms(forms)

        if entities.get("groups"):
            self.process_groups(entities["groups"])

        # Phase 7: org config, reports, privileges (deterministic, no LLM needed)
        self._generate_organisation_config()
        self._generate_report_cards()
        self._generate_report_dashboard()
        self._generate_group_dashboards()
        self._generate_group_privileges()

        self.validate()
        self.calculate_confidence()

        return {
            "bundle": self.bundle,
            "validation": self.validation,
            "confidence": self.confidence,
            "flags": self.flags,
        }

    # ── Export to ZIP ────────────────────────────────────────────────

    def to_zip_bytes(self) -> bytes:
        """Create an in-memory ZIP file of the bundle."""
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            # Follow server processing order (BundleZipFileImporter.java)
            # 1. organisationConfig (object)
            if self.bundle["organisationConfig"]:
                zf.writestr(
                    "organisationConfig.json",
                    json.dumps(self.bundle["organisationConfig"], indent=2),
                )

            # 2. Address level types (array)
            zf.writestr(
                "addressLevelTypes.json",
                json.dumps(self.bundle["addressLevelTypes"], indent=2),
            )

            # 3-5. Core entity types (arrays)
            for key in ("subjectTypes", "programs", "encounterTypes"):
                zf.writestr(f"{key}.json", json.dumps(self.bundle[key], indent=2))

            # 6-8. Operational configs (wrapper objects)
            for key in (
                "operationalSubjectTypes",
                "operationalPrograms",
                "operationalEncounterTypes",
            ):
                zf.writestr(f"{key}.json", json.dumps(self.bundle[key], indent=2))

            # 9. Concepts
            zf.writestr("concepts.json", json.dumps(self.bundle["concepts"], indent=2))

            # 10. Forms in subdirectory
            for form in self.bundle["forms"]:
                zf.writestr(f"forms/{form['name']}.json", json.dumps(form, indent=2))

            # 11. Form mappings
            zf.writestr(
                "formMappings.json",
                json.dumps(self.bundle["formMappings"], indent=2),
            )

            # 12. Groups and privileges
            zf.writestr("groups.json", json.dumps(self.bundle["groups"], indent=2))
            zf.writestr(
                "groupPrivilege.json",
                json.dumps(self.bundle["groupPrivileges"], indent=2),
            )

            # 13. Report cards and dashboards
            zf.writestr(
                "reportCard.json",
                json.dumps(self.bundle["reportCards"], indent=2),
            )
            zf.writestr(
                "reportDashboard.json",
                json.dumps(self.bundle["reportDashboards"], indent=2),
            )
            zf.writestr(
                "groupDashboards.json",
                json.dumps(self.bundle["groupDashboards"], indent=2),
            )

            # Validation report (not imported by server, informational only)
            zf.writestr(
                "validation_report.json",
                json.dumps(
                    {
                        "confidence": self.confidence,
                        "validation": self.validation,
                        "summary": {
                            "concepts": len(self.bundle["concepts"]),
                            "forms": len(self.bundle["forms"]),
                            "subjectTypes": len(self.bundle["subjectTypes"]),
                            "programs": len(self.bundle["programs"]),
                            "encounterTypes": len(self.bundle["encounterTypes"]),
                            "formMappings": len(self.bundle["formMappings"]),
                            "addressLevelTypes": len(self.bundle["addressLevelTypes"]),
                            "reportCards": len(self.bundle["reportCards"]),
                            "groupPrivileges": len(self.bundle["groupPrivileges"]),
                        },
                    },
                    indent=2,
                ),
            )

        return buf.getvalue()
