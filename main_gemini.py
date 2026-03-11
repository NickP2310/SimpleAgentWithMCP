"""Main entry point for Gemini-powered AI Agent.

This version uses Google's Gemini API for real AI reasoning instead of
rule-based keyword matching. The key differences from main.py:

1. Uses GeminiAgent instead of LearningAgent
2. Requires GEMINI_API_KEY environment variable
3. Provides natural language understanding
4. Can handle complex queries and conversations

Flow: User Input → Gemini Agent → Gemini API → Tool Selection → MCP → Tools

The Gemini agent uses the AI to:
- Understand natural language prompts
- Decide which tools to use
- Generate natural responses
"""
import sys
import os
from src.mcp_server import MCPServer, ToolRegistry
from src.mcp_client import MCPClient
from src.gemini_agent import GeminiAgent
from src.tools import CalculatorTool, FileOperationsTool, WebSearchTool


def print_banner():
    """Print welcome banner.
    
    Shows that this is the Gemini-powered version.
    """
    print("=" * 60)
    print("  AI Agent MCP Learning Project - Gemini Powered")
    print("  Using Google Gemini API for real AI reasoning")
    print("=" * 60)
    print()


def print_trace(agent: GeminiAgent):
    """Print execution trace.
    
    Displays execution statistics for the Gemini agent.
    Similar to the rule-based agent, but shows Gemini-specific steps.
    
    Args:
        agent: Gemini agent instance with execution trace
    """
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
    """Get Gemini API key from environment or user input.
    
    Tries to get the API key from environment variables:
    - GEMINI_API_KEY (preferred)
    - GOOGLE_API_KEY (alternative)
    
    If not found, prompts the user to enter it.
    
    Returns:
        API key string
        
    Exits:
        If no API key is provided
    """
    # Try to get from environment
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        # Not in environment - prompt user
        print("⚠️  Gemini API key not found in environment")
        print("Please set GEMINI_API_KEY environment variable or enter it now:")
        print("Get your key at: https://makersuite.google.com/app/apikey")
        api_key = input("API Key: ").strip()
    
    if not api_key:
        # Still no key - exit
        print("❌ No API key provided. Cannot use Gemini agent.")
        sys.exit(1)
    
    return api_key


def run_prompt(prompt: str, api_key: str):
    """Execute a single prompt with Gemini agent.
    
    Similar to run_prompt() in main.py, but uses GeminiAgent instead
    of LearningAgent. The Gemini agent uses real AI for reasoning.
    
    Args:
        prompt: User's input text
        api_key: Gemini API key
    """
    # Step 1: Initialize MCP server with tools
    print("🚀 Initializing MCP server...")
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool())
    tool_registry.register(FileOperationsTool())
    tool_registry.register(WebSearchTool())
    
    mcp_server = MCPServer(tool_registry)
    
    # Step 2: Initialize MCP client
    print("🔌 Connecting MCP client...")
    mcp_client = MCPClient(mcp_server)
    if not mcp_client.connect():
        print("❌ Failed to connect to MCP server")
        return
    
    # Step 3: Initialize Gemini agent
    # This is the key difference - we use GeminiAgent with real AI
    print("🤖 Initializing Gemini Agent...")
    agent = GeminiAgent(mcp_client, api_key=api_key, model="models/gemini-2.5-flash")
    
    # Step 4: Process prompt through Gemini
    response = agent.process_prompt(prompt)
    
    # Step 5: Display results
    print("\n" + "=" * 60)
    print("📤 AGENT RESPONSE")
    print("=" * 60)
    if response.success:
        print(response.result)
    else:
        print(f"❌ Error: {response.error}")
    
    # Step 6: Display execution trace
    print_trace(agent)
    
    # Step 7: Cleanup
    mcp_client.disconnect()


def run_interactive(api_key: str):
    """Run interactive mode with Gemini agent.
    
    Similar to interactive mode in main.py, but uses Gemini for
    natural language understanding. This allows for:
    - Complex queries
    - Conversational interactions
    - Better tool selection
    
    Args:
        api_key: Gemini API key
    """
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
    
    # Create Gemini agent (reused for all prompts)
    agent = GeminiAgent(mcp_client, api_key=api_key, model="models/gemini-2.5-flash")
    
    # Main interactive loop
    while True:
        try:
            # Get user input
            prompt = input("\n💬 You: ").strip()
            
            # Check for exit commands
            if prompt.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Skip empty prompts
            if not prompt:
                continue
            
            # Process through Gemini agent
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
            # Handle Ctrl+C gracefully
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            # Handle any unexpected errors
            print(f"\n❌ Error: {str(e)}")
    
    # Cleanup
    mcp_client.disconnect()


def main():
    """Main entry point.
    
    Similar to main() in main.py, but:
    1. Gets API key first
    2. Uses Gemini agent instead of rule-based agent
    3. Supports only interactive and prompt modes (no examples)
    """
    print_banner()
    
    # Get API key (required for Gemini)
    api_key = get_api_key()
    
    # Check if user provided command
    if len(sys.argv) < 2:
        # No command - show usage
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
    
    # Parse command
    command = sys.argv[1].lower()
    
    # Route to appropriate handler
    if command == "interactive":
        run_interactive(api_key)
    elif command == "prompt":
        # Validate prompt provided
        if len(sys.argv) < 3:
            print("❌ Please provide a prompt")
            return
        # Join all remaining arguments as the prompt
        prompt = " ".join(sys.argv[2:])
        run_prompt(prompt, api_key)
    else:
        # Unknown command
        print(f"❌ Unknown command: {command}")
        print("Use 'interactive' or 'prompt'")


# Entry point - run main() when script is executed
if __name__ == "__main__":
    main()
