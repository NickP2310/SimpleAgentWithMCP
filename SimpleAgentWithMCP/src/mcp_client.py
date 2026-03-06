"""MCP Client implementation."""
from typing import List, Dict, Any
from src.models import MCPRequest, MCPResponse, ToolSchema, ToolResult, ContentBlock
from src.mcp_server import MCPServer


class MCPClient:
    """Handles communication with MCP servers."""
    
    def __init__(self, server: MCPServer):
        """Initialize client with server reference (in-process for simplicity)."""
        self.server = server
        self.connected = False
        self.request_id = 0
    
    def connect(self) -> bool:
        """Establish connection to MCP server."""
        try:
            request = MCPRequest(
                method="initialize",
                id=self._next_id()
            )
            response = self.server.handle_request(request)
            
            if response.error:
                print(f"❌ Connection error: {response.error.message}")
                return False
            
            self.connected = True
            print("✅ Connected to MCP server")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False
    
    def discover_tools(self) -> List[ToolSchema]:
        """Request list of available tools from server."""
        if not self.connected:
            print("⚠️  Not connected to server")
            return []
        
        try:
            request = MCPRequest(
                method="tools/list",
                id=self._next_id()
            )
            response = self.server.handle_request(request)
            
            if response.error:
                print(f"❌ Tool discovery error: {response.error.message}")
                return []
            
            tools_data = response.result.get("tools", [])
            tools = []
            for tool_data in tools_data:
                tools.append(ToolSchema(
                    name=tool_data["name"],
                    description=tool_data["description"],
                    input_schema=tool_data["inputSchema"]
                ))
            
            print(f"🔧 Discovered {len(tools)} tools")
            return tools
        except Exception as e:
            print(f"❌ Tool discovery failed: {str(e)}")
            return []
    
    def invoke_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        """Invoke a specific tool with parameters."""
        if not self.connected:
            return ToolResult(
                success=False,
                content=[],
                error="Not connected to server"
            )
        
        try:
            request = MCPRequest(
                method="tools/call",
                params={
                    "name": tool_name,
                    "arguments": parameters
                },
                id=self._next_id()
            )
            
            print(f"📞 Calling tool '{tool_name}' with parameters: {parameters}")
            response = self.server.handle_request(request)
            
            if response.error:
                error_msg = response.error.message
                print(f"❌ Tool call error: {error_msg}")
                return ToolResult(
                    success=False,
                    content=[],
                    error=error_msg
                )
            
            # Parse content blocks
            content_data = response.result.get("content", [])
            content_blocks = []
            for block_data in content_data:
                content_blocks.append(ContentBlock(
                    type=block_data.get("type", "text"),
                    text=block_data.get("text")
                ))
            
            print(f"✅ Tool returned result")
            return ToolResult(
                success=True,
                content=content_blocks,
                error=None
            )
        except Exception as e:
            error_msg = f"Tool invocation failed: {str(e)}"
            print(f"❌ {error_msg}")
            return ToolResult(
                success=False,
                content=[],
                error=error_msg
            )
    
    def disconnect(self) -> None:
        """Clean up connection to server."""
        self.connected = False
        print("👋 Disconnected from MCP server")
    
    def _next_id(self) -> int:
        """Generate next request ID."""
        self.request_id += 1
        return self.request_id
