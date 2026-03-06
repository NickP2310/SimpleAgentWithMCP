"""Main entry point for the AI Agent MCP Learning Project."""
import sys
from src.mcp_server import MCPServer, ToolRegistry
from src.mcp_client import MCPClient
from src.agent import LearningAgent
from src.tools import CalculatorTool, FileOperationsTool, WebSearchTool


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("  AI Agent MCP Learning Project")
    print("  A hands-on educational implementation")
    print("=" * 60)
    print()


def print_trace(agent: LearningAgent):
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


def run_example(example_name: str):
    """Run a predefined example."""
    examples = {
        "simple": "Calculate 15 * 23",
        "moderate": "Calculate 15 * 23 and save result to file",
        "advanced": "Search for Python tutorials"
    }
    
    if example_name not in examples:
        print(f"❌ Unknown example: {example_name}")
        print(f"Available examples: {', '.join(examples.keys())}")
        return
    
    prompt = examples[example_name]
    print(f"\n🎯 Running example: {example_name}")
    print(f"📝 Prompt: {prompt}\n")
    
    run_prompt(prompt)


def run_prompt(prompt: str):
    """Execute a single prompt."""
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
    
    # Initialize agent
    print("🤖 Initializing AI agent...")
    agent = LearningAgent(mcp_client, max_iterations=5)
    
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


def run_interactive():
    """Run interactive mode."""
    print("🎮 Interactive Mode")
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
    
    agent = LearningAgent(mcp_client, max_iterations=5)
    
    while True:
        try:
            prompt = input("\n💬 You: ").strip()
            
            if prompt.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not prompt:
                continue
            
            response = agent.process_prompt(prompt)
            
            print("\n🤖 Agent:", response.result if response.success else f"Error: {response.error}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    
    mcp_client.disconnect()


def main():
    """Main entry point."""
    print_banner()
    
    if len(sys.argv) < 2:
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
    
    command = sys.argv[1].lower()
    
    if command == "interactive":
        run_interactive()
    elif command == "example":
        if len(sys.argv) < 3:
            print("❌ Please specify example name: simple, moderate, or advanced")
            return
        run_example(sys.argv[2])
    elif command == "prompt":
        if len(sys.argv) < 3:
            print("❌ Please provide a prompt")
            return
        prompt = " ".join(sys.argv[2:])
        run_prompt(prompt)
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'interactive', 'example', or 'prompt'")


if __name__ == "__main__":
    main()
