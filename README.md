# 🤖 AI Agent MCP Learning Project

A hands-on educational project to learn how AI agents and the Model Context Protocol (MCP) work. Choose from three different agents to match your learning style and needs!

## 🎯 What You'll Learn

- How AI agents process instructions and make decisions
- How the Model Context Protocol enables tool discovery and invocation
- How agents and tools interact through a client-server architecture
- The difference between rule-based and AI-powered reasoning
- How to integrate real AI (Gemini/OpenAI) into agent systems

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Basic dependencies (for rule-based agent)
pip install pydantic rich pyyaml

# For Gemini agent (recommended!)
pip install google-genai

# For OpenAI agent (optional)
pip install openai
```

### 2. Choose Your Agent

| Agent | Command | API Key | Cost | Best For |
|-------|---------|---------|------|----------|
| **Rule-Based** | `python main.py interactive` | ❌ None | Free | Learning architecture |
| **Gemini** ⭐ | `python main_gemini.py interactive` | ✅ Required | Free tier | Learning AI (recommended!) |
| **OpenAI** | `python main_llm.py interactive` | ✅ Required | Paid | Production use |

### 3. Run Your First Example

**Rule-Based Agent** (no setup needed):
```bash
python main.py example simple
```

**Gemini Agent** (recommended for real AI):
```bash
# Get API key from: https://makersuite.google.com/app/apikey
export GEMINI_API_KEY="your-key-here"
python main_gemini.py interactive
```

---

## 🌟 Three Agents to Choose From

### Rule-Based Agent (Free, Offline)

**Perfect for:** Understanding agent architecture and MCP protocol

**Pros:**
- ✅ No API key needed
- ✅ Works offline
- ✅ Free forever
- ✅ Instant responses
- ✅ Great for learning MCP

**Cons:**
- ❌ Limited understanding (keywords only)
- ❌ Can't handle complex queries
- ❌ Template responses

**Quick Start:**
```bash
python main.py interactive
```

---

### Gemini Agent (Free Tier, Recommended!) ⭐

**Perfect for:** Learning real AI behavior without spending money

**Pros:**
- ✅ Real AI reasoning
- ✅ FREE tier (15 req/min)
- ✅ No billing required
- ✅ Natural language understanding
- ✅ Smart tool selection
- ✅ Fast responses

**Cons:**
- ❌ Requires API key
- ❌ Needs internet
- ❌ Rate limited (15/min on free tier)

**Setup:**

1. Get API key: https://makersuite.google.com/app/apikey (no credit card needed!)

2. Install package:
```bash
pip install google-genai
```

**Note:** The old `google-generativeai` package is deprecated. Use `google-genai` instead.

3. Set environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-key-here"
```

4. Run it:
```bash
python main_gemini.py interactive
```

**Available Models:**
- `models/gemini-2.5-flash` (default) - Fast, free tier, stable
- `models/gemini-2.5-pro` - More powerful, same free tier
- `models/gemini-3-flash-preview` - Newest, experimental

To list all available models:
```bash
python list_gemini_models.py
```

---

### OpenAI Agent (Paid, Production-Ready)

**Perfect for:** Production applications or if you already have OpenAI credits

**Pros:**
- ✅ Excellent reasoning
- ✅ Very consistent
- ✅ Production-ready
- ✅ Well-documented

**Cons:**
- ❌ Requires API key
- ❌ Costs money (~$0.0001/query)
- ❌ Billing required
- ❌ Needs internet

**Setup:**

1. Get API key: https://platform.openai.com/api-keys

2. Install package:
```bash
pip install openai
```

