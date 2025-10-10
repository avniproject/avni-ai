"""Utility functions for JSON schema conversion."""

from typing import Dict, Any, get_origin, get_args, Union
from dataclasses import fields, is_dataclass, MISSING


def dataclass_to_json_schema(dataclass_type: type) -> Dict[str, Any]:
    """Convert a dataclass to JSON schema format.

    Args:
        dataclass_type: The dataclass type to convert

    Returns:
        JSON schema dictionary for the dataclass
    """
    if not is_dataclass(dataclass_type):
        return {"type": "object"}

    schema = {"type": "object", "properties": {}, "required": []}

    for field in fields(dataclass_type):
        field_schema = type_to_json_schema(field.type)
        schema["properties"][field.name] = field_schema

        # Mark as required if no default value and not Optional
        if field.default == field.default_factory == MISSING:
            # Check if it's Optional (Union with None)
            origin = get_origin(field.type)
            if origin is Union:
                args = get_args(field.type)
                if type(None) not in args:
                    schema["required"].append(field.name)
            else:
                schema["required"].append(field.name)

    return schema


def type_to_json_schema(param_type: type) -> Dict[str, Any]:
    """Convert a Python type to JSON schema format.

    Args:
        param_type: The Python type to convert

    Returns:
        JSON schema dictionary for the type
    """
    # Handle Optional types (Union[X, None])
    origin = get_origin(param_type)
    if origin is Union:
        args = get_args(param_type)
        if len(args) == 2 and type(None) in args:
            # This is Optional[X]
            non_none_type = args[0] if args[1] is type(None) else args[1]
            return type_to_json_schema(non_none_type)

    # Handle List types
    if origin is list or param_type is list:
        if origin is list:
            args = get_args(param_type)
            if args:
                item_schema = type_to_json_schema(args[0])
                return {"type": "array", "items": item_schema}
        return {"type": "array", "items": {"type": "string"}}

    # Handle Dict types
    if origin is dict or param_type is dict:
        return {"type": "object"}

    # Handle dataclass types
    if is_dataclass(param_type):
        return dataclass_to_json_schema(param_type)

    # Handle primitive types
    if param_type is str:
        return {"type": "string"}
    elif param_type is int:
        return {"type": "integer"}
    elif param_type is float:
        return {"type": "number"}
    elif param_type is bool:
        return {"type": "boolean"}
    else:
        # Default fallback
        return {"type": "string"}
