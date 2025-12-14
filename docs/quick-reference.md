# Quick Reference: iTerm2 Context Switcher

**ADHD-friendly cheat sheet**

---

## 🎯 Profile Switching (Automatic)

| Directory / File | Profile | Badge |
|------------------|---------|-------|
| `*/production/*` or `*/prod/*` | Production (red) | 🔴 PROD ✗ |
| `~/claude-sessions/` | AI-Session (purple) | 🤖 Claude |
| `~/gemini-sessions/` | AI-Session (purple) | 🤖 Gemini |
| `*/research/*` | Default | 🔬 project-name ✗ |
| R package (has `DESCRIPTION`) | R-Dev (blue) | 📦 package-name ✗ |
| Quarto (has `_quarto.yml`) | Default | 📝 title ✗ |
| Python (has `pyproject.toml`) | Python-Dev | 🐍 package-name ✗ |
| Node.js (has `package.json`) | Node-Dev | 📦 package-name ✗ |
| MCP (has `mcp-server/` dir) | Node-Dev | 🔌 project-name ✗ |
| Emacs Lisp (has `*.el` files) | Default | 🦬 project-name ✗ |
| Anywhere else | Default | (none) |

**Note:** `✗` appears when git repo has uncommitted changes

---

## ⌨️ Hotkeys

| Key | Action |
|-----|--------|
| `⌘⇧C` | Open Claude session window |
| `⌘⇧G` | Open Gemini session window |
| `` ⌘` `` | Open default terminal |

---

## 🔧 Enhanced Functions

### Focus Mode
```bash
focus 25              # 25-min focus session
                      # → Switches to Focus profile
                      # → Shows 🎯 FOCUS badge
                      # → Closes distractions
                      # → Starts timer

unfocus               # Exit focus mode
                      # → Restores context-based profile
```

### Workflow Integration
```bash
startwork medfit      # Jump to project
                      # → Auto-switches to R-Dev
                      # → Shows 📦 medfit badge

here                  # Show context
                      # → Displays current profile/badge info
```

---

## 🧪 Testing

### Quick Test
```bash
# Test R package switching
cd ~/projects/r-packages/active/medfit
# Should see: Blue theme, 📦 medfit

# Test AI switching
cd ~/claude-sessions
# Should see: Purple theme, 🤖 Claude

# Test focus
focus 1
# Should see: Dark theme, 🎯 FOCUS
```

---

## 🔍 Verify Setup

```bash
# Run the verification script (checks everything)
./scripts/verify-setup.sh
```

---

## 🆘 Troubleshooting

### Not Switching?
```bash
# Check if in iTerm2
echo $TERM_PROGRAM
# Should output: iTerm.app

# Check if function loaded
type chpwd_iterm_profile
# Should show function definition

# Manually trigger
chpwd_iterm_profile
```

### Badge Not Showing?
- Preferences → Profiles → Session → Enable "Show badge"

### Profile Not Found?
- Verify exact names: `R-Dev`, `AI-Session`, `Focus`, `Production`
- Case-sensitive!

---

## 📊 Common Workflows

### Morning Start
```bash
startwork medfit      # Jump to project + auto-switch
here                  # Verify context
lt                    # Load + test
```

### Focus Session
```bash
cd ~/projects/r-packages/active/medfit
focus 25              # Enter focus mode
# Work for 25 min
unfocus               # Exit (auto-restores R-Dev)
```

### AI Session
```bash
# Option 1: Hotkey
⌘⇧C                   # Opens Claude window

# Option 2: Navigate
cd ~/claude-sessions
ccc                   # Launch Claude
```

---

## 🔗 Files

- **Integration:** `~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh`
- **Config:** `~/.config/zsh/.zshrc` (sourcing line)
- **Functions:** `~/.config/zsh/functions.zsh` (enhanced focus)

---

**Last Updated:** 2025-12-13
