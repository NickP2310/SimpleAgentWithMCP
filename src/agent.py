"""AI Agent implementation with reasoning loop.

This is the core "brain" of the system. The agent:
1. Analyzes user prompts to understand intent
2. Plans which tools to use
3. Executes tools via MCP client
4. Composes final responses

Reasoning Loop: Analyze → Plan → Execute → Reflect
"""
import time
from datetime import datetime
from typing import List, Dict, Any
from src.models import (
    AgentResponse, ExecutionTrace, ExecutionStep, ToolCall,
    Context, Message, ToolSchema
)
from src.mcp_client import MCPClient


class LearningAgent:
    """Core reasoning engine that processes prompts and orchestrates tool usage.
    
    This is a rule-based agent (not using real AI) that demonstrates how
    an AI agent would work. It uses keyword matching to understand prompts
    and simple heuristics to decide which tools to use.
    """
    
    def __init__(self, mcp_client: MCPClient, model: str = "gpt-4", max_iterations: int = 5):
        """Initialize agent with MCP client and configuration.
        
        Args:
            mcp_client: Client for communicating with MCP server
            model: Model name (not used in rule-based version)
            max_iterations: Maximum reasoning loop iterations
        """
        self.mcp_client = mcp_client  # Connection to MCP server
        self.model = model  # Model identifier (for future use)
        self.max_iterations = max_iterations  # Safety limit
        self.context = Context()  # Maintains conversation state
        self.execution_trace = ExecutionTrace()  # Records what agent does
    
    def process_prompt(self, prompt: str) -> AgentResponse:
        """Main entry point for agent execution.
        
        This is the top-level function that orchestrates the entire reasoning process.
        It coordinates all the steps and handles errors.
        
        Args:
            prompt: User's input text
            
        Returns:
            AgentResponse with result, success status, and execution trace
        """
        print(f"\n🤔 Agent received prompt: '{prompt}'")
        start_time = time.time()  # Track total execution time
        
        # Add user message to conversation history
        # This maintains context across multiple interactions
        self.context.conversation_history.append(
            Message(role="user", content=prompt)
        )
        self.context.current_task = prompt  # Store current task
        
        # Discover available tools from MCP server
        # The agent needs to know what tools it can use
        print("🔍 Discovering available tools...")
        self.context.available_tools = self.mcp_client.discover_tools()
        
        # Execute reasoning loop (the main logic)
        try:
            response = self._reasoning_loop(prompt)  # Do the actual work
            duration = time.time() - start_time  # Calculate total time
            self.execution_trace.total_duration = duration
            
            print(f"\n✨ Agent completed in {duration:.2f}s")
            return response
        except Exception as e:
            # Handle any errors that occur during execution
            error_msg = f"Agent execution error: {str(e)}"
            print(f"\n❌ {error_msg}")
            return AgentResponse(
                result="",
                success=False,
                execution_trace=self.execution_trace,
                error=error_msg
            )
    
    def _reasoning_loop(self, prompt: str) -> AgentResponse:
        """Internal loop: analyze → plan → execute → reflect.
        
        This is the core reasoning cycle that all AI agents follow:
        1. ANALYZE: Understand what the user wants
        2. PLAN: Decide which tools to use and how
        3. EXECUTE: Call the tools via MCP
        4. REFLECT: Compose the final response
        
        Args:
            prompt: User's input text
            
        Returns:
            AgentResponse with the final result
        """
        tool_calls = []  # Track all tool invocations
        
        # STEP 1: ANALYZE - Understand the prompt
        # Figure out what the user is asking for
        print("\n📋 Step 1: Analyzing prompt...")
        step_start = time.time()
        analysis = self._analyze_prompt(prompt)  # Extract intent and requirements
        self.execution_trace.steps.append(ExecutionStep(
            step_number=1,
            step_type="reasoning",
            description="Analyzed user prompt",
            input_data={"prompt": prompt},
            output_data={"analysis": analysis},
            duration=time.time() - step_start
        ))
        
        # STEP 2: PLAN - Decide which tools to use
        # Based on the analysis, create an action plan
        print("\n🎯 Step 2: Planning actions...")
        step_start = time.time()
        plan = self._plan_actions(prompt, analysis)  # Create execution plan
        self.execution_trace.steps.append(ExecutionStep(
            step_number=2,
            step_type="reasoning",
            description="Created action plan",
            input_data={"analysis": analysis},
            output_data={"plan": plan},
            duration=time.time() - step_start
        ))
        
        # STEP 3: EXECUTE - Call the tools
        # If the plan requires tools, execute them via MCP
        if plan.get("needs_tools"):
            print("\n🔧 Step 3: Executing tools...")
            for tool_action in plan.get("tool_actions", []):
                step_start = time.time()
                # Call the tool via MCP client
                tool_call = self._execute_tool(
                    tool_action["tool"],  # Tool name
                    tool_action["parameters"]  # Tool parameters
                )
                tool_calls.append(tool_call)  # Record the call
                
                # Add to execution trace for debugging
                self.execution_trace.steps.append(ExecutionStep(
                    step_number=len(self.execution_trace.steps) + 1,
                    step_type="tool_call",
                    description=f"Called tool: {tool_action['tool']}",
                    input_data=tool_action["parameters"],
                    output_data={"result": tool_call.result.to_dict() if tool_call.result else {}},
                    duration=time.time() - step_start
                ))
                self.execution_trace.tool_calls_count += 1  # Increment counter
        
        # STEP 4: REFLECT - Compose final response
        # Take all the tool results and create a human-readable response
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
        
        # Add assistant message to conversation history
        # This maintains context for future interactions
        self.context.conversation_history.append(
            Message(role="assistant", content=final_result, tool_calls=tool_calls)
        )
        
        self.execution_trace.iterations = 1  # Track iterations
        
        # Return the final response
        return AgentResponse(
            result=final_result,
            success=True,
            execution_trace=self.execution_trace,
            tool_calls=tool_calls
        )
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze the prompt to understand intent.
        
        This is a simple rule-based analyzer that uses keyword matching.
        A real AI agent would use an LLM here to understand natural language.
        
        Args:
            prompt: User's input text
            
        Returns:
            Dictionary with intent and requirements
        """
        # Simple rule-based analysis for educational purposes
        prompt_lower = prompt.lower()  # Case-insensitive matching
        
        # Initialize analysis result
        analysis = {
            "intent": "unknown",  # What does the user want?
            "requires_calculation": False,  # Need calculator?
            "requires_file_ops": False,  # Need file operations?
            "requires_search": False  # Need web search?
        }
        
        # Detect calculation needs by looking for math keywords
        calc_keywords = ["calculate", "compute", "math", "+", "-", "*", "/", "="]
        if any(kw in prompt_lower for kw in calc_keywords):
            analysis["intent"] = "calculation"
            analysis["requires_calculation"] = True
        
        # Detect file operations by looking for file keywords
        file_keywords = ["save", "write", "read", "file", "create"]
        if any(kw in prompt_lower for kw in file_keywords):
            analysis["requires_file_ops"] = True
            if analysis["intent"] == "unknown":
                analysis["intent"] = "file_operation"
        
        # Detect search needs by looking for search keywords
        search_keywords = ["search", "find", "look up", "lookup"]
        if any(kw in prompt_lower for kw in search_keywords):
            analysis["requires_search"] = True
            if analysis["intent"] == "unknown":
                analysis["intent"] = "search"
        
        print(f"   Intent: {analysis['intent']}")
        return analysis
    
    def _plan_actions(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create an action plan based on analysis.
        
        This function decides which tools to use and with what parameters.
        A real AI agent would use an LLM to create more sophisticated plans.
        
        Args:
            prompt: User's input text
            analysis: Result from _analyze_prompt
            
        Returns:
            Dictionary with execution plan
        """
        plan = {
            "needs_tools": False,  # Do we need to call any tools?
            "tool_actions": []  # List of tools to call
        }
        
        # Plan calculator usage if calculation is needed
        if analysis["requires_calculation"]:
            # Extract expression using simple regex
            import re
            # Look for mathematical expressions (numbers and operators)
            expr_match = re.search(r'[\d\s+\-*/().]+', prompt)
            if expr_match:
                expression = expr_match.group().strip()
                plan["needs_tools"] = True
                plan["tool_actions"].append({
                    "tool": "calculator",  # Tool name
                    "parameters": {"expression": expression},  # Tool parameters
                    "reason": "Perform calculation"  # Why we're calling it
                })
                print(f"   Planned: Use calculator for '{expression}'")
        
        # Plan file operations if file work is needed
        if analysis["requires_file_ops"]:
            # Simple heuristic: if "save" or "write", plan a write operation
            if "save" in prompt.lower() or "write" in prompt.lower():
                plan["needs_tools"] = True
                plan["tool_actions"].append({
                    "tool": "file_ops",
                    "parameters": {
                        "operation": "write",
                        "path": "result.txt",  # Default filename
                        "content": "Result will be saved here"  # Placeholder
                    },
                    "reason": "Save result to file"
                })
                print(f"   Planned: Write to file")
        
        # Plan search if search is needed
        if analysis["requires_search"]:
            # Extract search query by removing search keywords
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
        """Execute a single tool via MCP client.
        
        This function calls a tool through the MCP protocol and records
        the result along with timing information.
        
        Args:
            tool_name: Name of the tool to call
            parameters: Parameters to pass to the tool
            
        Returns:
            ToolCall object with result and metadata
        """
        start_time = time.time()  # Track execution time
        
        # Call the tool via MCP client
        # The client handles the protocol communication with the server
        result = self.mcp_client.invoke_tool(tool_name, parameters)
        duration = time.time() - start_time  # Calculate how long it took
        
        # Return a ToolCall object with all the details
        return ToolCall(
            tool_name=tool_name,
            parameters=parameters,
            result=result,
            error=result.error if not result.success else None,
            duration=duration
        )
    
    def _compose_response(self, prompt: str, plan: Dict[str, Any], tool_calls: List[ToolCall]) -> str:
        """Compose final response based on plan and tool results.
        
        This function takes all the tool results and creates a human-readable
        response. A real AI agent would use an LLM to generate natural language.
        
        Args:
            prompt: Original user prompt
            plan: Execution plan that was created
            tool_calls: List of tool calls that were executed
            
        Returns:
            Human-readable response string
        """
        # If no tools were called, return a default message
        if not tool_calls:
            return f"I understand you want to: {prompt}. However, I don't have the specific tools needed to complete this task in this demo."
        
        response_parts = []  # Build response from multiple parts
        
        # Process each tool call result
        for tool_call in tool_calls:
            if tool_call.result and tool_call.result.success:
                # Extract text from content blocks
                result_text = ""
                for block in tool_call.result.content:
                    if block.text:
                        result_text = block.text
                        break
                
                # Format response based on which tool was called
                if tool_call.tool_name == "calculator":
                    response_parts.append(f"The calculation result is: {result_text}")
                elif tool_call.tool_name == "file_ops":
                    response_parts.append(f"File operation completed: {result_text}")
                elif tool_call.tool_name == "web_search":
                    response_parts.append(f"Search results:\n{result_text}")
            else:
                # Tool call failed - include error message
                response_parts.append(f"Tool {tool_call.tool_name} failed: {tool_call.error}")
        
        # Join all parts with double newlines for readability
        return "\n\n".join(response_parts)
