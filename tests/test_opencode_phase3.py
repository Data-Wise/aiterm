"""Tests for OpenCode Phase 3 features.

Phase 3 features:
- Research agent (Opus 4.5)
- Keyboard shortcuts (keybinds)
- Custom commands
- Tool permissions
- Time MCP server
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from aiterm.cli.main import app
from aiterm.opencode.config import (
    Command,
    OpenCodeConfig,
    load_config,
)

runner = CliRunner()


# =============================================================================
# Command Dataclass Tests
# =============================================================================


class TestCommand:
    """Tests for Command dataclass."""

    def test_create_basic_command(self) -> None:
        """Should create a basic command."""
        cmd = Command(
            name="test",
            description="Test command",
            command="echo test",
        )
        assert cmd.name == "test"
        assert cmd.description == "Test command"
        assert cmd.command == "echo test"

    def test_command_defaults(self) -> None:
        """Should have correct default values."""
        cmd = Command(name="test")
        assert cmd.description == ""
        assert cmd.command == ""

    def test_command_to_dict(self) -> None:
        """Should convert to dictionary correctly."""
        cmd = Command(
            name="sync",
            description="Git sync",
            command="git add -A && git commit -m 'sync' && git push",
        )
        d = cmd.to_dict()
        assert d["description"] == "Git sync"
        assert d["command"] == "git add -A && git commit -m 'sync' && git push"

    def test_command_to_dict_minimal(self) -> None:
        """Should exclude empty fields in to_dict."""
        cmd = Command(name="test")
        d = cmd.to_dict()
        assert d == {}


# =============================================================================
# Research Agent Tests
# =============================================================================


class TestResearchAgent:
    """Tests for research agent configuration."""

    def test_research_agent_exists(self, tmp_path: Path) -> None:
        """Should load config with research agent."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "agents": {
                "research": {
                    "description": "Academic research and manuscript writing",
                    "model": "anthropic/claude-opus-4-5",
                    "tools": ["read", "write", "edit", "glob", "grep", "websearch", "webfetch"],
                }
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert "research" in config.agents
        assert config.agents["research"].model == "anthropic/claude-opus-4-5"

    def test_research_agent_tools(self, tmp_path: Path) -> None:
        """Should have web tools for research."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "agents": {
                "research": {
                    "model": "anthropic/claude-opus-4-5",
                    "tools": ["read", "write", "websearch", "webfetch"],
                }
            }
        }))

        config = load_config(config_file)
        assert config is not None
        tools = config.agents["research"].tools
        assert "websearch" in tools
        assert "webfetch" in tools

    def test_research_agent_uses_opus(self, tmp_path: Path) -> None:
        """Research agent should use Opus model."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "agents": {
                "research": {"model": "anthropic/claude-opus-4-5"}
            }
        }))

        config = load_config(config_file)
        assert "opus" in config.agents["research"].model.lower()


# =============================================================================
# Keybinds Tests
# =============================================================================


class TestKeybinds:
    """Tests for keyboard shortcuts configuration."""

    def test_load_keybinds(self, tmp_path: Path) -> None:
        """Should load keybinds from config."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "keybinds": {
                "ctrl+r": "agent:r-dev",
                "ctrl+q": "agent:quick",
                "ctrl+s": "agent:research",
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert len(config.keybinds) == 3
        assert config.keybinds["ctrl+r"] == "agent:r-dev"

    def test_keybinds_empty(self, tmp_path: Path) -> None:
        """Should handle empty keybinds."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({}))

        config = load_config(config_file)
        assert config is not None
        assert config.keybinds == {}

    def test_keybinds_to_dict(self, tmp_path: Path) -> None:
        """Should serialize keybinds correctly."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            keybinds={"ctrl+r": "agent:r-dev"},
        )
        d = config.to_dict()
        assert "keybinds" in d
        assert d["keybinds"]["ctrl+r"] == "agent:r-dev"


# =============================================================================
# Commands Tests
# =============================================================================


class TestCommands:
    """Tests for custom commands configuration."""

    def test_load_commands(self, tmp_path: Path) -> None:
        """Should load commands from config."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "commands": {
                "sync": {
                    "description": "Git sync",
                    "command": "git add -A && git commit -m 'sync' && git push",
                },
                "status": {
                    "description": "Show status",
                    "command": "git status",
                },
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert len(config.commands) == 2
        assert "sync" in config.commands
        assert config.commands["sync"].command == "git add -A && git commit -m 'sync' && git push"

    def test_r_package_commands(self, tmp_path: Path) -> None:
        """Should load R package commands."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "commands": {
                "rpkg-check": {
                    "description": "Run R CMD check",
                    "command": "R CMD check --as-cran .",
                },
                "rpkg-document": {
                    "description": "Generate documentation",
                    "command": "Rscript -e 'devtools::document()'",
                },
                "rpkg-test": {
                    "description": "Run tests",
                    "command": "Rscript -e 'devtools::test()'",
                },
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert len(config.commands) == 3
        assert "rpkg-check" in config.commands
        assert "rpkg-document" in config.commands
        assert "rpkg-test" in config.commands

    def test_commands_to_dict(self, tmp_path: Path) -> None:
        """Should serialize commands correctly."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            commands={
                "test": Command(
                    name="test",
                    description="Test command",
                    command="echo test",
                ),
            },
        )
        d = config.to_dict()
        assert "commands" in d
        assert d["commands"]["test"]["description"] == "Test command"


