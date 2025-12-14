# Context Detection

How the switcher detects your project type.

## Detection Priority

Contexts are checked in this order (first match wins):

```
1. 🚨 Production   (path)     ─┐
2. 🤖 AI-Session   (path)      │ Safety first
3. 📦 R Package    (DESCRIPTION)─┐
4. 🐍 Python       (pyproject.toml)│ Language-specific
5. 📦 Node         (package.json)  ─┘
6. 📊 Quarto       (_quarto.yml)─┐
7. ⚡ Emacs        (Cask, etc.)  │ Document/Tool types
8. 🔧 Dev-Tools    (commands/)  ─┘
9.    Default      (fallback)
```

## Detection Methods

### Path-based Detection

| Context | Path Pattern |
|---------|--------------|
| Production | `*/production/*` or `*/prod/*` |
| AI Sessions | `*/claude-sessions/*` or `*/gemini-sessions/*` |

### File-based Detection

| Context | File/Directory |
|---------|----------------|
| R Package | `DESCRIPTION` file |
| Python | `pyproject.toml` file |
| Node.js | `package.json` file |
| Quarto | `_quarto.yml` file |
| Emacs | `Cask`, `.dir-locals.el`, `init.el`, or `early-init.el` |
| Dev-Tools | `commands/` directory |

## Conflict Resolution

When multiple markers exist, the **first match** wins:

| Scenario | Winner | Why |
|----------|--------|-----|
| R pkg with Quarto vignettes | 📦 R | R detected first |
| Python with Makefile | 🐍 Python | Python detected first |
| Quarto in production folder | 🚨 Production | Safety priority |

## Project Name Extraction

For some contexts, the project name is extracted from files:

| Context | Source |
|---------|--------|
| R Package | `Package:` field in DESCRIPTION |
| Node.js | `"name"` field in package.json |
| Quarto | `title:` field in _quarto.yml |
| Others | Directory name |
