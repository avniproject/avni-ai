"""Tool registry for direct function calling with OpenAI."""

import inspect
from typing import Dict, List, Any, Callable, get_type_hints
from dataclasses import dataclass

from ..utils.schema_utils import type_to_json_schema
from ..utils.type_conversion_utils import convert_arguments_for_function


@dataclass
class ToolDefinition:
    """Definition of a tool for OpenAI function calling."""

    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]


class ToolRegistry:
    """Registry for managing tools that can be called directly."""

    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}

    def register_tool(
        self, func: Callable, name: str = None, description: str = None
    ) -> None:
        """Register a tool function for direct calling."""
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Execute {tool_name}"

        # Extract function signature and create OpenAI function schema
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        parameters = {"type": "object", "properties": {}, "required": []}

        for param_name, param in sig.parameters.items():
            # Skip auth_token as it's automatically injected
            if param_name == "auth_token":
                continue

            param_type = type_hints.get(param_name, str)

            # Convert Python type to JSON schema using utility function
            param_schema = type_to_json_schema(param_type)

            # Add description
            param_schema["description"] = f"Parameter {param_name}"

            parameters["properties"][param_name] = param_schema

            # Mark as required if no default value
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
        """Get tools in OpenAI function calling format.

        Args:
            filter_tools: List of tool names to include. If None, returns all tools.
        """
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
        """Call a registered tool with the given arguments."""
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


# Global tool registry instance
tool_registry = ToolRegistry()
