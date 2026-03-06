# Troubleshooting Guide

Common issues and solutions for the AI Agent MCP Learning Project.

## Installation Issues

### Problem: "No module named 'src'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
Make sure you're running commands from the project root directory:
```bash
cd /path/to/SimpleAgentWithMCP
python main.py example simple
```

### Problem: "ModuleNotFoundError: No module named 'openai'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'openai'
```

**Solution:**
Install the required dependencies:
```bash
pip install openai pydantic rich pyyaml
```

Or install from requirements if available:
```bash
pip install -r requirements.txt
```

### Problem: "Permission denied" when installing packages

**Symptoms:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solution:**
Use `--user` flag or a virtual environment:
```bash
# Option 1: Install for current user only
pip install --user openai pydantic rich pyyaml

# Option 2: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install openai pydantic rich pyyaml
```

## Runtime Issues

### Problem: Tool not found

**Symptoms:**
```
❌ Tool call error: Tool not found: my_tool
```

**Solution:**
1. Check that the tool is registered in `main.py`:
```python
tool_registry.register(MyTool())
```

2. Verify the tool name matches exactly (case-sensitive):
```python
@property
def name(self) -> str:
    return "my_tool"  # Must match exactly
```

### Problem: File operation fails

**Symptoms:**
```
❌ Tool call error: Path must be within workspace directory
```

**Solution:**
File operations are restricted to the `workspace/` directory for safety:
```python
# ✅ Correct - relative to workspace
tool.execute(operation="write", path="result.txt", content="data")

# ❌ Wrong - absolute path
tool.execute(operation="write", path="/tmp/result.txt", content="data")
```

### Problem: Calculator returns error

**Symptoms:**
```
❌ Tool call error: Invalid characters in expression
```

**Solution:**
Only basic math operations are allowed:
```python
# ✅ Allowed
"15 * 23"
"(10 + 5) / 3"
"2 ** 8"

# ❌ Not allowed
"import os"  # No imports
"eval('code')"  # No eval
"x = 5"  # No assignments
```

## Configuration Issues

### Problem: Config file not found

**Symptoms:**
```
ℹ️  Config file not found at config/agent_config.yaml, using defaults
```

**Solution:**
This is just informational - the system uses default configuration. To customize:

1. Create the config directory:
```bash
mkdir config
```

2. Create `config/agent_config.yaml`:
```yaml
agent:
  model: "gpt-4"
  max_iterations: 10
  temperature: 0.7
  debug_mode: false

logging:
  level: "INFO"
  show_reasoning: true
  show_tool_calls: true
  show_protocol_messages: false
```

### Problem: Invalid YAML syntax

**Symptoms:**
```
⚠️  Error loading config file: ...
```

**Solution:**
Check YAML syntax:
- Use spaces, not tabs for indentation
- Ensure proper nesting
- Quote strings with special characters

```yaml
# ✅ Correct
agent:
  model: "gpt-4"
  max_iterations: 10

# ❌ Wrong (tabs instead of spaces)
agent:
	model: "gpt-4"
```

## Agent Behavior Issues

### Problem: Agent doesn't use the right tool

**Symptoms:**
Agent uses wrong tool or no tool at all.

**Solution:**
The agent uses simple rule-based reasoning. Make your prompt clearer:

```python
# ❌ Vague
"Do some math"

# ✅ Clear
"Calculate 15 * 23"

# ❌ Ambiguous
"Process this data"

# ✅ Specific
"Calculate the sum of 10 and 20"
```

### Problem: Agent doesn't remember previous context

**Symptoms:**
Agent forgets earlier conversation.

**Solution:**
Context is maintained within a single session. Each run of `main.py` starts fresh:

```bash
# ❌ Separate sessions - no memory between them
python main.py prompt "My name is Alice"
python main.py prompt "What's my name?"  # Won't remember

# ✅ Same session - maintains context
python main.py interactive
> My name is Alice
> What's my name?  # Will remember
```

### Problem: Max iterations exceeded

**Symptoms:**
```
⚠️  Max iterations (10) exceeded
```

**Solution:**
The agent has a safety limit. Increase it in config if needed:

```yaml
agent:
  max_iterations: 20  # Increase from default 10
