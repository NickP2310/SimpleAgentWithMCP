"""Built-in tools for the learning agent.

This file contains three example tools:
1. CalculatorTool - Performs safe mathematical calculations
2. FileOperationsTool - Read, write, and list files
3. WebSearchTool - Simulated web search (for learning)

Each tool follows the same pattern:
- Inherits from Tool base class
- Defines name, description, and input schema
- Implements execute() method
- Returns ToolResult with content blocks

Tools are the "hands" of the agent - they let it interact with the world.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import os
from pathlib import Path
from src.models import ToolResult, ToolSchema, ContentBlock


class Tool(ABC):
    """Base class for all tools.
    
    This abstract base class defines the interface that all tools must implement.
    Every tool must provide:
    - name: Unique identifier
    - description: What the tool does (helps agent decide when to use it)
    - input_schema: JSON Schema defining parameters
    - execute: Method that does the actual work
    
    To create a new tool, inherit from this class and implement all methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name (unique identifier).
        
        This is how the agent refers to the tool. Should be lowercase
        with underscores (e.g., "calculator", "web_search").
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description (what it does).
        
        This helps the agent decide when to use the tool. Should be
        clear and concise, describing the tool's purpose and capabilities.
        """
        pass
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON schema for tool parameters.
        
        Defines what parameters the tool accepts, their types, and
        which ones are required. Follows JSON Schema specification.
        
        Example:
            {
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "..."},
                    "param2": {"type": "number", "description": "..."}
                },
                "required": ["param1"]
            }
        """
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with provided parameters.
        
        This is where the actual work happens. The method receives
        parameters as keyword arguments and returns a ToolResult.
        
        Args:
            **kwargs: Tool parameters (defined by input_schema)
            
        Returns:
            ToolResult with success status and content
        """
        pass
    
    def get_schema(self) -> ToolSchema:
        """Return JSON schema describing this tool.
        
        This is used by the MCP server to advertise the tool to clients.
        It combines the name, description, and input_schema into a
        ToolSchema object.
        
        Returns:
            ToolSchema describing this tool
        """
        return ToolSchema(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema
        )


class CalculatorTool(Tool):
    """Perform mathematical calculations safely.
    
    This tool evaluates mathematical expressions using Python's eval()
    function, but with safety restrictions:
    - Only allows numbers and basic operators (+, -, *, /, parentheses)
    - No access to built-in functions or variables
    - Catches division by zero and other errors
    
    Examples:
        "15 * 23" → 345
        "(10 + 5) * 2" → 30
        "100 / 4" → 25.0
    """
    
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
        """Safely evaluate mathematical expressions.
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            ToolResult with calculation result or error
        """
        expression = kwargs.get("expression", "")
        
        try:
            # Security: Only allow safe mathematical operations
            # Check that expression only contains allowed characters
            allowed_chars = set("0123456789+-*/().  ")
            if not all(c in allowed_chars for c in expression):
                return ToolResult(
                    success=False,
                    content=[],
                    error="Invalid characters in expression. Only numbers and +, -, *, /, (, ) are allowed."
                )
            
            # Evaluate the expression safely
            # __builtins__={} prevents access to built-in functions
            result = eval(expression, {"__builtins__": {}}, {})
            
            # Return successful result
            return ToolResult(
                success=True,
                content=[ContentBlock(type="text", text=str(result))],
                error=None
            )
        except ZeroDivisionError:
            # Handle division by zero
            return ToolResult(
                success=False,
                content=[],
                error="Division by zero error"
            )
        except Exception as e:
            # Handle any other errors (syntax errors, etc.)
            return ToolResult(
                success=False,
                content=[],
                error=f"Error evaluating expression: {str(e)}"
            )


class FileOperationsTool(Tool):
    """Read, write, and list files.
    
    This tool provides file system operations, but with safety restrictions:
    - All operations are restricted to a workspace directory
    - Paths cannot escape the workspace (no ../ tricks)
    - The workspace directory is created automatically if it doesn't exist
    
    Supported operations:
    - read: Read file contents
    - write: Write content to a file
    - list: List files in a directory
    
    Examples:
        read: {"operation": "read", "path": "data.txt"}
        write: {"operation": "write", "path": "result.txt", "content": "Hello"}
        list: {"operation": "list", "path": "."}
    """
    
    def __init__(self, workspace_dir: str = "./workspace"):
        """Initialize with workspace directory.
        
        Args:
            workspace_dir: Directory where files can be accessed
                          (default: "./workspace")
        """
        self.workspace_dir = Path(workspace_dir)
        # Create workspace directory if it doesn't exist
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
        """Execute file operation.
        
        Args:
            operation: "read", "write", or "list"
            path: File path relative to workspace
            content: Content to write (for write operation)
            
        Returns:
            ToolResult with operation result or error
        """
        operation = kwargs.get("operation")
        path = kwargs.get("path", "")
        content = kwargs.get("content")
        
        # Security: Validate path is within workspace
        # This prevents directory traversal attacks (e.g., "../../etc/passwd")
        try:
            full_path = (self.workspace_dir / path).resolve()
            # Check that resolved path starts with workspace path
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
            # Handle READ operation
            if operation == "read":
                # Check file exists
                if not full_path.exists():
                    return ToolResult(
                        success=False,
                        content=[],
                        error=f"File not found: {path}"
                    )
                
                # Read file contents
                text = full_path.read_text()
                return ToolResult(
                    success=True,
                    content=[ContentBlock(type="text", text=text)],
                    error=None
                )
            
            # Handle WRITE operation
            elif operation == "write":
                # Validate content parameter is provided
                if content is None:
                    return ToolResult(
                        success=False,
                        content=[],
                        error="Content parameter required for write operation"
                    )
                
                # Create parent directories if needed
                full_path.parent.mkdir(parents=True, exist_ok=True)
                # Write content to file
                full_path.write_text(content)
                return ToolResult(
                    success=True,
                    content=[ContentBlock(type="text", text=f"Successfully wrote to {path}")],
                    error=None
                )
            
            # Handle LIST operation
            elif operation == "list":
                # Check path exists
                if not full_path.exists():
                    return ToolResult(
                        success=False,
                        content=[],
                        error=f"Directory not found: {path}"
                    )
                
                # List files
                if full_path.is_file():
                    # If path is a file, just return its name
                    files = [full_path.name]
                else:
                    # If path is a directory, list all files in it
                    files = [f.name for f in full_path.iterdir()]
                
                return ToolResult(
                    success=True,
                    content=[ContentBlock(type="text", text="\n".join(files))],
                    error=None
                )
            
            # Unknown operation
            else:
                return ToolResult(
                    success=False,
                    content=[],
                    error=f"Unknown operation: {operation}"
                )
        
        except Exception as e:
            # Handle any unexpected errors
            return ToolResult(
                success=False,
                content=[],
                error=f"Error performing {operation}: {str(e)}"
            )


class WebSearchTool(Tool):
    """Simulated web search for educational purposes.
    
    This tool returns simulated search results. It doesn't actually
    search the web - it just generates fake results based on the query.
    
    This is intentional for educational purposes:
    - No API keys required
    - Works offline
    - Predictable results for testing
    
    In a real system, you would integrate with a search API like:
    - Google Custom Search API
    - Bing Search API
    - DuckDuckGo API
    
    Example:
        {"query": "Python tutorials"} → Simulated search results
    """
    
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
        """Return simulated search results.
        
        Args:
            query: Search query string
            
        Returns:
            ToolResult with simulated search results
        """
        query = kwargs.get("query", "")
        
        # Generate simulated results based on the query
        # In a real implementation, you would call a search API here
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