3. Set environment variable:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Mac/Linux
export OPENAI_API_KEY="sk-your-key-here"
```

4. Run it:
```bash
python main_llm.py interactive
```

**Cost Estimate:**
- Simple query: ~$0.0001 (less than a penny)
- Complex query with tools: ~$0.0005
- 100 queries: ~$0.05 (5 cents)

---

## 💡 Example Prompts to Try

### Simple Prompts (All Agents)
```
Calculate 15 * 23
Search for Python tutorials
List files in workspace
```

### Complex Prompts (Gemini/OpenAI Only)
```
What is Python and why should I learn it?
Calculate 42 * 17 and explain the math
Search for machine learning and summarize what you find
Calculate the area of a circle with radius 5 and explain the formula
```

### Very Complex (Gemini/OpenAI Only)
```
Explain the difference between AI and machine learning
Calculate 100 / 4, multiply by 3, and save the result to a file
Search for Python tutorials and recommend the best one for beginners
```

---

## 📁 Project Structure

```
.
├── src/
│   ├── models.py          # Core data models (MCP protocol, agent)
│   ├── tools.py           # Built-in tools (calculator, file ops, search)
│   ├── mcp_server.py      # MCP server implementation
│   ├── mcp_client.py      # MCP client implementation
│   ├── agent.py           # Rule-based agent with reasoning loop
│   ├── gemini_agent.py    # Gemini-powered agent
│   ├── llm_agent.py       # OpenAI-powered agent
│   ├── config.py          # Configuration management
│   └── logging_setup.py   # Educational logging system
├── config/
│   ├── agent_config.yaml  # Agent configuration
│   └── tools_config.yaml  # Tools configuration
├── examples/
│   ├── custom_tool_template.py
│   ├── simple_custom_tool.py
│   ├── moderate_custom_tool.py
│   └── advanced_custom_tool.py
├── docs/
│   ├── CONCEPTS.md        # AI agent and MCP concepts
│   ├── MCP_ARCHITECTURE.md # Protocol details
│   └── TROUBLESHOOTING.md # Common issues and solutions
├── main.py                # Rule-based agent entry point
├── main_gemini.py         # Gemini agent entry point
├── main_llm.py            # OpenAI agent entry point
├── list_gemini_models.py  # Helper to list Gemini models
├── compare_agents.py      # Compare agent behaviors
├── workspace/             # File operations workspace (auto-created)
└── README.md             # This file
```

---

## 🔧 How It Works

### Agent Reasoning Loop

All agents follow a similar cycle:

1. **Analyze** - Understand the user's prompt
2. **Plan** - Decide which tools to use
3. **Execute** - Call the tools via MCP
4. **Reflect** - Compose the final response

**Rule-Based Agent:** Uses keyword matching and templates
**Gemini/OpenAI Agents:** Use real AI for natural language understanding

### MCP Protocol

The Model Context Protocol enables:
- **Tool Discovery** - Agent discovers available tools
- **Tool Invocation** - Agent calls tools with parameters
- **Result Handling** - Agent receives structured results

### Built-in Tools

1. **Calculator** - Performs mathematical calculations
   - Example: `Calculate 15 * 23`

2. **File Operations** - Read, write, and list files
   - Example: `Save result to file`
   - Restricted to `workspace/` directory for safety

3. **Web Search** - Simulated search (for learning)
   - Example: `Search for Python tutorials`

---

## 🎓 Learning Path

### Step 1: Rule-Based Agent (5 minutes)
```bash
python main.py interactive
```
- Understand MCP protocol
- See agent architecture
- Learn tool invocation
- No API needed

### Step 2: Gemini Agent (10 minutes) ⭐ Recommended
```bash
python main_gemini.py interactive
```
- Experience real AI
- See natural language understanding
- Compare with rule-based
- Free tier available

### Step 3: OpenAI Agent (Optional)
```bash
python main_llm.py interactive
```
- Compare different LLMs
- See production-quality AI
- Understand trade-offs

### Step 4: Explore the Code
- Read `src/agent.py` to see reasoning logic
- Read `src/mcp_server.py` to understand MCP
- Read `docs/CONCEPTS.md` for deep dive
- Try creating a custom tool

---

## 📊 Example Output

### Rule-Based Agent
```
$ python main.py interactive

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

### Gemini Agent
```
$ python main_gemini.py interactive

🤖 Initialized Gemini Agent with model: models/gemini-2.5-flash

💬 You: What is Python and why should I learn it?

🤔 Gemini Agent received prompt...
🧠 Asking Gemini to analyze and plan...

💬 Gemini responded directly (no tools needed)

============================================================
🤖 AGENT RESPONSE
============================================================
Python is a high-level, general-purpose programming language 
known for its clear syntax and readability, making it relatively 
easy to learn. Python is widely used in various fields including 
web development, data science, machine learning, scripting, and 
automation.

You should learn Python because:
1. Easy to learn for beginners
2. Versatile - used in many domains
3. Large community and extensive libraries
4. High demand in job market
5. Great for rapid prototyping
============================================================

💬 You: Calculate 15 * 23

🤔 Gemini Agent received prompt...
🧠 Asking Gemini to analyze and plan...

🔧 Gemini decided to use 1 tool(s)
📞 Executing tool: calculator
   Parameters: {'expression': '15 * 23'}
✅ Tool returned result

💭 Asking Gemini to compose final response...

============================================================
🤖 AGENT RESPONSE
============================================================
15 × 23 = 345
============================================================
```

