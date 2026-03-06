# LLM-Powered Agent Guide

This guide shows you how to use the **real LLM-powered agent** that uses OpenAI's API for actual AI reasoning.

## 🆚 Comparison: Rule-Based vs LLM-Powered

### Rule-Based Agent (Original)
- ✅ No API key needed
- ✅ Works offline
- ✅ Free to use
- ✅ Predictable behavior
- ❌ Limited understanding
- ❌ Keyword matching only
- ❌ Can't handle complex queries

### LLM-Powered Agent (New)
- ✅ Real AI reasoning
- ✅ Natural language understanding
- ✅ Handles complex queries
- ✅ Better tool selection
- ✅ Natural responses
- ❌ Requires API key
- ❌ Costs money (small amount)
- ❌ Needs internet connection

## 🔑 Setup: Get OpenAI API Key

### Step 1: Get API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

### Step 2: Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Or enter it when prompted** - The script will ask for it if not set.

## 🚀 Usage

### Interactive Mode

```bash
python main_llm.py interactive
```

Then try these prompts:

```
💬 You: What is Python and why should I learn it?

💬 You: Calculate 15 * 23 and explain what multiplication means

💬 You: Search for machine learning tutorials and summarize what you find

💬 You: Calculate the area of a circle with radius 5
```

### Single Prompt

```bash
python main_llm.py prompt "What is Python and how do I learn it?"

python main_llm.py prompt "Calculate 42 * 17 and save the result to a file"

python main_llm.py prompt "Explain the difference between AI and machine learning"
```

## 🎯 What Makes It Different?

### Example 1: Complex Question

**Rule-Based Agent:**
```
You: What is Python and why should I learn it?
Agent: I understand you want to: What is Python and why should I learn it?. 
        However, I don't have the specific tools needed to complete this task.
```

**LLM-Powered Agent:**
```
You: What is Python and why should I learn it?
Agent: Python is a high-level, interpreted programming language known for its 
       simplicity and readability. You should learn it because:
       1. Easy to learn for beginners
       2. Versatile - used in web dev, data science, AI, automation
       3. Large community and extensive libraries
       4. High demand in job market
```

### Example 2: Tool Selection

**Rule-Based Agent:**
```
You: Find the square root of 144
Agent: [Doesn't recognize "square root" - no tool used]
```

**LLM-Powered Agent:**
```
You: Find the square root of 144
Agent: [Uses calculator tool with "144 ** 0.5"]
       The square root of 144 is 12.
```

### Example 3: Natural Conversation

**Rule-Based Agent:**
```
You: Calculate 10 + 5
Agent: The calculation result is: 15

You: Now multiply that by 2
Agent: [Doesn't remember previous result]
```

**LLM-Powered Agent:**
```
You: Calculate 10 + 5
Agent: The result is 15.

You: Now multiply that by 2
Agent: [Remembers context] 15 × 2 = 30
```

## 💰 Cost Estimate

Using `gpt-4o-mini` (the cheapest model):
- **Input**: $0.15 per 1M tokens
- **Output**: $0.60 per 1M tokens

**Typical costs:**
- Simple query: ~$0.0001 (less than a penny)
- Complex query with tools: ~$0.0005
- 100 queries: ~$0.05 (5 cents)

**Very affordable for learning!**

## 🔧 How It Works

### 1. LLM Analyzes Prompt

Instead of keyword matching, the LLM:
- Understands natural language
- Identifies user intent
- Considers context from conversation

### 2. LLM Decides on Tools

The LLM sees available tools and decides:
- Which tools to use (if any)
- What parameters to pass
- In what order to call them

### 3. Tools Execute via MCP

Same as before:
- MCP client invokes tools
- Tools execute and return results
- Results go back to LLM

### 4. LLM Composes Response

The LLM:
- Interprets tool results
- Generates natural language response
- Provides helpful explanations

## 📊 Architecture

```
User Prompt
    ↓
LLM (OpenAI API)
    ↓
Decides: Use calculator tool
    ↓
MCP Client → MCP Server → Calculator Tool
    ↓
Result: 345
    ↓
LLM (OpenAI API)
    ↓
Natural Response: "The calculation 15 × 23 equals 345"
```

## 🎓 Learning Benefits

### With Rule-Based Agent
- Learn MCP protocol
- Understand tool architecture
- See agent structure
- No API complexity

### With LLM-Powered Agent
- See real AI reasoning
- Understand LLM integration
- Learn function calling
- Experience production-like behavior

**Use both!** Start with rule-based to understand the architecture, then try LLM-powered to see real AI in action.

## 🐛 Troubleshooting

### "No API key provided"

Set the environment variable:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

Or enter it when prompted.

### "Authentication failed"

Check your API key:
- Starts with `sk-`
- No extra spaces
- Still valid (not revoked)

### "Rate limit exceeded"

You're making too many requests. Wait a minute and try again.

### "Insufficient quota"

Add credits to your OpenAI account at https://platform.openai.com/account/billing

## 🔄 Switching Between Agents

**Rule-Based (Free, Offline):**
```bash
python main.py interactive
```

**LLM-Powered (Real AI, Requires API Key):**
```bash
python main_llm.py interactive
```

## 📝 Example Session

```bash
$ python main_llm.py interactive

============================================================
  AI Agent MCP Learning Project - LLM Powered
  Using OpenAI API for real AI reasoning
============================================================

🚀 Initializing MCP server...
🔌 Connecting MCP client...
✅ Connected to MCP server
🤖 Initialized LLM Agent with model: gpt-4o-mini
🎮 Interactive Mode (LLM-Powered)
Type your prompts below. Type 'exit' or 'quit' to stop.

💬 You: What is Python?

🤔 LLM Agent received prompt: 'What is Python?'
🔍 Discovering available tools...
🔧 Discovered 3 tools

🧠 Asking LLM to analyze and plan...

💬 LLM responded directly (no tools needed)

✨ LLM Agent completed in 1.23s

============================================================
🤖 AGENT RESPONSE
============================================================
Python is a high-level, interpreted programming language created 
by Guido van Rossum in 1991. It's known for its simple, readable 
syntax that emphasizes code readability. Python is versatile and 
used in web development, data science, artificial intelligence, 
automation, and more. Its extensive standard library and active 
community make it one of the most popular programming languages.
============================================================

💬 You: Calculate 15 * 23

🤔 LLM Agent received prompt: 'Calculate 15 * 23'
🔍 Discovering available tools...
🔧 Discovered 3 tools

🧠 Asking LLM to analyze and plan...

🔧 LLM decided to use 1 tool(s)
📞 Executing tool: calculator
   Parameters: {'expression': '15 * 23'}
✅ Tool returned result

💭 Asking LLM to compose final response...

✨ LLM Agent completed in 2.15s

============================================================
🤖 AGENT RESPONSE
============================================================
The result of 15 × 23 is 345.
============================================================

💬 You: exit

👋 Goodbye!
```

## 🎯 Best Practices

1. **Start with rule-based** - Understand the architecture first
2. **Try LLM-powered** - See real AI in action
3. **Compare behaviors** - Notice the differences
4. **Experiment** - Try complex queries with LLM
5. **Monitor costs** - Check your OpenAI usage dashboard

## 🚀 Next Steps

1. Try both agents with the same prompts
2. Notice how LLM handles complex queries better
3. See how LLM composes more natural responses
4. Experiment with conversation context
5. Try queries that require reasoning

**Have fun exploring real AI reasoning!** 🤖✨
