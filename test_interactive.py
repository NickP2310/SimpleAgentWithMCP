"""Test script to verify interactive mode behavior."""
from src.mcp_server import MCPServer, ToolRegistry
from src.mcp_client import MCPClient
from src.agent import LearningAgent
from src.tools import CalculatorTool, FileOperationsTool, WebSearchTool

# Initialize components
tool_registry = ToolRegistry()
tool_registry.register(CalculatorTool())
tool_registry.register(FileOperationsTool())
tool_registry.register(WebSearchTool())

mcp_server = MCPServer(tool_registry)
mcp_client = MCPClient(mcp_server)

if not mcp_client.connect():
    print("❌ Failed to connect to MCP server")
    exit(1)

agent = LearningAgent(mcp_client, max_iterations=5)

# Test prompt
prompt = "what is python"
print(f"\n💬 You: {prompt}")

response = agent.process_prompt(prompt)

print(f"\n🤖 Agent: {response.result if response.success else f'Error: {response.error}'}")
print(f"\nSuccess: {response.success}")
print(f"Result length: {len(response.result)}")
print(f"Tool calls: {len(response.tool_calls)}")

if response.tool_calls:
    for tc in response.tool_calls:
        print(f"\nTool: {tc.tool_name}")
        print(f"Success: {tc.result.success if tc.result else 'No result'}")
        if tc.result and tc.result.content:
            print(f"Content blocks: {len(tc.result.content)}")
            for block in tc.result.content:
                print(f"  Block type: {block.type}")
                print(f"  Block text length: {len(block.text) if block.text else 0}")

mcp_client.disconnect()
