"""Tests for OpenCode configuration management.

This module provides comprehensive unit and validation tests for the
OpenCode configuration system, including MCP servers, models, agents,
and configuration validation.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aiterm.opencode.config import (
    Agent,
    MCPServer,
    OpenCodeConfig,
    DEFAULT_MCP_SERVERS,
    RECOMMENDED_MODELS,
    VALID_PERMISSIONS,
    backup_config,
    get_config_path,
    load_config,
    save_config,
    validate_config,
)


# =============================================================================
# MCPServer Tests
# =============================================================================


class TestMCPServer:
    """Tests for MCPServer dataclass."""

    def test_create_basic_server(self) -> None:
        """Should create a basic MCP server."""
        server = MCPServer(
            name="filesystem",
            type="local",
            command=["npx", "-y", "@modelcontextprotocol/server-filesystem"],
            enabled=True,
        )
        assert server.name == "filesystem"
        assert server.type == "local"
        assert server.enabled is True
        assert len(server.command) == 3

    def test_server_with_env_vars(self) -> None:
        """Should create server with environment variables."""
        server = MCPServer(
            name="github",
            command=["npx", "-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_TOKEN": "test_token"},
        )
        assert server.env["GITHUB_TOKEN"] == "test_token"

    def test_server_defaults(self) -> None:
        """Should have correct default values."""
        server = MCPServer(name="test")
        assert server.type == "local"
        assert server.enabled is False
        assert server.command == []
        assert server.env == {}

    def test_server_to_dict(self) -> None:
        """Should convert to dictionary correctly."""
        server = MCPServer(
            name="test",
            type="local",
            command=["echo", "test"],
            enabled=True,
            env={"KEY": "value"},
        )
        d = server.to_dict()
        assert d["type"] == "local"
        assert d["enabled"] is True
        assert d["command"] == ["echo", "test"]
        assert d["env"] == {"KEY": "value"}

    def test_server_to_dict_minimal(self) -> None:
        """Should exclude empty fields in to_dict."""
        server = MCPServer(name="test", enabled=False)
        d = server.to_dict()
        assert "command" not in d
        assert "env" not in d


class TestMCPServerValidation:
    """Tests for MCPServer validation."""

    def test_valid_local_server(self) -> None:
        """Should validate a correct local server."""
        server = MCPServer(
            name="filesystem",
            type="local",
            command=["npx", "-y", "@modelcontextprotocol/server-filesystem"],
        )
        valid, errors = server.is_valid()
        assert valid is True
        assert errors == []

    def test_invalid_missing_name(self) -> None:
        """Should reject server without name."""
        server = MCPServer(name="", command=["test"])
        valid, errors = server.is_valid()
        assert valid is False
        assert "Server name is required" in errors

    def test_invalid_type(self) -> None:
        """Should reject invalid server type."""
        server = MCPServer(name="test", type="invalid")
        valid, errors = server.is_valid()
        assert valid is False
        assert any("Invalid server type" in e for e in errors)

    def test_local_server_without_command(self) -> None:
        """Should reject local server without command."""
        server = MCPServer(name="test", type="local", command=[])
        valid, errors = server.is_valid()
        assert valid is False
        assert "Local servers require a command" in errors

    def test_valid_remote_server(self) -> None:
        """Should validate remote server without command."""
        server = MCPServer(name="test", type="remote")
        valid, errors = server.is_valid()
        assert valid is True


# =============================================================================
# Agent Tests
# =============================================================================


class TestAgent:
    """Tests for Agent dataclass."""

    def test_create_basic_agent(self) -> None:
        """Should create a basic agent."""
        agent = Agent(
            name="r-dev",
            description="R package development",
            model="anthropic/claude-sonnet-4-5",
        )
        assert agent.name == "r-dev"
        assert agent.description == "R package development"
        assert agent.model == "anthropic/claude-sonnet-4-5"

    def test_agent_with_tools(self) -> None:
        """Should create agent with tool restrictions."""
        agent = Agent(
            name="quick",
            tools=["read", "glob", "grep"],
        )
        assert agent.tools == ["read", "glob", "grep"]

    def test_agent_defaults(self) -> None:
        """Should have correct default values."""
        agent = Agent(name="test")
        assert agent.description == ""
        assert agent.model == ""
        assert agent.prompt == ""
        assert agent.tools == []

    def test_agent_to_dict(self) -> None:
        """Should convert to dictionary correctly."""
        agent = Agent(
            name="test",
            description="Test agent",
            model="anthropic/claude-sonnet-4-5",
            tools=["read", "write"],
        )
        d = agent.to_dict()
        assert d["description"] == "Test agent"
        assert d["model"] == "anthropic/claude-sonnet-4-5"
        assert d["tools"] == ["read", "write"]

    def test_agent_to_dict_minimal(self) -> None:
        """Should exclude empty fields in to_dict."""
        agent = Agent(name="test")
        d = agent.to_dict()
        assert d == {}


class TestAgentValidation:
    """Tests for Agent validation."""

    def test_valid_agent(self) -> None:
        """Should validate a correct agent."""
        agent = Agent(
            name="r-dev",
            model="anthropic/claude-sonnet-4-5",
        )
        valid, errors = agent.is_valid()
        assert valid is True
        assert errors == []

    def test_invalid_missing_name(self) -> None:
        """Should reject agent without name."""
        agent = Agent(name="")
        valid, errors = agent.is_valid()
        assert valid is False
        assert "Agent name is required" in errors

    def test_invalid_model_format(self) -> None:
        """Should reject invalid model format."""
        agent = Agent(name="test", model="claude-sonnet")
        valid, errors = agent.is_valid()
        assert valid is False
        assert any("provider/model" in e for e in errors)

    def test_valid_agent_no_model(self) -> None:
        """Should accept agent without model (inherits default)."""
        agent = Agent(name="test")
        valid, errors = agent.is_valid()
        assert valid is True


# =============================================================================
# OpenCodeConfig Tests
# =============================================================================


class TestOpenCodeConfig:
    """Tests for OpenCodeConfig dataclass."""

    def test_create_basic_config(self, tmp_path: Path) -> None:
        """Should create a basic config."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            model="anthropic/claude-sonnet-4-5",
        )
        assert config.model == "anthropic/claude-sonnet-4-5"
        assert config.mcp_servers == {}
        assert config.agents == {}

    def test_enabled_servers_property(self, tmp_path: Path) -> None:
        """Should return list of enabled servers."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            mcp_servers={
                "filesystem": MCPServer(name="filesystem", enabled=True, command=["test"]),
                "memory": MCPServer(name="memory", enabled=True, command=["test"]),
                "playwright": MCPServer(name="playwright", enabled=False, command=["test"]),
            },
        )
        assert set(config.enabled_servers) == {"filesystem", "memory"}
        assert config.disabled_servers == ["playwright"]

    def test_scroll_acceleration_property(self, tmp_path: Path) -> None:
        """Should check scroll acceleration correctly."""
        config_enabled = OpenCodeConfig(
            path=tmp_path / "config.json",
            tui={"scroll_acceleration": {"enabled": True}},
        )
        assert config_enabled.has_scroll_acceleration is True

        config_disabled = OpenCodeConfig(
            path=tmp_path / "config.json",
            tui={},
        )
        assert config_disabled.has_scroll_acceleration is False

    def test_to_dict(self, tmp_path: Path) -> None:
        """Should convert to dictionary correctly."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            model="anthropic/claude-sonnet-4-5",
            small_model="anthropic/claude-haiku-4-5",
            tui={"scroll_acceleration": {"enabled": True}},
            mcp_servers={
                "filesystem": MCPServer(name="filesystem", enabled=True, command=["test"]),
            },
        )
        d = config.to_dict()
        assert d["$schema"] == "https://opencode.ai/config.json"
        assert d["model"] == "anthropic/claude-sonnet-4-5"
        assert d["small_model"] == "anthropic/claude-haiku-4-5"
        assert "mcp" in d
        assert "filesystem" in d["mcp"]