# =============================================================================
# Tool Permissions Tests
# =============================================================================


class TestToolPermissions:
    """Tests for tool permissions configuration."""

    def test_load_tool_permissions(self, tmp_path: Path) -> None:
        """Should load tool permissions from config."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "tools": {
                "bash": {"permission": "auto"},
                "read": {"permission": "auto"},
                "write": {"permission": "ask"},
                "edit": {"permission": "ask"},
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert len(config.tools) == 4
        assert config.tools["bash"]["permission"] == "auto"
        assert config.tools["write"]["permission"] == "ask"

    def test_auto_permissions_for_read_ops(self, tmp_path: Path) -> None:
        """Read-only tools should have auto permission."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "tools": {
                "bash": {"permission": "auto"},
                "read": {"permission": "auto"},
                "glob": {"permission": "auto"},
                "grep": {"permission": "auto"},
            }
        }))

        config = load_config(config_file)
        assert config is not None
        for tool in ["bash", "read", "glob", "grep"]:
            assert config.tools[tool]["permission"] == "auto"

    def test_ask_permissions_for_write_ops(self, tmp_path: Path) -> None:
        """Write tools should have ask permission."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "tools": {
                "write": {"permission": "ask"},
                "edit": {"permission": "ask"},
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert config.tools["write"]["permission"] == "ask"
        assert config.tools["edit"]["permission"] == "ask"

    def test_tools_to_dict(self, tmp_path: Path) -> None:
        """Should serialize tools correctly."""
        config = OpenCodeConfig(
            path=tmp_path / "config.json",
            tools={"bash": {"permission": "auto"}},
        )
        d = config.to_dict()
        assert "tools" in d
        assert d["tools"]["bash"]["permission"] == "auto"


# =============================================================================
# Time MCP Server Tests
# =============================================================================


class TestTimeMCPServer:
    """Tests for Time MCP server configuration."""

    def test_time_server_enabled(self, tmp_path: Path) -> None:
        """Should load config with time server enabled."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "mcp": {
                "time": {
                    "type": "local",
                    "enabled": True,
                    "command": ["npx", "-y", "@modelcontextprotocol/server-time"],
                }
            }
        }))

        config = load_config(config_file)
        assert config is not None
        assert "time" in config.mcp_servers
        assert config.mcp_servers["time"].enabled is True

    def test_time_server_in_enabled_list(self, tmp_path: Path) -> None:
        """Time server should appear in enabled_servers."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "mcp": {
                "filesystem": {"type": "local", "enabled": True, "command": ["test"]},
                "memory": {"type": "local", "enabled": True, "command": ["test"]},
                "time": {"type": "local", "enabled": True, "command": ["test"]},
            }
        }))

        config = load_config(config_file)
        assert "time" in config.enabled_servers


# =============================================================================
# CLI Keybinds Command Tests
# =============================================================================


class TestKeybindsCommand:
    """Tests for keybinds CLI command."""

    def test_keybinds_list_empty(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should show message when no keybinds configured."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"$schema": "https://opencode.ai/config.json"}))
        monkeypatch.setattr(
            "aiterm.opencode.config.get_config_path",
            lambda: config_path,
        )
        result = runner.invoke(app, ["opencode", "keybinds"])
        assert result.exit_code == 0
        assert "No keybinds" in result.output

    def test_keybinds_list_with_binds(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should list configured keybinds."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "keybinds": {
                "ctrl+r": "agent:r-dev",
                "ctrl+q": "agent:quick",
            }
        }))
        monkeypatch.setattr(
            "aiterm.opencode.config.get_config_path",
            lambda: config_path,
        )
        result = runner.invoke(app, ["opencode", "keybinds"])
        assert result.exit_code == 0
        assert "ctrl+r" in result.output
        assert "agent:r-dev" in result.output


# =============================================================================
# CLI Commands Command Tests
# =============================================================================


class TestCommandsCommand:
    """Tests for commands CLI command."""

    def test_commands_list_empty(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should show message when no commands configured."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"$schema": "https://opencode.ai/config.json"}))
        monkeypatch.setattr(
            "aiterm.opencode.config.get_config_path",
            lambda: config_path,
        )
        result = runner.invoke(app, ["opencode", "commands"])
        assert result.exit_code == 0
        assert "No custom commands" in result.output

    def test_commands_list_with_commands(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should list configured commands."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "commands": {
                "sync": {
                    "description": "Git sync",
                    "command": "git add -A && git commit",
                }
            }
        }))
        monkeypatch.setattr(
            "aiterm.opencode.config.get_config_path",
            lambda: config_path,
        )
        result = runner.invoke(app, ["opencode", "commands"])
        assert result.exit_code == 0
        assert "sync" in result.output
        assert "Git sync" in result.output


# =============================================================================
# CLI Tools Command Tests
# =============================================================================


class TestToolsCommand:
    """Tests for tools CLI command."""

    def test_tools_list_empty(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should show message when no tool permissions configured."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"$schema": "https://opencode.ai/config.json"}))
        monkeypatch.setattr(
            "aiterm.opencode.config.get_config_path",
            lambda: config_path,
        )
        result = runner.invoke(app, ["opencode", "tools"])
        assert result.exit_code == 0
        assert "No tool" in result.output or "permission" in result.output.lower()

    def test_tools_list_with_permissions(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should list configured tool permissions."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "tools": {
                "bash": {"permission": "auto"},
                "write": {"permission": "ask"},
            }
        }))
        monkeypatch.setattr(
            "aiterm.opencode.config.get_config_path",
            lambda: config_path,
        )
        result = runner.invoke(app, ["opencode", "tools"])
        assert result.exit_code == 0
        assert "bash" in result.output
        assert "auto" in result.output


# =============================================================================
# CLI Summary Command Tests
# =============================================================================


class TestSummaryCommand:
    """Tests for summary CLI command."""

    def test_summary_full_config(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Should show complete configuration summary."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "model": "anthropic/claude-sonnet-4-5",
            "small_model": "anthropic/claude-haiku-4-5",
            "default_agent": "build",
            "instructions": ["CLAUDE.md"],
            "tui": {"scroll_acceleration": {"enabled": True}},
            "keybinds": {"ctrl+r": "agent:r-dev"},
            "commands": {"sync": {"command": "git push"}},
            "tools": {"bash": {"permission": "auto"}},
            "agents": {
                "r-dev": {"model": "anthropic/claude-sonnet-4-5"},
                "quick": {"model": "anthropic/claude-haiku-4-5"},
            },
            "mcp": {
                "filesystem": {"type": "local", "enabled": True, "command": ["test"]},
                "memory": {"type": "local", "enabled": True, "command": ["test"]},
            },
        }))
        monkeypatch.setattr(
            "aiterm.opencode.config.get_config_path",
            lambda: config_path,
        )
        result = runner.invoke(app, ["opencode", "summary"])
        assert result.exit_code == 0
        # Check summary includes all sections
        assert "anthropic/claude-sonnet-4-5" in result.output
        assert "Agents" in result.output or "agent" in result.output.lower()
        assert "Keybinds" in result.output.lower() or "keybind" in result.output.lower() or "shortcut" in result.output.lower()


# =============================================================================
# Integration Test: Full Phase 3 Config
# =============================================================================


class TestPhase3Integration:
    """Integration tests for complete Phase 3 configuration."""

    def test_full_phase3_config(self, tmp_path: Path) -> None:
        """Should load and validate complete Phase 3 config."""
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({
            "$schema": "https://opencode.ai/config.json",
            "model": "anthropic/claude-sonnet-4-5",
            "small_model": "anthropic/claude-haiku-4-5",
            "default_agent": "build",
            "instructions": ["CLAUDE.md", ".claude/rules/*.md"],
            "tui": {"scroll_acceleration": {"enabled": True}},
            "keybinds": {
                "ctrl+r": "agent:r-dev",
                "ctrl+q": "agent:quick",
                "ctrl+s": "agent:research",
            },
            "commands": {
                "rpkg-check": {"description": "Run R CMD check", "command": "R CMD check --as-cran ."},
                "rpkg-document": {"description": "Generate docs", "command": "Rscript -e 'devtools::document()'"},
                "rpkg-test": {"description": "Run tests", "command": "Rscript -e 'devtools::test()'"},
                "sync": {"description": "Git sync", "command": "git add -A && git commit -m 'sync' && git push"},
                "status": {"description": "Show status", "command": "git status && git log --oneline -5"},
            },
            "tools": {
                "bash": {"permission": "auto"},
                "read": {"permission": "auto"},
                "glob": {"permission": "auto"},
                "grep": {"permission": "auto"},
                "write": {"permission": "ask"},
                "edit": {"permission": "ask"},
            },
            "agents": {
                "r-dev": {
                    "description": "R package development specialist",
                    "model": "anthropic/claude-sonnet-4-5",
                    "tools": ["bash", "read", "write", "edit", "glob", "grep"],
                },
                "quick": {
                    "description": "Fast responses for simple questions",
                    "model": "anthropic/claude-haiku-4-5",
                    "tools": ["read", "glob", "grep"],
                },
                "research": {
                    "description": "Academic research and manuscript writing",
                    "model": "anthropic/claude-opus-4-5",
                    "tools": ["read", "write", "edit", "glob", "grep", "websearch", "webfetch"],
                },
            },
            "mcp": {
                "filesystem": {"type": "local", "enabled": True, "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem"]},
                "memory": {"type": "local", "enabled": True, "command": ["npx", "-y", "@modelcontextprotocol/server-memory"]},
                "time": {"type": "local", "enabled": True, "command": ["npx", "-y", "@modelcontextprotocol/server-time"]},
                "github": {"type": "local", "enabled": True, "command": ["npx", "-y", "@modelcontextprotocol/server-github"]},
            },
        }))

        config = load_config(config_file)
        assert config is not None

        # Validate Phase 3 features
        # 3.1: Research agent
        assert "research" in config.agents
        assert "opus" in config.agents["research"].model.lower()
        assert "websearch" in config.agents["research"].tools

        # 3.2: Keybinds
        assert len(config.keybinds) == 3
        assert config.keybinds["ctrl+s"] == "agent:research"

        # 3.3: Commands
        assert len(config.commands) == 5
        assert "rpkg-check" in config.commands
        assert "sync" in config.commands

        # 3.4: Tool permissions
        assert len(config.tools) == 6
        assert config.tools["bash"]["permission"] == "auto"
        assert config.tools["write"]["permission"] == "ask"

        # 3.5: Time MCP
        assert "time" in config.mcp_servers
        assert config.mcp_servers["time"].enabled is True
        assert "time" in config.enabled_servers

        # Validate config is valid
        valid, errors = config.is_valid()
        assert valid is True, f"Config should be valid: {errors}"

    def test_roundtrip_phase3_config(self, tmp_path: Path) -> None:
        """Should save and reload Phase 3 config identically."""
        from aiterm.opencode.config import save_config

        config_file = tmp_path / "config.json"

        # Create Phase 3 config
        original = OpenCodeConfig(
            path=config_file,
            model="anthropic/claude-sonnet-4-5",
            keybinds={"ctrl+r": "agent:r-dev"},
            commands={"sync": Command(name="sync", command="git push")},
            tools={"bash": {"permission": "auto"}},
        )

        # Save
        assert save_config(original) is True

        # Reload
        loaded = load_config(config_file)
        assert loaded is not None

        # Compare
        assert loaded.keybinds == original.keybinds
        assert loaded.tools == original.tools
        assert "sync" in loaded.commands
        assert loaded.commands["sync"].command == "git push"