---

## 🆚 Detailed Comparison

### Understanding Complex Queries

**Prompt:** "What is Python and why should I learn it?"

**Rule-Based:**
```
I understand you want to: What is Python and why should I learn it?
However, I don't have the specific tools needed to complete this task.
```

**Gemini/OpenAI:**
```
Python is a high-level programming language known for its simplicity...
You should learn it because:
1. Easy to learn for beginners
2. Versatile - used in web dev, data science, AI
3. Large community and extensive libraries
4. High demand in job market
```

### Tool Selection

**Prompt:** "Find the square root of 144"

**Rule-Based:**
```
[Doesn't recognize "square root" - no tool used]
```

**Gemini/OpenAI:**
```
[Uses calculator tool with "144 ** 0.5"]
The square root of 144 is 12.
```

### Context Awareness

**Conversation:**
```
You: Calculate 10 + 5
Agent: The result is 15.
You: Now multiply that by 2
```

**Rule-Based:**
```
[Doesn't remember previous result]
```

**Gemini/OpenAI:**
```
[Remembers context] 15 × 2 = 30
```

---

## 💰 Cost Comparison

| Agent | Cost | Limit | Best For |
|-------|------|-------|----------|
| **Rule-Based** | $0 | Unlimited | Learning architecture |
| **Gemini** | $0 (free tier) | 15 req/min, 1,500/day | Learning AI |
| **OpenAI** | ~$0.0001/query | Based on billing | Production |

**For Learning: Gemini is perfect!** Free tier is generous and no billing required.

---

## 🔧 Usage Examples

### Interactive Mode

```bash
# Rule-based
python main.py interactive

# Gemini (recommended!)
python main_gemini.py interactive

# OpenAI
python main_llm.py interactive
```

### Run Predefined Examples

```bash
# Simple example (single tool)
python main.py example simple

# Moderate example (multiple tools)
python main.py example moderate

# Advanced example (search)
python main.py example advanced
```

### Single Prompt

```bash
# Rule-based
python main.py prompt "Calculate 42 * 17"

# Gemini
python main_gemini.py prompt "What is Python?"

# OpenAI
python main_llm.py prompt "Explain machine learning"
```

---

## 🎯 Key Features

### Educational Focus
- ✅ Verbose logging shows every step
- ✅ Execution traces explain agent decisions
- ✅ Inline code comments explain concepts
- ✅ Simple synchronous execution model
- ✅ Clear error messages with suggestions

### Three Learning Modes
- ✅ Rule-based for architecture understanding
- ✅ Gemini for real AI (free tier)
- ✅ OpenAI for production-quality AI

### Extensibility
- ✅ Easy to add new tools
- ✅ Template and examples provided
- ✅ Tools auto-discovered by agent
- ✅ Configuration-driven behavior

### Observability
- ✅ Step-by-step execution visualization
- ✅ Tool call highlighting
- ✅ Timing information
- ✅ Debug mode for detailed traces
- ✅ MCP protocol message logging

---

## 🛠️ Creating Custom Tools

### Simple Example

```python
from src.tools import Tool
from src.models import ToolResult

class StringReverser(Tool):
    def __init__(self):
        super().__init__(
            name="string_reverser",
            description="Reverses a string",
            parameters={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to reverse"
                    }
                },
                "required": ["text"]
            }
        )
    
    def execute(self, text: str) -> ToolResult:
        reversed_text = text[::-1]
        return ToolResult(
            tool_name=self.name,
            success=True,
            result=reversed_text
        )
```

See `examples/` directory for more examples!

---

## 🐛 Troubleshooting

### Gemini: "No API key provided"
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-key-here"

# Mac/Linux
export GEMINI_API_KEY="your-key-here"
```
Get key: https://makersuite.google.com/app/apikey

### Gemini: "Module not found: google.genai"
```bash
# Uninstall old package if you have it
pip uninstall google-generativeai

