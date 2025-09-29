#!/bin/bash

# Build All Components Script
# Builds all components for all domains and platforms

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_SCRIPT="$SCRIPT_DIR/build.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Component configurations
declare -A COMPONENTS=(
    ["navbar"]="both"
    ["footer"]="both"
    ["card"]="both"
    ["svg-card"]="both"
    ["ticker"]="mobile"
)

# Parse command line arguments
DOMAIN="all"
VALIDATE=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --validate)
            VALIDATE=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            cat << EOF
Build All Components Script

Usage: $0 [options]

Options:
  --domain <type>      Target domain: dev, server, www, or all (default: all)
  --validate          Validate generated components
  --verbose           Enable verbose output
  --help              Show this help message

This script builds all available components for the specified domain(s).
Components are built for their appropriate platforms automatically:
  - navbar, footer, card, svg-card: both mobile and desktop
  - ticker: mobile only

EOF
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate domain
if [[ ! "$DOMAIN" =~ ^(dev|server|www|all)$ ]]; then
    log_error "Invalid domain: $DOMAIN. Must be dev, server, www, or all"
    exit 1
fi

log_info "Building all components for domain: $DOMAIN"
log_info "Validation: $VALIDATE"
log_info "Verbose: $VERBOSE"

# Build counters
TOTAL_BUILDS=0
SUCCESSFUL_BUILDS=0
FAILED_BUILDS=0

# Build each component
for component in "${!COMPONENTS[@]}"; do
    platform="${COMPONENTS[$component]}"
    
    log_info "Building $component (platform: $platform)..."
    
    # Construct build command
    BUILD_CMD="$BUILD_SCRIPT --component $component --platform $platform --domain $DOMAIN"
    
    if [[ "$VALIDATE" == true ]]; then
        BUILD_CMD="$BUILD_CMD --validate"
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        BUILD_CMD="$BUILD_CMD --verbose"
    fi
    
    # Execute build
    if eval "$BUILD_CMD"; then
        log_success "✓ $component built successfully"
        ((SUCCESSFUL_BUILDS++))
    else
        log_error "✗ Failed to build $component"
        ((FAILED_BUILDS++))
    fi
    
    ((TOTAL_BUILDS++))
    echo ""
done

# Summary
log_info "Build Summary:"
log_info "Total builds: $TOTAL_BUILDS"
log_success "Successful: $SUCCESSFUL_BUILDS"

if [[ $FAILED_BUILDS -gt 0 ]]; then
    log_error "Failed: $FAILED_BUILDS"
    exit 1
else
    log_success "All components built successfully!"
fi

# Update manifest with build timestamp
MANIFEST_FILE="$SCRIPT_DIR/component-manifest.json"
if [[ -f "$MANIFEST_FILE" ]]; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    # Simple manifest update (in a real implementation, you might use jq or a proper JSON parser)
    echo "Build completed at $TIMESTAMP for domain: $DOMAIN" >> "${MANIFEST_FILE}.log"
    log_info "Build logged to manifest"
fi

log_success "Build-all completed successfully!"