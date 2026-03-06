"""MCP Server implementation."""
from typing import Dict, List, Optional, Any
from src.models import MCPRequest, MCPResponse, MCPError, ToolSchema
from src.tools import Tool


class ToolRegistry:
    """Manages collection of available tools."""
    
    def __init__(self):
        """Initialize empty registry."""
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Add a tool to the registry."""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Retrieve tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[ToolSchema]:
        """Return schemas for all registered tools."""
        return [tool.get_schema() for tool in self.tools.values()]
    
    def execute(self, name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with given parameters."""
        tool = self.get_tool(name)
        if tool is None:
            raise ValueError(f"Tool not found: {name}")
        
        result = tool.execute(**parameters)
        return result.to_dict()


class MCPServer:
    """MCP Server that exposes tools following the protocol."""
    
    def __init__(self, tool_registry: ToolRegistry):
        """Initialize server with tool registry."""
        self.tool_registry = tool_registry
        self.connected = False
        self.request_id_counter = 0
    
    def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Route incoming MCP requests to appropriate handlers."""
        try:
            if request.method == "initialize":
                return self._handle_initialize(request)
            elif request.method == "tools/list":
                return self._handle_tools_list(request)
            elif request.method == "tools/call":
                return self._handle_tools_call(request)
            elif request.method == "ping":
                return self._handle_ping(request)
            else:
                return MCPResponse(
                    error=MCPError(
                        code=-32601,
                        message=f"Method not found: {request.method}"
                    ),
                    id=request.id
                )
        except Exception as e:
            return MCPResponse(
                error=MCPError(
                    code=-32603,
                    message=f"Internal error: {str(e)}"
                ),
                id=request.id
            )
    
    def _handle_initialize(self, request: MCPRequest) -> MCPResponse:
        """Handle connection initialization."""
        self.connected = True
        return MCPResponse(
            result={
                "protocolVersion": "1.0",
                "serverInfo": {
                    "name": "learning-mcp-server",
                    "version": "0.1.0"
                }
            },
            id=request.id
        )
    
    def _handle_tools_list(self, request: MCPRequest) -> MCPResponse:
        """Return list of available tools."""
        tools = self.tool_registry.list_tools()
        return MCPResponse(
            result={
                "tools": [tool.to_dict() for tool in tools]
            },
            id=request.id
        )
    
    def _handle_tools_call(self, request: MCPRequest) -> MCPResponse:
        """Execute a tool and return results."""
        if not request.params:
            return MCPResponse(
                error=MCPError(
                    code=-32602,
                    message="Missing params for tools/call"
                ),
                id=request.id
            )
        
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})
        
        if not tool_name:
            return MCPResponse(
                error=MCPError(
                    code=-32602,
                    message="Missing tool name in params"
                ),
                id=request.id
            )
        
        try:
            result = self.tool_registry.execute(tool_name, arguments)
            return MCPResponse(
                result={"content": result["content"]},
                id=request.id
            )
        except ValueError as e:
            return MCPResponse(
                error=MCPError(
                    code=-32602,
                    message=str(e)
                ),
                id=request.id
            )
        except Exception as e:
            return MCPResponse(
                error=MCPError(
                    code=-32603,
                    message=f"Tool execution error: {str(e)}"
                ),
                id=request.id
            )
    
    def _handle_ping(self, request: MCPRequest) -> MCPResponse:
        """Handle ping health check."""
        return MCPResponse(
            result={"status": "ok"},
            id=request.id
        )
