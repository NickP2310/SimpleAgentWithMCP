"""MCP Client implementation.

The MCP Client is responsible for:
1. Connecting to MCP servers
2. Discovering available tools
3. Invoking tools with parameters
4. Handling responses and errors

Flow: Agent → Client → Server → Tool → Server → Client → Agent

In this implementation, the client and server are in the same process
for simplicity. In a real system, they would communicate over a network.
"""
from typing import List, Dict, Any
from src.models import MCPRequest, MCPResponse, ToolSchema, ToolResult, ContentBlock
from src.mcp_server import MCPServer


class MCPClient:
    """Handles communication with MCP servers.
    
    The client provides a simple API for agents to:
    - Connect to servers
    - Discover available tools
    - Invoke tools
    - Disconnect
    
    This implementation uses in-process communication (direct method calls)
    for simplicity. A production client would use HTTP, WebSocket, or stdio.
    """
    
    def __init__(self, server: MCPServer):
        """Initialize client with server reference (in-process for simplicity).
        
        Args:
            server: MCP server instance to communicate with
            
        In a real system, you would pass a connection URL instead of
        a direct server reference. But for learning purposes, we keep
        it simple with in-process communication.
        """
        self.server = server  # Direct reference to server (in-process)
        self.connected = False  # Are we connected?
        self.request_id = 0  # Counter for generating unique request IDs
    
    def connect(self) -> bool:
        """Establish connection to MCP server.
        
        Sends an "initialize" request to the server to establish the
        connection and exchange protocol information.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create initialize request
            request = MCPRequest(
                method="initialize",  # Initialize connection
                id=self._next_id()  # Unique request ID
            )
            
            # Send request to server (in-process call)
            response = self.server.handle_request(request)
            
            # Check for errors
            if response.error:
                print(f"❌ Connection error: {response.error.message}")
                return False
            
            # Connection successful
            self.connected = True
            print("✅ Connected to MCP server")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False
    
    def discover_tools(self) -> List[ToolSchema]:
        """Request list of available tools from server.
        
        Sends a "tools/list" request to discover what tools the server
        provides. This is typically called once after connecting.
        
        Returns:
            List of ToolSchema objects describing available tools
        """
        # Check if connected
        if not self.connected:
            print("⚠️  Not connected to server")
            return []
        
        try:
            # Create tools/list request
            request = MCPRequest(
                method="tools/list",  # Request tool list
                id=self._next_id()
            )
            
            # Send request to server
            response = self.server.handle_request(request)
            
            # Check for errors
            if response.error:
                print(f"❌ Tool discovery error: {response.error.message}")
                return []
            
            # Parse tool schemas from response
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
        """Invoke a specific tool with parameters.
        
        This is the main method agents use to execute tools. It:
        1. Creates a tools/call request
        2. Sends it to the server
        3. Parses the response
        4. Returns a ToolResult
        
        Args:
            tool_name: Name of the tool to invoke
            parameters: Parameters to pass to the tool
            
        Returns:
            ToolResult with success status and content
        """
        # Check if connected
        if not self.connected:
            return ToolResult(
                success=False,
                content=[],
                error="Not connected to server"
            )
        
        try:
            # Create tools/call request
            request = MCPRequest(
                method="tools/call",  # Call a tool
                params={
                    "name": tool_name,  # Which tool to call
                    "arguments": parameters  # Tool parameters
                },
                id=self._next_id()
            )
            
            # Log the call for debugging
            print(f"📞 Calling tool '{tool_name}' with parameters: {parameters}")
            
            # Send request to server
            response = self.server.handle_request(request)
            
            # Check for errors
            if response.error:
                error_msg = response.error.message
                print(f"❌ Tool call error: {error_msg}")
                return ToolResult(
                    success=False,
                    content=[],
                    error=error_msg
                )
            
            # Parse content blocks from response
            # Content blocks are the actual results from the tool
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
            # Unexpected error during invocation
            error_msg = f"Tool invocation failed: {str(e)}"
            print(f"❌ {error_msg}")
            return ToolResult(
                success=False,
                content=[],
                error=error_msg
            )
    
    def disconnect(self) -> None:
        """Clean up connection to server.
        
        Marks the client as disconnected. In a real system, this would
        close network connections, clean up resources, etc.
        """
        self.connected = False
        print("👋 Disconnected from MCP server")
    
    def _next_id(self) -> int:
        """Generate next request ID.
        
        Request IDs are used to match responses to requests. Each request
        gets a unique incrementing ID.
        
        Returns:
            Next request ID
        """
        self.request_id += 1
        return self.request_id
