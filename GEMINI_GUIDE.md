# 🌟 Gemini-Powered Agent Guide

Use Google's Gemini AI for real reasoning in your agent!

## 🎯 Why Gemini?

✅ **Generous Free Tier** - 15 requests per minute free!
✅ **Fast** - gemini-2.5-flash is very quick
✅ **Powerful** - Great natural language understanding
✅ **Easy Setup** - Simple API key, no billing required for free tier

## 🚀 Quick Start

### Step 1: Get Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

**No credit card required for free tier!**

### Step 2: Install Gemini Package

```bash
pip install google-genai
```

**Note:** The old `google-generativeai` package is deprecated. Use `google-genai` instead.

### Step 3: Set Environment Variable

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY="your-key-here"
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY="your-key-here"
```

### Step 4: Run It!

```bash
python main_gemini.py interactive
```

## 💡 Usage Examples

### Interactive Mode

```bash
python main_gemini.py interactive
```

Try these prompts:
```
What is Python and why is it popular?
Calculate 15 * 23 and explain the math
Search for machine learning tutorials
Calculate the area of a circle with radius 5
Explain how AI agents work
```

### Single Prompt

```bash
python main_gemini.py prompt "What is Python?"

python main_gemini.py prompt "Calculate 42 * 17 and save to file"

python main_gemini.py prompt "Explain machine learning in simple terms"
```

## 🆚 Comparison: All Three Agents

| Feature | Rule-Based | OpenAI | Gemini |
|---------|-----------|--------|--------|
| **Cost** | Free | ~$0.0001/query | Free (15/min) |
| **API Key** | Not needed | Required | Required |
| **Setup** | None | Billing required | No billing needed |
| **Speed** | Instant | ~1-2s | ~1-2s |
| **Understanding** | Keywords | Excellent | Excellent |
| **Free Tier** | Unlimited | No | 15 requests/min |
| **Best For** | Learning | Production | Learning & Testing |

## 💰 Gemini Pricing

**Free Tier:**
- 15 requests per minute
- 1,500 requests per day
- Perfect for learning!

**Paid Tier** (if you exceed free):
- gemini-2.5-flash: $0.075 per 1M input tokens
- Much cheaper than OpenAI!

## 🎯 Example Session

```bash
$ python main_gemini.py interactive

============================================================
  AI Agent MCP Learning Project - Gemini Powered
  Using Google Gemini API for real AI reasoning
============================================================

🚀 Initializing MCP server...
🔌 Connecting MCP client...
✅ Connected to MCP server
🤖 Initialized Gemini Agent with model: models/gemini-2.5-flash
🎮 Interactive Mode (Gemini-Powered)
Type your prompts below. Type 'exit' or 'quit' to stop.

💬 You: What is Python?

🤔 Gemini Agent received prompt: 'What is Python?'
🔍 Discovering available tools...
🔧 Discovered 3 tools

🧠 Asking Gemini to analyze and plan...

💬 Gemini responded directly (no tools needed)

✨ Gemini Agent completed in 1.15s

============================================================
🤖 AGENT RESPONSE
============================================================
Python is a high-level, general-purpose programming language. 
It's known for its clear syntax and readability, making it 
relatively easy to learn. Python is widely used in various 
fields including web development, data science, machine learning, 
scripting, and automation.
============================================================

💬 You: Calculate 15 * 23

🤔 Gemini Agent received prompt: 'Calculate 15 * 23'
🔍 Discovering available tools...
🔧 Discovered 3 tools

🧠 Asking Gemini to analyze and plan...

🔧 Gemini decided to use 1 tool(s)
📞 Executing tool: calculator
   Parameters: {'expression': '15 * 23'}
✅ Tool returned result

💭 Asking Gemini to compose final response...

✨ Gemini Agent completed in 1.82s

============================================================
🤖 AGENT RESPONSE
============================================================
15 * 23 = 345
============================================================

💬 You: exit

