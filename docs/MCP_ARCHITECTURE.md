# MCP Architecture Guide

A detailed guide to the Model Context Protocol architecture and implementation.

## Overview

The Model Context Protocol (MCP) is a standardized way for AI agents to discover and invoke tools. This guide explains how MCP works in our learning project.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Learning System                          │
│                                                              │
│  ┌────────────────┐         ┌──────────────────┐           │
│  │   CLI Runner   │────────▶│    AI Agent      │           │
│  │                │         │                  │           │
│  │  - Parse args  │         │  - Process prompt│           │
│  │  - Load config │         │  - Plan actions  │           │
│  │  - Run examples│         │  - Execute loop  │           │
│  └────────────────┘         └─────────┬────────┘           │
│                                       │                     │
│                                       │ uses                │
│                                       ▼                     │
│                             ┌──────────────────┐           │
│                             │   MCP Client     │           │
│                             │                  │           │
│                             │  - Connect       │           │
│                             │  - Discover tools│           │
│                             │  - Invoke tools  │           │
│                             └─────────┬────────┘           │
│                                       │                     │
│                                       │ MCP Protocol        │
│                                       ▼                     │
│                             ┌──────────────────┐           │
│                             │   MCP Server     │           │
│                             │                  │           │
│                             │  - Register tools│           │
│                             │  - Execute tools │           │
│                             │  - Provide       │           │
│                             │    resources     │           │
│                             └─────────┬────────┘           │
│                                       │                     │
│                                       │ executes            │
│                                       ▼                     │
│                             ┌──────────────────┐           │
│                             │   Tool Registry  │           │
│                             │                  │           │
│                             │  - File ops      │           │
│                             │  - Calculator    │           │
│                             │  - Web search    │           │
│                             │  - Custom tools  │           │
│                             └──────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Protocol Specification

### JSON-RPC 2.0 Base

MCP uses JSON-RPC 2.0 as its base protocol:

```json
{
    "jsonrpc": "2.0",
    "method": "method_name",
    "params": {...},
    "id": 1
}
```

### Supported Methods

#### 1. initialize

Establish connection and exchange capabilities.

**Request:**
```json
{
    "jsonrpc": "2.0",
    "method": "initialize",
    "id": 1
}
```

**Response:**
```json
{
    "jsonrpc": "2.0",
    "result": {
        "protocolVersion": "1.0",
        "serverInfo": {
            "name": "learning-mcp-server",
            "version": "0.1.0"
        }
    },
    "id": 1
}
```

#### 2. tools/list

Discover available tools.

**Request:**
```json
{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 2
}
```

**Response:**
```json
{
    "jsonrpc": "2.0",
    "result": {
        "tools": [
            {
                "name": "calculator",
                "description": "Perform mathematical calculations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string"}
                    },
                    "required": ["expression"]
                }
            }
        ]
    },
    "id": 2
}
```

#### 3. tools/call

Invoke a specific tool.

**Request:**
```json
{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "calculator",
        "arguments": {
            "expression": "15 * 23"
        }
    },
    "id": 3
}
```

**Response:**
```json
{
    "jsonrpc": "2.0",
    "result": {
        "content": [
            {
                "type": "text",
                "text": "345"
            }
        ]
    },
    "id": 3
}
```

#### 4. ping

Health check.

**Request:**
```json
{
    "jsonrpc": "2.0",
    "method": "ping",
    "id": 4
}
```

**Response:**
```json
{
    "jsonrpc": "2.0",
    "result": {
        "status": "ok"
    },
    "id": 4
}
```

## Component Details

### MCP Server

**Responsibilities:**
- Implement MCP protocol specification
- Route requests to appropriate handlers
- Validate tool parameters against schemas
- Format responses according to MCP protocol
- Handle errors and return appropriate error responses

**Key Methods:**
```python
class MCPServer:
    def handle_request(request: MCPRequest) -> MCPResponse
    def _handle_initialize(request: MCPRequest) -> MCPResponse
    def _handle_tools_list(request: MCPRequest) -> MCPResponse
    def _handle_tools_call(request: MCPRequest) -> MCPResponse
    def _handle_ping(request: MCPRequest) -> MCPResponse
```

**Connection Lifecycle:**
```
1. Client sends initialize
2. Server responds with capabilities
3. Client sends tools/list
4. Server responds with tool schemas
5. Client sends tools/call (multiple times)
6. Server executes and responds
7. Connection remains open for more calls
```

### MCP Client

**Responsibilities:**
- Manage connection lifecycle with MCP server
- Format requests according to MCP protocol
- Parse MCP responses into usable data structures
- Handle protocol-level errors
- Log all protocol messages for educational visibility

**Key Methods:**
```python
class MCPClient:
    def connect() -> bool
    def discover_tools() -> List[ToolSchema]
    def invoke_tool(tool_name: str, parameters: Dict) -> ToolResult
    def disconnect() -> None
```

**Request Flow:**
```
1. Format request as MCPRequest
2. Send to server
3. Receive MCPResponse
4. Parse result or error
5. Convert to domain objects (ToolResult, etc.)
6. Return to agent
```

### Tool Registry

**Responsibilities:**
- Manage collection of available tools
- Provide tool lookup by name
- Execute tools with parameters
- Return results in standard format

