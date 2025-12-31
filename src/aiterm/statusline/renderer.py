"""StatusLine renderer for Claude Code.

This module provides the main Renderer class that:
- Reads JSON from stdin (from Claude Code)
- Parses and extracts relevant fields
- Delegates to segment renderers
- Outputs formatted 2-line Powerlevel10k-style statusLine
"""

import json
import sys
from typing import Dict, Any, Optional
from pathlib import Path

from aiterm.statusline.config import StatusLineConfig
from aiterm.statusline.themes import Theme, get_theme


class StatusLineRenderer:
    """Main renderer for statusLine output."""

    def __init__(self, config: Optional[StatusLineConfig] = None, theme: Optional[Theme] = None):
        """Initialize renderer.

        Args:
            config: StatusLineConfig instance (creates new if None)
            theme: Theme instance (loads from config if None)
        """
        self.config = config or StatusLineConfig()
        self.theme = theme or get_theme(self.config.get('theme.name', 'purple-charcoal'))

    def render(self, json_input: Optional[str] = None) -> str:
        """Render statusLine from JSON input.

        Args:
            json_input: JSON string from Claude Code (reads from stdin if None)

        Returns:
            Formatted statusLine output (2 lines)
        """
        # Read JSON from stdin if not provided
        if json_input is None:
            json_input = sys.stdin.read()

        # Parse JSON
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError as e:
            # Return error message in statusLine format
            return f"╭─ ⚠️  Invalid JSON input\n╰─ Error: {e.msg}"

        # Extract fields
        workspace = data.get('workspace', {})
        model_data = data.get('model', {})
        cost_data = data.get('cost', {})
        output_style = data.get('output_style', {})
        context_window = data.get('context_window', {})

        cwd = workspace.get('current_dir', '')
        project_dir = workspace.get('project_dir', cwd)
        model_name = model_data.get('display_name', 'Unknown')
        style_name = output_style.get('name', 'default')
        session_id = data.get('session_id', 'default')
        transcript_path = data.get('transcript_path')

        # Extract cost/usage fields
        lines_added = cost_data.get('total_lines_added', 0)
        lines_removed = cost_data.get('total_lines_removed', 0)
        total_duration_ms = cost_data.get('total_duration_ms', 0)

        # Extract context window data
        context_size = context_window.get('context_window_size', 0)
        current_usage = context_window.get('current_usage', {})
        input_tokens = current_usage.get('input_tokens', 0)
        output_tokens = current_usage.get('output_tokens', 0)

        # Build line 1 (directory + git)
        line1 = self._build_line1(cwd, project_dir)

        # Build line 2 (model + time + stats)
        line2 = self._build_line2(
            model_name=model_name,
            session_id=session_id,
            lines_added=lines_added,
            lines_removed=lines_removed,
            style_name=style_name,
            transcript_path=transcript_path
        )

        # Set window title
        self._set_window_title(project_dir, model_name)

        return f"{line1}\n{line2}"

    def _build_line1(self, cwd: str, project_dir: str) -> str:
        """Build line 1 (directory + git).

        Args:
            cwd: Current working directory
            project_dir: Project root directory

        Returns:
            Formatted line 1
        """
        # Import here to avoid circular imports
        from aiterm.statusline.segments import (
            ProjectSegment,
            GitSegment
        )

        # Get project segment
        project_segment = ProjectSegment(self.config, self.theme)
        project_output = project_segment.render(cwd, project_dir)

        # Get git segment
        git_segment = GitSegment(self.config, self.theme)
        git_output = git_segment.render(cwd)

        # Assemble line 1
        line1 = f"╭─{project_output}"

        if git_output:
            line1 += git_output
        else:
            # Close directory segment
            line1 += "\033[0m\033[38;5;4m▓▒░\033[0m"

        return line1

    def _build_line2(
        self,
        model_name: str,
        session_id: str,
        lines_added: int,
        lines_removed: int,
        style_name: str,
        transcript_path: Optional[str] = None
    ) -> str:
        """Build line 2 (model + time + stats).

        Args:
            model_name: Model display name
            session_id: Session ID for duration tracking
            lines_added: Total lines added
            lines_removed: Total lines removed
            style_name: Output style name
            transcript_path: Optional path to session transcript

        Returns:
            Formatted line 2
        """
        # Import here to avoid circular imports
        from aiterm.statusline.segments import (
            ModelSegment,
            TimeSegment,
            ThinkingSegment,
            LinesSegment,
            UsageSegment
        )

        # Model segment
        model_segment = ModelSegment(self.config, self.theme)
        model_output = model_segment.render(model_name)

        # Thinking mode indicator
        thinking_segment = ThinkingSegment(self.config, self.theme)
        thinking_output = thinking_segment.render()

        # Time segments
        time_segment = TimeSegment(self.config, self.theme)
        time_output = time_segment.render(session_id, transcript_path)

        # Lines changed
        lines_segment = LinesSegment(self.config, self.theme)
        lines_output = lines_segment.render(lines_added, lines_removed)

        # Build line 2
        line2 = f"╰─ {model_output}"

        # Add thinking indicator (includes separator if enabled)
        line2 += thinking_output

        # Add background agents count
        if self.config.get('display.show_background_agents', True):
            from aiterm.statusline.agents import AgentDetector
            detector = AgentDetector()
            agent_count = detector.get_running_count(session_id)
            if agent_count > 0:
                line2 += f" \033[{self.theme.separator_fg}m│\033[0m \033[38;5;2m🤖{agent_count}\033[0m"

        # Add time
        line2 += time_output

        # Add usage tracking
        usage_segment = UsageSegment(self.config, self.theme)
        usage_output = usage_segment.render()
        if usage_output:
            line2 += f" \033[{self.theme.separator_fg}m│\033[0m {usage_output}"

        # Add lines if available
        if lines_output:
            line2 += f" \033[{self.theme.separator_fg}m│\033[0m {lines_output}"

        # Add style if not default
        if style_name and style_name != 'default':
            line2 += f" \033[{self.theme.separator_fg}m│\033[0m \033[{self.theme.style_fg}m[{style_name}]\033[0m"

        return line2

    def _set_window_title(self, project_dir: str, model_name: str) -> None:
        """Set terminal window title.

        Args:
            project_dir: Project directory path
            model_name: Model name
        """
        # Import here to avoid circular imports
        from aiterm.statusline.segments import ProjectSegment

        project_segment = ProjectSegment(self.config, self.theme)
        project_name = Path(project_dir).name
        project_icon = project_segment._get_project_icon(project_dir)

        # ANSI escape sequence for window title
        # Format: ESC ] 0 ; text BEL
        title = f"{project_icon} {project_name} ({model_name})"
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()
