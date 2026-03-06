"""Main entry point for Gemini-powered AI Agent.

This version uses Google's Gemini API for real AI reasoning.
"""
import sys
import os
from src.mcp_server import MCPServer, ToolRegistry
from src.mcp_client import MCPClient
from src.gemini_agent import GeminiAgent
from src.tools import CalculatorTool, FileOperationsTool, WebSearchTool


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("  AI Agent MCP Learning Project - Gemini Powered")
    print("  Using Google Gemini API for real AI reasoning")
    print("=" * 60)
    print()


def print_trace(agent: GeminiAgent):
    """Print execution trace."""
    trace = agent.execution_trace
    print("\n" + "=" * 60)
    print("📊 EXECUTION TRACE")
    print("=" * 60)
    print(f"Total Duration: {trace.total_duration:.2f}s")
    print(f"Tool Calls: {trace.tool_calls_count}")
    print(f"Steps: {len(trace.steps)}")
    print()
    
    for step in trace.steps:
        print(f"Step {step.step_number}: {step.description}")
        print(f"  Type: {step.step_type}")
        print(f"  Duration: {step.duration:.3f}s")
        print()


def get_api_key() -> str:
    """Get Gemini API key from environment or user input."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        print("⚠️  Gemini API key not found in environment")
        print("Please set GEMINI_API_KEY environment variable or enter it now:")
        print("Get your key at: https://makersuite.google.com/app/apikey")
        api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Cannot use Gemini agent.")
        sys.exit(1)
    
    return api_key


def run_prompt(prompt: str, api_key: str):
    """Execute a single prompt with Gemini agent."""
    # Initialize MCP server with tools
    print("🚀 Initializing MCP server...")
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool())
    tool_registry.register(FileOperationsTool())
    tool_registry.register(WebSearchTool())
    
    mcp_server = MCPServer(tool_registry)
    
    # Initialize MCP client
    print("🔌 Connecting MCP client...")
    mcp_client = MCPClient(mcp_server)
    if not mcp_client.connect():
        print("❌ Failed to connect to MCP server")
        return
    
    # Initialize Gemini agent
    print("🤖 Initializing Gemini Agent...")
    agent = GeminiAgent(mcp_client, api_key=api_key, model="models/gemini-2.5-flash")
    
    # Process prompt
    response = agent.process_prompt(prompt)
    
    # Display results
    print("\n" + "=" * 60)
    print("📤 AGENT RESPONSE")
    print("=" * 60)
    if response.success:
        print(response.result)
    else:
        print(f"❌ Error: {response.error}")
    
    # Display execution trace
    print_trace(agent)
    
    # Cleanup
    mcp_client.disconnect()


def run_interactive(api_key: str):
    """Run interactive mode with Gemini agent."""
    print("🎮 Interactive Mode (Gemini-Powered)")
    print("Type your prompts below. Type 'exit' or 'quit' to stop.\n")
    
    # Initialize components once
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool())
    tool_registry.register(FileOperationsTool())
    tool_registry.register(WebSearchTool())
    
    mcp_server = MCPServer(tool_registry)
    mcp_client = MCPClient(mcp_server)
    
    if not mcp_client.connect():
        print("❌ Failed to connect to MCP server")
        return
    
    agent = GeminiAgent(mcp_client, api_key=api_key, model="models/gemini-2.5-flash")
    
    while True:
        try:
            prompt = input("\n💬 You: ").strip()
            
            if prompt.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not prompt:
                continue
            
            response = agent.process_prompt(prompt)
            
            # Display agent response with clear formatting
            print("\n" + "=" * 60)
            print("🤖 AGENT RESPONSE")
            print("=" * 60)
            if response.success:
                print(response.result)
            else:
                print(f"❌ Error: {response.error}")
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    
    mcp_client.disconnect()


def main():
    """Main entry point."""
    print_banner()
    
    # Get API key
    api_key = get_api_key()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main_gemini.py interactive              - Start interactive mode")
        print("  python main_gemini.py prompt \"<your prompt>\"   - Execute single prompt")
        print()
        print("Examples:")
        print("  python main_gemini.py interactive")
        print("  python main_gemini.py prompt \"What is Python and how do I learn it?\"")
        print("  python main_gemini.py prompt \"Calculate 42 * 17 and explain the result\"")
        print()
        print("Note: Requires GEMINI_API_KEY environment variable")
        print("Get your key at: https://makersuite.google.com/app/apikey")
        return
    
    command = sys.argv[1].lower()
    
    if command == "interactive":
        run_interactive(api_key)
    elif command == "prompt":
        if len(sys.argv) < 3:
            print("❌ Please provide a prompt")
            return
        prompt = " ".join(sys.argv[2:])
        run_prompt(prompt, api_key)
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'interactive' or 'prompt'")


if __name__ == "__main__":
    main()
