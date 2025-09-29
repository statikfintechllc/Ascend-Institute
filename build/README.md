# Multi-Domain Component Build System

A sophisticated component build system that generates platform-optimized (mobile/desktop) components for three distinct domains (dev, server, www) from global templates, applying domain-specific styling while maintaining architectural consistency.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Build Scripts](#build-scripts)
- [Configuration](#configuration)
- [Components](#components)
- [Domain Styling](#domain-styling)
- [Platform Optimization](#platform-optimization)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)

## Overview

The build system transforms global component templates into domain-specific, platform-optimized components through an automated pipeline that:

1. **Sources** templates from `components/global.c/`
2. **Processes** with domain-specific styles from `<domain>/<domain>.styles/`
3. **Outputs** to both domain folders and centralized management locations

### Key Features

- 🎯 **Multi-Domain Support**: dev, server, www domains with unique styling
- 📱 **Platform Optimization**: Mobile (≤768px) and Desktop (>768px) variants
- 🎨 **Domain-Specific Styling**: CSS and Tailwind utilities per domain
- 🔧 **Automated Build Pipeline**: Command-line tools with validation
- 📊 **Component Manifest**: Track builds, dependencies, and status
- 🔄 **Watch Mode**: Auto-rebuild on file changes
- ✅ **Validation**: Syntax checking and output verification

## Architecture

### Directory Structure

```
build/
├── README.md                 # This documentation
├── build.sh                  # Main build script
├── build-all.sh             # Build all components
├── components.json          # Component configurations
├── tailwind.config.js       # Enhanced Tailwind config
└── component-manifest.json  # Build tracking and metadata

components/global.c/         # Global component templates
├── README.md
├── desktop/                 # Desktop platform components
│   ├── navbar.js
│   ├── footer.js
│   ├── card.js
│   ├── svg-card.js
│   └── navbar-example.html
└── mobile/                  # Mobile platform components
    ├── navbar.js
    ├── footer.js
    ├── card.js
    ├── svg-card.js
    ├── ticker.js            # Mobile-only component
    └── navbar-example.html

<domain>/                    # Domain-specific outputs and styles
├── components/
│   └── <domain>.c/
│       ├── desktop.c/       # Generated desktop components
│       └── mobile.c/        # Generated mobile components
└── <domain>.styles/
    ├── <domain>-styles.css  # Custom CSS styles
    └── <domain>.tailwind.css # Tailwind utilities

components/<domain>.c/       # Centralized component management
├── desktop/                 # Cross-domain desktop components
└── mobile/                  # Cross-domain mobile components
```

### Build Pipeline Flow

```
Global Template → Domain Styles → Platform Config → Output Generation
```

1. **Template Loading**: Read component from `components/global.c/<platform>/`
2. **Style Application**: Apply styles from `<domain>/<domain>.styles/`
3. **Path Resolution**: Update domain-specific paths and links
4. **Header Injection**: Add build metadata and timestamps
5. **Dual Output**: Write to both domain and centralized locations
6. **Validation**: Optional syntax and structure checking
7. **Manifest Update**: Log build status and metadata

## Quick Start

### 1. Build a Single Component

```bash
# Build navbar for all platforms and domains
./build/build.sh --component navbar --platform both --domain all

# Build mobile footer for dev domain only
./build/build.sh --component footer --platform mobile --domain dev

# Build with validation
./build/build.sh --component card --platform both --domain all --validate
```

### 2. Build All Components

```bash
# Build everything
./build/build-all.sh

# Build for specific domain with validation
./build/build-all.sh --domain dev --validate

# Verbose output
./build/build-all.sh --verbose
```

### 3. Watch Mode (Auto-rebuild)

```bash
# Watch for changes and auto-rebuild
./build/build.sh --component navbar --platform both --domain all --watch
```

## Build Scripts

### build.sh

Main build script with comprehensive options:

```bash
./build/build.sh --component <name> --platform <mobile|desktop|both> --domain <dev|server|www|all> [options]
```

**Required Arguments:**
- `--component <name>`: Component name (navbar, footer, card, svg-card, ticker)
- `--platform <type>`: Target platform (mobile, desktop, both)
- `--domain <type>`: Target domain (dev, server, www, all)

**Options:**
- `--watch`: Enable watch mode for automatic rebuilds
- `--validate`: Validate generated components
- `--verbose`: Enable verbose output
- `--help`: Show help message

**Examples:**
```bash
# Build navbar for all platforms and domains
./build/build.sh --component navbar --platform both --domain all

# Build mobile footer for dev domain with validation
./build/build.sh --component footer --platform mobile --domain dev --validate

# Watch mode for development
./build/build.sh --component card --platform both --domain dev --watch --verbose
```

### build-all.sh

Convenience script to build all components:

```bash
./build/build-all.sh [options]
```

**Options:**
- `--domain <type>`: Target domain (default: all)
- `--validate`: Validate all generated components
- `--verbose`: Enable verbose output
- `--help`: Show help message

## Configuration

### components.json

Component metadata and build settings:

```json
{
  "components": {
    "navbar": {
      "version": "1.0.0",
      "platforms": ["mobile", "desktop"],
      "dependencies": {
        "mobile": ["ticker.js"],
        "desktop": []
      },
      "shadcn": {
        "variant": "default",
        "size": "default"
      }
    }
  },
  "buildSettings": {
    "breakpoints": {
      "mobile": "768px",
      "desktop": "769px"
    },
    "touchTargets": {
      "minimum": "44px"
    }
  }
}
```

### tailwind.config.js

Enhanced Tailwind configuration with:

- **Domain-specific colors**: dev (blue), server (green), www (purple)
- **Platform breakpoints**: mobile (≤768px), desktop (>768px)
- **Touch-friendly utilities**: 44px minimum targets
- **Component base styles**: navbar, ticker, dropdown utilities
- **Animation keyframes**: ticker, fade-in, slide effects

## Components

### Available Components

| Component | Platforms | Description |
|-----------|-----------|-------------|
| **navbar** | Mobile, Desktop | Navigation bar with platform-specific behavior |
| **footer** | Mobile, Desktop | Footer with responsive grid layout |
| **card** | Mobile, Desktop | Content card with touch/hover optimizations |
| **svg-card** | Mobile, Desktop | SVG-enhanced card with icon support |
| **ticker** | Mobile only | Scrolling announcement ticker |

### Component Features

#### Mobile Components
- **Touch-friendly**: 44px minimum tap targets
- **Gesture support**: Touch start/end events
- **Optimized layouts**: Single-column, stacked designs
- **Performance**: Reduced animations, efficient rendering

#### Desktop Components
- **Hover effects**: Sophisticated interactions and transitions
- **Keyboard navigation**: Full accessibility support
- **Multi-column layouts**: Efficient use of screen space
- **Enhanced typography**: Refined spacing and sizing

### Component Dependencies

- **Mobile navbar** → requires `ticker.js`
- **Desktop navbar** → standalone (no ticker)
- All other components are standalone

## Domain Styling

### Domain Themes

| Domain | Theme | Primary Color | Description |
|--------|-------|---------------|-------------|
| **dev** | Blue | #3b82f6 | Development environment |
| **server** | Green | #22c55e | Server/backend focus |
| **www** | Purple | #a855f7 | Public web interface |

### Style Files per Domain

Each domain includes:

1. **Custom CSS** (`<domain>-styles.css`):
   - CSS custom properties
   - Component-specific styles
   - Responsive utilities
   - Animation definitions

2. **Tailwind Utilities** (`<domain>.tailwind.css`):
   - Domain-specific component classes
   - Color utilities
   - Responsive modifiers
   - Layer-organized styles

### Path Replacements

The build system automatically updates paths:

- `href="/"` → `href="/dev/"` (dev domain)
- `src="/assets/"` → `src="/server/assets/"` (server domain)
- `href="/api"` → `href="/www/api"` (www domain)

## Platform Optimization

### Breakpoint Strategy

- **Mobile**: `@media (max-width: 768px)`
- **Desktop**: `@media (min-width: 769px)`
- **Touch targets**: Minimum 44x44px on mobile
- **Hover effects**: Desktop only

### Mobile Optimizations

- Simplified layouts and interactions
- Touch gesture support
- Reduced animation complexity
- Optimized font sizes and spacing
- Battery-efficient rendering

### Desktop Optimizations

- Advanced hover and focus states
- Keyboard navigation support
- Multi-column layouts
- Enhanced typography
- Sophisticated animations

## API Reference

### Build Script Functions

#### validate_component_exists()
Checks if component exists in global templates.

#### apply_domain_styles()
Applies domain-specific styling and path replacements.

#### process_component()
Main processing function for component generation.

#### update_manifest()
Updates build manifest with timestamps and status.

### Component Classes

#### MobileNavbar
Mobile navigation with hamburger menu and ticker.

**Options:**
- `logoText`: Navigation logo text
- `showTicker`: Enable/disable ticker
- `tickerText`: Ticker message content

**Methods:**
- `toggleMenu()`: Toggle navigation menu
- `updateTickerText(text)`: Update ticker content
- `destroy()`: Remove component

#### DesktopNavbar
Desktop navigation with horizontal layout.

**Options:**
- `logoText`: Navigation logo text
- `showSearch`: Enable/disable search
- `searchPlaceholder`: Search input placeholder

**Methods:**
- `performSearch(query)`: Handle search submission
- `setActiveNavLink()`: Update active navigation state
- `addDropdownToNavItem()`: Add dropdown menu

### Component Events

Components dispatch custom events:

```javascript
// Card click events
document.addEventListener('cardClick', (e) => {
  console.log('Card clicked:', e.detail);
});

// Newsletter subscription
document.addEventListener('newsletterSubscribe', (e) => {
  console.log('Newsletter signup:', e.detail.email);
});
```

## Troubleshooting

### Common Issues

#### Build Fails: "Component not found"
```bash
[ERROR] Component navbar.js not found in components/global.c/mobile/
```
**Solution**: Ensure component exists in the correct platform directory.

#### Invalid Platform Error
```bash
[ERROR] Invalid platform: desktop. Must be mobile, desktop, or both
```
**Solution**: Check spelling and use exact platform names.

#### Path Resolution Issues
**Problem**: Generated components have incorrect paths.
**Solution**: Check domain-specific path replacement logic in `apply_domain_styles()`.

#### Validation Failures
**Problem**: Components fail syntax validation.
**Solution**: Check generated JavaScript syntax, ensure proper template structure.

### Debug Mode

Enable verbose logging:
```bash
./build/build.sh --component navbar --platform both --domain all --verbose
```

### Manual Validation

Check generated components:
```bash
# Validate JavaScript syntax
node -c /path/to/generated/component.js

# Check file existence
ls -la dev/components/dev.c/mobile.c/
```

### Manifest Inspection

Check build history:
```bash
cat build/component-manifest.json.log
```

## Advanced Usage

### Custom Component Development

1. Create component template in `components/global.c/<platform>/`
2. Add component entry to `build/components.json`
3. Update manifest with component metadata
4. Build and test across all domains

### Extending Domain Styles

1. Add styles to `<domain>/<domain>.styles/<domain>-styles.css`
2. Update Tailwind utilities in `<domain>/<domain>.styles/<domain>.tailwind.css`
3. Rebuild components to apply new styles

### Continuous Integration

```bash
# CI/CD pipeline example
./build/build-all.sh --validate
if [ $? -eq 0 ]; then
  echo "All components built successfully"
else
  echo "Build failed - check logs"
  exit 1
fi
```

## Contributing

When adding new components or features:

1. Follow existing naming conventions
2. Add comprehensive documentation
3. Include example HTML files
4. Test across all domains and platforms
5. Update this README with new features

## Support

For issues, questions, or contributions, please refer to the main project documentation or create an issue in the repository.