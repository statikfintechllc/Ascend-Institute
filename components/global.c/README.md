# Global Component Templates

This directory contains the global component templates that are used to generate platform-optimized components for all domains (dev, server, www).

## Structure

```
components/global.c/
├── README.md
├── desktop/           # Desktop platform components (>768px)
│   ├── card.js
│   ├── footer.js
│   ├── navbar.js
│   ├── navbar-example.html
│   └── svg-card.js
└── mobile/            # Mobile platform components (≤768px)
    ├── card.js
    ├── footer.js
    ├── navbar.js
    ├── navbar-example.html
    ├── svg-card.js
    └── ticker.js      # Mobile-only component
```

## Platform Definitions

- **Desktop**: Any screen wider than 768px (iPad Mini width and above)
- **Mobile**: Screens 768px and below
- Breakpoint implementation uses `@media (min-width: 769px)` for desktop styles

## Component Features

### Mobile Components
- **navbar.js**: Includes hamburger menu with dropdown navigation and integrated ticker
- **ticker.js**: Mobile-only scrolling ticker component
- **footer.js**: Single-column responsive layout with touch-friendly targets
- **card.js**: Touch-optimized card component
- **svg-card.js**: SVG-based card with mobile optimizations

### Desktop Components
- **navbar.js**: Horizontal navigation with no hamburger menu or ticker
- **footer.js**: Multi-column layout with detailed information
- **card.js**: Desktop-optimized card component with hover states
- **svg-card.js**: SVG-based card with desktop interactions

## Build Process

Components in this directory are processed by the build system to generate domain-specific versions with:

1. Domain-specific styling applied
2. Platform-appropriate behavior
3. Path replacements for domain routing
4. Tailwind utility classes injected
5. Build metadata headers

## Usage

Use the build script to generate components:

```bash
# Build navbar for all platforms and domains
./build/build.sh --component navbar --platform both --domain all

# Build mobile footer for dev domain only
./build/build.sh --component footer --platform mobile --domain dev

# Build with validation
./build/build.sh --component card --platform both --domain all --validate
```

## Development Guidelines

- Keep components platform-agnostic in terms of business logic
- Use CSS classes that can be customized by domain styles
- Follow touch-friendly guidelines for mobile components (44px minimum targets)
- Ensure desktop components have appropriate hover states
- Test components at their target breakpoints
- Document any component-specific dependencies or requirements