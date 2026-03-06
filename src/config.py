"""Configuration management for the learning agent."""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AgentConfig:
    """Agent configuration."""
    model: str = "gpt-4"
    max_iterations: int = 10
    temperature: float = 0.7
    debug_mode: bool = False


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    show_reasoning: bool = True
    show_tool_calls: bool = True
    show_protocol_messages: bool = False


@dataclass
class MCPConfig:
    """MCP server configuration."""
    server_url: str = "http://localhost:8080"
    timeout: int = 30


@dataclass
class Config:
    """Complete system configuration."""
    agent: AgentConfig = field(default_factory=AgentConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from YAML file with defaults."""
    if config_path is None:
        config_path = "config/agent_config.yaml"
    
    config_file = Path(config_path)
    
    # Start with defaults
    config = Config()
    
    # Load from file if it exists
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                data = yaml.safe_load(f)
            
            # Update agent config
            if 'agent' in data:
                agent_data = data['agent']
                config.agent = AgentConfig(
                    model=agent_data.get('model', config.agent.model),
                    max_iterations=agent_data.get('max_iterations', config.agent.max_iterations),
                    temperature=agent_data.get('temperature', config.agent.temperature),
                    debug_mode=agent_data.get('debug_mode', config.agent.debug_mode)
                )
            
            # Update logging config
            if 'logging' in data:
                logging_data = data['logging']
                config.logging = LoggingConfig(
                    level=logging_data.get('level', config.logging.level),
                    show_reasoning=logging_data.get('show_reasoning', config.logging.show_reasoning),
                    show_tool_calls=logging_data.get('show_tool_calls', config.logging.show_tool_calls),
                    show_protocol_messages=logging_data.get('show_protocol_messages', config.logging.show_protocol_messages)
                )
            
            # Update MCP config
            if 'mcp' in data:
                mcp_data = data['mcp']
                config.mcp = MCPConfig(
                    server_url=mcp_data.get('server_url', config.mcp.server_url),
                    timeout=mcp_data.get('timeout', config.mcp.timeout)
                )
            
            print(f"✅ Loaded configuration from {config_path}")
        except Exception as e:
            print(f"⚠️  Error loading config file: {e}")
            print("   Using default configuration")
    else:
        print(f"ℹ️  Config file not found at {config_path}, using defaults")
    
    return config


@dataclass
class ToolConfig:
    """Configuration for a single tool."""
    name: str
    enabled: bool = True
    config: Dict[str, Any] = field(default_factory=dict)


def load_tools_config(config_path: Optional[str] = None) -> list[ToolConfig]:
    """Load tools configuration from YAML file."""
    if config_path is None:
        config_path = "config/tools_config.yaml"
    
    config_file = Path(config_path)
    
    # Default tools
    default_tools = [
        ToolConfig(name="calculator", enabled=True),
        ToolConfig(name="file_ops", enabled=True, config={"allowed_paths": ["./workspace"]}),
        ToolConfig(name="web_search", enabled=True, config={"simulated": True})
    ]
    
    if not config_file.exists():
        print(f"ℹ️  Tools config not found at {config_path}, using defaults")
        return default_tools
    
    try:
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
        
        tools = []
        for tool_data in data.get('tools', []):
            tools.append(ToolConfig(
                name=tool_data['name'],
                enabled=tool_data.get('enabled', True),
                config=tool_data.get('config', {})
            ))
        
        print(f"✅ Loaded tools configuration from {config_path}")
        return tools
    except Exception as e:
        print(f"⚠️  Error loading tools config: {e}")
        print("   Using default tools configuration")
        return default_tools
