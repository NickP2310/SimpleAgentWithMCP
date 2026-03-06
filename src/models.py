"""Core data models for MCP protocol and agent execution."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# MCP Protocol Models

@dataclass
class MCPRequest:
    """MCP protocol request message."""
    method: str
    jsonrpc: str = "2.0"
    params: Optional[Dict[str, Any]] = None
    id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {"jsonrpc": self.jsonrpc, "method": self.method}
        if self.params is not None:
            result["params"] = self.params
        if self.id is not None:
            result["id"] = self.id
        return result


@dataclass
class MCPError:
    """MCP protocol error."""
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {"code": self.code, "message": self.message}
        if self.data is not None:
            result["data"] = self.data
        return result


@dataclass
class MCPResponse:
    """MCP protocol response message."""
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[MCPError] = None
    id: Optional[int] = None
    
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


@dataclass
class ContentBlock:
    """Single content block in MCP format."""
    type: str  # "text", "image", "resource"
    text: Optional[str] = None
    data: Optional[bytes] = None
    mime_type: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"type": self.type}
        if self.text is not None:
            result["text"] = self.text
        if self.mime_type is not None:
            result["mimeType"] = self.mime_type
        return result


@dataclass
class ToolResult:
    """Result from tool execution."""
    success: bool
    content: List[ContentBlock]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "content": [block.to_dict() for block in self.content],
            "error": self.error
        }


@dataclass
class ToolSchema:
    """JSON Schema describing a tool's interface."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MCP protocol."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }


# Agent Models

@dataclass
class ToolCall:
    """Represents a single tool invocation."""
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[ToolResult] = None
    error: Optional[str] = None
    duration: float = 0.0


@dataclass
class ExecutionStep:
    """Single step in agent execution."""
    step_number: int
    step_type: str  # "reasoning", "tool_call", "reflection"
    description: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    duration: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ExecutionTrace:
    """Detailed trace of agent execution for educational purposes."""
    steps: List[ExecutionStep] = field(default_factory=list)
    total_duration: float = 0.0
    tool_calls_count: int = 0
    iterations: int = 0


@dataclass
class Message:
    """Single message in conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tool_calls: Optional[List[ToolCall]] = None


@dataclass
class Context:
    """Agent's current context."""
    conversation_history: List[Message] = field(default_factory=list)
    available_tools: List[ToolSchema] = field(default_factory=list)
    current_task: str = ""
    iteration: int = 0


@dataclass
class AgentResponse:
    """Response from agent after processing a prompt."""
    result: str
    success: bool
    execution_trace: ExecutionTrace
    tool_calls: List[ToolCall] = field(default_factory=list)
    error: Optional[str] = None
