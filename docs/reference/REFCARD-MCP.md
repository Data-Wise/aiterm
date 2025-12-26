# MCP Servers Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│ AITERM - MCP Server Commands                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ LISTING                                                     │
│ ────────                                                    │
│ ait mcp list             List all configured servers        │
│ ait mcp info <name>      Show server details                │
│                                                             │
│ TESTING                                                     │
│ ────────                                                    │
│ ait mcp test <name>      Test specific server               │
│ ait mcp test-all         Test all servers                   │
│ ait mcp test <n> -t 10   Test with 10s timeout              │
│                                                             │
│ VALIDATION                                                  │
│ ───────────                                                 │
│ ait mcp validate         Check configuration syntax         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ COMMON SERVERS                                              │
│ ──────────────                                              │
│                                                             │
│ filesystem     File read/write access                       │
│ memory         Persistent context memory                    │
│ github         PR/issue management (needs token)            │
│ time           Timezone and deadline tracking               │
│ playwright     Browser automation                           │
│ sequential-thinking  Complex reasoning chains               │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ CONFIG FILE                                                 │
│ ───────────                                                 │
│ Claude Code: ~/.claude/settings.json                        │
│ OpenCode:    ~/.config/opencode/config.json                 │
│                                                             │
│ Claude Code format:                                         │
│   {                                                         │
│     "mcpServers": {                                         │
│       "filesystem": {                                       │
│         "command": "npx",                                   │
│         "args": ["-y", "@anthropic/server-filesystem"]      │
│       }                                                     │
│     }                                                       │
│   }                                                         │
│                                                             │
│ OpenCode format:                                            │
│   {                                                         │
│     "mcp": {                                                │
│       "filesystem": {                                       │
│         "type": "local",                                    │
│         "command": ["npx", "-y", "@anthropic/..."],         │
│         "enabled": true                                     │
│       }                                                     │
│     }                                                       │
│   }                                                         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ COMMON WORKFLOWS                                            │
│ ────────────────                                            │
│                                                             │
│ Check all servers work:                                     │
│   ait mcp validate && ait mcp test-all                      │
│                                                             │
│ Debug a server:                                             │
│   ait mcp info <name>                                       │
│   ait mcp test <name> -t 30                                 │
│                                                             │
│ See server command:                                         │
│   ait mcp info filesystem                                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ TROUBLESHOOTING                                             │
│ ───────────────                                             │
│ "Server unreachable"                                        │
│   → Check: which npx (command exists?)                      │
│   → Check: npm install -g @anthropic/server-filesystem      │
│                                                             │
│ "Invalid JSON"                                              │
│   → Check: cat ~/.claude/settings.json | jq .               │
│                                                             │
│ "Timeout"                                                   │
│   → Try: ait mcp test <name> -t 30                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ SEE ALSO                                                    │
│ ─────────                                                   │
│ Main REFCARD:   docs/REFCARD.md                             │
│ Claude REFCARD: docs/reference/REFCARD-CLAUDE.md            │
│ Hooks REFCARD:  docs/reference/REFCARD-HOOKS.md             │
│ MCP Registry:   https://registry.modelcontextprotocol.io    │
└─────────────────────────────────────────────────────────────┘
```
