from typing import Any, Dict, Optional
from ..clients.avni_client import ApiResult


def format_error_message(result: ApiResult, operation: str) -> str:
    return f"Failed to {operation}: {result.error}"


def format_empty_message(resource: str) -> str:
    return f"No {resource} found."


def format_list_response(
    items,
    id_key: str = "id",
    name_key: str = "name",
    extra_key: Optional[str] = None,
) -> str:
    if isinstance(items, dict):
        if "content" in items:
            items = items["content"]
        elif "page" in items and not items.get("content"):
            page_info = items["page"]
            total = page_info.get("totalElements", 0)
            if total == 0:
                return "No items found."
            else:
                return f"Found {total} items but no content returned."
        else:
            # If it's a dict but not paginated, treat as single item
            items = [items]

    if not items:
        return "No items found."

    result = []
    for item in items:
        if isinstance(item, str):
            line = item
        else:
            line = f"ID: {item.get(id_key)}, Name: {item.get(name_key)}"
            if extra_key and extra_key in item:
                value = item.get(extra_key)
                if isinstance(value, float):
                    line += f", {extra_key.title()}: {value:.1f}"
                else:
                    line += f", {extra_key.title()}: {value}"
        result.append(line)

    return "\n".join(result)


def format_creation_response(
    resource: str, name: str, id_field: str, response_data: Dict[str, Any]
) -> str:
    id_value = response_data.get(id_field)
    return (
        f"{resource} '{name}' created successfully with {id_field.upper()} {id_value}"
    )


def format_update_response(
    resource: str, name: str, id_field: str, response_data: Dict[str, Any]
) -> str:
    id_value = response_data.get(id_field)
    return (
        f"{resource} '{name}' updated successfully with {id_field.upper()} {id_value}"
    )


def format_deletion_response(resource: str, resource_id: Any) -> str:
    return f"{resource} with ID {resource_id} successfully deleted (voided)"


def format_validation_error(operation: str, error_message: str) -> str:
    return f"Failed to {operation}: {error_message}"


def format_implementation_deletion_response(
    delete_metadata: bool = True, delete_admin_config: bool = True
) -> str:
    deleted_items = []

    if delete_metadata:
        deleted_items.append(
            "app designer config (subject types, programs, encounters)"
        )

    if delete_admin_config:
        deleted_items.append(
            "admin configuration (location types, locations, catchments)"
        )

    if not deleted_items:
        return "No items were selected for deletion"

    items_text = " and ".join(deleted_items)
    return f"✅ Implementation successfully cleared: {items_text}. Your Avni workspace is now ready for a fresh configuration."
