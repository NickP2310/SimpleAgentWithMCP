"""Gemini-powered AI Agent using Google's Gemini API.

This agent uses Google's Gemini LLM for real AI reasoning.
Uses the new google.genai SDK (not the deprecated google.generativeai).
"""
import time
from typing import List, Dict, Any
from google import genai
from google.genai import types
from src.models import (
    AgentResponse, ExecutionTrace, ExecutionStep, ToolCall,
    Context, Message, ToolSchema
)
from src.mcp_client import MCPClient


def list_available_models(api_key: str) -> List[str]:
    """
    List all available Gemini models.
    
    Args:
        api_key: Google Gemini API key
        
    Returns:
        List of model names
    """
    client = genai.Client(api_key=api_key)
    models = []
    
    try:
        for model in client.models.list():
            models.append(model.name)
        return models
    except Exception as e:
        print(f"⚠️  Error listing models: {e}")
        return []


class GeminiAgent:
    """AI Agent powered by Google's Gemini LLM."""
    
    def __init__(self, mcp_client: MCPClient, api_key: str, 
                 model: str = "models/gemini-2.5-flash", max_iterations: int = 5):
        """
        Initialize Gemini-powered agent.
        
        Args:
            mcp_client: MCP client for tool access
            api_key: Google Gemini API key
            model: Gemini model to use (models/gemini-2.5-flash is stable and fast)
            max_iterations: Maximum reasoning iterations
        """
        self.mcp_client = mcp_client
        self.model_name = model
        self.max_iterations = max_iterations
        self.context = Context()
        self.execution_trace = ExecutionTrace()
        
        # Configure Gemini client
        self.client = genai.Client(api_key=api_key)
        
        print(f"🤖 Initialized Gemini Agent with model: {model}")
    
    def process_prompt(self, prompt: str) -> AgentResponse:
        """Main entry point for agent execution."""
        print(f"\n🤔 Gemini Agent received prompt: '{prompt}'")
        start_time = time.time()
        
        # Add user message to context
        self.context.conversation_history.append(
            Message(role="user", content=prompt)
        )
        self.context.current_task = prompt
        
        # Discover available tools
        print("🔍 Discovering available tools...")
        self.context.available_tools = self.mcp_client.discover_tools()
        
        # Execute Gemini-powered reasoning loop
        try:
            response = self._gemini_reasoning_loop(prompt)
            duration = time.time() - start_time
            self.execution_trace.total_duration = duration
            
            print(f"\n✨ Gemini Agent completed in {duration:.2f}s")
            return response
        except Exception as e:
            error_msg = f"Gemini Agent execution error: {str(e)}"
            print(f"\n❌ {error_msg}")
            
            # Try to list available models to help debug
            if "not found" in str(e).lower() or "404" in str(e):
                print("\n💡 Listing available models...")
                try:
                    available = list_available_models(self.client.api_key)
                    if available:
                        print("Available models:")
                        for m in available:
                            print(f"  - {m}")
                except:
                    pass
            
            return AgentResponse(
                result="",
                success=False,
                execution_trace=self.execution_trace,
                error=error_msg
            )
    
    def _convert_tools_to_gemini_format(self) -> List[Dict[str, Any]]:
        """Convert MCP tool schemas to Gemini function declarations."""
        function_declarations = []
        
        for tool_schema in self.context.available_tools:
            # Convert JSON Schema to Gemini format
            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }
            
            if "properties" in tool_schema.input_schema:
                parameters["properties"] = tool_schema.input_schema["properties"]
                parameters["required"] = tool_schema.input_schema.get("required", [])
            
            function_declarations.append({
                "name": tool_schema.name,
                "description": tool_schema.description,
                "parameters": parameters
            })
        
        return function_declarations
    
    def _gemini_reasoning_loop(self, prompt: str) -> AgentResponse:
        """Gemini-powered reasoning loop with function calling."""
        tool_calls = []
        
        # Convert tools to Gemini format
        function_declarations = self._convert_tools_to_gemini_format()
        tools = types.Tool(function_declarations=function_declarations)
        config = types.GenerateContentConfig(tools=[tools])
        
        # Build conversation history
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=self._build_system_instruction() + "\n\n" + prompt)]
            )
        ]
        
        print("\n🧠 Asking Gemini to analyze and plan...")
        step_start = time.time()
        
        try:
            # Send request to Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
            
            self.execution_trace.steps.append(ExecutionStep(
                step_number=1,
                step_type="reasoning",
                description="Gemini analyzed prompt and created plan",
                input_data={"prompt": prompt},
                output_data={"response": str(response.text) if response.text else "Function calls requested"},
                duration=time.time() - step_start
            ))
            
            # Check if Gemini wants to call functions
            if response.function_calls and len(response.function_calls) > 0:
                print(f"\n🔧 Gemini decided to use {len(response.function_calls)} tool(s)")
                
                # Execute each function call
                for function_call in response.function_calls:
                    step_start = time.time()
                    
                    tool_name = function_call.name
                    tool_args = dict(function_call.args)
                    
                    print(f"📞 Executing tool: {tool_name}")
                    print(f"   Parameters: {tool_args}")
                    
                    # Execute the tool via MCP
                    tool_call_obj = self._execute_tool(tool_name, tool_args)
                    tool_calls.append(tool_call_obj)
                    
                    # Get result text
                    result_text = ""
                    if tool_call_obj.result and tool_call_obj.result.success:
                        for block in tool_call_obj.result.content:
                            if block.text:
                                result_text = block.text
                                break
                    
                    self.execution_trace.steps.append(ExecutionStep(
                        step_number=len(self.execution_trace.steps) + 1,
                        step_type="tool_call",
                        description=f"Executed tool: {tool_name}",
                        input_data=tool_args,
                        output_data={"result": tool_call_obj.result.to_dict() if tool_call_obj.result else {}},
                        duration=time.time() - step_start
                    ))
                    self.execution_trace.tool_calls_count += 1
                
                # Send function responses back to Gemini
                print("\n💭 Asking Gemini to compose final response...")
                step_start = time.time()
                
                # Append model's response with function calls
                contents.append(response.candidates[0].content)
                
                # Append function responses
                function_response_parts = []
                for tc in tool_calls:
                    result_text = ""
                    if tc.result and tc.result.success:
                        for block in tc.result.content:
                            if block.text:
                                result_text = block.text
                                break
                    
                    function_response_parts.append(
                        types.Part.from_function_response(
                            name=tc.tool_name,
                            response={"result": result_text or "Tool execution failed"}
                        )
                    )
                
                contents.append(
                    types.Content(role="user", parts=function_response_parts)
                )
                
                # Get final response
                final_response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config
                )
                final_result = final_response.text
                
                self.execution_trace.steps.append(ExecutionStep(
                    step_number=len(self.execution_trace.steps) + 1,
                    step_type="reflection",
                    description="Gemini composed final response",
                    input_data={"tool_results": [tc.result.to_dict() if tc.result else {} for tc in tool_calls]},
                    output_data={"response": final_result},
                    duration=time.time() - step_start
                ))
            else:
                # Gemini responded directly without tools
                print("\n💬 Gemini responded directly (no tools needed)")
                final_result = response.text
            
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
            error_msg = f"Gemini reasoning error: {str(e)}"
            print(f"❌ {error_msg}")
            
            # Try to list available models to help debug
            if "not found" in str(e).lower() or "404" in str(e):
                print("\n💡 Listing available models...")
                try:
                    available = list_available_models(self.client.api_key)
                    if available:
                        print("Available models:")
                        for m in available:
                            print(f"  - {m}")
                except:
                    pass
            
            return AgentResponse(
                result="",
                success=False,
                execution_trace=self.execution_trace,
                error=error_msg
            )
    
    def _build_system_instruction(self) -> str:
        """Build system instruction describing the agent's role."""
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
