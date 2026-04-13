"""
Bulk administration handlers.

Provides endpoints for bulk location and user creation via the AVNI API,
supporting hierarchy-sorted location creation and user provisioning with
catchment/group assignment.

Endpoints:
  POST /bulk-admin/locations  — bulk-create locations in hierarchy order
  POST /bulk-admin/users      — bulk-create users with catchment/group assignment
"""

from __future__ import annotations

import logging
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.uuid_utils import generate_deterministic_uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sort_locations_by_hierarchy(locations: list[dict]) -> list[dict]:
    """
    Sort locations so that parent locations are created before their children.

    Locations are sorted by level descending (highest level = topmost in hierarchy).
    Within the same level, preserves original ordering.
    """
    return sorted(locations, key=lambda loc: loc.get("level", 0), reverse=True)


def _validate_location_hierarchy(locations: list[dict]) -> list[str]:
    """Validate that all parent references resolve within the location set."""
    errors: list[str] = []
    name_set = {loc.get("name", "") for loc in locations if isinstance(loc, dict)}

    for loc in locations:
        if not isinstance(loc, dict):
            continue
        parent = loc.get("parent", "")
        if parent and parent not in name_set:
            errors.append(
                f"Location '{loc.get('name')}' references parent '{parent}' "
                "which is not in the location set"
            )
        if not loc.get("name"):
            errors.append("Location entry missing 'name' field")
        if not loc.get("type"):
            errors.append(
                f"Location '{loc.get('name', '?')}' missing 'type' field "
                "(e.g. 'State', 'District')"
            )

    return errors


def _validate_users(users: list[dict]) -> list[str]:
    """Validate user entries before bulk creation."""
    errors: list[str] = []

    for idx, user in enumerate(users):
        if not isinstance(user, dict):
            errors.append(f"User at index {idx} is not an object")
            continue
        if not user.get("username"):
            errors.append(f"User at index {idx} missing 'username'")
        if not user.get("name"):
            errors.append(f"User at index {idx} missing 'name'")

    return errors


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_bulk_locations(request: Request) -> JSONResponse:
    """
    POST /bulk-admin/locations
    Body: {
        "conversation_id": "...",
        "locations": [
            {"name": "Karnataka", "type": "State", "level": 4},
            {"name": "Bangalore", "type": "District", "level": 3, "parent": "Karnataka"},
            ...
        ]
    }
    Validates and sorts locations by hierarchy, then returns them in
    creation order with generated UUIDs. The caller (agent) can then
    use the AVNI admin API to create each location in order.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    locations = body.get("locations", [])

    if not isinstance(locations, list):
        return JSONResponse(
            {"error": "'locations' must be an array"}, status_code=400
        )
    if not locations:
        return JSONResponse(
            {"error": "No locations provided"}, status_code=400
        )

    # Validate hierarchy
    validation_errors = _validate_location_hierarchy(locations)
    if validation_errors:
        return JSONResponse(
            {
                "error": "Location validation failed",
                "validation_errors": validation_errors,
            },
            status_code=422,
        )

    # Sort by hierarchy
    sorted_locations = _sort_locations_by_hierarchy(locations)

    # Assign UUIDs
    results: list[dict] = []
    name_to_uuid: dict[str, str] = {}

    for loc in sorted_locations:
        loc_name = loc.get("name", "")
        loc_uuid = generate_deterministic_uuid(f"location:{loc_name}")
        name_to_uuid[loc_name] = loc_uuid

        entry: dict[str, Any] = {
            "name": loc_name,
            "type": loc.get("type", ""),
            "level": loc.get("level", 1),
            "uuid": loc_uuid,
        }

        parent_name = loc.get("parent", "")
        if parent_name and parent_name in name_to_uuid:
            entry["parentUuid"] = name_to_uuid[parent_name]
            entry["parent"] = parent_name

        # Copy any extra properties
        for key in ("properties", "lineage", "title"):
            if key in loc:
                entry[key] = loc[key]

        results.append(entry)

    logger.info(
        "bulk-admin/locations: prepared %d locations in hierarchy order",
        len(results),
    )
    return JSONResponse(
        {
            "ok": True,
            "locations": results,
            "location_count": len(results),
            "creation_order": [r["name"] for r in results],
        }
    )


async def handle_bulk_users(request: Request) -> JSONResponse:
    """
    POST /bulk-admin/users
    Body: {
        "conversation_id": "...",
        "users": [
            {
                "username": "field_worker_1",
                "name": "Field Worker 1",
                "email": "fw1@example.com",
                "phone": "9876543210",
                "catchment": "Block A",
                "groups": ["Everyone"],
                "language": "en",
                "operating_scope": "ByDistrict"
            }
        ]
    }
    Validates user entries and prepares them for creation with UUIDs,
    catchment references, and group assignments.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    users = body.get("users", [])

    if not isinstance(users, list):
        return JSONResponse({"error": "'users' must be an array"}, status_code=400)
    if not users:
        return JSONResponse({"error": "No users provided"}, status_code=400)

    # Validate
    validation_errors = _validate_users(users)
    if validation_errors:
        return JSONResponse(
            {
                "error": "User validation failed",
                "validation_errors": validation_errors,
            },
            status_code=422,
        )

    results: list[dict] = []
    for user in users:
        if not isinstance(user, dict):
            continue

        username = user.get("username", "")
        user_uuid = generate_deterministic_uuid(f"user:{username}")

        entry: dict[str, Any] = {
            "uuid": user_uuid,
            "username": username,
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "phoneNumber": user.get("phone", ""),
            "language": user.get("language", "en"),
            "operatingIndividualScope": user.get(
                "operating_scope", "ByDistrict"
            ),
        }

        # Catchment assignment
        catchment = user.get("catchment", "")
        if catchment:
            entry["catchment"] = {
                "name": catchment,
                "uuid": generate_deterministic_uuid(f"catchment:{catchment}"),
            }

        # Group assignment
        groups = user.get("groups", [])
        if isinstance(groups, list):
            entry["groups"] = [
                {
                    "name": g,
                    "uuid": generate_deterministic_uuid(f"group:{g}"),
                }
                for g in groups
                if isinstance(g, str)
            ]

        results.append(entry)

    logger.info(
        "bulk-admin/users: prepared %d user(s) for creation",
        len(results),
    )
    return JSONResponse(
        {
            "ok": True,
            "users": results,
            "user_count": len(results),
        }
    )
