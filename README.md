# AI Agent MCP Learning Project

A hands-on educational project to learn how AI agents and the Model Context Protocol (MCP) work.

## What You'll Learn

- How AI agents process instructions and make decisions
- How the Model Context Protocol enables tool discovery and invocation
- How agents and tools interact through a client-server architecture

## Quick Start

### 1. Install Dependencies

```bash
pip install openai pydantic rich pyyaml
```

### 2. Run Examples

**Simple Example** (single tool):
```bash
python main.py example simple
```

**Moderate Example** (multiple tools):
```bash
python main.py example moderate
```

**Advanced Example** (search):
```bash
python main.py example advanced
```

### 3. Try Interactive Mode

```bash
python main.py interactive
```

Then type prompts like:
- "Calculate 25 * 4"
- "Calculate 100 / 5 and save result to file"
- "Search for machine learning tutorials"

### 4. Run Custom Prompts

```bash
python main.py prompt "Calculate 42 * 17"
```

## Project Structure

```
.
├── src/
│   ├── models.py          # Core data models (MCP protocol, agent)
│   ├── tools.py           # Built-in tools (calculator, file ops, search)
│   ├── mcp_server.py      # MCP server implementation
│   ├── mcp_client.py      # MCP client implementation
│   └── agent.py           # AI agent with reasoning loop
├── main.py                # CLI entry point
├── workspace/             # File operations workspace (auto-created)
└── README.md             # This file
```

## How It Works

### 1. Agent Reasoning Loop

The agent follows a simple cycle:
1. **Analyze** - Understand the user's prompt
2. **Plan** - Decide which tools to use
3. **Execute** - Call the tools via MCP
4. **Reflect** - Compose the final response

### 2. MCP Protocol

The Model Context Protocol enables:
- **Tool Discovery** - Agent discovers available tools
- **Tool Invocation** - Agent calls tools with parameters
- **Result Handling** - Agent receives structured results

### 3. Built-in Tools

- **Calculator** - Performs mathematical calculations
- **File Operations** - Read, write, and list files
- **Web Search** - Simulated search (for learning)

## Example Output

```
🤖 Initializing AI agent...
🤔 Agent received prompt: 'Calculate 15 * 23'

📋 Step 1: Analyzing prompt...
   Intent: calculation

🎯 Step 2: Planning actions...
   Planned: Use calculator for '15 * 23'

🔧 Step 3: Executing tools...
📞 Calling tool 'calculator' with parameters: {'expression': '15 * 23'}
✅ Tool returned result

💭 Step 4: Composing response...

📤 AGENT RESPONSE
The calculation result is: 345

📊 EXECUTION TRACE
Total Duration: 0.05s
Tool Calls: 1
Steps: 4
```

## Learning Path

1. **Start with examples** - Run the predefined examples to see the system in action
2. **Try interactive mode** - Experiment with your own prompts
3. **Read the code** - Explore `src/` to understand how each component works
4. **Modify behavior** - Try changing the agent's reasoning logic
5. **Add custom tools** - Create your own tools by extending the `Tool` class

## Key Concepts

### Agent
An agent is a program that:
- Receives instructions (prompts)
- Makes decisions about what to do
- Uses tools to accomplish tasks
- Returns results to the user

### MCP (Model Context Protocol)
A protocol that standardizes how agents discover and use tools:
- **Server** - Exposes tools and handles requests
- **Client** - Discovers tools and invokes them
- **Protocol** - JSON-RPC based message format

### Tools
Discrete functions that agents can invoke:
- Each tool has a name, description, and parameter schema
- Tools execute operations and return structured results
- Tools can be added dynamically

## Next Steps

- Explore the code in `src/` directory
- Try modifying the agent's reasoning logic in `src/agent.py`
- Create a custom tool by extending the `Tool` class in `src/tools.py`
- Experiment with different prompts in interactive mode

## Notes

- This is an educational implementation focused on clarity over performance
- The agent uses simple rule-based reasoning (no actual LLM calls in this demo)
- All operations are synchronous to keep the execution model simple
- File operations are restricted to the `workspace/` directory for safety

## Troubleshooting

**Import errors?**
- Make sure you're running from the project root directory
- Ensure all dependencies are installed: `pip install openai pydantic rich pyyaml`

**Tool not found?**
- Check that the tool is registered in `main.py`
- Verify the tool name matches exactly

**File operation errors?**
- File operations are restricted to the `workspace/` directory
- The directory is created automatically on first use

## License

This is an educational project for learning purposes.