```

## Tool Development Issues

### Problem: Custom tool not discovered

**Symptoms:**
Agent doesn't see your custom tool.

**Solution:**
1. Ensure tool is registered:
```python
from my_tools import MyCustomTool
tool_registry.register(MyCustomTool())
```

2. Verify tool implements all required methods:
```python
class MyCustomTool(Tool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    @property
    def description(self) -> str:
        return "What it does"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {...}
    
    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(...)
```

### Problem: Tool parameter validation fails

**Symptoms:**
```
❌ Tool call error: Missing required parameter: ...
```

**Solution:**
Check your input schema matches the parameters:

```python
# Schema says "expression" is required
input_schema = {
    "properties": {
        "expression": {"type": "string"}
    },
    "required": ["expression"]
}

# But execute expects "expr"
def execute(self, **kwargs):
    expr = kwargs.get("expr")  # ❌ Wrong parameter name
    
# Fix: Match the schema
def execute(self, **kwargs):
    expression = kwargs.get("expression")  # ✅ Correct
```

## Performance Issues

### Problem: Agent is slow

**Symptoms:**
Takes a long time to respond.

**Solution:**
This is expected for educational purposes:
- Synchronous execution (one step at a time)
- Verbose logging (shows every step)
- No caching or optimization

For faster execution:
```yaml
logging:
  level: "WARNING"  # Reduce logging
  show_reasoning: false
  show_tool_calls: false
```

### Problem: Too much output

**Symptoms:**
Terminal flooded with messages.

**Solution:**
Reduce logging verbosity:

```yaml
logging:
  level: "WARNING"  # Only show warnings and errors
  show_reasoning: false
  show_tool_calls: false
  show_protocol_messages: false
```

## Debugging Tips

### Enable Debug Mode

See detailed internal state:

```yaml
agent:
  debug_mode: true

logging:
  level: "DEBUG"
  show_protocol_messages: true
```

### Check Execution Trace

The execution trace shows exactly what happened:

```
📊 EXECUTION TRACE
Total Duration: 0.05s
Tool Calls: 1
Steps: 4

Step 1: Analyzed user prompt
  Type: reasoning
  Duration: 0.001s
...
```

### Test Tools Independently

Test your tool outside the agent:

```python
# test_my_tool.py
from my_tools import MyCustomTool

tool = MyCustomTool()
result = tool.execute(param="test")
print(f"Success: {result.success}")
print(f"Content: {result.content}")
print(f"Error: {result.error}")
```

### Use Interactive Mode for Experimentation

```bash
python main.py interactive
```

Try different prompts and see immediate results.

## Common Error Messages

### "Connection refused"

**Cause:** MCP server not running (only relevant if using network transport)

**Solution:** In this implementation, server is in-process, so this shouldn't happen. If it does, check your modifications.

### "Invalid JSON"

**Cause:** Malformed MCP message

**Solution:** Check protocol message formatting in your code.

### "Method not found"

**Cause:** Unsupported MCP method

**Solution:** Use supported methods: initialize, tools/list, tools/call, ping

### "Internal error"

**Cause:** Unexpected exception in tool or server

**Solution:** Check the error details and stack trace. Enable debug mode for more info.

## Getting Help

### Check the Documentation

- `README.md` - Project overview and quick start
- `CONCEPTS.md` - Core concepts explained
- `MCP_ARCHITECTURE.md` - Protocol details
- `GETTING_STARTED.md` - Learning guide

### Review the Code

- `src/agent.py` - Agent reasoning logic
- `src/tools.py` - Tool implementations
- `src/mcp_server.py` - MCP protocol server
- `src/mcp_client.py` - MCP protocol client

### Check Examples

- `examples/simple_custom_tool.py` - Basic tool example
- `examples/moderate_custom_tool.py` - Intermediate tool
- `examples/advanced_custom_tool.py` - Complex tool

### Enable Verbose Logging

```yaml
logging:
  level: "DEBUG"
  show_reasoning: true
  show_tool_calls: true
  show_protocol_messages: true
```

## Still Having Issues?

1. **Check Python version**: Requires Python 3.9+
   ```bash
   python --version
   ```

2. **Verify dependencies**: Ensure all packages installed
   ```bash
   pip list | grep -E "openai|pydantic|rich|pyyaml"
   ```

3. **Check file permissions**: Ensure you can read/write in the project directory

4. **Try a fresh start**: Delete `workspace/` and `config/` directories and start over

5. **Review recent changes**: If it was working before, what did you change?

## Quick Fixes Checklist

- [ ] Running from project root directory?
- [ ] All dependencies installed?
- [ ] Python 3.9 or higher?
- [ ] Config files have valid YAML syntax?
- [ ] Tool names match exactly (case-sensitive)?
- [ ] File paths relative to workspace?
- [ ] Tool registered in main.py?
- [ ] Input schema matches execute parameters?

If all else fails, start with the simple example and work your way up:

```bash
python main.py example simple
```

This should always work if the installation is correct!
