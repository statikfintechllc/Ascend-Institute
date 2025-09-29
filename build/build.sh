#!/bin/bash

# Multi-Domain Component Build System
# Generates platform-optimized components for dev, server, and www domains

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPONENTS_CONFIG="$SCRIPT_DIR/components.json"
TAILWIND_CONFIG="$SCRIPT_DIR/tailwind.config.js"
MANIFEST_FILE="$SCRIPT_DIR/component-manifest.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Usage function
usage() {
    cat << EOF
Multi-Domain Component Build System

Usage: $0 --component <name> --platform <mobile|desktop|both> --domain <dev|server|www|all> [options]

Required Arguments:
  --component <name>    Component name (e.g., navbar, footer, card)
  --platform <type>     Target platform: mobile, desktop, or both
  --domain <type>       Target domain: dev, server, www, or all

Options:
  --watch              Enable watch mode for automatic rebuilds
  --validate           Validate generated components
  --verbose            Enable verbose output
  --help               Show this help message

Examples:
  $0 --component navbar --platform both --domain all
  $0 --component footer --platform mobile --domain dev
  $0 --component card --platform desktop --domain www --validate
EOF
}

# Parse command line arguments
parse_args() {
    COMPONENT=""
    PLATFORM=""
    DOMAIN=""
    WATCH_MODE=false
    VALIDATE=false
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --component)
                COMPONENT="$2"
                shift 2
                ;;
            --platform)
                PLATFORM="$2"
                shift 2
                ;;
            --domain)
                DOMAIN="$2"
                shift 2
                ;;
            --watch)
                WATCH_MODE=true
                shift
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
                usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$COMPONENT" || -z "$PLATFORM" || -z "$DOMAIN" ]]; then
        log_error "Missing required arguments"
        usage
        exit 1
    fi

    # Validate platform
    if [[ ! "$PLATFORM" =~ ^(mobile|desktop|both)$ ]]; then
        log_error "Invalid platform: $PLATFORM. Must be mobile, desktop, or both"
        exit 1
    fi

    # Validate domain
    if [[ ! "$DOMAIN" =~ ^(dev|server|www|all)$ ]]; then
        log_error "Invalid domain: $DOMAIN. Must be dev, server, www, or all"
        exit 1
    fi
}

# Check if component exists in global templates
validate_component_exists() {
    local component=$1
    local platform=$2
    
    if [[ "$platform" == "both" ]]; then
        local platforms=("mobile" "desktop")
    else
        local platforms=("$platform")
    fi
    
    for p in "${platforms[@]}"; do
        local component_file="$PROJECT_ROOT/components/global.c/$p/$component.js"
        if [[ ! -f "$component_file" ]]; then
            log_error "Component $component.js not found in components/global.c/$p/"
            return 1
        fi
    done
    
    log_info "Component $component validated for platform(s): ${platforms[*]}"
}

# Load component configuration
load_component_config() {
    local component=$1
    
    if [[ ! -f "$COMPONENTS_CONFIG" ]]; then
        log_error "Components configuration file not found: $COMPONENTS_CONFIG"
        exit 1
    fi
    
    # Check if component exists in config (using basic grep since we may not have jq)
    if ! grep -q "\"$component\"" "$COMPONENTS_CONFIG" 2>/dev/null; then
        log_warning "Component $component not found in configuration, using defaults"
    fi
}

# Get platform configuration
get_platform_config() {
    local platform=$1
    
    if [[ "$platform" == "mobile" ]]; then
        # Mobile-specific settings
        MOBILE_DEPS=("ticker.js")
        BREAKPOINT="@media (max-width: 768px)"
        TOUCH_TARGETS=true
    elif [[ "$platform" == "desktop" ]]; then
        # Desktop-specific settings
        MOBILE_DEPS=()
        BREAKPOINT="@media (min-width: 769px)"
        TOUCH_TARGETS=false
    fi
}

# Apply domain-specific styles
apply_domain_styles() {
    local component=$1
    local domain=$2
    local platform=$3
    local source_file=$4
    local output_content
    
    log_info "Applying $domain domain styles to $component ($platform)"
    
    # Read the source component
    output_content=$(<"$source_file")
    
    # Load domain-specific styles
    local domain_styles_dir="$PROJECT_ROOT/$domain/$domain.styles"
    local domain_css="$domain_styles_dir/$domain-styles.css"
    local domain_tailwind="$domain_styles_dir/$domain.tailwind.css"
    
    # Add build header comment
    local build_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local header_comment="/**
 * Generated by Multi-Domain Component Build System
 * Component: $component
 * Platform: $platform
 * Domain: $domain
 * Build Time: $build_timestamp
 * Source: components/global.c/$platform/$component.js
 */

"
    
    # Combine header with content
    output_content="$header_comment$output_content"
    
    # Apply domain-specific path replacements
    case $domain in
        "dev")
            output_content=$(echo "$output_content" | sed 's|href="/|href="/dev/|g' | sed 's|src="/|src="/dev/|g')
            ;;
        "server")
            output_content=$(echo "$output_content" | sed 's|href="/|href="/server/|g' | sed 's|src="/|src="/server/|g')
            ;;
        "www")
            output_content=$(echo "$output_content" | sed 's|href="/|href="/www/|g' | sed 's|src="/|src="/www/|g')
            ;;
    esac
    
    echo "$output_content"
}

