#!/usr/bin/env zsh

# Test suite for iTerm2 context switcher
# Tests the chpwd_iterm_profile function from zsh/iterm2-integration.zsh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass() {
    echo "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
    ((TESTS_RUN++))
}

fail() {
    echo "${RED}✗${NC} $1"
    echo "  Expected: $2"
    echo "  Got: $3"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

info() {
    echo "${YELLOW}ℹ${NC} $1"
}

# Override it2profile and printf BEFORE sourcing the integration file
# This way they'll be used by the integration script

# Mock it2profile to capture what profile would be set
it2profile() {
    echo "PROFILE_SET:$1"
}

# Track what would be set
_TEST_PROFILE=""
_TEST_BADGE=""

# Mock the actual iTerm2 escape sequence functions
_iterm_title() { :; }  # No-op
_iterm_badge() {
    _TEST_BADGE="$1"
}
_iterm_uservar() { :; }  # No-op

# Source the integration file
INTEGRATION_FILE="$(dirname "$0")/../zsh/iterm2-integration.zsh"

if [[ ! -f "$INTEGRATION_FILE" ]]; then
    echo "${RED}Error:${NC} Cannot find $INTEGRATION_FILE"
    exit 1
fi

info "Loading integration file: $INTEGRATION_FILE"

# Temporarily disable the actual execution
_ITERM_TEST_MODE=1

source "$INTEGRATION_FILE"

# Create temporary test directory
TEST_DIR=$(mktemp -d)
trap "rm -rf $TEST_DIR" EXIT

info "Test directory: $TEST_DIR"
echo ""

# ============================================================================
# TEST 1: R Package Detection
# ============================================================================
echo "Test 1: R package detection (DESCRIPTION file)"

# Setup test environment
mkdir -p "$TEST_DIR/test-r-package"
cat > "$TEST_DIR/test-r-package/DESCRIPTION" <<EOF
Package: testpkg
Title: Test Package
Version: 0.1.0
EOF

# Change to test directory
cd "$TEST_DIR/test-r-package"

# Clear the cache so the function will output again
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""

# Run the function and capture output (it will output iTerm2 escape sequences)
output=$(_iterm_detect_context 2>&1)

# Check if R-Dev profile sequence was output
if echo "$output" | grep -q "SetProfile=R-Dev"; then
    pass "R-Dev profile set for R package"
else
    fail "R-Dev profile not set for R package" "SetProfile=R-Dev" "$output"
fi

# Check if badge contains package name (it's in the title escape sequence)
if echo "$output" | grep -q "📦 testpkg"; then
    pass "Badge/title set to '📦 testpkg' for R package"
else
    fail "Badge/title not set correctly for R package" "📦 testpkg" "$output"
fi

# ============================================================================
# TEST 2: Default Fallback
# ============================================================================
echo ""
echo "Test 2: Default fallback (no special files)"

# Setup test environment
mkdir -p "$TEST_DIR/test-default"
cd "$TEST_DIR/test-default"

# Clear cache
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""

# Run the function and capture output
output=$(_iterm_detect_context 2>&1)

# Check if Default profile was set
if echo "$output" | grep -q "SetProfile=Default"; then
    pass "Default profile set for generic directory"
else
    fail "Default profile not set for generic directory" "SetProfile=Default" "$output"
fi

# For default, the title should be cleared (no special badge/icon)
# We can check that there's no package icon in the output
if echo "$output" | grep -qE "📦|🐍|🔴"; then
    fail "Badge should be cleared for default" "No special icons" "$output"
else
    pass "Badge cleared for default directory (no special icons)"
fi

# ============================================================================
# TEST 3: Python Project Detection
# ============================================================================
echo ""
echo "Test 3: Python project detection (pyproject.toml)"

# Setup test environment
mkdir -p "$TEST_DIR/test-python"
cat > "$TEST_DIR/test-python/pyproject.toml" <<EOF
[project]
name = "mypyapp"
version = "1.0.0"
EOF

# Change to test directory and capture output
cd "$TEST_DIR/test-python"
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""
output=$(_iterm_detect_context 2>&1)

# Check if Python-Dev profile sequence was output
if echo "$output" | grep -q "SetProfile=Python-Dev"; then
    pass "Python-Dev profile set for Python project"
else
    fail "Python-Dev profile not set for Python project" "SetProfile=Python-Dev" "$output"
fi

# Check if badge contains Python icon
if echo "$output" | grep -q "🐍"; then
    pass "Python icon (🐍) set for Python project"
else
    fail "Python icon not set for Python project" "🐍" "$output"
fi

# ============================================================================
# TEST 4: Node.js Project Detection
# ============================================================================
echo ""
echo "Test 4: Node.js project detection (package.json)"

# Setup test environment
mkdir -p "$TEST_DIR/test-node"
cat > "$TEST_DIR/test-node/package.json" <<EOF
{
  "name": "my-node-app",
  "version": "1.0.0"
}
EOF

# Change to test directory and capture output
cd "$TEST_DIR/test-node"
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""
output=$(_iterm_detect_context 2>&1)

# Check if Node-Dev profile sequence was output
if echo "$output" | grep -q "SetProfile=Node-Dev"; then
    pass "Node-Dev profile set for Node.js project"
else
    fail "Node-Dev profile not set for Node.js project" "SetProfile=Node-Dev" "$output"
fi

# Check if badge contains package icon
if echo "$output" | grep -q "📦"; then
    pass "Package icon (📦) set for Node.js project"
else
    fail "Package icon not set for Node.js project" "📦" "$output"
fi

# ============================================================================
# TEST 5: MCP Server Detection
# ============================================================================
echo ""
echo "Test 5: MCP server detection (mcp-server/ directory)"

# Setup test environment
mkdir -p "$TEST_DIR/test-mcp/mcp-server"
cat > "$TEST_DIR/test-mcp/package.json" <<EOF
{
  "name": "my-mcp-server",
  "version": "1.0.0"
}
EOF

# Change to test directory and capture output
cd "$TEST_DIR/test-mcp"
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""
output=$(_iterm_detect_context 2>&1)

# Check if Node-Dev profile sequence was output (MCP uses Node-Dev)
if echo "$output" | grep -q "SetProfile=Node-Dev"; then
    pass "Node-Dev profile set for MCP project"
else
    fail "Node-Dev profile not set for MCP project" "SetProfile=Node-Dev" "$output"
fi

# Check if badge contains MCP icon
if echo "$output" | grep -q "🔌"; then
    pass "MCP icon (🔌) set for MCP project"
else
    fail "MCP icon not set for MCP project" "🔌" "$output"
fi

# ============================================================================
# TEST 6: Production Path Detection
# ============================================================================
echo ""
echo "Test 6: Production path detection (*/production/*)"

# Setup test environment
mkdir -p "$TEST_DIR/production/app"
cd "$TEST_DIR/production/app"
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""
output=$(_iterm_detect_context 2>&1)

# Check if Production profile sequence was output
if echo "$output" | grep -q "SetProfile=Production"; then
    pass "Production profile set for production path"
else
    fail "Production profile not set for production path" "SetProfile=Production" "$output"
fi

# Check if badge contains warning icon
if echo "$output" | grep -q "🔴"; then
    pass "Warning icon (🔴) set for production path"
else
    fail "Warning icon not set for production path" "🔴" "$output"
fi

# ============================================================================
# TEST 7: Git Dirty Indicator
# ============================================================================
echo ""
echo "Test 7: Git dirty indicator (uncommitted changes)"

# Setup test environment with git repo
mkdir -p "$TEST_DIR/test-git-dirty"
cd "$TEST_DIR/test-git-dirty"
git init -q
cat > DESCRIPTION <<EOF
Package: dirtypkg
Title: Dirty Package
Version: 0.1.0
EOF
git add DESCRIPTION
git commit -q -m "Initial commit"

# Make uncommitted change
echo "# Modified" >> DESCRIPTION

# Capture output
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""
output=$(_iterm_detect_context 2>&1)

# Check if dirty indicator appears in title
if echo "$output" | grep -q "✗"; then
    pass "Dirty indicator (✗) shown for uncommitted changes"
else
    fail "Dirty indicator not shown for uncommitted changes" "✗" "$output"
fi

# ============================================================================
# TEST 8: Quarto Project Detection
# ============================================================================
echo ""
echo "Test 8: Quarto project detection (_quarto.yml)"

# Setup test environment
mkdir -p "$TEST_DIR/test-quarto"
cat > "$TEST_DIR/test-quarto/_quarto.yml" <<EOF
project:
  type: default
  title: "My Quarto Project"
EOF

# Change to test directory and capture output
cd "$TEST_DIR/test-quarto"
_ITERM_CURRENT_PROFILE=""
_ITERM_CURRENT_TITLE=""
output=$(_iterm_detect_context 2>&1)

# Check if Default profile is used (Quarto doesn't have custom profile yet)
if echo "$output" | grep -q "SetProfile=Default"; then
    pass "Default profile set for Quarto project"
else
    fail "Default profile not set for Quarto project" "SetProfile=Default" "$output"
fi

# Check if badge contains Quarto icon
if echo "$output" | grep -q "📝"; then
    pass "Quarto icon (📝) set for Quarto project"
else
    fail "Quarto icon not set for Quarto project" "📝" "$output"
fi

# ============================================================================
# Test Summary
# ============================================================================
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Tests run:    $TESTS_RUN"
echo "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo "${RED}Some tests failed.${NC}"
    exit 1
fi
