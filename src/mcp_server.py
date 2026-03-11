"""MCP Server implementation.

The MCP Server is responsible for:
1. Managing the registry of available tools
2. Handling MCP protocol requests (JSON-RPC 2.0)
3. Routing requests to appropriate handlers
4. Executing tools and returning results

Flow: Client Request → Server Router → Handler → Tool Execution → Response
"""
from typing import Dict, List, Optional, Any
from src.models import MCPRequest, MCPResponse, MCPError, ToolSchema
from src.tools import Tool


class ToolRegistry:
    """Manages collection of available tools.
    
    The registry is a simple dictionary that maps tool names to tool instances.
    It provides methods to:
    - Register new tools
    - Look up tools by name
    - List all available tools
    - Execute tools with parameters
    """
    
    def __init__(self):
        """Initialize empty registry.
        
        Creates an empty dictionary to store tools.
        Tools are added via the register() method.
        """
        self.tools: Dict[str, Tool] = {}  # tool_name -> Tool instance
    
    def register(self, tool: Tool) -> None:
        """Add a tool to the registry.
        
        Args:
            tool: Tool instance to register
            
        The tool's name (from tool.name property) is used as the key.
        If a tool with the same name already exists, it will be replaced.
        """
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Retrieve tool by name.
        
        Args:
            name: Tool name to look up
            
        Returns:
            Tool instance if found, None otherwise
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[ToolSchema]:
        """Return schemas for all registered tools.
        
        Returns:
            List of ToolSchema objects describing each tool
            
        This is used by the "tools/list" MCP method to advertise
        available tools to clients.
        """
        return [tool.get_schema() for tool in self.tools.values()]
    
    def execute(self, name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with given parameters.
        
        Args:
            name: Tool name to execute
            parameters: Parameters to pass to the tool
            
        Returns:
            Tool result as dictionary
            
        Raises:
            ValueError: If tool not found
        """
        tool = self.get_tool(name)
        if tool is None:
            raise ValueError(f"Tool not found: {name}")
        
        # Execute the tool and convert result to dictionary
        result = tool.execute(**parameters)
        return result.to_dict()


class MCPServer:
    """MCP Server that exposes tools following the protocol.
    
    The server implements the Model Context Protocol (MCP) which uses
    JSON-RPC 2.0 as its transport protocol. It handles these methods:
    
    - initialize: Establish connection and exchange capabilities
    - tools/list: Return list of available tools
    - tools/call: Execute a specific tool
    - ping: Health check
    
    The server is stateful - it tracks whether a client is connected.
    """
    
    def __init__(self, tool_registry: ToolRegistry):
        """Initialize server with tool registry.
        
        Args:
            tool_registry: Registry containing all available tools
        """
        self.tool_registry = tool_registry  # Tools we can execute
        self.connected = False  # Is a client connected?
        self.request_id_counter = 0  # For generating request IDs
    
    def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Route incoming MCP requests to appropriate handlers.
        
        This is the main entry point for all requests. It:
        1. Examines the request method
        2. Routes to the appropriate handler
        3. Catches any errors and returns proper error responses
        
        Args:
            request: MCP request from client
            
        Returns:
            MCP response (either success or error)
        """
        try:
            # Route based on method name
            if request.method == "initialize":
                return self._handle_initialize(request)
            elif request.method == "tools/list":
                return self._handle_tools_list(request)
            elif request.method == "tools/call":
                return self._handle_tools_call(request)
            elif request.method == "ping":
                return self._handle_ping(request)
            else:
                # Unknown method - return error
                return MCPResponse(
                    error=MCPError(
                        code=-32601,  # Method not found
                        message=f"Method not found: {request.method}"
                    ),
                    id=request.id
                )
        except Exception as e:
            # Unexpected error - return internal error
            return MCPResponse(
                error=MCPError(
                    code=-32603,  # Internal error
                    message=f"Internal error: {str(e)}"
                ),
                id=request.id
            )
    
    def _handle_initialize(self, request: MCPRequest) -> MCPResponse:
        """Handle connection initialization.
        
        This is the first request a client sends. It establishes the
        connection and exchanges protocol version and capabilities.
        
        Args:
            request: Initialize request
            
        Returns:
            Response with server info and protocol version
        """
        self.connected = True  # Mark client as connected
        return MCPResponse(
            result={
                "protocolVersion": "1.0",  # MCP protocol version
                "serverInfo": {
                    "name": "learning-mcp-server",  # Server name
                    "version": "0.1.0"  # Server version
                }
            },
            id=request.id
        )
    
    def _handle_tools_list(self, request: MCPRequest) -> MCPResponse:
        """Return list of available tools.
        
        This is how clients discover what tools are available.
        Each tool is described by its schema (name, description, parameters).
        
        Args:
            request: tools/list request
            
        Returns:
            Response with array of tool schemas
        """
        # Get all tool schemas from registry
        tools = self.tool_registry.list_tools()
        return MCPResponse(
            result={
                "tools": [tool.to_dict() for tool in tools]
            },
            id=request.id
        )
    
    def _handle_tools_call(self, request: MCPRequest) -> MCPResponse:
        """Execute a tool and return results.
        
        This is the core functionality - executing tools on behalf of clients.
        The request must include:
        - name: Tool name to execute
        - arguments: Parameters to pass to the tool
        
        Args:
            request: tools/call request with tool name and arguments
            
        Returns:
            Response with tool result or error
        """
        # Validate request has parameters
        if not request.params:
            return MCPResponse(
                error=MCPError(
                    code=-32602,  # Invalid params
                    message="Missing params for tools/call"
                ),
                id=request.id
            )
        
        # Extract tool name and arguments
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        
        # Validate tool name is provided
        if not tool_name:
            return MCPResponse(
                error=MCPError(
                    code=-32602,  # Invalid params
                    message="Missing tool name in params"
                ),
                id=request.id
            )
        
        try:
            # Execute the tool via registry
            result = self.tool_registry.execute(tool_name, arguments)
            return MCPResponse(
                result={"content": result["content"]},  # Return content blocks
                id=request.id
            )
        except ValueError as e:
            # Tool not found
            return MCPResponse(
                error=MCPError(
                    code=-32602,  # Invalid params
                    message=str(e)
                ),
                id=request.id
            )
        except Exception as e:
            # Tool execution failed
            return MCPResponse(
                error=MCPError(
                    code=-32603,  # Internal error
                    message=f"Tool execution error: {str(e)}"
                ),
                id=request.id
            )
    
    def _handle_ping(self, request: MCPRequest) -> MCPResponse:
        """Handle ping health check.
        
        Simple health check endpoint to verify server is responsive.
        
        Args:
            request: ping request
            
        Returns:
            Response with status "ok"
        """
        return MCPResponse(
            result={"status": "ok"},
            id=request.id
        )
