# Installation

Complete installation guide for iTerm2 Context Switcher.

## Requirements

- iTerm2 (macOS terminal)
- Zsh shell
- Git (for project detection)

---

## Option 1: Install Script (Recommended)

The fastest way to get started:

```bash
cd ~/projects/dev-tools/iterm2-context-switcher
bash scripts/install-profiles.sh
```

This automatically installs all 7 color profiles via iTerm2 Dynamic Profiles.

### After Running Install Script

1. **Add to your .zshrc** (before Oh-My-Zsh loads):

    ```zsh
    DISABLE_AUTO_TITLE="true"
    ```

2. **Add at end of .zshrc**:

    ```zsh
    source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh
    ```

3. **Configure iTerm2 profiles** (one-time):

    For each installed profile (R-Dev, AI-Session, etc.):

    - Open iTerm2 → Settings → Profiles
    - Select the profile
    - Go to **General** tab
    - Set **Title** to: `Session Name`
    - Check: `Applications in terminal may change title`

4. **Reload shell**:

    ```bash
    source ~/.zshrc
    ```

---

## Option 2: Manual Installation

### Step 1: Install Dynamic Profiles

Copy the profiles JSON to iTerm2:

```bash
cp profiles/context-switcher-profiles.json \
   ~/Library/Application\ Support/iTerm2/DynamicProfiles/
```

### Step 2: Configure Shell

Add to `~/.config/zsh/.zshrc` (or `~/.zshrc`):

```zsh
# Disable OMZ auto-title (MUST be before Oh My Zsh loads)
DISABLE_AUTO_TITLE="true"

# At end of file:
source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh
```

!!! warning "DISABLE_AUTO_TITLE"
    This must be set **before** Oh My Zsh or Antidote loads, otherwise
    OMZ will override your tab titles.

### Step 3: Configure iTerm2 Title

For **each profile** (R-Dev, AI-Session, Production, etc.):

1. Open iTerm2 → Settings → Profiles → General
2. Set **Title** to: `Session Name`
3. Check: `Applications in terminal may change title`

!!! tip "Why Session Name?"
    iTerm2 escape sequences only work when Title is set to "Session Name".
    Without this, titles will show "zsh" instead of your project name.

### Step 4: Reload Shell

```bash
source ~/.zshrc
```

---

## Installed Profiles

The install script adds these 7 profiles:

| Profile | Theme | Use Case |
|---------|-------|----------|
| R-Dev | Blue | R packages, Quarto |
| AI-Session | Purple | Claude/Gemini sessions |
| Production | Red | Production warning |
| Dev-Tools | Amber | Shell scripts, CLI tools |
| Emacs | Purple | Emacs configurations |
| Python-Dev | Green | Python projects |
| Node-Dev | Dark | Node.js projects |

---

## Verify Installation

```bash
# Test R package
cd ~/projects/r-packages/active/medfit
# Expected: 📦 medfit (main) with blue theme

# Test default
cd ~
# Expected: Default profile, no icon

# Check hook is registered
type chpwd_iterm_profile
```

---

## Troubleshooting

**Title shows "zsh" instead of project name:**

- Set each profile's Title to "Session Name" in iTerm2 Preferences

**Profile colors don't change:**

- Verify profile names match exactly (case-sensitive)
- Check `echo $TERM_PROGRAM` shows `iTerm.app`

**Git branch not showing:**

- Ensure you're in a git repository
- Run `git branch --show-current` to verify

See [Troubleshooting Guide](../reference/troubleshooting.md) for more help.
