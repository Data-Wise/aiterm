# iTerm2 Context Switcher

**Smart context switching for iTerm2 with auto-profile switching and tab titles.**

---

## What It Does

Automatically switches iTerm2 profiles (colors) and sets tab titles based on your current directory:

| Context | Icon | Profile | Detection |
|---------|------|---------|-----------|
| Production | 🚨 | Production | `*/production/*` or `*/prod/*` |
| AI Sessions | 🤖 | AI-Session | `*/claude-sessions/*` or `*/gemini-sessions/*` |
| R Package | 📦 | R-Dev | `DESCRIPTION` file |
| Python | 🐍 | Python-Dev | `pyproject.toml` file |
| Node.js | 📦 | Node-Dev | `package.json` file |
| Quarto | 📊 | Default | `_quarto.yml` file |
| Emacs | ⚡ | Default | `Cask`, `.dir-locals.el`, `init.el` |
| Dev-Tools | 🔧 | Default | `commands/` directory |

---

## Quick Start

### 1. Create iTerm2 Profiles

The following profiles are required (create in iTerm2 → Settings → Profiles):

| Profile | Purpose | Suggested Colors |
|---------|---------|------------------|
| Default | Fallback | Your default |
| R-Dev | R packages | Green background |
| Python-Dev | Python projects | Green/jungle |
| Node-Dev | Node.js projects | Dark theme |
| AI-Session | Claude/Gemini work | Purple |
| Production | Production servers | Red (warning) |

### 2. Enable Auto-Switching

Add to `~/.config/zsh/.zshrc`:

```zsh
# Disable OMZ auto-title (we set our own)
DISABLE_AUTO_TITLE="true"

# iTerm2 Smart Context Switching
[[ -f ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh ]] && \
  source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh
```

### 3. Configure iTerm2 Title

- Settings → Profiles → General → Title
- Set to: **Session Name** (or **Session Name + Job**)

### 4. Reload Shell

```bash
source ~/.config/zsh/.zshrc
```

---

## Features

- ✅ Auto-switch profiles by directory context
- ✅ Tab titles with icons (📦 medfit, 🐍 myproject)
- ✅ Production environment warnings (🚨)
- ✅ Caches state to prevent redundant switches
- ✅ No conflicts with other shell hooks
- ✅ Zero configuration after setup

---

## Optional: Claude Code Triggers

Add iTerm2 triggers for Claude Code notifications:

**Settings → Profiles → Default → Advanced → Triggers → Edit**

| Regex | Action | Parameter |
|-------|--------|-----------|
| `^> $` | Post Notification | `Claude waiting` |
| `(Allow\|Deny)\?` | Bounce Dock Icon | |

---

## Project Structure

```
iterm2-context-switcher/
├── README.md
├── CLAUDE.md              # AI assistant instructions
├── profiles/              # Dynamic Profiles JSON
├── zsh/
│   └── iterm2-integration.zsh  # Main integration
├── scripts/
│   ├── verify-setup.sh    # Setup verification
│   ├── diagnose.sh        # Troubleshooting
│   └── add-triggers.sh    # Trigger setup guide
└── docs/
    ├── setup-guide.md
    └── quick-reference.md
```

---

## Troubleshooting

**Profiles not switching?**
- Verify profile names exist exactly (case-sensitive)
- Check `echo $TERM_PROGRAM` shows "iTerm.app"
- Run: `source ~/.config/zsh/.zshrc`

**Title not showing?**
- Set iTerm2 title to "Session Name"
- Add `DISABLE_AUTO_TITLE="true"` before OMZ loads

**Colors not changing?**
- Ensure profiles have different background colors
- Check Dynamic Profiles at `~/Library/Application Support/iTerm2/DynamicProfiles/`

---

## License

MIT

---

**Last Updated:** 2025-12-13
**Version:** 2.0
