"""Advanced custom tool example: Data Transformer.

This example shows a complex tool with multiple operations and stateful patterns.
"""
from typing import Dict, Any, List
from src.tools import Tool
from src.models import ToolResult, ContentBlock


class DataTransformerTool(Tool):
    """A tool that performs various data transformations."""
    
    def __init__(self):
        """Initialize with transformation history."""
        self.transformation_history: List[Dict[str, Any]] = []
    
    @property
    def name(self) -> str:
        return "data_transformer"
    
    @property
    def description(self) -> str:
        return ("Transform data using various operations: uppercase, lowercase, "
                "capitalize, count_words, count_chars, extract_numbers, or reverse. "
                "Maintains history of transformations.")
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "The data to transform"
                },
                "operation": {
                    "type": "string",
                    "enum": ["uppercase", "lowercase", "capitalize", "count_words", 
                            "count_chars", "extract_numbers", "reverse"],
                    "description": "The transformation operation to perform"
                },
                "show_history": {
                    "type": "boolean",
                    "description": "Whether to include transformation history in result"
                }
            },
            "required": ["data", "operation"]
        }
    
    def execute(self, **kwargs) -> ToolResult:
        """Execute the transformation."""
        data = kwargs.get("data", "")
        operation = kwargs.get("operation", "")
        show_history = kwargs.get("show_history", False)
        
        # Validate inputs
        if not data:
            return ToolResult(
                success=False,
                content=[],
                error="No data provided"
            )
        
        if not operation:
            return ToolResult(
                success=False,
                content=[],
                error="No operation specified"
            )
        
        try:
            # Perform transformation
            result = self._transform(data, operation)
            
            # Record in history
            self.transformation_history.append({
                "operation": operation,
                "input_length": len(data),
                "output_length": len(str(result))
            })
            
            # Format output
            output = f"Result: {result}"
            
            if show_history:
                output += f"\n\nTransformation History ({len(self.transformation_history)} operations):"
                for i, record in enumerate(self.transformation_history[-5:], 1):
                    output += f"\n  {i}. {record['operation']}: {record['input_length']} → {record['output_length']} chars"
            
            return ToolResult(
                success=True,
                content=[ContentBlock(type="text", text=output)],
                error=None
            )
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=[],
                error=f"Transformation error: {str(e)}"
            )
    
    def _transform(self, data: str, operation: str) -> str:
        """Perform the actual transformation."""
        if operation == "uppercase":
            return data.upper()
        
        elif operation == "lowercase":
            return data.lower()
        
        elif operation == "capitalize":
            return data.title()
        
        elif operation == "count_words":
            word_count = len(data.split())
            return f"{word_count} words"
        
        elif operation == "count_chars":
            char_count = len(data)
            return f"{char_count} characters"
        
        elif operation == "extract_numbers":
            import re
            numbers = re.findall(r'\d+', data)
            return ", ".join(numbers) if numbers else "No numbers found"
        
        elif operation == "reverse":
            return data[::-1]
        
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get transformation history."""
        return self.transformation_history.copy()
    
    def clear_history(self):
        """Clear transformation history."""
        self.transformation_history.clear()


# Test the tool
if __name__ == "__main__":
    tool = DataTransformerTool()
    
    # Test 1: Uppercase
    result = tool.execute(data="hello world", operation="uppercase")
    print("Test 1: Uppercase")
    print(result.content[0].text if result.success else result.error)
    print()
    
    # Test 2: Count words
    result = tool.execute(data="The quick brown fox jumps", operation="count_words")
    print("Test 2: Count words")
    print(result.content[0].text if result.success else result.error)
    print()
    
    # Test 3: Extract numbers
    result = tool.execute(data="I have 3 cats and 2 dogs", operation="extract_numbers")
    print("Test 3: Extract numbers")
    print(result.content[0].text if result.success else result.error)
    print()
    
    # Test 4: Show history
    result = tool.execute(data="test", operation="reverse", show_history=True)
    print("Test 4: Reverse with history")
    print(result.content[0].text if result.success else result.error)
    print()
    
    # Test 5: Invalid operation
    result = tool.execute(data="test", operation="invalid")
    print("Test 5: Invalid operation")
    print(f"Success: {result.success}, Error: {result.error}")
