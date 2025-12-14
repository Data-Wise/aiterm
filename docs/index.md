# iTerm2 Context Switcher

**Smart context switching for iTerm2 with auto-profile switching and tab titles.**

---

## What It Does

Automatically switches iTerm2 profiles (colors) and sets tab titles based on your current directory:

| Context | Icon | Profile | Detection |
|---------|------|---------|-----------|
| Production | :rotating_light: | Production | `*/production/*` or `*/prod/*` |
| AI Sessions | :robot: | AI-Session | `*/claude-sessions/*` or `*/gemini-sessions/*` |
| R Package | :package: | R-Dev | `DESCRIPTION` file |
| Python | :snake: | Python-Dev | `pyproject.toml` file |
| Node.js | :package: | Node-Dev | `package.json` file |
| Quarto | :bar_chart: | Default | `_quarto.yml` file |
| Emacs | :zap: | Default | `Cask`, `.dir-locals.el`, `init.el` |
| Dev-Tools | :wrench: | Default | `commands/` directory |

---

## Features

- :white_check_mark: Auto-switch profiles by directory context
- :white_check_mark: Tab titles with icons (📦 medfit, 🐍 myproject)
- :white_check_mark: Production environment warnings (🚨)
- :white_check_mark: Caches state to prevent redundant switches
- :white_check_mark: No conflicts with other shell hooks
- :white_check_mark: Zero configuration after setup

---

## Quick Start

```bash
# Add to ~/.config/zsh/.zshrc
DISABLE_AUTO_TITLE="true"

source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh
```

Then reload your shell:

```bash
source ~/.config/zsh/.zshrc
```

See the [Installation Guide](getting-started/installation.md) for detailed setup.

---

## How It Works

When you `cd` into a directory, the integration:

1. **Detects context** - Checks for project files (DESCRIPTION, pyproject.toml, etc.)
2. **Switches profile** - Changes iTerm2 colors via escape sequence
3. **Sets title** - Updates tab title with icon + project name

All changes are cached to prevent redundant switches.
