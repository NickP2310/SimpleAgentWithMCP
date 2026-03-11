"""Core data models for MCP protocol and agent execution.

This file defines all the data structures used throughout the system:
- MCP Protocol Models: Request, Response, Error (following JSON-RPC 2.0)
- Tool Models: Schema, Result, Content blocks
- Agent Models: Execution trace, context, messages

These models use Python dataclasses for clean, type-safe data structures.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# MCP PROTOCOL MODELS
# These models implement the Model Context Protocol (MCP) specification
# MCP uses JSON-RPC 2.0 as its transport protocol
# ============================================================================

@dataclass
class MCPRequest:
    """MCP protocol request message (JSON-RPC 2.0 format).
    
    Represents a request from client to server. Every request has:
    - method: What operation to perform (e.g., "tools/list", "tools/call")
    - params: Optional parameters for the operation
    - id: Request ID for matching responses to requests
    """
    method: str  # The operation to perform (e.g., "tools/list")
    jsonrpc: str = "2.0"  # JSON-RPC version (always "2.0")
    params: Optional[Dict[str, Any]] = None  # Optional parameters
    id: Optional[int] = None  # Request ID for tracking
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.
        
        This is used when sending the request over the wire.
        """
        result = {"jsonrpc": self.jsonrpc, "method": self.method}
        if self.params is not None:
            result["params"] = self.params
        if self.id is not None:
            result["id"] = self.id
        return result


@dataclass
class MCPError:
    """MCP protocol error (JSON-RPC 2.0 error format).
    
    Represents an error that occurred during request processing.
    Follows JSON-RPC 2.0 error codes:
    - -32700: Parse error
    - -32600: Invalid request
    - -32601: Method not found
    - -32602: Invalid params
    - -32603: Internal error
    """
    code: int  # Error code (negative number)
    message: str  # Human-readable error message
    data: Optional[Dict[str, Any]] = None  # Optional additional error data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {"code": self.code, "message": self.message}
        if self.data is not None:
            result["data"] = self.data
        return result


@dataclass
class MCPResponse:
    """MCP protocol response message (JSON-RPC 2.0 format).
    
    Represents a response from server to client. A response contains either:
    - result: Successful result data
    - error: Error information if something went wrong
    
    Never both result and error at the same time.
    """
    jsonrpc: str = "2.0"  # JSON-RPC version
    result: Optional[Dict[str, Any]] = None  # Success result
    error: Optional[MCPError] = None  # Error if failed
    id: Optional[int] = None  # Matches request ID
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        response = {"jsonrpc": self.jsonrpc}
        if self.result is not None:
            response["result"] = self.result
        if self.error is not None:
            response["error"] = self.error.to_dict()
        if self.id is not None:
            response["id"] = self.id
        return response


# ============================================================================
# TOOL MODELS
# These models represent tools and their inputs/outputs
# ============================================================================

@dataclass
class ContentBlock:
    """Single content block in MCP format.
    
    Content blocks are the building blocks of tool results. They can contain:
    - text: Plain text content
    - image: Image data (future)
    - resource: File or resource reference (future)
    
    This allows tools to return rich, structured content.
    """
    type: str  # Content type: "text", "image", "resource"
    text: Optional[str] = None  # Text content (for type="text")
    data: Optional[bytes] = None  # Binary data (for images, etc.)
    mime_type: Optional[str] = None  # MIME type (e.g., "image/png")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {"type": self.type}
        if self.text is not None:
            result["text"] = self.text
        if self.mime_type is not None:
            result["mimeType"] = self.mime_type
        return result


@dataclass
class ToolResult:
    """Result from tool execution.
    
    Every tool returns a ToolResult containing:
    - success: Whether the tool executed successfully
    - content: List of content blocks with the actual results
    - error: Error message if something went wrong
    """
    success: bool  # Did the tool execute successfully?
    content: List[ContentBlock]  # Result content (can be multiple blocks)
    error: Optional[str] = None  # Error message if failed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "content": [block.to_dict() for block in self.content],
            "error": self.error
        }


