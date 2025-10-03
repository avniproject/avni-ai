"""Tool registry for direct function calling with OpenAI."""

import inspect
from typing import Dict, List, Any, Callable, get_type_hints
from dataclasses import dataclass
import json


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
    
    def register_tool(self, func: Callable, name: str = None, description: str = None) -> None:
        """Register a tool function for direct calling."""
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Execute {tool_name}"
        
        # Extract function signature and create OpenAI function schema
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in sig.parameters.items():
            # Skip auth_token as it's automatically injected
            if param_name == "auth_token":
                continue
                
            param_type = type_hints.get(param_name, str)
            
            # Convert Python types to JSON schema types
            if param_type == str:
                json_type = "string"
            elif param_type == int:
                json_type = "integer"
            elif param_type == float:
                json_type = "number"
            elif param_type == bool:
                json_type = "boolean"
            elif param_type == list or param_type == List:
                json_type = "array"
            elif param_type == dict or param_type == Dict:
                json_type = "object"
            else:
                json_type = "string"  # Default fallback
            
            parameters["properties"][param_name] = {
                "type": json_type,
                "description": f"Parameter {param_name}"
            }
            
            # Mark as required if no default value
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(param_name)
        
        tool_def = ToolDefinition(
            name=tool_name,
            description=tool_description,
            function=func,
            parameters=parameters
        )
        
        self.tools[tool_name] = tool_def
    
    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """Get tools in OpenAI function calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters
                }
            }
            for tool in self.tools.values()
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a registered tool with the given arguments."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        
        # Call the function with the provided arguments
        if inspect.iscoroutinefunction(tool.function):
            return await tool.function(**arguments)
        else:
            return tool.function(**arguments)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self.tools.keys())


# Global tool registry instance
tool_registry = ToolRegistry()
