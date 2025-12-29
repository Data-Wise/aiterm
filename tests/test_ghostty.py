"""Tests for Ghostty terminal integration."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest


class TestGhosttyDetection:
    """Test Ghostty terminal detection."""

    def test_is_ghostty_true(self):
        """Test detection when TERM_PROGRAM is ghostty."""
        from aiterm.terminal import ghostty

        with patch.dict(os.environ, {"TERM_PROGRAM": "ghostty"}):
            assert ghostty.is_ghostty() is True

    def test_is_ghostty_false_iterm(self):
        """Test detection when TERM_PROGRAM is iTerm."""
        from aiterm.terminal import ghostty

        with patch.dict(os.environ, {"TERM_PROGRAM": "iTerm.app"}):
            assert ghostty.is_ghostty() is False

    def test_is_ghostty_false_empty(self):
        """Test detection when TERM_PROGRAM is not set."""
        from aiterm.terminal import ghostty

        with patch.dict(os.environ, {"TERM_PROGRAM": ""}):
            assert ghostty.is_ghostty() is False

    def test_is_ghostty_case_insensitive(self):
        """Test detection is case-insensitive."""
        from aiterm.terminal import ghostty

        with patch.dict(os.environ, {"TERM_PROGRAM": "Ghostty"}):
            assert ghostty.is_ghostty() is True


class TestGhosttyConfig:
    """Test Ghostty configuration parsing."""

    def test_parse_empty_config(self, tmp_path: Path):
        """Test parsing an empty config file."""
        from aiterm.terminal import ghostty

        config_file = tmp_path / "config"
        config_file.write_text("")

        config = ghostty.parse_config(config_file)
        assert config.font_family == "monospace"
        assert config.font_size == 14
        assert config.theme == ""

    def test_parse_config_with_values(self, tmp_path: Path):
        """Test parsing config with actual values."""
        from aiterm.terminal import ghostty

        config_file = tmp_path / "config"
        config_file.write_text(
            """
font-family = JetBrains Mono
font-size = 16
theme = catppuccin-mocha
window-padding-x = 10
window-padding-y = 8
"""
        )

        config = ghostty.parse_config(config_file)
        assert config.font_family == "JetBrains Mono"
        assert config.font_size == 16
        assert config.theme == "catppuccin-mocha"
        assert config.window_padding_x == 10
        assert config.window_padding_y == 8

    def test_parse_config_with_comments(self, tmp_path: Path):
        """Test parsing config ignores comments."""
        from aiterm.terminal import ghostty

        config_file = tmp_path / "config"
        config_file.write_text(
            """
# This is a comment
font-family = Fira Code
# Another comment
font-size = 14
"""
        )

        config = ghostty.parse_config(config_file)
        assert config.font_family == "Fira Code"
        assert config.font_size == 14

    def test_parse_nonexistent_config(self, tmp_path: Path):
        """Test parsing returns defaults for nonexistent file."""
        from aiterm.terminal import ghostty

        config = ghostty.parse_config(tmp_path / "nonexistent")
        assert config.font_family == "monospace"
        assert config.font_size == 14


class TestGhosttyConfigWrite:
    """Test writing Ghostty configuration."""

    def test_set_config_value_new_file(self, tmp_path: Path):
        """Test setting value creates file if needed."""
        from aiterm.terminal import ghostty

        config_file = tmp_path / "config"
        ghostty.set_config_value("theme", "nord", config_file)

        assert config_file.exists()
        content = config_file.read_text()
        assert "theme = nord" in content

    def test_set_config_value_update_existing(self, tmp_path: Path):
        """Test updating existing value."""
        from aiterm.terminal import ghostty

        config_file = tmp_path / "config"
        config_file.write_text("theme = old-theme\nfont-size = 14\n")

        ghostty.set_config_value("theme", "new-theme", config_file)

        content = config_file.read_text()
        assert "theme = new-theme" in content
        assert "old-theme" not in content
        assert "font-size = 14" in content

    def test_set_config_value_add_new(self, tmp_path: Path):
        """Test adding new value to existing file."""
        from aiterm.terminal import ghostty

        config_file = tmp_path / "config"
        config_file.write_text("font-size = 14\n")

        ghostty.set_config_value("theme", "dracula", config_file)

        content = config_file.read_text()
        assert "theme = dracula" in content
        assert "font-size = 14" in content


class TestGhosttyThemes:
    """Test Ghostty theme functionality."""

    def test_list_themes(self):
        """Test listing available themes."""
        from aiterm.terminal import ghostty

        themes = ghostty.list_themes()
        assert len(themes) > 0
        assert "catppuccin-mocha" in themes
        assert "nord" in themes
        assert "dracula" in themes

    def test_set_theme(self, tmp_path: Path):
        """Test setting a theme."""
        from aiterm.terminal import ghostty

        config_file = tmp_path / "config"
        result = ghostty.set_theme("tokyo-night", config_file)

        assert result is True
        config = ghostty.parse_config(config_file)
        assert config.theme == "tokyo-night"


class TestTerminalDetector:
    """Test terminal type detection."""

    def test_detect_ghostty(self):
        """Test detecting Ghostty terminal."""
        from aiterm.terminal import detect_terminal, TerminalType

        with patch.dict(os.environ, {"TERM_PROGRAM": "ghostty"}):
            assert detect_terminal() == TerminalType.GHOSTTY

    def test_detect_iterm2(self):
        """Test detecting iTerm2 terminal."""
        from aiterm.terminal import detect_terminal, TerminalType

        with patch.dict(os.environ, {"TERM_PROGRAM": "iTerm.app"}):
            assert detect_terminal() == TerminalType.ITERM2

    def test_detect_kitty(self):
        """Test detecting Kitty terminal."""
        from aiterm.terminal import detect_terminal, TerminalType

        with patch.dict(os.environ, {"TERM_PROGRAM": "kitty"}):
            assert detect_terminal() == TerminalType.KITTY

    def test_detect_unknown(self):
        """Test detecting unknown terminal."""
        from aiterm.terminal import detect_terminal, TerminalType

        with patch.dict(os.environ, {"TERM_PROGRAM": ""}):
            assert detect_terminal() == TerminalType.UNKNOWN


class TestTerminalInfo:
    """Test get_terminal_info function."""

    def test_terminal_info_ghostty(self):
        """Test terminal info for Ghostty."""
        from aiterm.terminal import get_terminal_info

        with patch.dict(os.environ, {"TERM_PROGRAM": "ghostty"}):
            info = get_terminal_info()
            assert info["type"] == "ghostty"
            assert info["supports_themes"] is True
            assert info["config_editable"] is True
            assert info["supports_profiles"] is False

    def test_terminal_info_iterm2(self):
        """Test terminal info for iTerm2."""
        from aiterm.terminal import get_terminal_info

        with patch.dict(os.environ, {"TERM_PROGRAM": "iTerm.app"}):
            info = get_terminal_info()
            assert info["type"] == "iterm2"
            assert info["supports_profiles"] is True
            assert info["supports_user_vars"] is True