**Key Methods:**
```python
class ToolRegistry:
    def register(tool: Tool) -> None
    def get_tool(name: str) -> Optional[Tool]
    def list_tools() -> List[ToolSchema]
    def execute(name: str, parameters: Dict) -> Dict
```

**Tool Registration:**
```python
# Create registry
registry = ToolRegistry()

# Register tools
registry.register(CalculatorTool())
registry.register(FileOperationsTool())
registry.register(WebSearchTool())

# Tools are now available via MCP
```

## Message Flow Examples

### Example 1: Simple Calculation

```
1. Agent → Client: "I need to calculate 15 * 23"

2. Client → Server:
   {
       "method": "tools/call",
       "params": {
           "name": "calculator",
           "arguments": {"expression": "15 * 23"}
       }
   }

3. Server → Tool Registry: execute("calculator", {"expression": "15 * 23"})

4. Tool Registry → Calculator Tool: execute(expression="15 * 23")

5. Calculator Tool: Evaluates expression → 345

6. Calculator Tool → Tool Registry: ToolResult(success=True, content="345")

7. Tool Registry → Server: {"success": True, "content": [{"type": "text", "text": "345"}]}

8. Server → Client:
   {
       "result": {
           "content": [{"type": "text", "text": "345"}]
       }
   }

9. Client → Agent: ToolResult(success=True, content="345")

10. Agent: Composes response → "The calculation result is: 345"
```

### Example 2: Tool Discovery

```
1. Agent → Client: "What tools are available?"

2. Client → Server:
   {
       "method": "tools/list"
   }

3. Server → Tool Registry: list_tools()

4. Tool Registry: Returns [CalculatorTool.schema, FileOpsTool.schema, ...]

5. Server → Client:
   {
       "result": {
           "tools": [
               {"name": "calculator", "description": "...", "inputSchema": {...}},
               {"name": "file_ops", "description": "...", "inputSchema": {...}},
               {"name": "web_search", "description": "...", "inputSchema": {...}}
           ]
       }
   }

6. Client → Agent: [ToolSchema, ToolSchema, ToolSchema]

7. Agent: Now knows available tools and their parameters
```

## Error Handling

### Error Response Format

```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32602,
        "message": "Invalid params",
        "data": {
            "details": "Missing required parameter: expression"
        }
    },
    "id": 3
}
```

### Error Codes

- `-32700`: Parse error (invalid JSON)
- `-32600`: Invalid request (not valid JSON-RPC)
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error

### Error Handling Flow

```
1. Client sends invalid request
2. Server validates request
3. Server detects error
4. Server creates MCPError
5. Server returns error response
6. Client parses error
7. Client returns ToolResult with error
8. Agent handles error (retry, alternative, or report)
```

## Implementation Notes

### In-Process Communication

For simplicity, our implementation uses in-process communication:
- Client and Server in same process
- Direct method calls instead of network
- Still follows MCP protocol exactly

**Why?**
- Simpler for learning
- No network complexity
- Same protocol, easier debugging

**Production Alternative:**
- HTTP/WebSocket transport
- Separate processes
- Network error handling

### Synchronous Execution

All operations are synchronous:
- One request at a time
- Wait for response before next
- Clear execution order

**Why?**
- Easier to understand
- Predictable behavior
- Simpler error handling

**Production Alternative:**
- Async/await patterns
- Parallel tool execution
- Better performance

## Extension Points

### Adding New Tools

1. Create tool class extending `Tool`
2. Implement required methods
3. Register with `ToolRegistry`
4. Tool automatically available via MCP

```python
# 1. Create tool
class MyTool(Tool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    # ... implement other methods

# 2. Register
registry.register(MyTool())

# 3. Agent can now discover and use it!
```

### Adding New MCP Methods

1. Add method handler to `MCPServer`
2. Update `handle_request` routing
3. Document the new method

```python
def _handle_my_method(self, request: MCPRequest) -> MCPResponse:
    # Implementation
    pass
```

## Best Practices

### Tool Design

1. **Single Responsibility** - Each tool does one thing well
2. **Clear Schema** - Well-documented parameters
3. **Error Handling** - Return meaningful errors
4. **Validation** - Check parameters before execution

### Protocol Usage

1. **Always Validate** - Check request format
2. **Use Standard Errors** - Follow JSON-RPC error codes
3. **Log Everything** - For debugging and learning
4. **Handle Failures** - Graceful degradation

### Client Implementation

1. **Connection Management** - Handle connect/disconnect
2. **Request IDs** - Track requests and responses
3. **Timeout Handling** - Don't wait forever
4. **Error Recovery** - Retry transient failures

## Summary

Key points:

1. **MCP** standardizes agent-tool communication
2. **JSON-RPC 2.0** provides the base protocol
3. **Server** exposes tools following the protocol
4. **Client** discovers and invokes tools
5. **Registry** manages tool collection
6. **In-process** communication simplifies learning
7. **Synchronous** execution keeps it predictable

## Next Steps

- Read `src/mcp_server.py` to see the implementation
- Read `src/mcp_client.py` to understand the client
- Try adding a custom tool and see it work via MCP
- Experiment with the protocol messages in debug mode
