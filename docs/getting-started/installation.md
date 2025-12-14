# Installation

## Requirements

- iTerm2 (macOS terminal)
- Zsh shell
- Git repository for your project

## Step 1: Create iTerm2 Profiles

Open iTerm2 → Settings → Profiles, and create these profiles:

| Profile | Purpose | Suggested Colors |
|---------|---------|------------------|
| Default | Fallback | Your default |
| R-Dev | R packages | Green background |
| Python-Dev | Python projects | Green/jungle |
| Node-Dev | Node.js projects | Dark theme |
| AI-Session | Claude/Gemini work | Purple |
| Production | Production servers | Red (warning) |

!!! tip "Dynamic Profiles"
    Python-Dev and Node-Dev can be auto-installed via Dynamic Profiles.
    Copy `profiles/context-switcher-profiles.json` to:
    ```
    ~/Library/Application Support/iTerm2/DynamicProfiles/
    ```

## Step 2: Configure Shell

Add to `~/.config/zsh/.zshrc` (or `~/.zshrc`):

```zsh
# Disable OMZ auto-title (we set our own)
DISABLE_AUTO_TITLE="true"

# iTerm2 Smart Context Switching
[[ -f ~/path/to/iterm2-context-switcher/zsh/iterm2-integration.zsh ]] && \
  source ~/path/to/iterm2-context-switcher/zsh/iterm2-integration.zsh
```

!!! warning "DISABLE_AUTO_TITLE"
    This must be set **before** Oh My Zsh or Antidote loads, otherwise
    OMZ will override your tab titles.

## Step 3: Configure iTerm2 Title

1. Open iTerm2 → Settings → Profiles → General
2. Set **Title** to: `Session Name` (or `Session Name + Job`)

## Step 4: Reload Shell

```bash
source ~/.config/zsh/.zshrc
```

## Verify Installation

```bash
cd ~/some/r-package   # Should show 📦 + green background
cd ~                   # Should return to default
```
