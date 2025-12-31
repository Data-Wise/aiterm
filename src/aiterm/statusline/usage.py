"""Usage tracking for Claude Code sessions and weekly limits.

This module provides usage tracking functionality for the statusLine.
Currently uses placeholder data until Claude Code provides an official API.

Future integration points:
- Option A: Parse `claude --usage` command output
- Option B: Read from Claude Code internal files/database
- Option C: Use usage fields from JSON input (if added by Claude Code)
"""

from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import subprocess


@dataclass
class UsageData:
    """Usage tracking data.

    Attributes:
        current: Current usage count
        limit: Maximum allowed usage
        reset_time: Timestamp when usage resets (Unix timestamp)
    """
    current: int
    limit: int
    reset_time: int  # Unix timestamp

    def percent_used(self) -> float:
        """Calculate percentage of usage.

        Returns:
            Percentage (0.0 to 100.0)
        """
        if self.limit == 0:
            return 0.0
        return (self.current / self.limit) * 100

    def time_until_reset(self) -> str:
        """Format time until reset.

        Returns:
            Formatted string like "2h15m", "3d4h", etc.
        """
        now = int(datetime.now().timestamp())
        seconds_left = self.reset_time - now

        if seconds_left <= 0:
            return "now"

        # Convert to appropriate units
        if seconds_left < 3600:  # < 1 hour
            minutes = seconds_left // 60
            return f"{minutes}m"
        elif seconds_left < 86400:  # < 1 day
            hours = seconds_left // 3600
            minutes = (seconds_left % 3600) // 60
            return f"{hours}h{minutes}m" if minutes > 0 else f"{hours}h"
        else:  # >= 1 day
            days = seconds_left // 86400
            hours = (seconds_left % 86400) // 3600
            return f"{days}d{hours}h" if hours > 0 else f"{days}d"


class UsageTracker:
    """Tracks Claude Code usage limits.

    This is a placeholder implementation that returns mock data.
    Will be updated when Claude Code provides an official usage tracking API.
    """

    def __init__(self):
        """Initialize usage tracker."""
        pass

    def get_session_usage(self) -> Optional[UsageData]:
        """Get current session usage.

        Returns:
            UsageData for session usage, or None if not available
        """
        # PLACEHOLDER: Return mock data
        # TODO: Replace with actual Claude Code API call
        #
        # Potential implementation:
        # - Parse `claude --usage` output
        # - Read from ~/.claude/usage.json
        # - Extract from Claude Code's internal database
        #
        # For now, return None to disable display
        return None

        # Example of what real data might look like:
        # now = int(datetime.now().timestamp())
        # reset_in_2h = now + (2 * 3600)
        # return UsageData(
        #     current=45,
        #     limit=100,
        #     reset_time=reset_in_2h
        # )

    def get_weekly_usage(self) -> Optional[UsageData]:
        """Get current weekly usage.

        Returns:
            UsageData for weekly usage, or None if not available
        """
        # PLACEHOLDER: Return mock data
        # TODO: Replace with actual Claude Code API call
        return None

        # Example of what real data might look like:
        # now = int(datetime.now().timestamp())
        # reset_in_3d = now + (3 * 86400)
        # return UsageData(
        #     current=234,
        #     limit=500,
        #     reset_time=reset_in_3d
        # )

    def _parse_claude_usage_command(self) -> Tuple[Optional[UsageData], Optional[UsageData]]:
        """Parse output from `claude --usage` command (if it exists).

        This is a placeholder for future implementation.

        Returns:
            Tuple of (session_usage, weekly_usage)
        """
        # PLACEHOLDER: This command may not exist yet
        #
        # Future implementation:
        # try:
        #     result = subprocess.run(
        #         ['claude', '--usage'],
        #         capture_output=True,
        #         text=True,
        #         timeout=5
        #     )
        #
        #     if result.returncode == 0:
        #         output = result.stdout
        #         # Parse output like:
        #         # Session: 45/100 messages (resets in 2h 15m)
        #         # Weekly: 234/500 messages (resets in 3d 4h)
        #         ...
        #
        # except Exception:
        #     pass

        return (None, None)


def format_usage_display(
    session: Optional[UsageData],
    weekly: Optional[UsageData],
    compact: bool = True
) -> str:
    """Format usage data for statusLine display.

    Args:
        session: Session usage data
        weekly: Weekly usage data
        compact: Use compact format (default: True)

    Returns:
        Formatted string for display, or empty if no data
    """
    if not session and not weekly:
        return ""

    parts = []

    if session:
        if compact:
            # Compact: S:45/100(2h)
            parts.append(f"S:{session.current}/{session.limit}({session.time_until_reset()})")
        else:
            # Verbose: Session:45/100 (2h15m)
            parts.append(f"Session:{session.current}/{session.limit} ({session.time_until_reset()})")

    if weekly:
        if compact:
            # Compact: W:234/500(3d)
            parts.append(f"W:{weekly.current}/{weekly.limit}({weekly.time_until_reset()})")
        else:
            # Verbose: Weekly:234/500 (3d4h)
            parts.append(f"Weekly:{weekly.current}/{weekly.limit} ({weekly.time_until_reset()})")

    return " ".join(parts)


def get_usage_color(usage: UsageData, warning_threshold: int = 80) -> str:
    """Get color code based on usage percentage.

    Args:
        usage: Usage data
        warning_threshold: Percentage threshold for warning (default: 80)

    Returns:
        ANSI color code
    """
    percent = usage.percent_used()

    if percent < 50:
        return "38;5;2"  # Green
    elif percent < warning_threshold:
        return "38;5;3"  # Yellow
    elif percent < 95:
        return "38;5;208"  # Orange
    else:
        return "38;5;1"  # Red
