"""LLM-powered AI Agent using OpenAI API.

This agent uses actual LLM calls for reasoning instead of rule-based logic.
"""
import time
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from openai import OpenAI
from src.models import (
    AgentResponse, ExecutionTrace, ExecutionStep, ToolCall,
    Context, Message, ToolSchema
)
from src.mcp_client import MCPClient


class LLMAgent:
    """AI Agent powered by OpenAI's LLM for real reasoning."""
    
    def __init__(self, mcp_client: MCPClient, api_key: str, 
                 model: str = "gpt-4o-mini", max_iterations: int = 5):
        """
        Initialize LLM-powered agent.
        
        Args:
            mcp_client: MCP client for tool access
            api_key: OpenAI API key
            model: OpenAI model to use (gpt-4o-mini is fast and cheap)
            max_iterations: Maximum reasoning iterations
        """
        self.mcp_client = mcp_client
        self.model = model
        self.max_iterations = max_iterations
        self.context = Context()
        self.execution_trace = ExecutionTrace()
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        print(f"🤖 Initialized LLM Agent with model: {model}")
    
    def process_prompt(self, prompt: str) -> AgentResponse:
        """Main entry point for agent execution."""
        print(f"\n🤔 LLM Agent received prompt: '{prompt}'")
        start_time = time.time()
        
        # Add user message to context
        self.context.conversation_history.append(
            Message(role="user", content=prompt)
        )
        self.context.current_task = prompt
        
        # Discover available tools
        print("🔍 Discovering available tools...")
        self.context.available_tools = self.mcp_client.discover_tools()
        
        # Execute LLM-powered reasoning loop
        try:
            response = self._llm_reasoning_loop(prompt)
            duration = time.time() - start_time
            self.execution_trace.total_duration = duration
            
            print(f"\n✨ LLM Agent completed in {duration:.2f}s")
            return response
        except Exception as e:
            error_msg = f"LLM Agent execution error: {str(e)}"
            print(f"\n❌ {error_msg}")
            return AgentResponse(
                result="",
                success=False,
                execution_trace=self.execution_trace,
                error=error_msg
            )
    
    def _llm_reasoning_loop(self, prompt: str) -> AgentResponse:
        """LLM-powered reasoning loop using OpenAI API."""
        tool_calls = []
        
        # Build system message with available tools
        system_message = self._build_system_message()
        
        # Build conversation messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        print("\n🧠 Asking LLM to analyze and plan...")
        step_start = time.time()
        
        try:
            # Call OpenAI API with function calling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._get_tool_definitions(),
                tool_choice="auto"
            )
            
            self.execution_trace.steps.append(ExecutionStep(
                step_number=1,
                step_type="reasoning",
                description="LLM analyzed prompt and created plan",
                input_data={"prompt": prompt},
                output_data={"response": response.choices[0].message.model_dump()},
                duration=time.time() - step_start
            ))
            
            message = response.choices[0].message
            
            # Check if LLM wants to call tools
            if message.tool_calls:
                print(f"\n🔧 LLM decided to use {len(message.tool_calls)} tool(s)")
                
                # Execute each tool call
                for tool_call_request in message.tool_calls:
                    step_start = time.time()
                    
                    tool_name = tool_call_request.function.name
                    tool_args = json.loads(tool_call_request.function.arguments)
                    
                    print(f"📞 Executing tool: {tool_name}")
                    print(f"   Parameters: {tool_args}")
                    
                    # Execute the tool via MCP
                    tool_call = self._execute_tool(tool_name, tool_args)
                    tool_calls.append(tool_call)
                    
                    self.execution_trace.steps.append(ExecutionStep(
                        step_number=len(self.execution_trace.steps) + 1,
                        step_type="tool_call",
                        description=f"Executed tool: {tool_name}",
                        input_data=tool_args,
                        output_data={"result": tool_call.result.to_dict() if tool_call.result else {}},
                        duration=time.time() - step_start
                    ))
                    self.execution_trace.tool_calls_count += 1
                
                # Ask LLM to compose final response with tool results
                print("\n💭 Asking LLM to compose final response...")
                step_start = time.time()
                
                # Add tool results to conversation
                messages.append(message.model_dump())
                for i, tool_call_request in enumerate(message.tool_calls):
                    tool_result = tool_calls[i].result
                    result_text = ""
                    if tool_result and tool_result.success:
                        for block in tool_result.content:
                            if block.text:
                                result_text = block.text
                                break
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call_request.id,
                        "content": result_text or "Tool execution failed"
                    })
                
                # Get final response from LLM
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                final_result = final_response.choices[0].message.content
                
                self.execution_trace.steps.append(ExecutionStep(
                    step_number=len(self.execution_trace.steps) + 1,
                    step_type="reflection",
                    description="LLM composed final response",
                    input_data={"tool_results": [tc.result.to_dict() if tc.result else {} for tc in tool_calls]},
                    output_data={"response": final_result},
                    duration=time.time() - step_start
                ))
            else:
                # LLM responded directly without tools
                print("\n💬 LLM responded directly (no tools needed)")
                final_result = message.content
            
            # Add assistant message to context
            self.context.conversation_history.append(
                Message(role="assistant", content=final_result, tool_calls=tool_calls)
            )
            
            self.execution_trace.iterations = 1
            
            return AgentResponse(
                result=final_result,
                success=True,
                execution_trace=self.execution_trace,
                tool_calls=tool_calls
            )
        
        except Exception as e:
            error_msg = f"LLM reasoning error: {str(e)}"
            print(f"❌ {error_msg}")
            return AgentResponse(
                result="",
                success=False,
                execution_trace=self.execution_trace,
                error=error_msg
            )
    
    def _build_system_message(self) -> str:
        """Build system message describing the agent's role and available tools."""
        tools_desc = "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in self.context.available_tools
        ])
        
        return f"""You are a helpful AI assistant with access to tools via the Model Context Protocol (MCP).

Available tools:
{tools_desc}

Your job is to:
1. Understand the user's request
2. Decide which tools (if any) to use
3. Use the tools to accomplish the task
4. Provide a clear, helpful response

Be concise and helpful. Use tools when appropriate."""
    
    def _get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Convert MCP tool schemas to OpenAI function calling format."""
        tools = []
        
        for tool_schema in self.context.available_tools:
            tools.append({
                "type": "function",
                "function": {
                    "name": tool_schema.name,
                    "description": tool_schema.description,
                    "parameters": tool_schema.input_schema
                }
            })
        
        return tools
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolCall:
        """Execute a single tool via MCP."""
        start_time = time.time()
        
        result = self.mcp_client.invoke_tool(tool_name, parameters)
        duration = time.time() - start_time
        
        return ToolCall(
            tool_name=tool_name,
            parameters=parameters,
            result=result,
            error=result.error if not result.success else None,
            duration=duration
        )
