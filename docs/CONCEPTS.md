# Core Concepts Guide

This guide explains the fundamental concepts behind AI agents and the Model Context Protocol.

## Table of Contents
1. [What is an AI Agent?](#what-is-an-ai-agent)
2. [Agent Reasoning Loop](#agent-reasoning-loop)
3. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
4. [Tools and Tool Invocation](#tools-and-tool-invocation)
5. [State Management](#state-management)
6. [Error Handling](#error-handling)

## What is an AI Agent?

An **AI agent** is a software program that:
- Receives instructions from users (prompts)
- Makes decisions about how to accomplish tasks
- Uses tools to perform actions
- Returns results to the user

Think of an agent as an intelligent assistant that can:
- Understand what you want
- Figure out the steps needed
- Use available tools to get it done
- Tell you the results

### Key Characteristics

1. **Autonomy** - Makes its own decisions about which tools to use
2. **Goal-Oriented** - Works toward completing the user's request
3. **Tool Usage** - Can invoke external tools to accomplish tasks
4. **Adaptability** - Handles errors and tries alternative approaches

## Agent Reasoning Loop

Our agent follows a simple 4-step reasoning loop:

```
1. ANALYZE
   ↓
2. PLAN
   ↓
3. EXECUTE
   ↓
4. REFLECT
```

### 1. Analyze Phase

The agent examines the user's prompt to understand:
- What is the user asking for?
- What type of task is this?
- What tools might be needed?

**Example:**
- Prompt: "Calculate 15 * 23"
- Analysis: This is a calculation task, needs calculator tool

### 2. Plan Phase

The agent creates an action plan:
- Which tools to use
- In what order
- With what parameters

**Example:**
- Tool: calculator
- Parameters: {expression: "15 * 23"}
- Reason: Perform the calculation

### 3. Execute Phase

The agent calls the planned tools via MCP:
- Invokes each tool with parameters
- Receives results
- Handles any errors

**Example:**
- Call calculator("15 * 23")
- Receive result: 345

### 4. Reflect Phase

The agent composes the final response:
- Combines tool results
- Formats for the user
- Adds context if needed

**Example:**
- Response: "The calculation result is: 345"

## Model Context Protocol (MCP)

MCP is a standardized protocol for agents to discover and use tools.

### Why MCP?

Without MCP, every agent would need custom code for each tool. With MCP:
- Tools expose a standard interface
- Agents can discover tools automatically
- New tools work immediately without code changes

### MCP Architecture

```
┌─────────┐         ┌─────────┐         ┌─────────┐
│  Agent  │ ◄─────► │  Client │ ◄─────► │  Server │
└─────────┘         └─────────┘         └─────────┘
                                              │
                                              ▼
                                        ┌──────────┐
                                        │  Tools   │
                                        └──────────┘
```

### MCP Components

1. **MCP Server**
   - Exposes tools following the protocol
   - Handles tool discovery requests
   - Executes tool invocations
   - Returns results in standard format

2. **MCP Client**
   - Connects to MCP servers
   - Discovers available tools
   - Invokes tools on behalf of the agent
   - Parses results for the agent

3. **Protocol Messages**
   - JSON-RPC 2.0 format
   - Standard methods: tools/list, tools/call
   - Structured responses

### MCP Message Flow

**Tool Discovery:**
```
Client → Server: "What tools do you have?"
Server → Client: [calculator, file_ops, web_search]
```

**Tool Invocation:**
```
Client → Server: "Call calculator with '15 * 23'"
Server → Tool: Execute calculation
Tool → Server: Result: 345
Server → Client: {success: true, content: "345"}
```

## Tools and Tool Invocation

### What is a Tool?

A tool is a discrete function that performs a specific action:
- Read/write files
- Perform calculations
- Search for information
- Transform data

### Tool Components

Every tool has:

1. **Name** - Unique identifier (e.g., "calculator")
2. **Description** - What the tool does
3. **Input Schema** - What parameters it accepts
4. **Execute Method** - The actual implementation

### Tool Schema Example

```python
{
    "name": "calculator",
    "description": "Perform mathematical calculations",
    "inputSchema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Math expression to evaluate"
            }
        },
        "required": ["expression"]
    }
}
```

### Tool Invocation Process

1. **Agent decides** to use a tool
2. **Client formats** the request
3. **Server validates** parameters
4. **Tool executes** the operation
5. **Server formats** the response
6. **Client parses** the result
7. **Agent receives** the outcome

### Request-Response Pattern

All tool invocations follow this pattern:

```
Request:
{
    "method": "tools/call",
    "params": {
        "name": "calculator",
        "arguments": {"expression": "15 * 23"}
    }
}

Response:
{
    "result": {
        "content": [
            {"type": "text", "text": "345"}
        ]
    }
}
```

## State Management

### Agent Context

The agent maintains state across interactions:

```python
Context:
- conversation_history: [Message, Message, ...]
- available_tools: [ToolSchema, ToolSchema, ...]
- current_task: "Calculate 15 * 23"
- iteration: 1
```

### Conversation History

Each interaction is recorded:

```python
Message:
- role: "user" or "assistant"
- content: "Calculate 15 * 23"
- timestamp: 2024-01-15 10:30:00
- tool_calls: [ToolCall, ...]
```

### Why State Matters

State allows the agent to:
- Remember previous interactions
- Reference earlier results
- Build on past context
- Maintain conversation flow

**Example:**
```
User: "My name is Alice"
Agent: "Nice to meet you, Alice!"

User: "What's my name?"
Agent: "Your name is Alice" (remembered from history)
```

## Error Handling

### Error Categories

1. **Tool Errors** - Tool execution fails
2. **Protocol Errors** - MCP message issues
3. **Agent Errors** - Reasoning failures
4. **Configuration Errors** - Invalid settings

### Error Handling Strategies

#### 1. Graceful Degradation

If a tool fails, the agent:
- Logs the error
- Returns error to agent
- Agent decides next step (retry, alternative, or report)

#### 2. Retry Logic

For transient errors:
- Retry with exponential backoff
- Maximum 3 attempts
- Clear error messages

#### 3. Error Recovery

The agent can:
- Try alternative tools
- Simplify the approach
- Ask for clarification
- Report partial results

### Error Flow Example

```
Agent: "Use calculator"
   ↓
Tool: Error (invalid expression)
   ↓
Agent: Receives error
   ↓
Agent: "Try simpler expression"
   ↓
Tool: Success
   ↓
Agent: Returns result
```

## Synchronous vs Asynchronous

### This Implementation: Synchronous

We use synchronous execution because:
- **Simpler** - Easier to understand
- **Predictable** - Clear execution order
- **Educational** - Shows each step clearly

### Synchronous Flow

```
Step 1 → Wait → Complete
           ↓
Step 2 → Wait → Complete
           ↓
Step 3 → Wait → Complete
```

Each step waits for the previous to finish.

### When to Use Async

In production systems, async is better for:
- Multiple parallel tool calls
- Long-running operations
- High concurrency needs

But for learning, synchronous is clearer!

## Tool Composition

### Sequential Composition

Tools can be chained:

```
Calculator → File Writer
   ↓            ↓
  345    →   Save to file
```

**Example:**
"Calculate 15 * 23 and save to file"
1. Call calculator("15 * 23") → 345
2. Call file_ops(write, "result.txt", "345")

### Conditional Composition

Agent decides based on results:

```
Search → If found → Extract → Save
         If not found → Report error
```

### Parallel Composition

(Not in this implementation, but possible with async)

```
Tool A ─┐
Tool B ─┼→ Combine results
Tool C ─┘
```

## Summary

Key takeaways:

1. **Agents** make decisions and orchestrate tool usage
2. **MCP** provides a standard protocol for tool discovery and invocation
3. **Tools** are discrete functions with clear interfaces
4. **State** allows agents to maintain context across interactions
5. **Error handling** ensures robust operation
6. **Synchronous execution** keeps things simple for learning

## Next Steps

- Read the code in `src/agent.py` to see the reasoning loop
- Explore `src/mcp_server.py` to understand the protocol
- Try creating your own tool using the template
- Experiment with different prompts in interactive mode
