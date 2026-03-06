"""Template for creating custom tools.

This template shows you how to create your own tool that the agent can use.
Copy this file and modify it to create your custom tool.
"""
from typing import Dict, Any
from src.tools import Tool
from src.models import ToolResult, ContentBlock


class MyCustomTool(Tool):
    """
    Template for a custom tool.
    
    Replace this with your tool's description. This description will be shown
    to the agent so it knows when to use your tool.
    """
    
    @property
    def name(self) -> str:
        """
        Tool name - must be unique.
        
        This is how the agent will refer to your tool.
        Use lowercase with underscores (e.g., "my_custom_tool").
        """
        return "my_custom_tool"
    
    @property
    def description(self) -> str:
        """
        Tool description for the agent.
        
        Write a clear description of what your tool does.
        The agent uses this to decide when to call your tool.
        """
        return "Describe what your tool does here"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        """
        JSON Schema defining the tool's parameters.
        
        Define what parameters your tool accepts.
        The agent will provide these parameters when calling your tool.
        """
        return {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of parameter 1"
                },
                "param2": {
                    "type": "number",
                    "description": "Description of parameter 2"
                }
            },
            "required": ["param1"]  # List required parameters
        }
    
    def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with provided parameters.
        
        This is where your tool's logic goes.
        
        Args:
            **kwargs: Parameters matching your input_schema
        
        Returns:
            ToolResult with success status and content
        """
        # Get parameters
        param1 = kwargs.get("param1")
        param2 = kwargs.get("param2", 0)  # Optional parameter with default
        
        try:
            # Your tool logic here
            result = f"Processed {param1} with {param2}"
            
            # Return success result
            return ToolResult(
                success=True,
                content=[ContentBlock(type="text", text=result)],
                error=None
            )
        
        except Exception as e:
            # Return error result
            return ToolResult(
                success=False,
                content=[],
                error=f"Error in my_custom_tool: {str(e)}"
            )


# Example: How to register your tool
if __name__ == "__main__":
    """
    To use your custom tool:
    
    1. Import it in main.py:
       from examples.custom_tool_template import MyCustomTool
    
    2. Register it with the tool registry:
       tool_registry.register(MyCustomTool())
    
    3. The agent will automatically discover and use it!
    """
    
    # Test your tool
    tool = MyCustomTool()
    print(f"Tool Name: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Schema: {tool.input_schema}")
    
    # Test execution
    result = tool.execute(param1="test", param2=42)
    print(f"Result: {result}")
