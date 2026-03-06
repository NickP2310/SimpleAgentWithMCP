"""Compare rule-based agent vs LLM-powered agent side by side."""
import os
from src.mcp_server import MCPServer, ToolRegistry
from src.mcp_client import MCPClient
from src.agent import LearningAgent
from src.llm_agent import LLMAgent
from src.tools import CalculatorTool, FileOperationsTool, WebSearchTool


def setup_mcp():
    """Set up MCP server and client."""
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool())
    tool_registry.register(FileOperationsTool())
    tool_registry.register(WebSearchTool())
    
    mcp_server = MCPServer(tool_registry)
    mcp_client = MCPClient(mcp_server)
    mcp_client.connect()
    
    return mcp_client


def test_prompt(prompt: str, use_llm: bool = False):
    """Test a prompt with specified agent."""
    mcp_client = setup_mcp()
    
    if use_llm:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  Set OPENAI_API_KEY to test LLM agent")
            return
        agent = LLMAgent(mcp_client, api_key=api_key, model="gpt-4o-mini")
        agent_type = "LLM-Powered"
    else:
        agent = LearningAgent(mcp_client, max_iterations=5)
        agent_type = "Rule-Based"
    
    print(f"\n{'='*60}")
    print(f"🤖 {agent_type} Agent")
    print(f"{'='*60}")
    print(f"Prompt: {prompt}")
    print()
    
    response = agent.process_prompt(prompt)
    
    print(f"\n{'='*60}")
    print(f"📤 Response:")
    print(f"{'='*60}")
    print(response.result if response.success else f"Error: {response.error}")
    print()
    
    mcp_client.disconnect()


def main():
    """Run comparison tests."""
    print("=" * 60)
    print("  Agent Comparison: Rule-Based vs LLM-Powered")
    print("=" * 60)
    
    test_prompts = [
        "Calculate 15 * 23",
        "What is Python?",
        "Calculate 100 / 4 and explain the result",
    ]
    
    for prompt in test_prompts:
        print(f"\n\n{'#'*60}")
        print(f"# Test Prompt: {prompt}")
        print(f"{'#'*60}")
        
        # Test with rule-based agent
        test_prompt(prompt, use_llm=False)
        
        # Test with LLM agent (if API key available)
        if os.environ.get("OPENAI_API_KEY"):
            test_prompt(prompt, use_llm=True)
        else:
            print("\n⚠️  Set OPENAI_API_KEY environment variable to test LLM agent")
    
    print("\n" + "=" * 60)
    print("Comparison complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
