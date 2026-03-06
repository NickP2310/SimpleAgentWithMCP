"""Educational logging system with rich formatting."""
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from src.models import ExecutionTrace, ExecutionStep
from typing import Optional

console = Console()


class EducationalLogger:
    """Logger with educational formatting and emoji prefixes."""
    
    def __init__(self, level: str = "INFO", show_reasoning: bool = True, 
                 show_tool_calls: bool = True, show_protocol: bool = False):
        """Initialize logger with configuration."""
        self.level = getattr(logging, level.upper(), logging.INFO)
        self.show_reasoning = show_reasoning
        self.show_tool_calls = show_tool_calls
        self.show_protocol = show_protocol
        
        # Set up Python logging
        logging.basicConfig(
            level=self.level,
            format='%(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def info(self, message: str, emoji: str = "ℹ️"):
        """Log info message with emoji."""
        if self.level <= logging.INFO:
            console.print(f"{emoji}  {message}")
    
    def debug(self, message: str, emoji: str = "🔍"):
        """Log debug message with emoji."""
        if self.level <= logging.DEBUG:
            console.print(f"{emoji}  {message}", style="dim")
    
    def warning(self, message: str, emoji: str = "⚠️"):
        """Log warning message with emoji."""
        if self.level <= logging.WARNING:
            console.print(f"{emoji}  {message}", style="yellow")
    
    def error(self, message: str, emoji: str = "❌"):
        """Log error message with emoji."""
        if self.level <= logging.ERROR:
            console.print(f"{emoji}  {message}", style="bold red")
    
    def success(self, message: str, emoji: str = "✅"):
        """Log success message with emoji."""
        if self.level <= logging.INFO:
            console.print(f"{emoji}  {message}", style="green")
    
    def reasoning(self, message: str):
        """Log reasoning step."""
        if self.show_reasoning:
            console.print(f"🤔  {message}", style="cyan")
    
    def tool_call(self, tool_name: str, parameters: dict):
        """Log tool invocation."""
        if self.show_tool_calls:
            console.print(f"🔧  Calling tool: [bold]{tool_name}[/bold]")
            console.print(f"   Parameters: {parameters}", style="dim")
    
    def tool_result(self, success: bool, result: str):
        """Log tool result."""
        if self.show_tool_calls:
            if success:
                console.print(f"✅  Tool succeeded: {result[:100]}...", style="green")
            else:
                console.print(f"❌  Tool failed: {result}", style="red")
    
    def protocol_message(self, direction: str, message: dict):
        """Log MCP protocol message."""
        if self.show_protocol:
            console.print(f"📡  {direction}: {message}", style="dim")


def display_execution_trace(trace: ExecutionTrace, title: str = "Execution Trace"):
    """Display execution trace with rich formatting."""
    console.print()
    console.print(Panel.fit(
        f"[bold]📊 {title}[/bold]\n\n"
        f"Total Duration: {trace.total_duration:.3f}s\n"
        f"Tool Calls: {trace.tool_calls_count}\n"
        f"Iterations: {trace.iterations}\n"
        f"Steps: {len(trace.steps)}",
        border_style="blue"
    ))
    
    # Create tree visualization
    tree = Tree("🎯 Execution Flow")
    
    for step in trace.steps:
        step_emoji = {
            "reasoning": "🤔",
            "tool_call": "🔧",
            "reflection": "💭"
        }.get(step.step_type, "📍")
        
        step_node = tree.add(
            f"{step_emoji} Step {step.step_number}: {step.description} "
            f"[dim]({step.duration:.3f}s)[/dim]"
        )
        
        # Add details for tool calls
        if step.step_type == "tool_call" and step.output_data:
            result = step.output_data.get("result", {})
            if result.get("success"):
                step_node.add("✅ Success")
            else:
                step_node.add(f"❌ Error: {result.get('error', 'Unknown')}")
    
    console.print(tree)
    console.print()


def display_step_details(step: ExecutionStep):
    """Display detailed information about a single step."""
    table = Table(title=f"Step {step.step_number}: {step.description}")
    
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Type", step.step_type)
    table.add_row("Duration", f"{step.duration:.3f}s")
    table.add_row("Timestamp", step.timestamp.strftime("%H:%M:%S.%f")[:-3])
    
    if step.input_data:
        table.add_row("Input", str(step.input_data)[:100])
    
    if step.output_data:
        table.add_row("Output", str(step.output_data)[:100])
    
    console.print(table)


def display_welcome_banner():
    """Display welcome banner."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]AI Agent MCP Learning Project[/bold cyan]\n"
        "[dim]A hands-on educational implementation[/dim]",
        border_style="cyan"
    ))
    console.print()


def display_agent_response(result: str, success: bool = True):
    """Display agent's final response."""
    console.print()
    if success:
        console.print(Panel(
            result,
            title="[bold green]📤 Agent Response[/bold green]",
            border_style="green"
        ))
    else:
        console.print(Panel(
            result,
            title="[bold red]❌ Agent Error[/bold red]",
            border_style="red"
        ))
    console.print()


# Global logger instance
_logger: Optional[EducationalLogger] = None


def get_logger() -> EducationalLogger:
    """Get or create global logger instance."""
    global _logger
    if _logger is None:
        _logger = EducationalLogger()
    return _logger


def setup_logger(level: str = "INFO", show_reasoning: bool = True,
                 show_tool_calls: bool = True, show_protocol: bool = False):
    """Set up global logger with configuration."""
    global _logger
    _logger = EducationalLogger(level, show_reasoning, show_tool_calls, show_protocol)
    return _logger
