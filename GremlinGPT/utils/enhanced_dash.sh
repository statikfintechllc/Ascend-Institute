#!/bin/bash

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Enhanced Dashboard CLI Launcher

# Script detection and path setup
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${CYAN}${BOLD}🧠 GremlinGPT Enhanced Dashboard CLI${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo

# Check if enhanced dashboard exists
ENHANCED_CLI="$PROJECT_ROOT/utils/enhanced_dash_cli.py"

if [ ! -f "$ENHANCED_CLI" ]; then
    echo -e "${RED}❌ Enhanced dashboard CLI not found at: $ENHANCED_CLI${NC}"
    echo "Please ensure the file exists and try again."
    exit 1
fi

# Make sure it's executable
chmod +x "$ENHANCED_CLI"

# Check Python availability
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.6+ and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found: $($PYTHON_CMD --version)${NC}"
echo -e "${GREEN}✅ Enhanced CLI found: $ENHANCED_CLI${NC}"
echo

# Check required Python packages
echo -e "${YELLOW}🔍 Checking required packages...${NC}"

REQUIRED_PACKAGES=("toml")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! $PYTHON_CMD -c "import $package" &> /dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️ Missing packages: ${MISSING_PACKAGES[*]}${NC}"
    echo -e "${BLUE}Installing missing packages...${NC}"
    
    for package in "${MISSING_PACKAGES[@]}"; do
        echo "Installing $package..."
        $PYTHON_CMD -m pip install "$package" || {
            echo -e "${RED}❌ Failed to install $package${NC}"
            echo "Please install manually: pip install $package"
            exit 1
        }
    done
    echo -e "${GREEN}✅ All packages installed${NC}"
else
    echo -e "${GREEN}✅ All required packages found${NC}"
fi

echo

# Set environment variables
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
export GREMLIN_PROJECT_ROOT="$PROJECT_ROOT"

# Launch enhanced dashboard
echo -e "${CYAN}🚀 Launching Enhanced Dashboard CLI...${NC}"
echo -e "${BLUE}Project Root: $PROJECT_ROOT${NC}"
echo -e "${BLUE}Python: $PYTHON_CMD${NC}"
echo

cd "$PROJECT_ROOT" || exit 1

# Launch with error handling
if $PYTHON_CMD "$ENHANCED_CLI"; then
    echo -e "\n${GREEN}✅ Dashboard CLI exited normally${NC}"
else
    echo -e "\n${RED}❌ Dashboard CLI exited with error${NC}"
    echo -e "${YELLOW}Check the logs for more information${NC}"
fi

echo -e "${CYAN}👋 Thank you for using GremlinGPT Enhanced Dashboard!${NC}"
