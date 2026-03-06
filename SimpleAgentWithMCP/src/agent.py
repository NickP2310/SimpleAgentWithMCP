"""AI Agent implementation."""
import time
from datetime import datetime
from typing import List, Dict, Any
from src.models import (
    AgentResponse, ExecutionTrace, ExecutionStep, ToolCall,
    Context, Message, ToolSchema
)
from src.mcp_client import MCPClient


class LearningAgent:
    """Core reasoning engine that processes prompts and orchestrates tool usage."""
    
    def __init__(self, mcp_client: MCPClient, model: str = "gpt-4", max_iterations: int = 5):
        """Initialize agent with MCP client and configuration."""
        self.mcp_client = mcp_client
        self.model = model
        self.max_iterations = max_iterations
        self.context = Context()
        self.execution_trace = ExecutionTrace()
    
    def process_prompt(self, prompt: str) -> AgentResponse:
        """Main entry point for agent execution."""
        print(f"\n🤔 Agent received prompt: '{prompt}'")
        start_time = time.time()
        
        # Add user message to context
        self.context.conversation_history.append(
            Message(role="user", content=prompt)
        )
        self.context.current_task = prompt
        
        # Discover available tools
        print("🔍 Discovering available tools...")
        self.context.available_tools = self.mcp_client.discover_tools()
        
        # Execute reasoning loop
        try:
            response = self._reasoning_loop(prompt)
            duration = time.time() - start_time
            self.execution_trace.total_duration = duration
            
            print(f"\n✨ Agent completed in {duration:.2f}s")
            return response
        except Exception as e:
            error_msg = f"Agent execution error: {str(e)}"
            print(f"\n❌ {error_msg}")
            return AgentResponse(
                result="",
                success=False,
                execution_trace=self.execution_trace,
                error=error_msg
            )
    
    def _reasoning_loop(self, prompt: str) -> AgentResponse:
        """Internal loop: analyze → plan → execute → reflect."""
        tool_calls = []
        
        # Step 1: Analyze the prompt
        print("\n📋 Step 1: Analyzing prompt...")
        step_start = time.time()
        analysis = self._analyze_prompt(prompt)
        self.execution_trace.steps.append(ExecutionStep(
            step_number=1,
            step_type="reasoning",
            description="Analyzed user prompt",
            input_data={"prompt": prompt},
            output_data={"analysis": analysis},
            duration=time.time() - step_start
        ))
        
        # Step 2: Plan actions
        print("\n🎯 Step 2: Planning actions...")
        step_start = time.time()
        plan = self._plan_actions(prompt, analysis)
        self.execution_trace.steps.append(ExecutionStep(
            step_number=2,
            step_type="reasoning",
            description="Created action plan",
            input_data={"analysis": analysis},
            output_data={"plan": plan},
            duration=time.time() - step_start
        ))
        
        # Step 3: Execute tools
        if plan.get("needs_tools"):
            print("\n🔧 Step 3: Executing tools...")
            for tool_action in plan.get("tool_actions", []):
                step_start = time.time()
                tool_call = self._execute_tool(
                    tool_action["tool"],
                    tool_action["parameters"]
                )
                tool_calls.append(tool_call)
                
                self.execution_trace.steps.append(ExecutionStep(
                    step_number=len(self.execution_trace.steps) + 1,
                    step_type="tool_call",
                    description=f"Called tool: {tool_action['tool']}",
                    input_data=tool_action["parameters"],
                    output_data={"result": tool_call.result.to_dict() if tool_call.result else {}},
                    duration=time.time() - step_start
                ))
                self.execution_trace.tool_calls_count += 1
        
        # Step 4: Compose final response
        print("\n💭 Step 4: Composing response...")
        step_start = time.time()
        final_result = self._compose_response(prompt, plan, tool_calls)
        self.execution_trace.steps.append(ExecutionStep(
            step_number=len(self.execution_trace.steps) + 1,
            step_type="reflection",
            description="Composed final response",
            input_data={"plan": plan, "tool_results": [tc.result.to_dict() if tc.result else {} for tc in tool_calls]},
            output_data={"response": final_result},
            duration=time.time() - step_start
        ))
        
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
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze the prompt to understand intent."""
        # Simple rule-based analysis for educational purposes
        prompt_lower = prompt.lower()
        
        analysis = {
            "intent": "unknown",
            "requires_calculation": False,
            "requires_file_ops": False,
            "requires_search": False
        }
        
        # Detect calculation needs
        calc_keywords = ["calculate", "compute", "math", "+", "-", "*", "/", "="]
        if any(kw in prompt_lower for kw in calc_keywords):
            analysis["intent"] = "calculation"
            analysis["requires_calculation"] = True
        
        # Detect file operations
        file_keywords = ["save", "write", "read", "file", "create"]
        if any(kw in prompt_lower for kw in file_keywords):
            analysis["requires_file_ops"] = True
            if analysis["intent"] == "unknown":
                analysis["intent"] = "file_operation"
        
        # Detect search needs
        search_keywords = ["search", "find", "look up", "lookup"]
        if any(kw in prompt_lower for kw in search_keywords):
            analysis["requires_search"] = True
            if analysis["intent"] == "unknown":
                analysis["intent"] = "search"
        
        print(f"   Intent: {analysis['intent']}")
        return analysis
    
    def _plan_actions(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create an action plan based on analysis."""
        plan = {
            "needs_tools": False,
            "tool_actions": []
        }
        
        # Plan calculator usage
        if analysis["requires_calculation"]:
            # Extract expression (simple heuristic)
            import re
            # Look for mathematical expressions
            expr_match = re.search(r'[\d\s+\-*/().]+', prompt)
            if expr_match:
                expression = expr_match.group().strip()
                plan["needs_tools"] = True
                plan["tool_actions"].append({
                    "tool": "calculator",
                    "parameters": {"expression": expression},
                    "reason": "Perform calculation"
                })
                print(f"   Planned: Use calculator for '{expression}'")
        
        # Plan file operations
        if analysis["requires_file_ops"]:
            # Simple heuristic: if "save" or "write", plan a write operation
            if "save" in prompt.lower() or "write" in prompt.lower():
                plan["needs_tools"] = True
                plan["tool_actions"].append({
                    "tool": "file_ops",
                    "parameters": {
                        "operation": "write",
                        "path": "result.txt",
                        "content": "Result will be saved here"
                    },
                    "reason": "Save result to file"
                })
                print(f"   Planned: Write to file")
        
        # Plan search
        if analysis["requires_search"]:
            # Extract search query (simple heuristic)
            query = prompt.replace("search for", "").replace("find", "").strip()
            plan["needs_tools"] = True
            plan["tool_actions"].append({
                "tool": "web_search",
                "parameters": {"query": query},
                "reason": "Search for information"
            })
            print(f"   Planned: Search for '{query}'")
        
        if not plan["needs_tools"]:
            print("   No tools needed - will respond directly")
        
        return plan
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolCall:
        """Execute a single tool."""
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
    
    def _compose_response(self, prompt: str, plan: Dict[str, Any], tool_calls: List[ToolCall]) -> str:
        """Compose final response based on plan and tool results."""
        if not tool_calls:
            return f"I understand you want to: {prompt}. However, I don't have the specific tools needed to complete this task in this demo."
        
        response_parts = []
        
        for tool_call in tool_calls:
            if tool_call.result and tool_call.result.success:
                # Extract text from content blocks
                result_text = ""
                for block in tool_call.result.content:
                    if block.text:
                        result_text = block.text
                        break
                
                if tool_call.tool_name == "calculator":
                    response_parts.append(f"The calculation result is: {result_text}")
                elif tool_call.tool_name == "file_ops":
                    response_parts.append(f"File operation completed: {result_text}")
                elif tool_call.tool_name == "web_search":
                    response_parts.append(f"Search results:\n{result_text}")
            else:
                response_parts.append(f"Tool {tool_call.tool_name} failed: {tool_call.error}")
        
        return "\n\n".join(response_parts)
