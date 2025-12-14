#!/usr/bin/env zsh
# ITERM2 CONTEXT SWITCHER - Profile + Title
# Switches profile colors AND sets tab title with icon

# Cache to avoid redundant switches
typeset -g _ITERM_CURRENT_PROFILE=""
typeset -g _ITERM_CURRENT_TITLE=""

_iterm_switch_profile() {
    local new_profile="$1"
    [[ "$_ITERM_CURRENT_PROFILE" == "$new_profile" ]] && return
    _ITERM_CURRENT_PROFILE="$new_profile"
    printf '\033]1337;SetProfile=%s\007' "$new_profile"
}

_iterm_set_title() {
    local new_title="$1"
    [[ "$_ITERM_CURRENT_TITLE" == "$new_title" ]] && return
    _ITERM_CURRENT_TITLE="$new_title"
    printf '\033]2;%s\007' "$new_title"  # Window title (OSC 2)
}

_iterm_detect_context() {
    [[ "$TERM_PROGRAM" != "iTerm.app" ]] && return

    local profile="Default"
    local icon=""
    local name="${PWD:t}"  # Current directory name

    # Detect context and set profile + icon
    # Priority: Safety > AI > Language-specific > Document types > Tools
    if [[ $PWD == */production/* || $PWD == */prod/* ]]; then
        profile="Production"
        icon="🚨"
    elif [[ $PWD == */claude-sessions/* || $PWD == */gemini-sessions/* ]]; then
        profile="AI-Session"
        icon="🤖"
    elif [[ -f "DESCRIPTION" ]]; then
        profile="R-Dev"
        icon="📦"
        name=$(grep "^Package:" DESCRIPTION 2>/dev/null | cut -d' ' -f2 || echo "$name")
    elif [[ -f "pyproject.toml" ]]; then
        profile="Python-Dev"
        icon="🐍"
    elif [[ -f "package.json" ]]; then
        profile="Node-Dev"
        icon="📦"
        name=$(grep '"name"' package.json 2>/dev/null | head -1 | cut -d'"' -f4 || echo "$name")
    elif [[ -f "_quarto.yml" ]]; then
        icon="📊"
        # Get project title from _quarto.yml
        name=$(grep "^title:" _quarto.yml 2>/dev/null | head -1 | cut -d'"' -f2 || echo "$name")
    elif [[ -f "Cask" ]] || [[ -f ".dir-locals.el" ]] || [[ -f "init.el" ]] || [[ -f "early-init.el" ]]; then
        icon="⚡"
    elif [[ -d "commands" ]] || [[ -d "bin" && -f "Makefile" ]]; then
        icon="🔧"
    fi

    _iterm_switch_profile "$profile"

    # Set title: icon + name (or just directory if no special context)
    if [[ -n "$icon" ]]; then
        _iterm_set_title "$icon $name"
    else
        _iterm_set_title "$name"
    fi
}

# Register hook (only once)
if (( ! ${+_ITERM_HOOK_REGISTERED} )); then
    typeset -g _ITERM_HOOK_REGISTERED=1
    autoload -U add-zsh-hook
    add-zsh-hook chpwd _iterm_detect_context
fi

# Set initial profile for current directory
_iterm_detect_context
