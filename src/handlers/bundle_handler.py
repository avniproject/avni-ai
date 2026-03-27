import logging
import os

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..tools.bundle.models import (
    ParsedEntities,
    ParsedEncounter,
    ParsedLocationHierarchy,
    ParsedLocationLevel,
    ParsedProgram,
    ParsedSubjectType,
)
from ..tools.bundle.bundle_generator import generate_bundle
from ..tools.bundle import asset_store
from ..tools.bundle.bundle_uploader import upload_bundle
from .request import EntitiesData, GenerateBundleRequest
from .response import BundleSummary, GenerateBundleResponse

logger = logging.getLogger(__name__)

def _resource_to_parsed_entities(entities: EntitiesData) -> ParsedEntities:
    parsed = ParsedEntities()

    for row in entities.subject_types:
        parsed.subject_types.append(ParsedSubjectType.from_dict(row))

    for row in entities.programs:
        parsed.programs.append(ParsedProgram.from_dict(row))

    for row in entities.encounter_types:
        enc = ParsedEncounter.from_dict(row)
        if enc.is_program_encounter:
            parsed.program_encounters.append(enc)
        else:
            parsed.encounters.append(enc)

    if entities.address_levels:
        parsed.location_hierarchies.append(ParsedLocationHierarchy(
            levels=[ParsedLocationLevel.from_dict(row) for row in entities.address_levels]
        ))

    return parsed

async def generate_bundle_request(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        req = GenerateBundleRequest.from_body(body)

        error = req.validate()
        if error:
            return JSONResponse({"error": error}, status_code=400)

        auth_token = request.headers.get("avni-auth-token", "")
        if not auth_token:
            return JSONResponse(
                {"error": "avni-auth-token header is required"},
                status_code=401,
            )

        parsed_entities = _resource_to_parsed_entities(req.entities)
        logger.info(
            f"Rebuilt entities: {len(parsed_entities.subject_types)} subject types, "
            f"{len(parsed_entities.programs)} programs, "
            f"{len(parsed_entities.encounters) + len(parsed_entities.program_encounters)} encounters"
        )

        bundle = generate_bundle(parsed_entities, org_name=req.org_name)
        assets = bundle.to_asset_dict()

        session_id = await asset_store.create_session(req.org_name)

        entities_dict = {
            "subject_types": req.entities.subject_types,
            "programs": req.entities.programs,
            "encounter_types": req.entities.encounter_types,
            "address_levels": req.entities.address_levels,
        }
        await asset_store.store_jsonl(session_id, "entities", [entities_dict])

        for filename, content in assets.items():
            await asset_store.store_asset(session_id, filename, content)

        await asset_store.update_session_status(session_id, "bundle_generated")
        logger.info(f"Bundle stored in session {session_id}")

        upload_result = await upload_bundle(
            bundle, auth_token=auth_token,
            base_url=os.getenv("AVNI_BASE_URL", ""),
        )
        await asset_store.add_upload_record(session_id, upload_result)
        logger.info(f"Upload result: {upload_result.get('success')}")

        response = GenerateBundleResponse(
            session_id=session_id,
            status="uploaded" if upload_result.get("success") else "bundle_generated",
            bundle_summary=BundleSummary(
                subject_types=len(bundle.subject_types),
                programs=len(bundle.programs),
                encounter_types=len(bundle.encounter_types),
                address_level_types=len(bundle.address_level_types),
                form_mappings=len(bundle.form_mappings),
            ),
            upload_result=upload_result,
        )
        return JSONResponse(response.to_dict())

    except Exception as e:
        logger.error(f"Bundle generation error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return JSONResponse({"error": str(e)}, status_code=500)


async def get_bundle_status(request: Request) -> JSONResponse:
    try:
        session_id = request.path_params["session_id"]
        session = await asset_store.get_session(session_id)

        if not session:
            return JSONResponse(
                {"error": f"Session {session_id} not found"},
                status_code=404,
            )

        return JSONResponse({
            "session_id": session["session_id"],
            "org": session["org"],
            "status": session["status"],
            "version": session.get("version", 0),
            "created_at": session["created_at"].isoformat() if session.get("created_at") else None,
            "updated_at": session["updated_at"].isoformat() if session.get("updated_at") else None,
            "asset_names": list(session.get("assets", {}).keys()),
            "upload_history": session.get("upload_history", []),
        })

    except Exception as e:
        logger.error(f"Bundle status error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
