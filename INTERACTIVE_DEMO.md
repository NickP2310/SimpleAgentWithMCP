# Interactive Mode Demo

## How to Use Interactive Mode

```bash
python main.py interactive
```

## Example Session

Here's what you'll see when you ask "what is python":

```
🎮 Interactive Mode
Type your prompts below. Type 'exit' or 'quit' to stop.

💬 You: what is python

🤔 Agent received prompt: 'what is python'
🔍 Discovering available tools...
🔧 Discovered 3 tools

📋 Step 1: Analyzing prompt...
   Intent: search

🎯 Step 2: Planning actions...
   Planned: Search for 'python'

🔧 Step 3: Executing tools...
📞 Calling tool 'web_search' with parameters: {'query': 'python'}
✅ Tool returned result

💭 Step 4: Composing response...

✨ Agent completed in 0.00s

============================================================
🤖 AGENT RESPONSE
============================================================
Search results:
Simulated search results for: "python"

1. Introduction to python - Learn the basics
   https://example.com/intro-python

2. Advanced python techniques and best practices
   https://example.com/advanced-python

3. python tutorial for beginners
   https://example.com/tutorial-python

Note: These are simulated results for educational purposes.
============================================================

💬 You: calculate 15 * 23

🤔 Agent received prompt: 'calculate 15 * 23'
🔍 Discovering available tools...
🔧 Discovered 3 tools

📋 Step 1: Analyzing prompt...
   Intent: calculation

🎯 Step 2: Planning actions...
   Planned: Use calculator for '15 * 23'

🔧 Step 3: Executing tools...
📞 Calling tool 'calculator' with parameters: {'expression': '15 * 23'}
✅ Tool returned result

💭 Step 4: Composing response...

✨ Agent completed in 0.00s

============================================================
🤖 AGENT RESPONSE
============================================================
The calculation result is: 345
============================================================

💬 You: exit

👋 Goodbye!
```

## Tips for Interactive Mode

1. **The response is there!** - Look for the section between the `====` lines
2. **Scroll up if needed** - There's a lot of educational output showing the agent's thinking
3. **Try different prompts**:
   - Questions: "what is python", "how to learn AI"
   - Calculations: "calculate 42 * 17"
   - File operations: "calculate 100 / 4 and save to file"

## If You Don't See the Response

The response IS being shown, but there's a lot of output. Here's what to look for:

```
============================================================
🤖 AGENT RESPONSE
============================================================
[YOUR ANSWER IS HERE]
============================================================
```

## Want Less Output?

If you want to see less of the agent's thinking process, you can modify the config:

**config/agent_config.yaml:**
```yaml
logging:
  level: "WARNING"  # Only show warnings and errors
  show_reasoning: false
  show_tool_calls: false
```

Then the output will be much shorter:

```
💬 You: what is python

============================================================
🤖 AGENT RESPONSE
============================================================
Search results:
Simulated search results for: "python"
...
============================================================
```

## Verification

The agent IS working correctly and showing results. The test script confirms:
- ✅ Success: True
- ✅ Result length: 365 characters
- ✅ Tool calls: 1 (web_search)
- ✅ Content blocks: 1 with 349 characters

The response is definitely there - just look for the section with the `====` separators!
