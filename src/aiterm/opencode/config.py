"""OpenCode configuration management.

This module provides tools for managing OpenCode CLI configuration,
including MCP servers, models, agents, and tools.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# Recommended models for OpenCode
RECOMMENDED_MODELS = {
    "primary": [
        "anthropic/claude-sonnet-4-5",
        "anthropic/claude-opus-4-5",
        "anthropic/claude-sonnet-4-0",
        "google/gemini-2.5-pro",
        "google/gemini-2.5-flash",
    ],
    "small": [
        "anthropic/claude-haiku-4-5",
        "google/gemini-2.5-flash-lite",
        "anthropic/claude-3-5-haiku-latest",
    ],
}

# Default MCP servers configuration
DEFAULT_MCP_SERVERS = {
    "filesystem": {
        "type": "local",
        "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem"],
        "enabled": True,
        "essential": True,
        "description": "File system read/write access",
    },
    "memory": {
        "type": "local",
        "command": ["npx", "-y", "@modelcontextprotocol/server-memory"],
        "enabled": True,
        "essential": True,
        "description": "Persistent context memory",
    },
    "sequential-thinking": {
        "type": "local",
        "command": ["npx", "-y", "@modelcontextprotocol/server-sequential-thinking"],
        "enabled": False,
        "essential": False,
        "description": "Complex reasoning chains",
    },
    "playwright": {
        "type": "local",
        "command": ["npx", "-y", "@playwright/mcp@latest", "--browser", "chromium"],
        "enabled": False,
        "essential": False,
        "description": "Browser automation and testing",
    },
    "time": {
        "type": "local",
        "command": ["npx", "-y", "@modelcontextprotocol/server-time"],
        "enabled": False,
        "essential": False,
        "description": "Timezone and deadline tracking",
    },
    "github": {
        "type": "local",
        "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
        "enabled": False,
        "essential": False,
        "description": "GitHub integration for PRs and issues",
        "requires_env": ["GITHUB_TOKEN"],
    },
}

# Valid tool permissions
VALID_PERMISSIONS = ["auto", "ask", "deny"]

# Valid agent modes
VALID_AGENT_MODES = ["build", "plan", "review", "debug", "docs"]


@dataclass
class MCPServer:
    """Represents an MCP server configuration."""

    name: str
    type: str = "local"
    command: list[str] = field(default_factory=list)
    enabled: bool = False
    env: dict[str, str] = field(default_factory=dict)

    def is_valid(self) -> tuple[bool, list[str]]:
        """Validate the MCP server configuration.

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        if not self.name:
            errors.append("Server name is required")

        if self.type not in ["local", "remote", "stdio"]:
            errors.append(f"Invalid server type: {self.type}")

        if self.type == "local" and not self.command:
            errors.append("Local servers require a command")

        if self.command and not isinstance(self.command, list):
            errors.append("Command must be a list of strings")

        return len(errors) == 0, errors

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: dict[str, Any] = {
            "type": self.type,
            "enabled": self.enabled,
        }
        if self.command:
            result["command"] = self.command
        if self.env:
            result["env"] = self.env
        return result


@dataclass
class Agent:
    """Represents an OpenCode agent configuration."""

    name: str
    description: str = ""
    model: str = ""
    prompt: str = ""
    tools: list[str] = field(default_factory=list)

    def is_valid(self) -> tuple[bool, list[str]]:
        """Validate the agent configuration.

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        if not self.name:
            errors.append("Agent name is required")

        if self.model and "/" not in self.model:
            errors.append(f"Model should be in format 'provider/model': {self.model}")

        return len(errors) == 0, errors

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: dict[str, Any] = {}
        if self.description:
            result["description"] = self.description
        if self.model:
            result["model"] = self.model
        if self.prompt:
            result["prompt"] = self.prompt
        if self.tools:
            result["tools"] = self.tools
        return result


@dataclass
class OpenCodeConfig:
    """Represents a complete OpenCode configuration."""

    path: Path
    model: str = ""
    small_model: str = ""
    default_agent: str = ""
    mcp_servers: dict[str, MCPServer] = field(default_factory=dict)
    agents: dict[str, Agent] = field(default_factory=dict)
    tools: dict[str, dict[str, str]] = field(default_factory=dict)
    instructions: list[dict[str, str]] = field(default_factory=list)
    tui: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def enabled_servers(self) -> list[str]:
        """Return list of enabled MCP server names."""
        return [name for name, server in self.mcp_servers.items() if server.enabled]

    @property
    def disabled_servers(self) -> list[str]:
        """Return list of disabled MCP server names."""
        return [name for name, server in self.mcp_servers.items() if not server.enabled]

    @property
    def has_scroll_acceleration(self) -> bool:
        """Check if scroll acceleration is enabled."""
        return self.tui.get("scroll_acceleration", {}).get("enabled", False)

    def is_valid(self) -> tuple[bool, list[str]]:
        """Validate the complete configuration.

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Validate model format
        if self.model and "/" not in self.model:
            errors.append(f"Model should be in format 'provider/model': {self.model}")

        if self.small_model and "/" not in self.small_model:
            errors.append(f"Small model should be in format 'provider/model': {self.small_model}")

        # Validate default agent
        if self.default_agent and self.default_agent not in VALID_AGENT_MODES:
            if self.default_agent not in self.agents:
                errors.append(f"Default agent '{self.default_agent}' not found in agents or modes")

        # Validate MCP servers
        for name, server in self.mcp_servers.items():
            valid, server_errors = server.is_valid()
            if not valid:
                errors.extend([f"MCP server '{name}': {e}" for e in server_errors])

        # Validate agents
        for name, agent in self.agents.items():
            valid, agent_errors = agent.is_valid()
            if not valid:
                errors.extend([f"Agent '{name}': {e}" for e in agent_errors])

        # Validate tool permissions
        for tool_name, tool_config in self.tools.items():
            permission = tool_config.get("permission", "")
            if permission and permission not in VALID_PERMISSIONS:
                errors.append(f"Tool '{tool_name}': Invalid permission '{permission}'")

        return len(errors) == 0, errors

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result: dict[str, Any] = {"$schema": "https://opencode.ai/config.json"}

        if self.model:
            result["model"] = self.model
        if self.small_model:
            result["small_model"] = self.small_model
        if self.default_agent:
            result["default_agent"] = self.default_agent
        if self.tui:
            result["tui"] = self.tui
        if self.agents:
            result["agents"] = {name: agent.to_dict() for name, agent in self.agents.items()}
        if self.tools:
            result["tools"] = self.tools
        if self.instructions:
            result["instructions"] = self.instructions
        if self.mcp_servers:
            result["mcp"] = {name: server.to_dict() for name, server in self.mcp_servers.items()}

        return result


