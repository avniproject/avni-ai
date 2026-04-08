"""HTTP handlers for admin endpoints: location types, locations, catchments, users, implementation."""

import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..tools.admin.addressleveltypes import (
    create_location_type,
    update_location_type,
    delete_location_type,
)
from ..tools.admin.locations import (
    get_locations,
    create_location,
    update_location,
    delete_location,
)
from ..tools.admin.catchments import (
    get_catchments,
    create_catchment,
    update_catchment,
    delete_catchment,
)
from ..tools.admin.users import find_user, update_user
from ..tools.implementation.implementations import delete_implementation

from ..schemas.address_level_type_contract import (
    AddressLevelTypeContract,
    AddressLevelTypeUpdateContract,
    AddressLevelTypeDeleteContract,
)
from ..schemas.location_contract import (
    LocationContract,
    LocationUpdateContract,
    LocationDeleteContract,
    LocationParent,
)
from ..schemas.catchment_contract import (
    CatchmentContract,
    CatchmentUpdateContract,
    CatchmentDeleteContract,
)
from ..schemas.user_contract import UserFindContract, UserUpdateContract
from ..schemas.implementation_contract import ImplementationDeleteContract

logger = logging.getLogger(__name__)


def _get_auth_token(request: Request, body: dict | None = None) -> str | None:
    from ..auth_store import resolve_auth_token
    return resolve_auth_token(request, body)


def _auth_error() -> JSONResponse:
    return JSONResponse(
        {"error": "Missing auth: provide avni-auth-token header or conversation_id"},
        status_code=401,
    )


def _error_response(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse({"error": message}, status_code=status_code)


# --- Location Types ---


async def handle_create_location_type(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        contract = AddressLevelTypeContract(**body)
        result = await create_location_type(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error creating location type: {e}")
        return _error_response(str(e), 500)


async def handle_update_location_type(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        contract = AddressLevelTypeUpdateContract(**body)
        result = await update_location_type(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error updating location type: {e}")
        return _error_response(str(e), 500)


async def handle_delete_location_type(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        id_ = int(request.path_params["id"])
        contract = AddressLevelTypeDeleteContract(id=id_)
        result = await delete_location_type(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error deleting location type: {e}")
        return _error_response(str(e), 500)


# --- Locations ---


async def handle_get_locations(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        result = await get_locations(auth_token)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        return _error_response(str(e), 500)


async def handle_create_location(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        parents = [LocationParent(**p) for p in body.pop("parents", [])]
        contract = LocationContract(**body, parents=parents)
        result = await create_location(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error creating location: {e}")
        return _error_response(str(e), 500)


async def handle_update_location(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        contract = LocationUpdateContract(**body)
        result = await update_location(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error updating location: {e}")
        return _error_response(str(e), 500)


async def handle_delete_location(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        id_ = int(request.path_params["id"])
        contract = LocationDeleteContract(id=id_)
        result = await delete_location(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error deleting location: {e}")
        return _error_response(str(e), 500)


# --- Catchments ---


async def handle_get_catchments(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        result = await get_catchments(auth_token)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error fetching catchments: {e}")
        return _error_response(str(e), 500)


async def handle_create_catchment(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        contract = CatchmentContract(**body)
        result = await create_catchment(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error creating catchment: {e}")
        return _error_response(str(e), 500)


async def handle_update_catchment(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        contract = CatchmentUpdateContract(**body)
        result = await update_catchment(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error updating catchment: {e}")
        return _error_response(str(e), 500)


async def handle_delete_catchment(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        id_ = int(request.path_params["id"])
        contract = CatchmentDeleteContract(id=id_)
        result = await delete_catchment(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error deleting catchment: {e}")
        return _error_response(str(e), 500)


# --- Users ---


async def handle_find_user(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        name = request.query_params.get("name")
        if not name:
            return _error_response("'name' query parameter is required")
        contract = UserFindContract(name=name)
        result = await find_user(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error finding user: {e}")
        return _error_response(str(e), 500)


async def handle_update_user(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        contract = UserUpdateContract(**body)
        result = await update_user(auth_token, contract)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return _error_response(str(e), 500)


# --- Implementation ---


async def handle_delete_implementation(request: Request) -> JSONResponse:
    auth_token = _get_auth_token(request)
    if not auth_token:
        return _auth_error()
    try:
        body = await request.json()
        contract = ImplementationDeleteContract(**body)
        result = await delete_implementation(contract, auth_token)
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error deleting implementation: {e}")
        return _error_response(str(e), 500)
