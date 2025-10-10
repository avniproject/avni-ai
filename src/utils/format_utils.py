"""Data formatting utilities for Avni MCP Server."""

from typing import Any, Dict, Optional


def format_list_response(
    items,
    id_key: str = "id",
    name_key: str = "name",
    extra_key: Optional[str] = None,
) -> str:
    """Format a list of items into a readable string response.

    Args:
        items: List of dictionary items or paginated response object
        id_key: Key for ID field
        name_key: Key for name field
        extra_key: Optional extra field to include
    """
    # Handle paginated response - extract content array if it exists
    if isinstance(items, dict):
        if "content" in items:
            items = items["content"]
        elif "page" in items and not items.get("content"):
            # Handle empty paginated response
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
        # Handle both string items and dictionary items
        if isinstance(item, str):
            # If item is a string, just return it as-is
            line = item
        else:
            # If item is a dictionary, extract fields
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
    """Format creation success response.

    Args:
        resource: Type of resource created (e.g., "Organization", "User")
        name: Name of the created resource
        id_field: Field name for the ID (e.g., "id", "uuid")
        response_data: API response data
    """
    id_value = response_data.get(id_field)
    return (
        f"{resource} '{name}' created successfully with {id_field.upper()} {id_value}"
    )
