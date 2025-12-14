# Changelog

All notable changes to iterm2-context-switcher will be documented in this file.

## [1.0.0] - 2025-12-13

### Added
- Initial project structure
- Core auto-switching integration (iterm2-integration.zsh)
- Comprehensive documentation suite (979 lines)
- Profile creation guide with step-by-step instructions
- Setup guide with verification tests
- ADHD-friendly quick reference
- AI session directories (~/claude-sessions, ~/gemini-sessions)

### Changed
- Updated all documentation to use ~/.config/zsh/.zshrc (user's actual location)
- Corrected badge location from Session tab to General tab (iTerm2 3.4+)
- Enhanced profile creation guide with visual diagrams

### Fixed
- Badge configuration instructions (General tab, not Session tab)
- Path references for zsh configuration
- Badge text entry process (field vs Edit dialog)

### Documentation
- README.md - Project overview
- profile-creation-guide.md - Detailed profile setup
- setup-guide.md - Complete installation
- quick-reference.md - ADHD-friendly cheat sheet
- badge-location-correction.md - Badge reference

## [1.1.0] - 2025-12-13

### Added
- **Git dirty indicator** - Badges now show `✗` when repo has uncommitted changes
- **New context patterns:**
  - Python projects (`pyproject.toml`) → Python-Dev profile, 🐍 badge
  - Node.js projects (`package.json`) → Node-Dev profile, 📦 badge
  - Quarto projects (`_quarto.yml`) → 📝 badge with document title
  - MCP server projects (`mcp-server/` dir) → Node-Dev profile, 🔌 badge
  - Emacs Lisp projects (`*.el` files) → 🦬 badge
  - Research projects (`*/research/*`) → 🔬 badge
- **Verification script** - `scripts/verify-setup.sh` checks entire setup
- **Helper functions** - `_iterm_badge()`, `_git_dirty()`, `_project_name()`

### Changed
- Refactored main function with clear priority sections
- Improved code organization with helper functions
- Updated documentation with new context patterns

## [Unreleased]

### Planned
- Optional: Smart triggers for test results
- Optional: Command duration badges
- Optional: Python API automation
- Optional: Status bar integration

---

**Project Status:** Ready for implementation  
**Next:** User creates iTerm2 profiles and enables integration
