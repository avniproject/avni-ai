"""
Chat-based SRS session handlers.

Provides a multi-step conversational flow for building an AVNI configuration
through guided section-by-section data collection, with sector-aware defaults
and cross-validation between sections.

Endpoints:
  POST /chat-srs/init-session    — create a new chat SRS session
  POST /chat-srs/update-section  — update a specific section with data
  POST /chat-srs/build-entities  — transform completed sections into entities
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..utils.sector_templates import (
    get_sector_defaults,
    get_sector_form_fields,
    get_available_sectors,
    detect_sector,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Session data model
# ---------------------------------------------------------------------------

VALID_SECTIONS = [
    "org_info",
    "subject_types",
    "programs",
    "encounter_types",
    "address_levels",
    "groups",
    "forms",
    "rules",
    "reports",
    "users",
]


@dataclass
class ChatSrsSession:
    conversation_id: str
    sector: str = ""
    org_name: str = ""
    is_new_org: bool = True
    current_section: str = "org_info"
    completed_sections: list[str] = field(default_factory=list)
    section_data: dict[str, Any] = field(default_factory=dict)
    sector_defaults: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


# ---------------------------------------------------------------------------
# In-memory session store (TTL = 6 hours)
# ---------------------------------------------------------------------------
_SESSION_STORE_TTL = int(os.getenv("ENTITY_STORE_TTL_HOURS", "6")) * 3600


class _ChatSrsSessionStore:
    def __init__(self) -> None:
        self._store: dict[str, tuple[ChatSrsSession, float]] = {}

    def put(self, conversation_id: str, session: ChatSrsSession) -> None:
        self._store[conversation_id] = (
            session,
            time.time() + _SESSION_STORE_TTL,
        )

    def get(self, conversation_id: str) -> ChatSrsSession | None:
        entry = self._store.get(conversation_id)
        if entry is None:
            return None
        session, expiry = entry
        if time.time() > expiry:
            del self._store[conversation_id]
            return None
        return session

    def cleanup(self) -> int:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)


_session_store = _ChatSrsSessionStore()


def get_chat_srs_session_store() -> _ChatSrsSessionStore:
    """Return the global chat SRS session store."""
    return _session_store


# ---------------------------------------------------------------------------
# Cross-validation helpers
# ---------------------------------------------------------------------------


def _cross_validate(section: str, data: Any, session: ChatSrsSession) -> list[str]:
    """Run cross-section validation checks. Returns a list of warning strings."""
    warnings: list[str] = []

    if section == "encounter_types" and isinstance(data, list):
        program_names = {
            p.get("name", "").lower()
            for p in session.section_data.get("programs", [])
            if isinstance(p, dict)
        }
        subject_type_names = {
            s.get("name", "").lower()
            for s in session.section_data.get("subject_types", [])
            if isinstance(s, dict)
        }
        for et in data:
            if not isinstance(et, dict):
                continue
            if et.get("is_program_encounter"):
                pn = (et.get("program_name") or "").lower()
                if pn and pn not in program_names:
                    warnings.append(
                        f"Encounter '{et.get('name')}' references program "
                        f"'{et.get('program_name')}' which is not yet defined."
                    )
            else:
                st = (et.get("subject_type") or "").lower()
                if st and st not in subject_type_names:
                    warnings.append(
                        f"Encounter '{et.get('name')}' references subject type "
                        f"'{et.get('subject_type')}' which is not yet defined."
                    )

    if section == "programs" and isinstance(data, list):
        subject_type_names = {
            s.get("name", "").lower()
            for s in session.section_data.get("subject_types", [])
            if isinstance(s, dict)
        }
        for prog in data:
            if not isinstance(prog, dict):
                continue
            target = (prog.get("target_subject_type") or "").lower()
            if target and target not in subject_type_names:
                warnings.append(
                    f"Program '{prog.get('name')}' targets subject type "
                    f"'{prog.get('target_subject_type')}' which is not yet defined."
                )

    return warnings


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_init_session(request: Request) -> JSONResponse:
    """
    POST /chat-srs/init-session
    Body: { "conversation_id": "...", "sector": "MCH", "org_name": "...", "is_new_org": true }
    Creates a new chat SRS session with sector defaults pre-loaded.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)

    # Check for existing session
    existing = _session_store.get(conversation_id)
    if existing is not None:
        return JSONResponse(
            {
                "error": f"Session already exists for conversation_id={conversation_id}. "
                "Use update-section to modify it."
            },
            status_code=409,
        )

    sector = body.get("sector", "")
    org_name = body.get("org_name", "")
    is_new_org = body.get("is_new_org", True)

    # Auto-detect sector from description if not explicitly provided
    if not sector:
        description = body.get("description", "")
        sector = detect_sector(description) or ""

    sector_defaults = get_sector_defaults(sector) if sector else {}

    session = ChatSrsSession(
        conversation_id=conversation_id,
        sector=sector,
        org_name=org_name,
        is_new_org=is_new_org,
        sector_defaults=sector_defaults,
    )
    _session_store.put(conversation_id, session)

    logger.info(
        "chat-srs/init-session: created session for conversation_id=%s sector=%s",
        conversation_id,
        sector or "(none)",
    )
    return JSONResponse(
        {
            "ok": True,
            "conversation_id": conversation_id,
            "sector": sector,
            "available_sectors": get_available_sectors(),
            "has_defaults": bool(sector_defaults),
            "sections": VALID_SECTIONS,
            "current_section": session.current_section,
        }
    )