@dataclass
class ToolSchema:
    """JSON Schema describing a tool's interface.
    
    This is how tools advertise themselves to agents. Contains:
    - name: Unique tool identifier
    - description: What the tool does (helps agent decide when to use it)
    - input_schema: JSON Schema defining required/optional parameters
    
    Example:
        ToolSchema(
            name="calculator",
            description="Perform math calculations",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        )
    """
    name: str  # Tool identifier (e.g., "calculator")
    description: str  # What the tool does
    input_schema: Dict[str, Any]  # JSON Schema for parameters
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MCP protocol."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }


# ============================================================================
# AGENT MODELS
# These models track agent execution and maintain state
# ============================================================================

@dataclass
class ToolCall:
    """Represents a single tool invocation.
    
    Records everything about a tool call:
    - What tool was called
    - What parameters were passed
    - What result was returned
    - How long it took
    - Any errors that occurred
    
    This is used for execution tracing and debugging.
    """
    tool_name: str  # Name of the tool that was called
    parameters: Dict[str, Any]  # Parameters passed to the tool
    result: Optional[ToolResult] = None  # Result from the tool
    error: Optional[str] = None  # Error message if failed
    duration: float = 0.0  # How long the call took (seconds)


@dataclass
class ExecutionStep:
    """Single step in agent execution.
    
    The agent's reasoning loop consists of multiple steps:
    - reasoning: Analyzing, planning, reflecting
    - tool_call: Executing a tool
    - reflection: Composing final response
    
    Each step records its inputs, outputs, and timing for educational purposes.
    """
    step_number: int  # Sequential step number (1, 2, 3, ...)
    step_type: str  # Type: "reasoning", "tool_call", "reflection"
    description: str  # Human-readable description
    input_data: Dict[str, Any]  # What went into this step
    output_data: Dict[str, Any]  # What came out of this step
    duration: float  # How long this step took (seconds)
    timestamp: datetime = field(default_factory=datetime.now)  # When it happened


@dataclass
class ExecutionTrace:
    """Detailed trace of agent execution for educational purposes.
    
    This records everything the agent does, allowing you to:
    - See the step-by-step reasoning process
    - Understand which tools were called and why
    - Measure performance and timing
    - Debug issues
    
    This is the "execution log" that gets displayed after each run.
    """
    steps: List[ExecutionStep] = field(default_factory=list)  # All steps taken
    total_duration: float = 0.0  # Total execution time (seconds)
    tool_calls_count: int = 0  # How many tools were called
    iterations: int = 0  # How many reasoning iterations


@dataclass
class Message:
    """Single message in conversation.
    
    Represents one message in the conversation history:
    - role: Who sent it ("user", "assistant", "system")
    - content: The message text
    - tool_calls: Any tools that were called (for assistant messages)
    
    This maintains conversation context across multiple interactions.
    """
    role: str  # "user", "assistant", or "system"
    content: str  # Message text
    timestamp: datetime = field(default_factory=datetime.now)  # When sent
    tool_calls: Optional[List[ToolCall]] = None  # Tools called (if any)


@dataclass
class Context:
    """Agent's current context.
    
    Maintains all the state the agent needs:
    - conversation_history: All messages exchanged so far
    - available_tools: What tools the agent can use
    - current_task: What the agent is currently working on
    - iteration: Which iteration of the reasoning loop we're on
    
    This allows the agent to maintain context across multiple turns.
    """
    conversation_history: List[Message] = field(default_factory=list)  # All messages
    available_tools: List[ToolSchema] = field(default_factory=list)  # Available tools
    current_task: str = ""  # Current task description
    iteration: int = 0  # Current iteration number


@dataclass
class AgentResponse:
    """Response from agent after processing a prompt.
    
    This is what the agent returns after processing a user prompt:
    - result: The final response text
    - success: Whether execution succeeded
    - execution_trace: Detailed trace of what happened
    - tool_calls: All tools that were called
    - error: Error message if something went wrong
    """
    result: str  # Final response text
    success: bool  # Did execution succeed?
    execution_trace: ExecutionTrace  # Detailed execution log
    tool_calls: List[ToolCall] = field(default_factory=list)  # Tools called
    error: Optional[str] = None  # Error message if failed