# Install new package
pip install google-genai
```

### Gemini: "Resource exhausted"
You've exceeded the free tier (15 requests/min). Wait a minute and try again.

### OpenAI: "No API key provided"
```bash
export OPENAI_API_KEY="sk-your-key-here"
```
Get key: https://platform.openai.com/api-keys

### OpenAI: "Insufficient quota"
Add credits to your OpenAI account at https://platform.openai.com/account/billing

### "Import errors"
- Make sure you're running from the project root directory
- Ensure all dependencies are installed: `pip install pydantic rich pyyaml`

### "Tool not found"
- Check that the tool is registered in the main file
- Verify the tool name matches exactly

### "File operation errors"
- File operations are restricted to the `workspace/` directory
- The directory is created automatically on first use

For more help, see `docs/TROUBLESHOOTING.md`

---

## 📚 Documentation

- **Main Guide**: This README
- **Concepts**: `docs/CONCEPTS.md` - AI agent and MCP concepts explained
- **Architecture**: `docs/MCP_ARCHITECTURE.md` - Protocol details and implementation
- **Troubleshooting**: `docs/TROUBLESHOOTING.md` - Common issues and solutions

---

## 🎉 What's Implemented

### Core Components
- ✅ AI Agent with reasoning loop (Analyze → Plan → Execute → Reflect)
- ✅ MCP Server (protocol implementation, tool registry)
- ✅ MCP Client (connection management, tool invocation)
- ✅ Three agent types (Rule-based, Gemini, OpenAI)

### Built-in Tools
- ✅ Calculator (safe mathematical expressions)
- ✅ File Operations (read, write, list)
- ✅ Web Search (simulated for learning)

### Features
- ✅ Interactive CLI mode
- ✅ Predefined examples
- ✅ Custom tool support
- ✅ Configuration system
- ✅ Educational logging
- ✅ Execution traces
- ✅ Error handling

---

## 🚀 Next Steps

### Immediate Actions
1. Run all three agents to compare behaviors
2. Try the predefined examples
3. Experiment with different prompts
4. Read the execution traces

### Learning Activities
1. Read `docs/CONCEPTS.md` to understand AI agents
2. Read `docs/MCP_ARCHITECTURE.md` to understand the protocol
3. Explore the code in `src/` directory
4. Try modifying the agent's reasoning logic

### Extension Projects
1. Create a custom tool for your use case
2. Add a new example scenario
3. Modify the agent's planning logic
4. Add new configuration options

---

## 🌟 Why This Project?

This project is designed for learning. It prioritizes:
- **Clarity** over performance
- **Simplicity** over features
- **Education** over production-readiness
- **Observability** over efficiency

Every design decision was made to help you understand how AI agents and MCP work.

---

## 🎓 Learning Outcomes

After working with this project, you will understand:

- ✅ How AI agents make decisions
- ✅ How the Model Context Protocol works
- ✅ How tools are discovered and invoked
- ✅ How agents maintain state and context
- ✅ The difference between rule-based and AI reasoning
- ✅ How to integrate real AI (Gemini/OpenAI) into systems
- ✅ How to create extensible agent architectures

---

## 📝 Notes

- This is an educational implementation focused on clarity
- The rule-based agent uses simple keyword matching (no actual LLM)
- Gemini and OpenAI agents use real AI for reasoning
- All operations are synchronous to keep the execution model simple
- File operations are restricted to the `workspace/` directory for safety

---

## 🏆 Ready to Start?

**Recommended path:**

1. **Start with Rule-Based** (5 min):
   ```bash
   python main.py example simple
   python main.py interactive
   ```

2. **Try Gemini** (10 min):
   ```bash
   # Get free API key: https://makersuite.google.com/app/apikey
   pip install google-genai
   export GEMINI_API_KEY="your-key-here"
   python main_gemini.py interactive
   ```

3. **Compare behaviors** with the same prompts!

4. **Explore the code** in `src/` directory

5. **Create a custom tool** using examples in `examples/`

**Happy learning!** 🎓✨

---

## 📞 Quick Commands Reference

```bash
# Installation
pip install pydantic rich pyyaml google-genai openai

# Rule-Based Agent (free, offline)
python main.py interactive
python main.py example simple
python main.py prompt "Calculate 15 * 23"

# Gemini Agent (free tier, recommended!)
export GEMINI_API_KEY="your-key-here"
python main_gemini.py interactive
python main_gemini.py prompt "What is Python?"
python list_gemini_models.py

# OpenAI Agent (paid)
export OPENAI_API_KEY="sk-your-key-here"
python main_llm.py interactive
python main_llm.py prompt "Explain AI"

# Compare agents
python compare_agents.py
```

---

## License

This is an educational project for learning purposes.
