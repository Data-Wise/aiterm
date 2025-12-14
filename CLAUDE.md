# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**iTerm2 Context Switcher** - Smart context switching for iTerm2 with auto-profile switching, dynamic badges, and hotkey windows. Part of the Data-Wise development toolkit.

Automatically switches iTerm2 profiles and badges based on directory context:
- R packages → Blue theme with package name badge
- AI sessions → Purple theme with AI type badge
- Production paths → Red theme with warning badge
- Focus mode → Minimal dark theme

## Architecture

### Core Integration: zsh/iterm2-integration.zsh

The entire auto-switching logic is contained in a single zsh hook function:

1. **chpwd_iterm_profile()** - Hook function registered with `add-zsh-hook chpwd`
   - Runs on every directory change
   - Detects context by checking PWD patterns and file existence
   - Calls `it2profile` to switch profiles
   - Sets badges via iTerm2 escape sequences (base64 encoded)

2. **Context Detection Logic (priority order)**:
   - **Priority 1 - Location-based:**
     - Production paths (`*/production/*` or `*/prod/*`) → Production profile
     - AI sessions (`~/claude-sessions/` or `~/gemini-sessions/`) → AI-Session profile
     - Research projects (`*/research/*`) → Default profile + 🔬 badge
   - **Priority 2 - File-based:**
     - R packages (has `DESCRIPTION`) → R-Dev profile + 📦 package-name
     - Quarto projects (has `_quarto.yml`) → Default profile + 📝 title
     - Python projects (has `pyproject.toml`) → Python-Dev profile + 🐍 package-name
     - Node.js projects (has `package.json`) → Node-Dev profile + 📦 package-name
     - MCP projects (has `mcp-server/` dir) → Node-Dev profile + 🔌 project-name
     - Emacs Lisp projects (has `*.el` files) → Default profile + 🦬 project-name
   - **Priority 3:** Default fallback → Default profile + clear badge

3. **Git Dirty Indicator**: Badges show `✗` when repo has uncommitted changes (e.g., `📦 medfit ✗`)

4. **Badge Format**: Uses helper function `_iterm_badge "text"` which handles base64 encoding

### Integration Points

**User's zsh configuration** (`~/.config/zsh/.zshrc`):
```zsh
[[ -f ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh ]] && \
  source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh
```

**Enhanced focus functions** (user's `~/.config/zsh/functions.zsh`):
- `focus()` - Switches to Focus profile, sets 🎯 badge, closes distractions
- `unfocus()` - Calls `chpwd_iterm_profile` to restore context-based profile

### Dependencies

- **iTerm2 utilities** - Must be installed at `~/.iterm2/` (specifically `it2profile`)
- **iTerm2 profiles** - User must create these exact profiles: `R-Dev`, `AI-Session`, `Focus`, `Production`
- **$TERM_PROGRAM** - Must equal "iTerm.app" for switching to activate

## Common Commands

### Quick Verification
```bash
# Run the full setup verification (recommended)
./scripts/verify-setup.sh

# Or run from anywhere:
zsh ~/projects/dev-tools/iterm2-context-switcher/scripts/verify-setup.sh
```

### Testing Profile Switching
```bash
# Test R package detection
cd ~/projects/r-packages/active/medfit
# Expected: Blue theme, badge shows "📦 medfit" (or "📦 medfit ✗" if dirty)

# Test AI session detection
cd ~/claude-sessions
# Expected: Purple theme, badge shows "🤖 Claude"

# Test Python project detection
cd ~/projects/dev-tools/some-python-project
# Expected: Python-Dev theme, badge shows "🐍 project-name"

# Test production detection
cd ~/production/server
# Expected: Red theme, badge shows "🔴 PROD"

# Test default
cd ~
# Expected: Default theme, no badge

# Manually trigger switching (for debugging)
chpwd_iterm_profile

# Verify integration loaded
type chpwd_iterm_profile
```

### Debugging
```bash
# Check if running in iTerm2
echo $TERM_PROGRAM  # Should output: iTerm.app

# Verify it2profile utility exists
which it2profile  # Should output: /Users/dt/.iterm2/it2profile

# Check if hook is registered
add-zsh-hook -L | grep chpwd  # Should show chpwd_iterm_profile

# Test badge encoding
echo -n "📦 test" | base64  # See what badge format looks like
```

## Modifying Context Detection

When adding new context patterns to `zsh/iterm2-integration.zsh`:

1. **Add before the default fallback** (line 43-46)
2. **Use PWD pattern matching**: `[[ $PWD == */pattern/* ]]`
3. **Use file detection**: `[[ -f "filename" ]]`
4. **Extract dynamic badge text** from files when possible (see R package example, lines 28-31)
5. **Always redirect stderr**: `it2profile "ProfileName" 2>/dev/null`
6. **Always base64 encode badges**: `$(echo -n "text" | base64)`

Example adding a new context:
```zsh
# Python projects (check for pyproject.toml)
elif [[ -f "pyproject.toml" ]]; then
    local pkg=$(grep "^name" pyproject.toml 2>/dev/null | cut -d'"' -f2)
    it2profile "Python-Dev" 2>/dev/null
    printf "\033]1337;SetBadgeFormat=%s\a" $(echo -n "🐍 ${pkg:-Python}" | base64)
```

## File Structure

```
iterm2-context-switcher/
├── zsh/
│   └── iterm2-integration.zsh    # Core auto-switching logic (~120 lines)
├── scripts/
│   └── verify-setup.sh           # Setup verification script
├── docs/
│   ├── setup-guide.md             # Complete installation guide
│   ├── quick-reference.md         # ADHD-friendly cheat sheet
│   ├── profile-creation-guide.md  # Detailed profile setup
│   └── badge-location-correction.md
├── profiles/                      # Placeholder (profiles created in iTerm2)
├── README.md                      # Project overview
├── CHANGELOG.md                   # Version history
└── CLAUDE.md                      # Claude Code guidance
```

## Key Constraints

1. **Profile names are case-sensitive** - Must match exactly: `R-Dev`, `AI-Session`, `Focus`, `Production`
2. **Only runs in iTerm2** - Checks `$TERM_PROGRAM` before executing
3. **Requires iTerm2 utilities** - `it2profile` must be in PATH (typically `~/.iterm2/`)
4. **Badges require iTerm2 3.4+** - Badge setting moved to General tab in recent versions
5. **No Python/scripting** - Pure zsh for performance and simplicity

## Integration with Data-Wise Toolkit

Works seamlessly with existing 133+ zsh aliases and 22 functions:
- `startwork <project>` - Automatically switches profile when jumping to project
- `focus <minutes>` - Enhanced to switch to Focus profile
- `here` - Shows current context (can display profile info)
- All existing aliases continue working unchanged

## Future Enhancements (Not Implemented)

Documented in CHANGELOG.md under [Unreleased]:
- Smart triggers for test results (change badge on test pass/fail)
- Command duration badges (show how long last command took)
- Python API automation (programmatic profile creation)
- Status bar integration (show context in status bar)