class TestOpenCodeConfigValidation:
    """Tests for OpenCodeConfig validation."""

    def test_valid_config(self, tmp_path: Path) -> None:
        """Should validate a correct config."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            model="anthropic/claude-sonnet-4-5",
            mcp_servers={
                "filesystem": MCPServer(name="filesystem", enabled=True, command=["test"]),
            },
        )
        valid, errors = config.is_valid()
        assert valid is True

    def test_invalid_model_format(self, tmp_path: Path) -> None:
        """Should reject invalid model format."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            model="claude-sonnet",  # Missing provider
        )
        valid, errors = config.is_valid()
        assert valid is False
        assert any("provider/model" in e for e in errors)

    def test_invalid_small_model_format(self, tmp_path: Path) -> None:
        """Should reject invalid small_model format."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            model="anthropic/claude-sonnet-4-5",
            small_model="haiku",  # Missing provider
        )
        valid, errors = config.is_valid()
        assert valid is False
        assert any("Small model" in e for e in errors)

    def test_invalid_default_agent(self, tmp_path: Path) -> None:
        """Should reject unknown default agent."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            default_agent="unknown-agent",
        )
        valid, errors = config.is_valid()
        assert valid is False
        assert any("Default agent" in e for e in errors)

    def test_valid_default_agent_mode(self, tmp_path: Path) -> None:
        """Should accept valid agent mode as default."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            default_agent="build",
        )
        valid, errors = config.is_valid()
        assert valid is True

    def test_valid_default_agent_custom(self, tmp_path: Path) -> None:
        """Should accept custom agent as default if defined."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            default_agent="r-dev",
            agents={"r-dev": Agent(name="r-dev")},
        )
        valid, errors = config.is_valid()
        assert valid is True

    def test_invalid_tool_permission(self, tmp_path: Path) -> None:
        """Should reject invalid tool permission."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            tools={"bash": {"permission": "invalid"}},
        )
        valid, errors = config.is_valid()
        assert valid is False
        assert any("Invalid permission" in e for e in errors)

    def test_valid_tool_permissions(self, tmp_path: Path) -> None:
        """Should accept valid tool permissions."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            tools={
                "bash": {"permission": "auto"},
                "write": {"permission": "ask"},
                "rm": {"permission": "deny"},
            },
        )
        valid, errors = config.is_valid()
        assert valid is True