👋 Goodbye!
```

## 🔧 How It Works

1. **User sends prompt** → Gemini Agent
2. **Gemini analyzes** → Understands intent
3. **Gemini decides** → Which tools to use
4. **Tools execute** → Via MCP protocol
5. **Gemini composes** → Natural response

## 📊 Gemini vs OpenAI

**Gemini Advantages:**
- ✅ Free tier (no billing required)
- ✅ 15 requests/min free
- ✅ Fast (gemini-1.5-flash)
- ✅ Good for learning

**OpenAI Advantages:**
- ✅ Slightly better reasoning
- ✅ More consistent
- ✅ Better for production

**For Learning: Gemini is perfect!** 🎓

## 🎓 Learning Path

1. **Start with Rule-Based** (`main.py`)
   - Understand architecture
   - Learn MCP protocol
   - No API needed

2. **Try Gemini** (`main_gemini.py`)
   - Real AI reasoning
   - Free tier
   - Natural language

3. **Compare with OpenAI** (`main_llm.py`) - Optional
   - See differences
   - Understand trade-offs

## 🐛 Troubleshooting

### "No API key provided"

Set environment variable:
```bash
export GEMINI_API_KEY="your-key-here"
```

Or enter when prompted.

### "API key not valid"

- Check you copied the full key
- Get a new key at https://makersuite.google.com/app/apikey

### "Resource exhausted"

You've exceeded the free tier (15 requests/min). Wait a minute and try again.

### "Module not found: google.genai"

Install the package:
```bash
pip install google-genai
```

**Note:** If you have the old `google-generativeai` package, uninstall it first:
```bash
pip uninstall google-generativeai
pip install google-genai
```

## 📚 Available Models

- **models/gemini-2.5-flash** (default) - Fast, free tier, stable
- **models/gemini-2.5-pro** - More powerful, same free tier
- **models/gemini-3-flash-preview** - Newest, experimental
- **models/gemini-2.0-flash** - Also good, stable

To change model, edit `main_gemini.py`:
```python
agent = GeminiAgent(mcp_client, api_key=api_key, model="models/gemini-2.5-pro")
```

To list all available models with your API key:
```bash
python list_gemini_models.py
```

## 🎯 Best Practices

1. **Use models/gemini-2.5-flash** for learning (fast & free)
2. **Stay within free tier** (15 requests/min)
3. **Compare with rule-based** to see the difference
4. **Try complex queries** to see Gemini's power
5. **Use list_gemini_models.py** to see all available models

## 🌟 Gemini Features

- ✅ Function calling (tool use)
- ✅ Natural language understanding
- ✅ Context awareness
- ✅ Multi-turn conversations
- ✅ Fast responses
- ✅ 1 million token context window (gemini-2.5-flash)

## 📝 Example Prompts to Try

**Questions:**
```
What is Python and why is it popular?
Explain machine learning in simple terms
How do AI agents work?
What's the difference between AI and ML?
```

**With Tools:**
```
Calculate 15 * 23 and explain the result
Search for Python tutorials and summarize
Calculate 100 / 4 and save to a file
Find information about neural networks
```

**Complex:**
```
Calculate the area of a circle with radius 5 and explain the formula
Search for AI tutorials and tell me which one is best for beginners
Calculate 42 * 17, then divide by 2, and save the result
```

## 🎉 You're Ready!

Gemini is perfect for learning because:
- ✅ Free tier is generous
- ✅ No billing required
- ✅ Fast and powerful
- ✅ Easy to set up

**Start exploring real AI reasoning with Gemini!** 🚀

---

**Quick Commands:**

```bash
# Install
pip install google-genai

# Set key (Windows PowerShell)
$env:GEMINI_API_KEY="your-key-here"

# Set key (Mac/Linux)
export GEMINI_API_KEY="your-key-here"

# List available models
python list_gemini_models.py

# Run
python main_gemini.py interactive
```
