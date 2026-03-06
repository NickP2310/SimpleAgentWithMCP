"""Moderate custom tool example: JSON Validator.

This example shows a tool with parameter validation and error handling.
"""
import json
from typing import Dict, Any
from src.tools import Tool
from src.models import ToolResult, ContentBlock


class JSONValidatorTool(Tool):
    """A tool that validates and formats JSON strings."""
    
    @property
    def name(self) -> str:
        return "json_validator"
    
    @property
    def description(self) -> str:
        return "Validate and format JSON strings. Can also extract specific fields."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "json_string": {
                    "type": "string",
                    "description": "The JSON string to validate"
                },
                "extract_field": {
                    "type": "string",
                    "description": "Optional: Extract a specific field from the JSON"
                },
                "pretty_print": {
                    "type": "boolean",
                    "description": "Whether to format the JSON with indentation"
                }
            },
            "required": ["json_string"]
        }
    
    def execute(self, **kwargs) -> ToolResult:
        """Validate and optionally format JSON."""
        json_string = kwargs.get("json_string", "")
        extract_field = kwargs.get("extract_field")
        pretty_print = kwargs.get("pretty_print", False)
        
        # Validate input
        if not json_string:
            return ToolResult(
                success=False,
                content=[],
                error="No JSON string provided"
            )
        
        try:
            # Parse JSON
            data = json.loads(json_string)
            
            # Extract field if requested
            if extract_field:
                if extract_field in data:
                    result = str(data[extract_field])
                else:
                    return ToolResult(
                        success=False,
                        content=[],
                        error=f"Field '{extract_field}' not found in JSON"
                    )
            else:
                # Format JSON
                if pretty_print:
                    result = json.dumps(data, indent=2)
                else:
                    result = json.dumps(data)
            
            return ToolResult(
                success=True,
                content=[ContentBlock(type="text", text=result)],
                error=None
            )
        
        except json.JSONDecodeError as e:
            return ToolResult(
                success=False,
                content=[],
                error=f"Invalid JSON: {str(e)}"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=[],
                error=f"Error processing JSON: {str(e)}"
            )


# Test the tool
if __name__ == "__main__":
    tool = JSONValidatorTool()
    
    # Test 1: Valid JSON
    test_json = '{"name": "Alice", "age": 30, "city": "NYC"}'
    result = tool.execute(json_string=test_json, pretty_print=True)
    print("Test 1: Valid JSON with pretty print")
    print(result.content[0].text if result.success else result.error)
    print()
    
    # Test 2: Extract field
    result = tool.execute(json_string=test_json, extract_field="name")
    print("Test 2: Extract 'name' field")
    print(result.content[0].text if result.success else result.error)
    print()
    
    # Test 3: Invalid JSON
    result = tool.execute(json_string="{invalid json}")
    print("Test 3: Invalid JSON")
    print(f"Success: {result.success}, Error: {result.error}")
