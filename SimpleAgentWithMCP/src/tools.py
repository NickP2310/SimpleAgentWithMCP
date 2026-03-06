"""Built-in tools for the learning agent."""
from abc import ABC, abstractmethod
from typing import Dict, Any
import os
from pathlib import Path
from src.models import ToolResult, ToolSchema, ContentBlock


class Tool(ABC):
    """Base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description."""
        pass
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON schema for tool parameters."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with provided parameters."""
        pass
    
    def get_schema(self) -> ToolSchema:
        """Return JSON schema describing this tool."""
        return ToolSchema(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema
        )


class CalculatorTool(Tool):
    """Perform mathematical calculations safely."""
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Perform mathematical calculations. Supports basic arithmetic operations."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '15 * 23')"
                }
            },
            "required": ["expression"]
        }
    
    def execute(self, **kwargs) -> ToolResult:
        """Safely evaluate mathematical expressions."""
        expression = kwargs.get("expression", "")
        
        try:
            # Only allow safe mathematical operations
            allowed_chars = set("0123456789+-*/().  ")
            if not all(c in allowed_chars for c in expression):
                return ToolResult(
                    success=False,
                    content=[],
                    error="Invalid characters in expression. Only numbers and +, -, *, /, (, ) are allowed."
                )
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {})
            
            return ToolResult(
                success=True,
                content=[ContentBlock(type="text", text=str(result))],
                error=None
            )
        except ZeroDivisionError:
            return ToolResult(
                success=False,
                content=[],
                error="Division by zero error"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=[],
                error=f"Error evaluating expression: {str(e)}"
            )


class FileOperationsTool(Tool):
    """Read, write, and list files."""
    
    def __init__(self, workspace_dir: str = "./workspace"):
        """Initialize with workspace directory."""
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
    
    @property
    def name(self) -> str:
        return "file_ops"
    
    @property
    def description(self) -> str:
        return "Read, write, and list files in the workspace directory."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["read", "write", "list"],
                    "description": "Operation to perform"
                },
                "path": {
                    "type": "string",
                    "description": "File path relative to workspace"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write (required for write operation)"
                }
            },
            "required": ["operation", "path"]
        }
    
    def execute(self, **kwargs) -> ToolResult:
        """Execute file operation."""
        operation = kwargs.get("operation")
        path = kwargs.get("path", "")
        content = kwargs.get("content")
        
        # Validate path is within workspace
        try:
            full_path = (self.workspace_dir / path).resolve()
            if not str(full_path).startswith(str(self.workspace_dir.resolve())):
                return ToolResult(
                    success=False,
                    content=[],
                    error="Path must be within workspace directory"
                )
        except Exception as e:
            return ToolResult(
                success=False,
                content=[],
                error=f"Invalid path: {str(e)}"
            )
        
        try:
            if operation == "read":
                if not full_path.exists():
                    return ToolResult(
                        success=False,
                        content=[],
                        error=f"File not found: {path}"
                    )
                
                text = full_path.read_text()
                return ToolResult(
                    success=True,
                    content=[ContentBlock(type="text", text=text)],
                    error=None
                )
            
            elif operation == "write":
                if content is None:
                    return ToolResult(
                        success=False,
                        content=[],
                        error="Content parameter required for write operation"
                    )
                
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(content)
                return ToolResult(
                    success=True,
                    content=[ContentBlock(type="text", text=f"Successfully wrote to {path}")],
                    error=None
                )
            
            elif operation == "list":
                if not full_path.exists():
                    return ToolResult(
                        success=False,
                        content=[],
                        error=f"Directory not found: {path}"
                    )
                
                if full_path.is_file():
                    files = [full_path.name]
                else:
                    files = [f.name for f in full_path.iterdir()]
                
                return ToolResult(
                    success=True,
                    content=[ContentBlock(type="text", text="\n".join(files))],
                    error=None
                )
            
            else:
                return ToolResult(
                    success=False,
                    content=[],
                    error=f"Unknown operation: {operation}"
                )
        
        except Exception as e:
            return ToolResult(
                success=False,
                content=[],
                error=f"Error performing {operation}: {str(e)}"
            )


class WebSearchTool(Tool):
    """Simulated web search for educational purposes."""
    
    @property
    def name(self) -> str:
        return "web_search"
    
    @property
    def description(self) -> str:
        return "Search for information (simulated results for educational purposes)."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    
    def execute(self, **kwargs) -> ToolResult:
        """Return simulated search results."""
        query = kwargs.get("query", "")
        
        # Simulated results for educational purposes
        results = f"""Simulated search results for: "{query}"

1. Introduction to {query} - Learn the basics
   https://example.com/intro-{query.replace(' ', '-')}
   
2. Advanced {query} techniques and best practices
   https://example.com/advanced-{query.replace(' ', '-')}
   
3. {query} tutorial for beginners
   https://example.com/tutorial-{query.replace(' ', '-')}

Note: These are simulated results for educational purposes."""
        
        return ToolResult(
            success=True,
            content=[ContentBlock(type="text", text=results)],
            error=None
        )