# =============================================================================
# Load/Save Config Tests
# =============================================================================


class TestLoadConfig:
    """Tests for load_config function."""

    def test_load_valid_config(self, tmp_path: Path) -> None:
        """Should load a valid config file."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "model": "anthropic/claude-sonnet-4-5",
            "mcp": {
                "filesystem": {
                    "type": "local",
                    "command": ["npx", "-y", "server"],
                    "enabled": True,
                }
            },
        }))

        config = load_config(config_file)
        assert config is not None
        assert config.model == "anthropic/claude-sonnet-4-5"
        assert "filesystem" in config.mcp_servers
        assert config.mcp_servers["filesystem"].enabled is True

    def test_load_config_with_agents(self, tmp_path: Path) -> None:
        """Should load config with agents."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "agents": {
                "r-dev": {
                    "description": "R package development",
                    "model": "anthropic/claude-sonnet-4-5",
                    "tools": ["read", "write"],
                }
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert "r-dev" in config.agents
        assert config.agents["r-dev"].description == "R package development"

    def test_load_missing_file(self, tmp_path: Path) -> None:
        """Should return None for missing file."""
        config = load_config(tmp_path / "nonexistent.json")
        assert config is None

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        """Should return None for invalid JSON."""
        config_file = tmp_path / "config.json"
        config_file.write_text("not valid json {")

        config = load_config(config_file)
        assert config is None

    def test_load_default_path(self) -> None:
        """Should use default path when none specified."""
        # This will likely return None on test systems
        # but shouldn't raise an error
        config = load_config()
        # Just verify it doesn't crash
        assert config is None or isinstance(config, OpenCodeConfig)


class TestSaveConfig:
    """Tests for save_config function."""

    def test_save_config(self, tmp_path: Path) -> None:
        """Should save config to file."""
        config_file = tmp_path / "config.json"
        config = OpenCodeConfig(
            path=config_file,
            model="anthropic/claude-sonnet-4-5",
            mcp_servers={
                "filesystem": MCPServer(
                    name="filesystem",
                    command=["test"],
                    enabled=True,
                ),
            },
        )

        assert save_config(config) is True
        assert config_file.exists()

        # Verify content
        data = json.loads(config_file.read_text())
        assert data["model"] == "anthropic/claude-sonnet-4-5"
        assert data["mcp"]["filesystem"]["enabled"] is True

    def test_save_creates_directory(self, tmp_path: Path) -> None:
        """Should create parent directories if needed."""
        config_file = tmp_path / "subdir" / "config.json"
        config = OpenCodeConfig(path=config_file, model="test/model")

        assert save_config(config) is True
        assert config_file.exists()


