# 🤖 Three Agents to Learn From!

You now have **THREE different agents** - choose the one that fits your needs!

## 🎯 Quick Comparison

| Agent | File | API Key | Cost | Best For |
|-------|------|---------|------|----------|
| **Rule-Based** | `main.py` | ❌ None | Free | Learning architecture |
| **Gemini** | `main_gemini.py` | ✅ Required | Free tier | Learning AI (recommended!) |
| **OpenAI** | `main_llm.py` | ✅ Required | Paid | Production use |

## 🌟 Recommended: Start with Gemini!

**Why Gemini?**
- ✅ Real AI reasoning
- ✅ FREE tier (15 requests/min)
- ✅ No billing required
- ✅ Fast and powerful
- ✅ Perfect for learning

## 🚀 Quick Start: Gemini Agent

### 1. Install Package
```bash
pip install google-genai
```

**Note:** The old `google-generativeai` package is deprecated. Use `google-genai` instead.

### 2. Get API Key
Go to: https://makersuite.google.com/app/apikey
(No credit card needed!)

### 3. Set Environment Variable
```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your-key-here"
```

```bash
# Mac/Linux
export GEMINI_API_KEY="your-key-here"
```

### 4. Run It!
```bash
python main_gemini.py interactive
```

## 📊 Detailed Comparison

### Rule-Based Agent
**Command:** `python main.py interactive`

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

**Best For:** Understanding agent architecture and MCP protocol

---

### Gemini Agent (⭐ Recommended)
**Command:** `python main_gemini.py interactive`

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

**Best For:** Learning real AI behavior without spending money

---

### OpenAI Agent
**Command:** `python main_llm.py interactive`

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

**Best For:** Production applications or if you already have OpenAI credits

## 🎓 Learning Path

### Step 1: Rule-Based (5 minutes)
```bash
python main.py interactive
```
- Understand MCP protocol
- See agent architecture
- Learn tool invocation

### Step 2: Gemini (10 minutes) ⭐
```bash
python main_gemini.py interactive
```
- Experience real AI
- See natural language understanding
- Compare with rule-based

### Step 3: OpenAI (Optional)
```bash
python main_llm.py interactive
```
- Compare different LLMs
- See production-quality AI

## 💡 Example Prompts

Try these with each agent to see the differences:

**Simple:**
```
Calculate 15 * 23
What is Python?
Search for tutorials
```

**Complex:**
```
What is Python and why should I learn it?
Calculate 42 * 17 and explain the math
Search for machine learning and summarize what you find
```

**Very Complex:**
```
Explain the difference between AI and machine learning
Calculate the area of a circle with radius 5 and explain the formula
Search for Python tutorials and recommend the best one for beginners
```

## 📁 Files Overview

**Core Files:**
- `main.py` - Rule-based agent
- `main_gemini.py` - Gemini agent ⭐
- `main_llm.py` - OpenAI agent

**Agent Implementations:**
- `src/agent.py` - Rule-based logic
- `src/gemini_agent.py` - Gemini integration
- `src/llm_agent.py` - OpenAI integration

**Guides:**
- `README.md` - Main project documentation
- `GEMINI_GUIDE.md` - Gemini setup and usage ⭐
- `LLM_AGENT_GUIDE.md` - OpenAI setup and usage
- `README_AGENTS.md` - This file

## 🎯 Which Should I Use?

**For Learning (Recommended):**
1. Start with **Rule-Based** to understand architecture
2. Switch to **Gemini** for real AI experience
3. Compare both to see the difference

**For Production:**
- Use **OpenAI** for best quality
- Or **Gemini** for cost-effective solution

**For Offline/Free:**
- Use **Rule-Based** only

## 💰 Cost Comparison

**Rule-Based:**
- Cost: $0
- Limit: Unlimited

**Gemini:**
- Cost: $0 (free tier)
- Limit: 15 requests/min, 1,500/day
- Perfect for learning!

**OpenAI:**
- Cost: ~$0.0001 per query
- Limit: Based on your billing
- 100 queries ≈ $0.05

## 🐛 Troubleshooting

### Gemini: "No API key"
```bash
export GEMINI_API_KEY="your-key-here"
```
Get key: https://makersuite.google.com/app/apikey

### OpenAI: "No API key"
```bash
export OPENAI_API_KEY="sk-your-key-here"
```
Get key: https://platform.openai.com/api-keys

### "Module not found"
```bash
# For Gemini
pip install google-genai

# For OpenAI
pip install openai

# For both
pip install google-genai openai
```

**Note:** If you have the old `google-generativeai` package, uninstall it first:
```bash
pip uninstall google-generativeai
pip install google-genai
```

## 🎉 Summary

You have three powerful options:

1. **Rule-Based** - Learn the architecture (free, offline)
2. **Gemini** - Experience real AI (free tier, recommended!) ⭐
3. **OpenAI** - Production quality (paid, optional)

**Start with Gemini for the best learning experience!** 🚀

---

## Quick Commands

```bash
# Rule-Based (free, offline)
python main.py interactive

# Gemini (free tier, recommended!)
python main_gemini.py interactive

# OpenAI (paid)
python main_llm.py interactive
```

**Happy learning!** 🎓✨