async def handle_update_section(request: Request) -> JSONResponse:
    """
    POST /chat-srs/update-section
    Body: { "conversation_id": "...", "section": "subject_types", "data": [...] }
    Updates a specific section of the chat SRS session and runs cross-validation.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    section = body.get("section")
    data = body.get("data")

    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)
    if not section:
        return JSONResponse({"error": "Missing 'section'"}, status_code=400)
    if section not in VALID_SECTIONS:
        return JSONResponse(
            {
                "error": f"Invalid section '{section}'. "
                f"Valid sections: {VALID_SECTIONS}"
            },
            status_code=400,
        )

    session = _session_store.get(conversation_id)
    if session is None:
        return JSONResponse(
            {
                "error": f"No session found for conversation_id={conversation_id}. "
                "Call /chat-srs/init-session first."
            },
            status_code=404,
        )

    # Run cross-validation before accepting the data
    warnings = _cross_validate(section, data, session)

    # Store section data
    session.section_data[section] = data
    if section not in session.completed_sections:
        session.completed_sections.append(section)

    # Advance current_section to the next incomplete section
    for s in VALID_SECTIONS:
        if s not in session.completed_sections:
            session.current_section = s
            break
    else:
        session.current_section = "complete"

    _session_store.put(conversation_id, session)

    logger.info(
        "chat-srs/update-section: updated section=%s for conversation_id=%s warnings=%d",
        section,
        conversation_id,
        len(warnings),
    )
    return JSONResponse(
        {
            "ok": True,
            "section": section,
            "current_section": session.current_section,
            "completed_sections": session.completed_sections,
            "remaining_sections": [
                s for s in VALID_SECTIONS if s not in session.completed_sections
            ],
            "warnings": warnings,
            "progress": f"{len(session.completed_sections)}/{len(VALID_SECTIONS)}",
        }
    )


async def handle_build_entities(request: Request) -> JSONResponse:
    """
    POST /chat-srs/build-entities
    Body: { "conversation_id": "..." }
    Transforms completed sections into the standard entities dict that can
    be fed into the bundle generator. Auto-generates forms from encounter types
    and sector-specific field templates.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)

    session = _session_store.get(conversation_id)
    if session is None:
        return JSONResponse(
            {
                "error": f"No session found for conversation_id={conversation_id}. "
                "Call /chat-srs/init-session first."
            },
            status_code=404,
        )

    sd = session.section_data

    # Build entities from section data
    entities: dict[str, Any] = {
        "subject_types": sd.get("subject_types", []),
        "programs": sd.get("programs", []),
        "encounter_types": sd.get("encounter_types", []),
        "address_levels": sd.get("address_levels", []),
        "groups": sd.get("groups", []),
    }

    # Fall back to sector defaults for any missing sections
    if session.sector_defaults:
        for key in ("subject_types", "programs", "encounter_types", "address_levels", "groups"):
            if not entities.get(key):
                entities[key] = session.sector_defaults.get(key, [])

    # Auto-generate forms from encounter types + sector fields
    forms: list[dict] = sd.get("forms", [])
    if not forms:
        forms = _auto_generate_forms(entities, session.sector)
    entities["forms"] = forms

    logger.info(
        "chat-srs/build-entities: built entities for conversation_id=%s "
        "st=%d prog=%d enc=%d forms=%d",
        conversation_id,
        len(entities.get("subject_types", [])),
        len(entities.get("programs", [])),
        len(entities.get("encounter_types", [])),
        len(forms),
    )
    return JSONResponse(
        {
            "ok": True,
            "entities": entities,
            "entity_counts": {
                k: len(v) if isinstance(v, list) else 1
                for k, v in entities.items()
            },
            "completed_sections": session.completed_sections,
            "sector": session.sector,
        }
    )


def _auto_generate_forms(entities: dict, sector: str) -> list[dict]:
    """
    Auto-generate form specs from encounter types, using sector-specific
    field templates where available.
    """
    forms: list[dict] = []
    encounter_types = entities.get("encounter_types", [])
    programs = entities.get("programs", [])

    # Build program -> subject type map
    prog_to_st: dict[str, str] = {}
    for p in programs:
        if isinstance(p, dict):
            target = p.get("target_subject_type", "")
            if target:
                prog_to_st[p.get("name", "")] = target

    # Registration forms
    for st in entities.get("subject_types", []):
        if isinstance(st, dict) and st.get("name"):
            forms.append(
                {
                    "name": f"{st['name']} Registration",
                    "formType": "IndividualProfile",
                    "subjectType": st["name"],
                    "fields": [],
                }
            )

    # Enrolment forms
    for prog in programs:
        if not isinstance(prog, dict):
            continue
        st_name = prog_to_st.get(prog.get("name", ""), "")
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

    # Encounter forms with sector-specific fields
    for et in encounter_types:
        if not isinstance(et, dict):
            continue
        et_name = et.get("name", "")
        is_program = et.get("is_program_encounter", False)
        program_name = et.get("program_name", "")
        st_name = et.get("subject_type", "")

        if is_program and program_name and not st_name:
            st_name = prog_to_st.get(program_name, "")

        # Try to get sector-specific fields
        fields = get_sector_form_fields(sector, et_name) if sector else []

        form_type = "ProgramEncounter" if is_program else "Encounter"
        forms.append(
            {
                "name": et_name,
                "formType": form_type,
                "subjectType": st_name,
                "program": program_name if is_program else None,
                "encounterType": et_name,
                "fields": fields,
            }
        )

    return forms