class TestBackupConfig:
    """Tests for backup_config function."""

    def test_backup_creates_file(self, tmp_path: Path) -> None:
        """Should create timestamped backup."""
        config_file = tmp_path / "config.json"
        config_file.write_text('{"model": "test"}')

        backup_path = backup_config(config_file)
        assert backup_path is not None
        assert backup_path.exists()
        assert "backup-" in backup_path.name

    def test_backup_preserves_content(self, tmp_path: Path) -> None:
        """Should preserve original content."""
        original_content = '{"model": "anthropic/claude-sonnet-4-5"}'
        config_file = tmp_path / "config.json"
        config_file.write_text(original_content)

        backup_path = backup_config(config_file)
        assert backup_path is not None
        assert backup_path.read_text() == original_content

    def test_backup_missing_file(self, tmp_path: Path) -> None:
        """Should return None for missing file."""
        backup_path = backup_config(tmp_path / "nonexistent.json")
        assert backup_path is None


# =============================================================================
# Validate Config Tests
# =============================================================================


class TestValidateConfig:
    """Tests for validate_config function."""

    def test_validate_valid_config(self, tmp_path: Path) -> None:
        """Should validate a correct config file."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "model": "anthropic/claude-sonnet-4-5",
            "mcp": {
                "filesystem": {"type": "local", "command": ["test"], "enabled": True},
                "memory": {"type": "local", "command": ["test"], "enabled": True},
            },
        }))

        valid, errors = validate_config(config_file)
        assert valid is True

    def test_validate_missing_file(self, tmp_path: Path) -> None:
        """Should report missing file."""
        valid, errors = validate_config(tmp_path / "missing.json")
        assert valid is False
        assert any("not found" in e for e in errors)

    def test_validate_invalid_json(self, tmp_path: Path) -> None:
        """Should report invalid JSON."""
        config_file = tmp_path / "config.json"
        config_file.write_text("not json")

        valid, errors = validate_config(config_file)
        assert valid is False
        assert any("Invalid JSON" in e for e in errors)

    def test_validate_warns_missing_schema(self, tmp_path: Path) -> None:
        """Should warn about missing schema."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "model": "anthropic/claude-sonnet-4-5",
            "mcp": {
                "filesystem": {"type": "local", "command": ["test"], "enabled": True},
                "memory": {"type": "local", "command": ["test"], "enabled": True},
            },
        }))

        valid, errors = validate_config(config_file)
        assert any("$schema" in e for e in errors)

    def test_validate_warns_no_model(self, tmp_path: Path) -> None:
        """Should warn about missing model."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "mcp": {
                "filesystem": {"type": "local", "command": ["test"], "enabled": True},
                "memory": {"type": "local", "command": ["test"], "enabled": True},
            },
        }))

        valid, errors = validate_config(config_file)
        assert any("No model" in e for e in errors)

    def test_validate_warns_missing_essential_servers(self, tmp_path: Path) -> None:
        """Should warn about missing essential servers."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "model": "anthropic/claude-sonnet-4-5",
            "mcp": {
                "playwright": {"type": "local", "command": ["test"], "enabled": True},
            },
        }))

        valid, errors = validate_config(config_file)
        assert any("filesystem" in e for e in errors)
        assert any("memory" in e for e in errors)


# =============================================================================
# Constants Tests
# =============================================================================


