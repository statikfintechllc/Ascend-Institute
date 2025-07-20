#!/bin/bash

# GremlinGPT VS Code Extension and MCP Server Build & Install Script
# © 2025 StatikFintechLLC / AscendAI Project

set -e

echo "🧬 GremlinGPT VS Code Extension & MCP Server Builder"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREMLIN_ROOT="$SCRIPT_DIR"
EXTENSION_DIR="$GREMLIN_ROOT/vscode-extension"
MCP_DIR="$GREMLIN_ROOT/mcp-server"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js 18 or later."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        log_error "npm is not installed. Please install npm."
        exit 1
    fi
    
    # Check VS Code CLI
    if ! command -v code &> /dev/null; then
        log_warning "VS Code CLI not found. Extension installation may require manual steps."
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. GremlinGPT requires Python 3.8 or later."
        exit 1
    fi
    
    log_success "Dependencies check completed"
}

build_vscode_extension() {
    log_info "Building VS Code Extension..."
    
    cd "$EXTENSION_DIR"
    
    # Install dependencies
    log_info "Installing extension dependencies..."
    npm install
    
    # Install VS Code extension CLI
    if ! npm list -g @vscode/vsce &> /dev/null; then
        log_info "Installing @vscode/vsce globally..."
        npm install -g @vscode/vsce
    fi
    
    # Compile TypeScript
    log_info "Compiling TypeScript..."
    npm run compile
    
    # Package extension
    log_info "Packaging extension..."
    vsce package --out gremlingpt-extension.vsix
    
    log_success "VS Code extension built successfully: $EXTENSION_DIR/gremlingpt-extension.vsix"
}

build_mcp_server() {
    log_info "Building MCP Server..."
    
    cd "$MCP_DIR"
    
    # Install dependencies
    log_info "Installing MCP server dependencies..."
    npm install
    
    # Build TypeScript
    log_info "Building TypeScript..."
    npm run build
    
    # Make executable
    chmod +x dist/index.js
    
    # Create global symlink
    log_info "Creating global symlink..."
    npm link
    
    log_success "MCP server built successfully"
}

install_vscode_extension() {
    log_info "Installing VS Code Extension..."
    
    if command -v code &> /dev/null; then
        cd "$EXTENSION_DIR"
        code --install-extension gremlingpt-extension.vsix --force
        log_success "VS Code extension installed successfully"
    else
        log_warning "VS Code CLI not available. Please install manually:"
        log_warning "1. Open VS Code"
        log_warning "2. Go to Extensions (Ctrl+Shift+X)"
        log_warning "3. Click '...' menu and select 'Install from VSIX'"
        log_warning "4. Select: $EXTENSION_DIR/gremlingpt-extension.vsix"
    fi
}

setup_mcp_config() {
    log_info "Setting up MCP configuration..."
    
    # Create MCP config directory
    MCP_CONFIG_DIR="$HOME/.config/mcp"
    mkdir -p "$MCP_CONFIG_DIR"
    
    # Create or update MCP config
    MCP_CONFIG_FILE="$MCP_CONFIG_DIR/servers.json"
    
    if [ ! -f "$MCP_CONFIG_FILE" ]; then
        log_info "Creating new MCP servers configuration..."
        cat > "$MCP_CONFIG_FILE" << EOF
{
  "servers": {
    "gremlingpt": {
      "command": "gremlingpt-mcp",
      "env": {
        "GREMLIN_BASE_URL": "http://localhost:7777",
        "GREMLIN_WS_URL": "ws://localhost:7777/ws"
      }
    }
  }
}
EOF
    else
        log_info "Updating existing MCP servers configuration..."
        # Use jq to update if available, otherwise manual edit
        if command -v jq &> /dev/null; then
            jq '.servers.gremlingpt = {
                "command": "gremlingpt-mcp",
                "env": {
                    "GREMLIN_BASE_URL": "http://localhost:7777",
                    "GREMLIN_WS_URL": "ws://localhost:7777/ws"
                }
            }' "$MCP_CONFIG_FILE" > "$MCP_CONFIG_FILE.tmp" && mv "$MCP_CONFIG_FILE.tmp" "$MCP_CONFIG_FILE"
        else
            log_warning "jq not available. Please manually add GremlinGPT to your MCP config:"
            log_warning "File: $MCP_CONFIG_FILE"
        fi
    fi
    
    log_success "MCP configuration updated"
}

install_playwright_tools() {
    log_info "Installing Playwright for system automation..."
    
    cd "$GREMLIN_ROOT"
    
    # Install Playwright Python package if not already installed
    if ! python3 -c "import playwright" 2>/dev/null; then
        pip3 install playwright
        log_success "Playwright Python package installed"
    else
        log_info "Playwright Python package already installed"
    fi
    
    # Install browsers
    python3 -m playwright install
    
    log_success "Playwright browsers installed successfully"
}

run_tests() {
    log_info "Running installation tests..."
    
    # Test VS Code extension compilation
    cd "$EXTENSION_DIR"
    if npm run compile; then
        log_success "VS Code extension compiles successfully"
    else
        log_error "VS Code extension compilation failed"
        return 1
    fi
    
    # Test MCP server build
    cd "$MCP_DIR"
    if npm run build; then
        log_success "MCP server builds successfully"
    else
        log_error "MCP server build failed"
        return 1
    fi
    
    # Test GremlinGPT Python modules
    cd "$GREMLIN_ROOT"
    if python3 -c "import sys; sys.path.insert(0, '.'); from memory.vector_store.embedder import embed_text; print('Memory module OK')"; then
        log_success "GremlinGPT Python modules OK"
    else
        log_error "GremlinGPT Python modules have issues"
        return 1
    fi
    
    log_success "All tests passed"
}

main() {
    echo ""
    log_info "Starting GremlinGPT VS Code Extension & MCP Server build..."
    echo ""
    
    check_dependencies
    echo ""
    
    # Build components
    build_vscode_extension
    echo ""
    
    build_mcp_server
    echo ""
    
    # Install components
    install_vscode_extension
    echo ""
    
    setup_mcp_config
    echo ""
    
    install_playwright_tools
    echo ""
    
    # Run tests
    run_tests
    echo ""
    
    log_success "🎉 GremlinGPT VS Code Extension & MCP Server build completed successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Start GremlinGPT backend: cd $GREMLIN_ROOT && python3 run/unified_startup.py"
    echo "  2. Open VS Code and run: GremlinGPT: Open Dashboard"
    echo "  3. Access web dashboard: http://localhost:7777"
    echo "  4. Test MCP server: gremlingpt-mcp"
    echo ""
    log_info "For support, visit: https://github.com/statikfintechllc/AscendAI"
}

# Handle script arguments
case "$1" in
    --vscode-only)
        check_dependencies
        build_vscode_extension
        install_vscode_extension
        ;;
    --mcp-only)
        check_dependencies
        build_mcp_server
        setup_mcp_config
        ;;
    --test-only)
        run_tests
        ;;
    *)
        main
        ;;
esac
