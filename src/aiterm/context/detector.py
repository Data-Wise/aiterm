"""Context detection for project types.

Detects the type of project in a directory based on files and paths.
Ported from zsh/iterm2-integration.zsh.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional
import subprocess


class ContextType(Enum):
    """Project/context types that can be detected."""

    PRODUCTION = "production"
    AI_SESSION = "ai-session"
    R_PACKAGE = "rpkg"
    PYTHON = "python"
    NODE = "node"
    QUARTO = "quarto"
    EMACS = "emacs"
    DEV_TOOLS = "dev-tools"
    MCP_SERVER = "mcp-server"
    DEFAULT = "default"


@dataclass
class ContextInfo:
    """Information about the detected context."""

    type: ContextType
    name: str
    icon: str
    profile: str
    branch: Optional[str] = None
    is_dirty: bool = False

    @property
    def title(self) -> str:
        """Generate a title string for the terminal."""
        git_info = ""
        if self.branch:
            dirty = "*" if self.is_dirty else ""
            git_info = f" ({self.branch}){dirty}"

        if self.icon:
            return f"{self.icon} {self.name}{git_info}"
        return f"{self.name}{git_info}"


# Mapping of context types to iTerm2 profiles and icons
CONTEXT_CONFIG = {
    ContextType.PRODUCTION: {"profile": "Production", "icon": "🚨"},
    ContextType.AI_SESSION: {"profile": "AI-Session", "icon": "🤖"},
    ContextType.R_PACKAGE: {"profile": "R-Dev", "icon": "📦"},
    ContextType.PYTHON: {"profile": "Python-Dev", "icon": "🐍"},
    ContextType.NODE: {"profile": "Node-Dev", "icon": "📦"},
    ContextType.QUARTO: {"profile": "R-Dev", "icon": "📊"},
    ContextType.EMACS: {"profile": "Emacs", "icon": "⚡"},
    ContextType.DEV_TOOLS: {"profile": "Dev-Tools", "icon": "🔧"},
    ContextType.MCP_SERVER: {"profile": "AI-Session", "icon": "🔌"},
    ContextType.DEFAULT: {"profile": "Default", "icon": ""},
}


def get_git_info(path: Path) -> tuple[Optional[str], bool]:
    """Get git branch name and dirty status.

    Returns:
        Tuple of (branch_name, is_dirty). branch_name is None if not a git repo.
    """
    git_dir = path / ".git"
    if not git_dir.exists():
        # Check if we're in a subdirectory of a git repo
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=2,
            )
            if result.returncode != 0:
                return None, False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None, False

    # Get branch name
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=2,
        )
        branch = result.stdout.strip()

        # If no branch (detached HEAD), try to get tag or show "detached"
        if not branch:
            result = subprocess.run(
                ["git", "describe", "--tags", "--exact-match"],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=2,
            )
            branch = result.stdout.strip() if result.returncode == 0 else "detached"

        # Truncate long branch names
        if len(branch) > 20:
            branch = f"{branch[:8]}…{branch[-8:]}"

        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=2,
        )
        is_dirty = bool(result.stdout.strip())

        return branch, is_dirty

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None, False


def _read_file_field(path: Path, pattern: str, delimiter: str = " ", field: int = 1) -> Optional[str]:
    """Read a field from a file matching a pattern."""
    try:
        content = path.read_text()
        for line in content.splitlines():
            if line.startswith(pattern):
                parts = line.split(delimiter, field + 1)
                if len(parts) > field:
                    return parts[field].strip().strip('"').strip("'")
    except (OSError, UnicodeDecodeError):
        pass
    return None


def _get_json_field(path: Path, field: str) -> Optional[str]:
    """Get a field from a JSON file."""
    try:
        import json

        content = json.loads(path.read_text())
        return content.get(field)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def detect_context(path: Optional[Path] = None) -> ContextInfo:
    """Detect the context/project type for a directory.

    Args:
        path: Directory to analyze. Defaults to current working directory.

    Returns:
        ContextInfo with detected type, name, icon, and profile.
    """
    if path is None:
        path = Path.cwd()
    path = path.resolve()

    # Default name is directory name
    name = path.name
    context_type = ContextType.DEFAULT

    # Get git info first (used for all types)
    branch, is_dirty = get_git_info(path)

    # Priority 1: Safety checks (production paths)
    path_str = str(path).lower()
    if "/production/" in path_str or "/prod/" in path_str:
        context_type = ContextType.PRODUCTION

    # Priority 2: AI session paths
    elif "/claude-sessions/" in path_str or "/gemini-sessions/" in path_str:
        context_type = ContextType.AI_SESSION

    # Priority 3: MCP server detection
    elif (path / "mcp-server").is_dir() or ("mcp" in path_str and (path / "package.json").exists()):
        context_type = ContextType.MCP_SERVER

    # Priority 4: Specific project types
    elif (path / "DESCRIPTION").exists():
        # R package
        context_type = ContextType.R_PACKAGE
        pkg_name = _read_file_field(path / "DESCRIPTION", "Package:", ":", 1)
        if pkg_name:
            name = pkg_name

    elif (path / "pyproject.toml").exists():
        # Python project
        context_type = ContextType.PYTHON
        # Try to get project name from pyproject.toml
        proj_name = _read_file_field(path / "pyproject.toml", "name", "=", 1)
        if proj_name:
            name = proj_name

    elif (path / "package.json").exists():
        # Node.js project
        context_type = ContextType.NODE
        pkg_name = _get_json_field(path / "package.json", "name")
        if pkg_name:
            name = pkg_name

    elif (path / "_quarto.yml").exists():
        # Quarto project
        context_type = ContextType.QUARTO
        title = _read_file_field(path / "_quarto.yml", "title:", ":", 1)
        if title:
            name = title

    elif any((path / f).exists() for f in ["Cask", ".dir-locals.el", "init.el", "early-init.el"]):
        # Emacs project
        context_type = ContextType.EMACS

    elif (path / ".git").is_dir() and any(
        (path / d).is_dir() for d in ["commands", "scripts"]
    ) or ((path / "bin").is_dir() and (path / "Makefile").exists()):
        # Dev tools project
        context_type = ContextType.DEV_TOOLS

    # Get config for this type
    config = CONTEXT_CONFIG[context_type]

    return ContextInfo(
        type=context_type,
        name=name,
        icon=config["icon"],
        profile=config["profile"],
        branch=branch,
        is_dirty=is_dirty,
    )


def detect_context_type(path: Optional[Path] = None) -> ContextType:
    """Simplified detection that returns just the context type."""
    return detect_context(path).type