class TestConstants:
    """Tests for module constants."""

    def test_recommended_models_has_primary(self) -> None:
        """Should have primary models defined."""
        assert "primary" in RECOMMENDED_MODELS
        assert len(RECOMMENDED_MODELS["primary"]) > 0
        assert "anthropic/claude-sonnet-4-5" in RECOMMENDED_MODELS["primary"]

    def test_recommended_models_has_small(self) -> None:
        """Should have small models defined."""
        assert "small" in RECOMMENDED_MODELS
        assert len(RECOMMENDED_MODELS["small"]) > 0
        assert "anthropic/claude-haiku-4-5" in RECOMMENDED_MODELS["small"]

    def test_default_mcp_servers_has_essentials(self) -> None:
        """Should have essential servers defined."""
        assert "filesystem" in DEFAULT_MCP_SERVERS
        assert "memory" in DEFAULT_MCP_SERVERS
        assert DEFAULT_MCP_SERVERS["filesystem"]["essential"] is True
        assert DEFAULT_MCP_SERVERS["memory"]["essential"] is True

    def test_valid_permissions(self) -> None:
        """Should have correct permission values."""
        assert "auto" in VALID_PERMISSIONS
        assert "ask" in VALID_PERMISSIONS
        assert "deny" in VALID_PERMISSIONS

    def test_get_config_path(self) -> None:
        """Should return correct default path."""
        path = get_config_path()
        assert path.name == "config.json"
        assert "opencode" in str(path)


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_config_roundtrip(self, tmp_path: Path) -> None:
        """Should save and reload config identically."""
        config_file = tmp_path / "config.json"

        # Create config
        original = OpenCodeConfig(
            path=config_file,
            model="anthropic/claude-sonnet-4-5",
            small_model="anthropic/claude-haiku-4-5",
            default_agent="build",
            tui={"scroll_acceleration": {"enabled": True}},
            mcp_servers={
                "filesystem": MCPServer(
                    name="filesystem",
                    command=["npx", "-y", "server"],
                    enabled=True,
                ),
                "memory": MCPServer(
                    name="memory",
                    command=["npx", "-y", "memory"],
                    enabled=True,
                ),
            },
            agents={
                "r-dev": Agent(
                    name="r-dev",
                    description="R development",
                    model="anthropic/claude-sonnet-4-5",
                    tools=["read", "write", "bash"],
                ),
            },
            tools={
                "bash": {"permission": "auto"},
            },
        )

        # Save
        assert save_config(original) is True

        # Reload
        loaded = load_config(config_file)
        assert loaded is not None

        # Compare
        assert loaded.model == original.model
        assert loaded.small_model == original.small_model
        assert loaded.default_agent == original.default_agent
        assert loaded.has_scroll_acceleration == original.has_scroll_acceleration
        assert set(loaded.enabled_servers) == set(original.enabled_servers)
        assert "r-dev" in loaded.agents
        assert loaded.agents["r-dev"].tools == original.agents["r-dev"].tools

    def test_backup_and_restore(self, tmp_path: Path) -> None:
        """Should backup and restore config."""
        config_file = tmp_path / "config.json"

        # Create and save original
        original = OpenCodeConfig(
            path=config_file,
            model="anthropic/claude-sonnet-4-5",
        )
        save_config(original)

        # Backup
        backup_path = backup_config(config_file)
        assert backup_path is not None

        # Modify original
        modified = OpenCodeConfig(
            path=config_file,
            model="anthropic/claude-opus-4-5",
        )
        save_config(modified)

        # Verify modification
        current = load_config(config_file)
        assert current is not None
        assert current.model == "anthropic/claude-opus-4-5"

        # Restore from backup
        backup_content = backup_path.read_text()
        config_file.write_text(backup_content)

        # Verify restoration
        restored = load_config(config_file)
        assert restored is not None
        assert restored.model == "anthropic/claude-sonnet-4-5"

    def test_validate_real_option_a_config(self, tmp_path: Path) -> None:
        """Should validate the Option A config we applied."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "model": "anthropic/claude-sonnet-4-5",
            "small_model": "anthropic/claude-haiku-4-5",
            "tui": {
                "scroll_acceleration": {"enabled": True}
            },
            "mcp": {
                "filesystem": {
                    "type": "local",
                    "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/Users/dt"],
                    "enabled": True
                },
                "memory": {
                    "type": "local",
                    "command": ["npx", "-y", "@modelcontextprotocol/server-memory"],
                    "enabled": True
                },
                "sequential-thinking": {
                    "type": "local",
                    "command": ["npx", "-y", "@modelcontextprotocol/server-sequential-thinking"],
                    "enabled": False
                },
                "playwright": {
                    "type": "local",
                    "command": ["npx", "-y", "@playwright/mcp@latest", "--browser", "chromium"],
                    "enabled": False
                }
            }
        }))

        valid, errors = validate_config(config_file)
        assert valid is True, f"Option A config should be valid: {errors}"

        config = load_config(config_file)
        assert config is not None
        assert config.model == "anthropic/claude-sonnet-4-5"
        assert config.small_model == "anthropic/claude-haiku-4-5"
        assert config.has_scroll_acceleration is True
        assert set(config.enabled_servers) == {"filesystem", "memory"}
        assert set(config.disabled_servers) == {"sequential-thinking", "playwright"}
