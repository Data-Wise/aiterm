# Setup Guide: iTerm2 Context Switcher

Complete installation and configuration instructions.

---

## Prerequisites

- ✅ iTerm2 installed
- ✅ iTerm2 utilities installed (`~/.iterm2/` directory exists)
- ✅ Zsh shell
- ✅ Existing zsh configuration at `~/.config/zsh/`

---

## Step 1: Create iTerm2 Profiles (15 min)

### Profile 1: R-Dev (Blue Theme)

1. Open iTerm2 → **Preferences** (⌘,)
2. Go to **Profiles** tab
3. Click **+** or duplicate "Default"
4. Name: `R-Dev`
5. **Colors** tab:
   - Color Presets → **Solarized Dark**
   - Adjust to blue tint if desired
6. **Session** tab:
   - Badge: `📦`
7. Click outside to save

### Profile 2: AI-Session (Purple Theme)

1. Duplicate "Default" again
2. Name: `AI-Session`
3. **Colors** tab:
   - Color Presets → **Tango Dark** (purple tones)
4. **Session** tab:
   - Badge: `🤖`

### Profile 3: Focus (Minimal Dark)

1. Duplicate "Default" again
2. Name: `Focus`
3. **Colors** tab:
   - Color Presets → **Smoooooth** or **Minimal**
   - Use very dark, distraction-free colors
4. **Session** tab:
   - Badge: `🎯`
5. **Window** tab:
   - Consider enabling "Hide scrollbar"

### Profile 4: Production (Red Theme)

1. Duplicate "Default" again
2. Name: `Production`
3. **Colors** tab:
   - Color Presets → **Red Sands** or custom red theme
4. **Session** tab:
   - Badge: `🔴`

---

## Step 2: Enable Auto-Switching (5 min)

### Add to ~/.config/zsh/.zshrc

```bash
# Open your .zshrc
nano ~/.config/zsh/.zshrc

# Add at the end (or with other source commands):
# iTerm2 Smart Context Switching
[[ -f ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh ]] && \
  source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh
```

### Reload Shell

```bash
source ~/.config/zsh/.zshrc
```

---

## Step 3: Enhance Focus Functions (5 min)

### Backup Current Functions

```bash
cp ~/.config/zsh/functions.zsh ~/.config/zsh/functions.zsh.backup-$(date +%Y%m%d)
```

### Add Enhanced Focus

Open `~/.config/zsh/functions.zsh` and modify the `focus()` function:

```zsh
# Enhanced focus with iTerm2 integration
focus() {
    echo "🎯 ENTERING FOCUS MODE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Switch to Focus profile (iTerm2)
    if [[ "$TERM_PROGRAM" == "iTerm.app" ]]; then
        it2profile "Focus" 2>/dev/null
        printf "\033]1337;SetBadgeFormat=%s\a" $(echo -n "🎯 FOCUS" | base64)
    fi
    
    # Turn off notifications (macOS)
    osascript -e 'tell application "System Events" to keystroke "D" using {command down, shift down, option down, control down}' 2>/dev/null
    
    # Close distracting apps
    osascript -e 'quit app "Slack"' 2>/dev/null
    osascript -e 'quit app "Mail"' 2>/dev/null
    osascript -e 'quit app "Messages"' 2>/dev/null
    
    # Start timer if provided
    if [[ -n "$1" ]]; then
        worktimer "$1" "${2:-focus work}"
    fi
    
    echo "✅ Distractions minimized"
    echo "💪 Focus activated"
}

# Enhanced unfocus with profile restoration
unfocus() {
    echo "🌅 Exiting focus mode..."
    
    # Restore profile based on context
    if [[ "$TERM_PROGRAM" == "iTerm.app" ]]; then
        chpwd_iterm_profile  # Re-run auto-switching logic
    fi
    
    # Turn on notifications
    osascript -e 'tell application "System Events" to keystroke "D" using {command down, shift down, option down, control down}' 2>/dev/null
    
    echo "✅ Notifications restored"
}
```

### Reload Functions

```bash
source ~/.config/zsh/functions.zsh
```

---

## Step 4: Configure Hotkey Windows (Optional, 10 min)

### Hotkey 1: Claude (⌘⇧C)

1. Preferences → **Keys** → **Hotkey Window**
2. Click **Create a Dedicated Hotkey Window**
3. Set hotkey: **⌘⇧C**
4. Profile: **AI-Session**
5. Working Directory: **Reuse previous** or set to `~/claude-sessions`

### Hotkey 2: Gemini (⌘⇧G)

1. Click **+** to add another hotkey window
2. Set hotkey: **⌘⇧G**
3. Profile: **AI-Session**
4. Working Directory: `~/gemini-sessions`

### Hotkey 3: Default Terminal (⌘`)

1. Add another hotkey window
2. Set hotkey: **⌘`** (backtick)
3. Profile: **Default**
4. Working Directory: **Reuse previous**

---

## Step 5: Verification (5 min)

### Test Auto-Switching

```bash
# Test R package switching
cd ~/projects/r-packages/active/medfit
# Expected: Blue theme, badge shows "📦 medfit"

# Test AI session switching
cd ~/claude-sessions
# Expected: Purple theme, badge shows "🤖 Claude"

# Test default
cd ~
# Expected: Default theme, no badge
```

### Test Focus Mode

```bash
cd ~/projects/r-packages/active/medfit
focus 5
# Expected: Switches to Focus profile, badge shows "🎯 FOCUS"

# After 5 min or manually:
unfocus
# Expected: Returns to R-Dev profile, badge shows "📦 medfit"
```

### Test Hotkeys

1. Press **⌘⇧C** → Should open AI-Session window in `~/claude-sessions`
2. Press **⌘⇧G** → Should open AI-Session window in `~/gemini-sessions`
3. Press **⌘`** → Should open Default terminal

---

## Troubleshooting

### Profiles Not Switching

**Check iTerm2 utilities:**
```bash
which it2profile
# Should output: /Users/dt/.iterm2/it2profile
```

**Verify profile names:**
```bash
# Profile names must match exactly (case-sensitive)
# R-Dev, AI-Session, Focus, Production
```

### Badges Not Showing

1. Preferences → Profiles → Session
2. Enable "Show badge"
3. Verify badge text is set

### Function Not Found

```bash
# Verify integration loaded
type chpwd_iterm_profile
# Should show function definition
```

---

## Rollback

If you need to revert:

```bash
# 1. Comment out in ~/.config/zsh/.zshrc
# source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh

# 2. Restore original functions
cp ~/.config/zsh/functions.zsh.backup-YYYYMMDD ~/.config/zsh/functions.zsh

# 3. Reload
source ~/.config/zsh/.zshrc
```

---

## Next Steps

- [ ] Set up smart triggers (see implementation plan)
- [ ] Add command duration badges
- [ ] Customize profile colors
- [ ] Add more context patterns

---

**Setup Time:** ~40 minutes  
**Maintenance:** None (set and forget)
