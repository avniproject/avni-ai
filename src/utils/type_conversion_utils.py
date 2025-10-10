"""Utility functions for type conversion, especially dict to dataclass conversion."""

from typing import Dict, Any, Callable, get_type_hints, get_origin, get_args
from dataclasses import is_dataclass


def convert_arguments_for_function(
    func: Callable, arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """Convert dictionary arguments to appropriate types based on function signature.

    This function examines the function's type hints and converts dictionary arguments
    to dataclass instances where the parameter type is a dataclass.

    Args:
        func: The function whose signature will be used for type conversion
        arguments: Dictionary of arguments to convert

    Returns:
        Dictionary with converted arguments where applicable

    Example:
        def my_func(contract: MyDataclass, name: str) -> str:
            return f"{contract.field}: {name}"

        args = {"contract": {"field": "value"}, "name": "test"}
        converted = convert_arguments_for_function(my_func, args)
        # converted["contract"] will be MyDataclass(field="value")
    """
    type_hints = get_type_hints(func)
    converted_args = {}

    for param_name, param_value in arguments.items():
        if param_name in type_hints:
            param_type = type_hints[param_name]

            # If the parameter type is a dataclass and the value is a dict, convert it
            if is_dataclass(param_type) and isinstance(param_value, dict):
                try:
                    converted_args[param_name] = convert_dict_to_dataclass(
                        param_type, param_value
                    )
                except TypeError:
                    # If conversion fails, use the original value and let the function handle the error
                    # This allows for better error messages from the actual function
                    converted_args[param_name] = param_value
            else:
                converted_args[param_name] = param_value
        else:
            # Parameter not in type hints, pass through as-is
            converted_args[param_name] = param_value

    return converted_args


def convert_dict_to_dataclass(dataclass_type: type, data: Dict[str, Any]):
    """Convert a dictionary to a dataclass instance, handling nested dataclasses and lists.

    Args:
        dataclass_type: The dataclass type to convert to
        data: Dictionary containing the data to convert

    Returns:
        Instance of the dataclass

    Raises:
        TypeError: If the dataclass cannot be instantiated with the provided data
        ValueError: If dataclass_type is not actually a dataclass
    """
    if not is_dataclass(dataclass_type):
        raise ValueError(f"{dataclass_type} is not a dataclass")

    # Get type hints for the dataclass fields
    type_hints = get_type_hints(dataclass_type)
    converted_data = {}

    for field_name, field_value in data.items():
        if field_name in type_hints:
            field_type = type_hints[field_name]
            converted_data[field_name] = convert_value_to_type(field_value, field_type)
        else:
            # Field not in type hints, pass through as-is
            converted_data[field_name] = field_value

    # Create the dataclass instance
    return dataclass_type(**converted_data)


def convert_value_to_type(value: Any, target_type: type) -> Any:
    """Convert a value to the target type, handling nested structures.

    Args:
        value: The value to convert
        target_type: The target type to convert to

    Returns:
        Converted value
    """
    # Handle None values
    if value is None:
        return None

    # Get origin type for generic types (List, Optional, etc.)
    origin_type = get_origin(target_type)

    # Handle List types
    if origin_type is list or target_type is list:
        if not isinstance(value, list):
            return value  # Not a list, return as-is

        # Get the list item type
        type_args = get_args(target_type)
        if type_args:
            item_type = type_args[0]
            return [convert_value_to_type(item, item_type) for item in value]
        else:
            return value  # No type args, return as-is

    # Handle dataclass types
    if is_dataclass(target_type) and isinstance(value, dict):
        return convert_dict_to_dataclass(target_type, value)

    # For primitive types or no conversion needed, return as-is
    return value


def is_convertible_to_dataclass(dataclass_type: type, data: Any) -> bool:
    """Check if data can be converted to the specified dataclass type.

    Args:
        dataclass_type: The dataclass type to check against
        data: The data to check

    Returns:
        True if data can be converted to dataclass_type, False otherwise
    """
    if not is_dataclass(dataclass_type) or not isinstance(data, dict):
        return False

    try:
        convert_dict_to_dataclass(dataclass_type, data)
        return True
    except (TypeError, ValueError):
        return False
