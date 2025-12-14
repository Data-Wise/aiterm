# Quick Start

Get up and running in 2 minutes.

## Fastest Setup (Recommended)

```bash
# 1. Run install script
cd ~/projects/dev-tools/iterm2-context-switcher
bash scripts/install-profiles.sh

# 2. Add to your .zshrc
echo 'DISABLE_AUTO_TITLE="true"' >> ~/.zshrc
echo 'source ~/projects/dev-tools/iterm2-context-switcher/zsh/iterm2-integration.zsh' >> ~/.zshrc

# 3. Reload
source ~/.zshrc

# 4. Test
cd ~/projects/r-packages/active/medfit
# Tab should show: 📦 medfit (main)
```

## What You'll See

Titles now include **git branch** and **dirty indicator**:

| When you `cd` to... | Title shows | Profile |
|---------------------|-------------|---------|
| R package (clean) | `📦 medfit (main)` | R-Dev (blue) |
| R package (dirty) | `📦 medfit (main)*` | R-Dev (blue) |
| Python project | `🐍 myapp (dev)` | Python-Dev (green) |
| Node project | `📦 webapp (feature/x)` | Node-Dev (dark) |
| Quarto project | `📊 report (main)` | R-Dev (blue) |
| Emacs project | `⚡ dotemacs (master)` | Emacs (purple) |
| Dev tools | `🔧 cli-tool (dev)*` | Dev-Tools (amber) |
| Production folder | `🚨 server (main)` | Production (red) |
| AI session | `🤖 claude (main)` | AI-Session (purple) |

## Git Info Format

- `(branch)` - Current branch name
- `(branch)*` - Has uncommitted changes
- `(feature/lo…ng-name)` - Long branches truncated

## Next Steps

- [Full Installation](installation.md) - Detailed setup guide
- [Context Detection](../guide/context-detection.md) - How detection works
- [Profiles](../guide/profiles.md) - Customize colors
