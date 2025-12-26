# OpenCode Performance Optimization Plan

**Created:** 2025-12-25
**Status:** Phase 1 (Option A) Complete
**OpenCode Version:** 1.0.201

---

## Current State Analysis

### Configuration Audit (Dec 25, 2025)

| Metric | Value |
|--------|-------|
| Sessions | 12 |
| Messages | 1,434 |
| Total Cost | $0.00 (free models) |
| Input Tokens | 11.0M |
| Output Tokens | 681.9K |
| Cache Read | 95.5M (~90% hit rate!) |
| Top Tool | bash (48.7%) |

### MCP Servers Before

| Server | Status | Notes |
|--------|--------|-------|
| filesystem | enabled | Essential - keep |
| memory | enabled | Good for context - keep |
| sequential-thinking | enabled | Heavy - disabled |
| playwright | enabled | Heavy - disabled |
| everything | disabled | Already off |
| puppeteer | disabled | Already off |

---

## Phase 1: Option A (Lean & Fast) ✅ COMPLETE

**Applied:** Dec 25, 2025
**Config:** `~/.config/opencode/config.json`

### Changes Made

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-4-5",      // NEW
  "small_model": "anthropic/claude-haiku-4-5", // NEW
  "tui": {
    "scroll_acceleration": { "enabled": true } // NEW
  },
  "mcp": {
    "filesystem": { "enabled": true },
    "memory": { "enabled": true },
    "sequential-thinking": { "enabled": false }, // CHANGED
    "playwright": { "enabled": false },          // CHANGED
    "everything": { "enabled": false },
    "puppeteer": { "enabled": false }
  }
}
```

### Expected Improvements

1. **Faster Startup** - 2 fewer MCP servers to initialize
2. **Explicit Model** - No guessing, consistent behavior
3. **Cheaper Summaries** - Haiku for title generation
4. **Better Scrolling** - macOS-native scroll acceleration

---

## Phase 2: Option B (Balanced Power User)

**Status:** Planned
**When:** After validating Option A improvements

### Proposed Additions

```json
{
  "default_agent": "build",
  "agents": {
    "r-dev": {
      "description": "R package development specialist",
      "model": "anthropic/claude-sonnet-4-5",
      "tools": ["bash", "read", "write", "edit", "glob", "grep"]
    },
    "quick": {
      "description": "Fast responses for simple questions",
      "model": "anthropic/claude-haiku-4-5",
      "tools": ["read", "glob", "grep"]
    }
  },
  "tools": {
    "bash": { "permission": "auto" },
    "write": { "permission": "auto" },
    "edit": { "permission": "auto" }
  },
  "instructions": [
    { "path": "CLAUDE.md" },
    { "path": ".claude/rules/*.md" }
  ]
}
```

### Benefits

- Custom agents for different workflows
- Auto-approve safe tools (no dialogs)
- Reads CLAUDE.md files like Claude Code
- Time server for deadline tracking

---

## Phase 3: Option C (Full Ecosystem Integration)

**Status:** Future
**When:** After Option B validation

### Proposed Additions

```json
{
  "agents": {
    "r-dev": { /* R package work */ },
    "research": {
      "description": "Academic research and manuscript writing",
      "model": "anthropic/claude-opus-4-5",
      "tools": ["read", "write", "edit", "websearch", "webfetch"]
    },
    "quick": { /* Fast questions */ }
  },
  "keybinds": {
    "ctrl+r": "agent:r-dev",
    "ctrl+q": "agent:quick"
  },
  "commands": {
    "rpkg-check": {
      "description": "Run R CMD check on current package",
      "command": "R CMD check --as-cran ."
    },
    "sync": {
      "description": "Git sync (add, commit, push)",
      "command": "git add -A && git commit -m 'sync' && git push"
    }
  },
  "mcp": {
    "github": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "{env:GITHUB_TOKEN}" },
      "enabled": true
    }
  }
}
```

### Benefits

- Multiple specialized agents
- Keyboard shortcuts for agent switching
- Custom commands matching workflow
- GitHub integration for PRs

---

## Available Config Templates

### Location: `~/.config/opencode/`

| File | Description |
|------|-------------|
| `config.json` | Active config (Option A applied) |
| `config.json.backup-*` | Timestamped backups |
| `config-recommended.json` | Balanced setup template |
| `config-advanced-dev.json` | Full server catalog (20+ servers) |

### Switching Configs

```bash
# Backup current
cp ~/.config/opencode/config.json ~/.config/opencode/config.json.backup-$(date +%Y%m%d)

# Apply recommended
cp ~/.config/opencode/config-recommended.json ~/.config/opencode/config.json

# Apply advanced (all servers)
cp ~/.config/opencode/config-advanced-dev.json ~/.config/opencode/config.json
```

---

## MCP Server Reference

### Core (Always Enabled)

| Server | Purpose |
|--------|---------|
| filesystem | File read/write access |
| memory | Context persistence |

### On-Demand (Enable When Needed)

| Server | Purpose | When to Enable |
|--------|---------|----------------|
| playwright | Browser automation | E2E testing, scraping |
| sequential-thinking | Complex reasoning | Multi-step problems |
| github | PR/issue management | Code review work |
| time | Timezone/deadlines | Scheduling tasks |

### Specialized (config-advanced-dev.json)

| Server | Purpose |
|--------|---------|
| postgres | Database queries |
| sqlite | Local database |
| docker | Container management |
| kubernetes | K8s cluster ops |
| sentry | Error tracking |
| figma | Design-to-code |
| slack | Team notifications |
| linear | Issue tracking |

---

## Validation Checklist

### After Option A

- [ ] OpenCode starts faster
- [ ] Scroll acceleration feels better
- [ ] Model selection works correctly
- [ ] No missing functionality from disabled servers

### After Option B

- [ ] Custom agents accessible
- [ ] Auto-approval reduces dialogs
- [ ] CLAUDE.md files loaded
- [ ] Tool restrictions work per-agent

### After Option C

- [ ] Keyboard shortcuts work
- [ ] Custom commands execute
- [ ] GitHub MCP connects
- [ ] Full workflow integration smooth

---

## Resources

- [OpenCode Config Docs](https://opencode.ai/docs/config/)
- [OpenCode CLI Reference](https://opencode.ai/docs/cli/)
- [OpenCode GitHub](https://github.com/opencode-ai/opencode)
- [MCP Server Registry](https://registry.modelcontextprotocol.io/)

---

## Next Steps

1. **Validate Option A** - Use OpenCode for a day, note improvements
2. **Apply Option B** - When ready for agents and permissions
3. **Consider GitHub MCP** - For PR workflow integration
4. **Sync with Claude Code** - Share CLAUDE.md files between tools
