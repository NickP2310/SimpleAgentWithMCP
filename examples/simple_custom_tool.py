"""Simple custom tool example: String Reverser.

This example shows a basic tool that takes a string and reverses it.
"""
from typing import Dict, Any
from src.tools import Tool
from src.models import ToolResult, ContentBlock


class StringReverserTool(Tool):
    """A simple tool that reverses strings."""
    
    @property
    def name(self) -> str:
        return "string_reverser"
    
    @property
    def description(self) -> str:
        return "Reverse a string. Takes a text input and returns it reversed."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to reverse"
                }
            },
            "required": ["text"]
        }
    
    def execute(self, **kwargs) -> ToolResult:
        """Reverse the input string."""
        text = kwargs.get("text", "")
        
        if not text:
            return ToolResult(
                success=False,
                content=[],
                error="No text provided to reverse"
            )
        
        # Reverse the string
        reversed_text = text[::-1]
        
        return ToolResult(
            success=True,
            content=[ContentBlock(type="text", text=reversed_text)],
            error=None
        )


# Test the tool
if __name__ == "__main__":
    tool = StringReverserTool()
    
    # Test 1: Normal string
    result = tool.execute(text="Hello, World!")
    print(f"Input: 'Hello, World!'")
    print(f"Output: '{result.content[0].text}'")
    print()
    
    # Test 2: Empty string
    result = tool.execute(text="")
    print(f"Empty string test: Success={result.success}, Error={result.error}")
