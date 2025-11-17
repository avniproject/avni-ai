import inspect
from typing import (
    Dict,
    List,
    Any,
    Callable,
    get_type_hints,
    get_origin,
    get_args,
    Union,
)
from dataclasses import dataclass, is_dataclass, fields, MISSING


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


@dataclass
class ToolDefinition:
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}

    def register_tool(
        self, func: Callable, name: str = None, description: str = None
    ) -> None:
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Execute {tool_name}"

        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        parameters = {"type": "object", "properties": {}, "required": []}

        for param_name, param in sig.parameters.items():
            # Skip auth_token as it's automatically injected
            if param_name == "auth_token":
                continue

            param_type = type_hints.get(param_name, str)

            param_schema = type_to_json_schema(param_type)

            param_schema["description"] = f"Parameter {param_name}"

            parameters["properties"][param_name] = param_schema

            if param.default == inspect.Parameter.empty:
                parameters["required"].append(param_name)

        tool_def = ToolDefinition(
            name=tool_name,
            description=tool_description,
            function=func,
            parameters=parameters,
        )

        self.tools[tool_name] = tool_def

    def get_openai_tools(self, filter_tools: List[str] = None) -> List[Dict[str, Any]]:
        tools_to_include = self.tools.values()
        if filter_tools:
            tools_to_include = [
                tool for tool in self.tools.values() if tool.name in filter_tools
            ]

        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                },
            }
            for tool in tools_to_include
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        tool = self.tools[tool_name]

        # Convert dictionary arguments to dataclass instances where needed
        converted_args = convert_arguments_for_function(tool.function, arguments)

        # Call the function with the converted arguments
        if inspect.iscoroutinefunction(tool.function):
            return await tool.function(**converted_args)
        else:
            return tool.function(**converted_args)

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self.tools.keys())


# Global tool registry instance (singleton pattern)
tool_registry = ToolRegistry()