# Process component for a specific domain and platform
process_component() {
    local component=$1
    local domain=$2
    local platform=$3
    
    log_info "Processing $component for $domain domain ($platform platform)"
    
    local source_file="$PROJECT_ROOT/components/global.c/$platform/$component.js"
    local domain_output="$PROJECT_ROOT/$domain/components/$domain.c/${platform}.c/$component.js"
    local centralized_output="$PROJECT_ROOT/components/$domain.c/$platform/$component.js"
    
    # Create output directories
    mkdir -p "$(dirname "$domain_output")"
    mkdir -p "$(dirname "$centralized_output")"
    
    # Get platform configuration
    get_platform_config "$platform"
    
    # Apply domain-specific styling
    local processed_content
    processed_content=$(apply_domain_styles "$component" "$domain" "$platform" "$source_file")
    
    # Write to both output locations
    echo "$processed_content" > "$domain_output"
    echo "$processed_content" > "$centralized_output"
    
    log_success "Generated: $domain_output"
    log_success "Generated: $centralized_output"
    
    # Update manifest
    update_manifest "$component" "$domain" "$platform"
}

# Update component manifest
update_manifest() {
    local component=$1
    local domain=$2
    local platform=$3
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Create manifest file if it doesn't exist
    if [[ ! -f "$MANIFEST_FILE" ]]; then
        echo '{"builds": {}, "last_updated": ""}' > "$MANIFEST_FILE"
    fi
    
    # For now, just append to a simple log (could be enhanced with proper JSON handling)
    local manifest_entry="$timestamp: $component ($platform) -> $domain"
    echo "$manifest_entry" >> "${MANIFEST_FILE}.log"
}

# Validate generated components
validate_components() {
    local component=$1
    local domain=$2
    local platform=$3
    
    log_info "Validating generated components..."
    
    local domain_output="$PROJECT_ROOT/$domain/components/$domain.c/${platform}.c/$component.js"
    local centralized_output="$PROJECT_ROOT/components/$domain.c/$platform/$component.js"
    
    # Check if files exist and are not empty
    if [[ -f "$domain_output" && -s "$domain_output" ]]; then
        log_success "Domain output validated: $domain_output"
    else
        log_error "Domain output validation failed: $domain_output"
        return 1
    fi
    
    if [[ -f "$centralized_output" && -s "$centralized_output" ]]; then
        log_success "Centralized output validated: $centralized_output"
    else
        log_error "Centralized output validation failed: $centralized_output"
        return 1
    fi
    
    # Basic syntax check (if node is available)
    if command -v node >/dev/null 2>&1; then
        if node -c "$domain_output" 2>/dev/null; then
            log_success "JavaScript syntax validated for $domain_output"
        else
            log_warning "JavaScript syntax check failed for $domain_output"
        fi
    fi
}

# Main build function
build_component() {
    local component=$1
    local platform=$2
    local domain=$3
    
    log_info "Building $component (platform: $platform, domain: $domain)"
    
    # Validate component exists
    validate_component_exists "$component" "$platform"
    
    # Load component configuration
    load_component_config "$component"
    
    # Determine platforms to process
    if [[ "$platform" == "both" ]]; then
        local platforms=("mobile" "desktop")
    else
        local platforms=("$platform")
    fi
    
    # Determine domains to process
    if [[ "$domain" == "all" ]]; then
        local domains=("dev" "server" "www")
    else
        local domains=("$domain")
    fi
    
    # Process each combination
    for p in "${platforms[@]}"; do
        for d in "${domains[@]}"; do
            process_component "$component" "$d" "$p"
            
            if [[ "$VALIDATE" == true ]]; then
                validate_components "$component" "$d" "$p"
            fi
        done
    done
    
    log_success "Build completed for $component"
}

# Watch mode implementation
watch_mode() {
    log_info "Starting watch mode..."
    log_info "Monitoring changes in components/global.c/ and domain styles"
    log_info "Press Ctrl+C to stop"
    
    # Simple watch implementation using filesystem events
    if command -v inotifywait >/dev/null 2>&1; then
        while true; do
            inotifywait -r -e modify,create,delete \
                "$PROJECT_ROOT/components/global.c/" \
                "$PROJECT_ROOT/dev/" \
                "$PROJECT_ROOT/server/" \
                "$PROJECT_ROOT/www/" 2>/dev/null || true
            
            log_info "Changes detected, rebuilding..."
            build_component "$COMPONENT" "$PLATFORM" "$DOMAIN"
            sleep 1
        done
    else
        log_warning "inotifywait not available, using basic polling"
        while true; do
            sleep 5
            log_info "Periodic rebuild check..."
            build_component "$COMPONENT" "$PLATFORM" "$DOMAIN"
        done
    fi
}

# Main function
main() {
    log_info "Multi-Domain Component Build System"
    log_info "Project root: $PROJECT_ROOT"
    
    parse_args "$@"
    
    if [[ "$VERBOSE" == true ]]; then
        log_info "Component: $COMPONENT"
        log_info "Platform: $PLATFORM"
        log_info "Domain: $DOMAIN"
        log_info "Watch mode: $WATCH_MODE"
        log_info "Validate: $VALIDATE"
    fi
    
    # Build the component
    build_component "$COMPONENT" "$PLATFORM" "$DOMAIN"
    
    # Start watch mode if requested
    if [[ "$WATCH_MODE" == true ]]; then
        watch_mode
    fi
}

# Run main function with all arguments
main "$@"