# OpenCode Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│ AITERM - OpenCode Integration                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ SHELL ALIAS                                                 │
│ ────────────                                                │
│ oc                      → opencode (OpenCode CLI)           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ PYTHON API (aiterm.opencode)                                │
│ ─────────────────────────────                               │
│                                                             │
│ from aiterm.opencode import (                               │
│     load_config,        # Load config from file             │
│     save_config,        # Save config to file               │
│     validate_config,    # Validate configuration            │
│     backup_config,      # Create timestamped backup         │
│     get_config_path,    # Get default config path           │
│ )                                                           │
│                                                             │
│ USAGE                                                       │
│ ──────                                                      │
│ config = load_config()                                      │
│ print(config.enabled_servers)    # ['filesystem', 'memory'] │
│ print(config.has_scroll_acceleration)  # True               │
│                                                             │
│ valid, errors = validate_config()                           │
│ backup_path = backup_config()                               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ CONFIG FILE                                                 │
│ ───────────                                                 │
│ Location: ~/.config/opencode/config.json                    │
│ Backup:   ~/.config/opencode/config.backup-YYYYMMDD-*.json  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ CURRENT CONFIG (Option A - Lean & Fast)                     │
│ ────────────────────────────────────────                    │
│                                                             │
│ {                                                           │
│   "$schema": "https://opencode.ai/config.json",             │
│   "model": "anthropic/claude-sonnet-4-5",                   │
│   "small_model": "anthropic/claude-haiku-4-5",              │
│   "tui": {                                                  │
│     "scroll_acceleration": { "enabled": true }              │
│   },                                                        │
│   "mcp": {                                                  │
│     "filesystem": { "enabled": true },                      │
│     "memory": { "enabled": true },                          │
│     "sequential-thinking": { "enabled": false },            │
│     "playwright": { "enabled": false }                      │
│   }                                                         │
│ }                                                           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ RECOMMENDED MODELS                                          │
│ ───────────────────                                         │
│                                                             │
│ Primary (model):                                            │
│   anthropic/claude-sonnet-4-5    (balanced)                 │
│   anthropic/claude-opus-4-5      (most capable)             │
│   google/gemini-2.5-pro          (alternative)              │
│                                                             │
│ Small (small_model):                                        │
│   anthropic/claude-haiku-4-5     (fast, cheap)              │
│   google/gemini-2.5-flash-lite   (alternative)              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ MCP SERVERS                                                 │
│ ────────────                                                │
│                                                             │
│ Essential (always enabled):                                 │
│   filesystem    File read/write access                      │
│   memory        Persistent context                          │
│                                                             │
│ Optional (enable when needed):                              │
│   sequential-thinking   Complex reasoning                   │
│   playwright            Browser automation                  │
│   github                PR/issue management                 │
│   time                  Timezone tracking                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ OPENCODE CONFIG CLASSES                                     │
│ ────────────────────────                                    │
│                                                             │
│ OpenCodeConfig                                              │
│   .path                 Path to config file                 │
│   .model                Primary model                       │
│   .small_model          Small/fast model                    │
│   .mcp_servers          Dict of MCPServer                   │
│   .agents               Dict of Agent                       │
│   .enabled_servers      List of enabled server names        │
│   .has_scroll_acceleration  Bool                            │
│                                                             │
│ MCPServer                                                   │
│   .name                 Server name                         │
│   .type                 "local" | "remote" | "stdio"        │
│   .command              List of command args                │
│   .enabled              Bool                                │
│   .is_valid()           Returns (bool, errors)              │
│                                                             │
│ Agent                                                       │
│   .name                 Agent name                          │
│   .model                Model override                      │
│   .tools                List of allowed tools               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ OPTIMIZATION ROADMAP                                        │
│ ─────────────────────                                       │
│                                                             │
│ Option A (Applied):                                         │
│   ✓ Explicit models                                         │
│   ✓ Scroll acceleration                                     │
│   ✓ Disabled heavy MCP servers                              │
│                                                             │
│ Option B (Planned):                                         │
│   ○ Custom agents (r-dev, quick)                            │
│   ○ Tool permissions (auto-approve)                         │
│   ○ Instructions loading (CLAUDE.md)                        │
│                                                             │
│ Option C (Future):                                          │
│   ○ Keybinds (ctrl+r → r-dev agent)                         │
│   ○ Custom commands                                         │
│   ○ GitHub MCP integration                                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ COMMON WORKFLOWS                                            │
│ ────────────────                                            │
│                                                             │
│ Quick validate:                                             │
│   python -c "from aiterm.opencode import validate_config;   │
│              print(validate_config())"                      │
│                                                             │
│ Backup before changes:                                      │
│   python -c "from aiterm.opencode import backup_config;     │
│              print(backup_config())"                        │
│                                                             │
│ Check enabled servers:                                      │
│   python -c "from aiterm.opencode import load_config;       │
│              print(load_config().enabled_servers)"          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ SEE ALSO                                                    │
│ ─────────                                                   │
│ Main REFCARD:      docs/REFCARD.md                          │
│ Optimization Plan: OPENCODE-OPTIMIZATION-PLAN.md            │
│ OpenCode Docs:     https://opencode.ai/docs/                │
└─────────────────────────────────────────────────────────────┘
```