def get_config_path() -> Path:
    """Get the default OpenCode config path.

    Returns:
        Path to ~/.config/opencode/config.json
    """
    return Path.home() / ".config" / "opencode" / "config.json"


def load_config(path: Path | None = None) -> OpenCodeConfig | None:
    """Load OpenCode configuration from file.

    Args:
        path: Path to config file. Defaults to ~/.config/opencode/config.json

    Returns:
        OpenCodeConfig object or None if file doesn't exist or is invalid
    """
    if path is None:
        path = get_config_path()

    if not path.exists():
        return None

    try:
        raw = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None

    # Parse MCP servers
    mcp_servers = {}
    for name, server_data in raw.get("mcp", {}).items():
        if isinstance(server_data, dict):
            mcp_servers[name] = MCPServer(
                name=name,
                type=server_data.get("type", "local"),
                command=server_data.get("command", []),
                enabled=server_data.get("enabled", False),
                env=server_data.get("env", {}),
            )

    # Parse agents
    agents = {}
    for name, agent_data in raw.get("agents", {}).items():
        if isinstance(agent_data, dict):
            agents[name] = Agent(
                name=name,
                description=agent_data.get("description", ""),
                model=agent_data.get("model", ""),
                prompt=agent_data.get("prompt", ""),
                tools=agent_data.get("tools", []),
            )

    return OpenCodeConfig(
        path=path,
        model=raw.get("model", ""),
        small_model=raw.get("small_model", ""),
        default_agent=raw.get("default_agent", ""),
        mcp_servers=mcp_servers,
        agents=agents,
        tools=raw.get("tools", {}),
        instructions=raw.get("instructions", []),
        tui=raw.get("tui", {}),
        raw=raw,
    )


def save_config(config: OpenCodeConfig) -> bool:
    """Save OpenCode configuration to file.

    Args:
        config: OpenCodeConfig object to save

    Returns:
        True if saved successfully, False otherwise
    """
    try:
        config.path.parent.mkdir(parents=True, exist_ok=True)
        config.path.write_text(json.dumps(config.to_dict(), indent=2))
        return True
    except OSError:
        return False


def backup_config(path: Path | None = None) -> Path | None:
    """Create a timestamped backup of the config file.

    Args:
        path: Path to config file. Defaults to ~/.config/opencode/config.json

    Returns:
        Path to backup file or None if backup failed
    """
    if path is None:
        path = get_config_path()

    if not path.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_suffix(f".backup-{timestamp}.json")

    try:
        shutil.copy2(path, backup_path)
        return backup_path
    except OSError:
        return None


def validate_config(path: Path | None = None) -> tuple[bool, list[str]]:
    """Validate an OpenCode configuration file.

    Args:
        path: Path to config file. Defaults to ~/.config/opencode/config.json

    Returns:
        Tuple of (is_valid, list of error/warning messages)
    """
    if path is None:
        path = get_config_path()

    errors = []

    # Check file exists
    if not path.exists():
        return False, [f"Config file not found: {path}"]

    # Check JSON is valid
    try:
        raw = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    except OSError as e:
        return False, [f"Cannot read file: {e}"]

    # Check schema
    if "$schema" not in raw:
        errors.append("Missing $schema field (recommended: https://opencode.ai/config.json)")

    # Load and validate config
    config = load_config(path)
    if config is None:
        return False, ["Failed to parse configuration"]

    valid, config_errors = config.is_valid()
    errors.extend(config_errors)

    # Additional warnings
    if not config.model:
        errors.append("No model specified (recommend: anthropic/claude-sonnet-4-5)")

    if not config.enabled_servers:
        errors.append("No MCP servers enabled")

    essential_servers = ["filesystem", "memory"]
    for server in essential_servers:
        if server not in config.enabled_servers:
            errors.append(f"Essential server '{server}' not enabled")

    return len([e for e in errors if not e.startswith("No ")]) == 0, errors
