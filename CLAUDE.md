# CLAUDE.md

This file provides guidance to Claude Code when working with the aiterm project.

## Project Overview

**aiterm** (formerly iterm2-context-switcher) - Terminal optimizer CLI for AI-assisted development with Claude Code and Gemini CLI.

**What it does:**
- Optimizes terminal setup (iTerm2 primarily) for AI coding workflows
- Manages terminal profiles, context detection, and visual customization
- Integrates with Claude Code CLI (hooks, commands, auto-approvals, MCP servers)
- Supports Gemini CLI integration
- Provides workflow templates for different dev contexts

**Target Users:**
- Primary: DT (power user, R developer, statistician, ADHD-friendly workflows)
- Secondary: Public release (developers using Claude Code/Gemini CLI)

**Tech Stack:**
- **Language:** Python 3.10+
- **CLI Framework:** Typer (modern CLI with type hints)
- **Terminal:** Rich (beautiful terminal output)
- **Prompts:** Questionary (interactive prompts)
- **Testing:** pytest
- **Distribution:** pip/PyPI

---

## Project Status: Week 1 MVP (v0.1.0-dev)

**Current Phase:** Documentation complete, starting Python implementation

**This Week's Goals:**
1. Set up Python project structure (Poetry/pip)
2. Migrate zsh integration to Python
3. Build core CLI commands (init, doctor, profile, claude)
4. Port existing test suite
5. Get DT using it daily

See `ROADMAP.md` for detailed day-by-day plan.

---

## Architecture

### High-Level Structure

```
aiterm/
├── src/aiterm/              # Main package
│   ├── __init__.py
│   ├── cli/                 # CLI commands (Typer)
│   │   ├── __init__.py
│   │   ├── main.py          # Main entry point
│   │   ├── profile.py       # Profile commands
│   │   ├── claude.py        # Claude Code commands
│   │   └── context.py       # Context commands
│   ├── terminal/            # Terminal backends
│   │   ├── __init__.py
│   │   ├── base.py          # Abstract base
│   │   ├── iterm2.py        # iTerm2 implementation
│   │   └── detector.py      # Auto-detect terminal
│   ├── context/             # Context detection
│   │   ├── __init__.py
│   │   └── detector.py      # Project type detection
│   ├── claude/              # Claude Code integration
│   │   ├── __init__.py
│   │   ├── settings.py      # Settings management
│   │   ├── hooks.py         # Hook management
│   │   └── commands.py      # Command templates
│   └── utils/               # Utilities
│       ├── __init__.py
│       ├── config.py        # Config file handling
│       └── shell.py         # Shell integration
├── templates/               # User-facing templates
│   ├── profiles/            # iTerm2 profile JSON
│   ├── hooks/               # Hook templates
│   └── commands/            # Command templates
├── tests/                   # Test suite
│   ├── test_cli.py
│   ├── test_context.py
│   └── test_terminal.py
├── docs/                    # Documentation (MkDocs)
├── pyproject.toml           # Project config
└── README.md
```

### Key Design Principles

1. **CLI-First Architecture**
   - Core logic in library (`src/aiterm/`)
   - CLI wraps library (thin layer in `cli/`)
   - Testable, reusable components

2. **Progressive Enhancement**
   - Start simple (MVP in 1 week)
   - Add features incrementally
   - Maintain backwards compatibility

3. **Terminal Abstraction**
   - Abstract base class for terminals
   - iTerm2 first, others later
   - Graceful degradation for unsupported features

4. **Medium Integration Depth**
   - Active terminal control (escape sequences, API)
   - Not just config generation
   - Not full IDE replacement

---

## Code to Migrate from v2.5.0

### Priority 1: Core Functionality

**From:** `zsh/iterm2-integration.zsh` (186 lines)
**To:** `src/aiterm/terminal/iterm2.py` + `src/aiterm/context/detector.py`

Key functions to port:
- `_iterm_detect_context()` - Main detection logic
- `_iterm_switch_profile()` - Profile switching
- `_iterm_set_title()` - Tab title setting
- `_iterm_set_status_vars()` - Status bar variables
- `_iterm_git_info()` - Git branch/dirty detection

Context detection patterns (8 types):
1. Production paths (`*/production/*`, `*/prod/*`) → Production profile
2. AI sessions (`*/claude-sessions/*`, `*/gemini-sessions/*`) → AI-Session profile
3. R packages (`DESCRIPTION` file) → R-Dev profile
4. Python (`pyproject.toml`) → Python-Dev profile
5. Node.js (`package.json`) → Node-Dev profile
6. Quarto (`_quarto.yml`) → R-Dev profile
7. MCP (`mcp-server/` dir) → AI-Session profile
8. Dev-tools (`.git` + `scripts/`) → Dev-Tools profile

### Priority 2: Testing

