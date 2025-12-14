# Quick Start

Get up and running in 2 minutes.

## Minimal Setup

```bash
# 1. Add to your .zshrc
echo 'DISABLE_AUTO_TITLE="true"' >> ~/.zshrc
echo 'source ~/path/to/iterm2-context-switcher/zsh/iterm2-integration.zsh' >> ~/.zshrc

# 2. Reload
source ~/.zshrc

# 3. Test
cd ~/your/r-package
# Tab should show: 📦 package-name
```

## What You'll See

| When you `cd` to... | Title shows | Profile |
|---------------------|-------------|---------|
| R package (has DESCRIPTION) | 📦 pkgname | R-Dev (green) |
| Python project | 🐍 dirname | Python-Dev |
| Node project | 📦 pkgname | Node-Dev |
| Quarto project | 📊 dirname | Default |
| Emacs project | ⚡ dirname | Default |
| Dev tools | 🔧 dirname | Default |
| Production folder | 🚨 dirname | Production (red) |

## Next Steps

- [Full Installation](installation.md) - Create all profiles
- [Context Detection](../guide/context-detection.md) - How detection works
- [Triggers](../guide/triggers.md) - Claude Code notifications
