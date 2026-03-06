# Quick Start Guide

Get your AI agent running in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install openai pydantic rich pyyaml
```

## Step 2: Run Your First Example

```bash
python main.py example simple
```

You should see the agent:
1. Analyze the prompt "Calculate 15 * 23"
2. Plan to use the calculator tool
3. Execute the calculation
4. Return the result: 345

## Step 3: Try Interactive Mode

```bash
python main.py interactive
```

Now try these prompts:
- `Calculate 25 * 4`
- `Calculate 100 / 5 and save result to file`
- `Search for Python tutorials`

Type `exit` to quit.

## What Just Happened?

You just ran a complete AI agent system with:

✅ **MCP Server** - Exposing tools (calculator, file ops, search)
✅ **MCP Client** - Discovering and invoking tools
✅ **AI Agent** - Reasoning about what tools to use
✅ **Execution Trace** - Showing you every step

## Next Steps

1. **Explore the code** - Check out `src/agent.py` to see how the agent thinks
2. **Modify behavior** - Try changing the reasoning logic
3. **Add a tool** - Create your own tool in `src/tools.py`
4. **Read the docs** - See `README.md` for detailed information

## Understanding the Output

When you run an example, you'll see:

```
🤔 Agent received prompt     - Agent starts processing
📋 Step 1: Analyzing         - Understanding the request
🎯 Step 2: Planning          - Deciding which tools to use
🔧 Step 3: Executing         - Calling the tools
💭 Step 4: Composing         - Creating the response
📤 AGENT RESPONSE            - Final result
📊 EXECUTION TRACE           - Detailed breakdown
```

## Common Commands

```bash
# Run examples
python main.py example simple
python main.py example moderate
python main.py example advanced

# Interactive mode
python main.py interactive

# Single prompt
python main.py prompt "Your prompt here"
```

## Troubleshooting

**"No module named 'src'"**
- Make sure you're in the project root directory

**"ModuleNotFoundError: No module named 'openai'"**
- Run: `pip install openai pydantic rich pyyaml`

**Want to see more details?**
- Check the execution trace at the end of each run
- Look at the step-by-step breakdown

---

**Ready to learn more?** Open `README.md` for the full documentation!