**From:** `scripts/test-context-switcher.sh` (370 lines)
**To:** `tests/test_context.py`, `tests/test_terminal.py`

15 existing tests to port:
- R package detection
- Python project detection
- Node.js project detection
- MCP server detection
- Production path detection
- Git dirty indicator
- Quarto project detection
- Default fallback
- (Plus integration tests)

### Priority 3: Templates

**From:** `statusline-alternatives/`, existing profiles
**To:** `templates/profiles/`

3 theme variants:
- cool-blues
- forest-greens
- purple-charcoal

---

## Development Workflow

### Setting Up Dev Environment

```bash
# Clone repo
cd ~/projects/dev-tools/iterm2-context-switcher

# Set up Python environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Try CLI
aiterm --help
```

### Adding a New Command

1. Create command file in `src/aiterm/cli/`
2. Define command using Typer
3. Add tests in `tests/`
4. Update documentation

Example:
```python
# src/aiterm/cli/profile.py
import typer
from rich import print

app = typer.Typer()

@app.command()
def list():
    """List available profiles"""
    print("[bold]Available Profiles:[/bold]")
    # Implementation
```

### Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_cli.py::test_init_command

# Run with coverage
pytest --cov=aiterm

# Run integration tests (requires iTerm2)
pytest -m integration
```

---

## Common Commands for Claude Code

When working on this project, you might run:

```bash
# Development
aiterm --help                    # See available commands
aiterm doctor                    # Check installation
python -m pytest                 # Run tests

# Testing existing functionality
cd ~/test-dir
# (zsh integration still works for now)

# Git operations
git status
git add .
git commit -m "feat: add profile management"
git push
```

---

## File-Specific Guidance

### `src/aiterm/cli/main.py`
- Main entry point
- Registers all subcommands
- Global options (--verbose, --config)
- Version info

### `src/aiterm/terminal/iterm2.py`
- iTerm2-specific implementation
- Escape sequences for profile/title
- Python API integration (future)
- Status bar user variables

### `src/aiterm/context/detector.py`
- Project type detection
- File-based detection (DESCRIPTION, package.json, etc.)
- Path-based detection (production/, claude-sessions/)
- Git integration

### `src/aiterm/claude/settings.py`
- Read/write `~/.claude/settings.json`
- Validate settings structure
- Merge auto-approvals
- Backup functionality

---

## Current Limitations & Future Work

### MVP Limitations (v0.1.0)
- iTerm2 only (no multi-terminal yet)
- Basic Claude Code integration (settings only, no hooks/commands)
- No Gemini integration yet
- No web UI
- Manual installation

### Planned for v0.2.0 (Phase 2)
- Hook management system
- Command template library
- MCP server integration
- Advanced status bar builder

See `IDEAS.md` for full feature roadmap.

---

## Integration with DT's Existing Setup

### This Project Fits Into:

**Existing Tools:**
- `~/.claude/statusline-p10k.sh` - Status bar (will integrate)
- `~/.claude/quota-config.json` - Quota tracking (will use)
- `qu` shell command - Quick quota update (will call)
- `~/.claude/settings.json` - Claude Code config (will manage)
- `~/.config/zsh/functions.zsh` - Shell functions (will complement)

**Workflow Commands:**
- `/recap`, `/next`, `/focus` - ADHD-friendly workflow (will enhance)
- `work`, `finish`, `dash`, `pp` - Project management (will integrate with context)

**MCP Servers:**
- Statistical Research MCP (14 tools, 17 skills)
- Shell MCP server
- Filesystem MCP
- (aiterm will help configure these)

---

## Key Constraints

1. **ADHD-Friendly:** Fast commands, clear output, no analysis paralysis
2. **Week 1 MVP:** Ship v0.1.0 in 7 days, DT using daily
3. **No Regressions:** Must work as well as v2.5.0 zsh version
4. **Python 3.10+:** Modern Python, type hints, async-ready
5. **Medium Integration:** Active control, not just config files

---

## Success Criteria

### MVP (v0.1.0)
- [ ] Installs in <5 minutes
- [ ] `aiterm init` sets up terminal
- [ ] Context switching works (8 types)
- [ ] Claude Code auto-approvals manageable
- [ ] Tests pass (>80% coverage)
- [ ] DT uses daily for 1 week

### Long-term (v1.0.0)
- [ ] Multi-terminal support
- [ ] 10+ external users
- [ ] Community templates
- [ ] Web UI option
- [ ] Featured in Claude Code docs

---

## Questions? Check:

1. `IDEAS.md` - Full feature brainstorm
2. `ROADMAP.md` - Week 1 day-by-day plan
3. `.STATUS` - Current progress
4. Existing code in `zsh/` and `scripts/` for reference

---

**Remember:** This is a pivot from a working project. The zsh integration still works. We're rebuilding in Python for expandability, not fixing something broken. Take time to understand the existing code before porting!
