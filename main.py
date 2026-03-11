"""Main entry point for the AI Agent MCP Learning Project.

This file orchestrates the entire system:
1. Sets up the MCP server with available tools
2. Connects the MCP client to the server
3. Initializes the AI agent with the client
4. Processes user prompts through the agent

Flow: User Input → Agent → MCP Client → MCP Server → Tools → Results

The system supports three modes:
- interactive: Chat with the agent
- example: Run predefined examples
- prompt: Execute a single prompt
"""
import sys
from src.mcp_server import MCPServer, ToolRegistry
from src.mcp_client import MCPClient
from src.agent import LearningAgent
from src.tools import CalculatorTool, FileOperationsTool, WebSearchTool


def print_banner():
    """Print welcome banner.
    
    Displays a friendly banner when the program starts.
    """
    print("=" * 60)
    print("  AI Agent MCP Learning Project")
    print("  A hands-on educational implementation")
    print("=" * 60)
    print()


def print_trace(agent: LearningAgent):
    """Print execution trace.
    
    Displays a detailed breakdown of what the agent did:
    - Total execution time
    - Number of tool calls
    - Step-by-step breakdown with timing
    
    This is educational - it helps you understand the agent's reasoning process.
    
    Args:
        agent: Agent instance with execution trace
    """
    trace = agent.execution_trace
    print("\n" + "=" * 60)
    print("📊 EXECUTION TRACE")
    print("=" * 60)
    print(f"Total Duration: {trace.total_duration:.2f}s")
    print(f"Tool Calls: {trace.tool_calls_count}")
    print(f"Steps: {len(trace.steps)}")
    print()
    
    # Print each step with details
    for step in trace.steps:
        print(f"Step {step.step_number}: {step.description}")
        print(f"  Type: {step.step_type}")
        print(f"  Duration: {step.duration:.3f}s")
        print()


def run_example(example_name: str):
    """Run a predefined example.
    
    Provides three example prompts to demonstrate the system:
    - simple: Single tool (calculator)
    - moderate: Multiple tools (calculator + file)
    - advanced: Search tool
    
    Args:
        example_name: Name of example to run
    """
    # Predefined example prompts
    examples = {
        "simple": "Calculate 15 * 23",
        "moderate": "Calculate 15 * 23 and save result to file",
        "advanced": "Search for Python tutorials"
    }
    
    # Validate example name
    if example_name not in examples:
        print(f"❌ Unknown example: {example_name}")
        print(f"Available examples: {', '.join(examples.keys())}")
        return
    
    # Get the prompt and run it
    prompt = examples[example_name]
    print(f"\n🎯 Running example: {example_name}")
    print(f"📝 Prompt: {prompt}\n")
    
    run_prompt(prompt)


def run_prompt(prompt: str):
    """Execute a single prompt.
    
    This function demonstrates the complete agent lifecycle:
    1. Setup: Create server, register tools, connect client
    2. Execution: Agent processes the prompt
    3. Display: Show results and execution trace
    4. Cleanup: Disconnect client
    
    Args:
        prompt: User's input text
    """
    # Step 1: Initialize MCP server with tools
    # The server acts as a registry and executor for all available tools
    print("🚀 Initializing MCP server...")
    tool_registry = ToolRegistry()  # Create empty registry
    tool_registry.register(CalculatorTool())  # Add calculator tool
    tool_registry.register(FileOperationsTool())  # Add file operations tool
    tool_registry.register(WebSearchTool())  # Add search tool
    
    mcp_server = MCPServer(tool_registry)  # Create server with registered tools
    
    # Step 2: Initialize MCP client
    # The client handles communication between agent and server
    print("🔌 Connecting MCP client...")
    mcp_client = MCPClient(mcp_server)  # Create client pointing to server
    if not mcp_client.connect():  # Establish connection
        print("❌ Failed to connect to MCP server")
        return
    
    # Step 3: Initialize agent
    # The agent is the "brain" that decides what to do with the prompt
    print("🤖 Initializing AI agent...")
    agent = LearningAgent(mcp_client, max_iterations=5)  # Create agent with client
    
    # Step 4: Process prompt through the agent
    # This triggers the full reasoning loop: Analyze → Plan → Execute → Reflect
    response = agent.process_prompt(prompt)
    
    # Step 5: Display results
    # Show the final response from the agent
    print("\n" + "=" * 60)
    print("📤 AGENT RESPONSE")
    print("=" * 60)
    if response.success:
        print(response.result)  # Show successful result
    else:
        print(f"❌ Error: {response.error}")  # Show error if something went wrong
    
    # Step 6: Display execution trace
    # This shows the detailed breakdown of what the agent did
    print_trace(agent)
    
    # Step 7: Cleanup
    # Properly disconnect the client from the server
    mcp_client.disconnect()


def run_interactive():
    """Run interactive mode.
    
    In interactive mode, we initialize the components once and reuse them
    for multiple prompts. This is more efficient than recreating everything
    for each prompt.
    
    The user can type prompts and see responses in real-time, similar to
    chatting with ChatGPT or other AI assistants.
    """
    print("🎮 Interactive Mode")
    print("Type your prompts below. Type 'exit' or 'quit' to stop.\n")
    
    # Initialize components once (reused for all prompts)
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool())
    tool_registry.register(FileOperationsTool())
    tool_registry.register(WebSearchTool())
    
    mcp_server = MCPServer(tool_registry)
    mcp_client = MCPClient(mcp_server)
    
    # Connect to server
    if not mcp_client.connect():
        print("❌ Failed to connect to MCP server")
        return
    
    # Create agent (reused for all prompts)
    agent = LearningAgent(mcp_client, max_iterations=5)
    
    # Main interactive loop - keeps running until user exits
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
            
            # Process the prompt through the agent
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
    
    Parses command-line arguments and routes to the appropriate mode:
    - interactive: Start interactive chat mode
    - example <name>: Run a predefined example
    - prompt "<text>": Execute a single prompt
    
    If no arguments provided, displays usage information.
    """
    print_banner()
    
    # Check if user provided command
    if len(sys.argv) < 2:
        # No command - show usage
        print("Usage:")
        print("  python main.py interactive              - Start interactive mode")
        print("  python main.py example <name>           - Run example (simple, moderate, advanced)")
        print("  python main.py prompt \"<your prompt>\"   - Execute single prompt")
        print()
        print("Examples:")
        print("  python main.py interactive")
        print("  python main.py example simple")
        print("  python main.py prompt \"Calculate 42 * 17\"")
        return
    
    # Parse command
    command = sys.argv[1].lower()
    
    # Route to appropriate handler
    if command == "interactive":
        run_interactive()
    elif command == "example":
        # Validate example name provided
        if len(sys.argv) < 3:
            print("❌ Please specify example name: simple, moderate, or advanced")
            return
        run_example(sys.argv[2])
    elif command == "prompt":
        # Validate prompt provided
        if len(sys.argv) < 3:
            print("❌ Please provide a prompt")
            return
        # Join all remaining arguments as the prompt
        prompt = " ".join(sys.argv[2:])
        run_prompt(prompt)
    else:
        # Unknown command
        print(f"❌ Unknown command: {command}")
        print("Use 'interactive', 'example', or 'prompt'")


# Entry point - run main() when script is executed
if __name__ == "__main__":
    main()
