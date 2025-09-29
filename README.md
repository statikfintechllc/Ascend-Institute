# Ascend Institute - Multi-Domain Component Build System

A sophisticated component build system that generates platform-optimized (mobile/desktop) components for three distinct domains (dev, server, www) from global templates. The system applies domain-specific styling while maintaining architectural consistency throughout all domains.

## 🚀 Quick Start

```bash
# Build navbar for all platforms and domains
./build/build.sh --component navbar --platform both --domain all

# Build all components
./build/build-all.sh

# Build with validation
./build/build.sh --component footer --platform both --domain dev --validate

# Watch mode for development
./build/build.sh --component card --platform both --domain all --watch
```

## 📁 Project Structure

```
Ascend-Institute/
├── build/                           # Build system core
│   ├── build.sh                     # Main build script
│   ├── build-all.sh                 # Build all components
│   ├── components.json              # Component configurations
│   ├── tailwind.config.js           # Enhanced Tailwind config
│   ├── component-manifest.json      # Build tracking
│   └── README.md                    # Build system documentation
│
├── components/                      # Component management
│   ├── global.c/                    # Global templates
│   │   ├── README.md
│   │   ├── desktop/                 # Desktop components (>768px)
│   │   │   ├── navbar.js
│   │   │   ├── footer.js
│   │   │   ├── card.js
│   │   │   ├── svg-card.js
│   │   │   └── navbar-example.html
│   │   └── mobile/                  # Mobile components (≤768px)
│   │       ├── navbar.js            # With hamburger menu
│   │       ├── footer.js            # Touch-optimized 
│   │       ├── card.js
│   │       ├── svg-card.js
│   │       ├── ticker.js            # Mobile-only
│   │       └── navbar-example.html
│   │
│   ├── dev.c/                       # Dev domain components
│   ├── server.c/                    # Server domain components
│   └── www.c/                       # WWW domain components
│
├── dev/                             # Development domain
│   ├── components/dev.c/            # Generated components
│   │   ├── desktop.c/
│   │   └── mobile.c/
│   └── dev.styles/                  # Domain styles
│       ├── dev-styles.css           # Blue theme
│       └── dev.tailwind.css
│
├── server/                          # Server domain
│   ├── components/server.c/         # Generated components
│   │   ├── desktop.c/
│   │   └── mobile.c/
│   └── server.styles/               # Domain styles
│       ├── server-styles.css        # Green theme
│       └── server.tailwind.css
│
├── www/                             # Web domain
│   ├── components/www.c/            # Generated components
│   │   ├── desktop.c/
│   │   └── mobile.c/
│   └── www.styles/                  # Domain styles
│       ├── www-styles.css           # Purple theme
│       └── www.tailwind.css
│
├── docs/                            # Documentation
│   ├── index.html
│   ├── scrollFX.js
│   └── build_dashboard_html.py
│
├── builder.script/                  # Legacy build scripts
│   └── BAi.script.mjs
│
├── About Us/                        # Project documentation
│   ├── Final_Leg_v1.0.3.md
│   ├── GREMLINGPT-v1.0.3_PATCH_PLAN.md
│   ├── GREMLINGPT_AUTONOMY_REPORT.md
│   ├── CODE_OF_CONDUCT.md
│   └── CONTRIBUTING.md
│
├── .github/                         # GitHub configuration
├── LICENSE.md
└── README.md                        # This file
```

## 🎯 Core Features

### Multi-Domain Architecture
- **dev**: Development environment (Blue theme)
- **server**: Backend/API domain (Green theme)  
- **www**: Public web interface (Purple theme)

### Platform Optimization
- **Mobile**: ≤768px with touch-friendly interactions
- **Desktop**: >768px with hover effects and keyboard navigation

### Component Pipeline
1. **Global Templates** → Platform-specific base components
2. **Domain Styling** → Apply theme-specific CSS and Tailwind
3. **Path Resolution** → Update domain-relative URLs
4. **Dual Output** → Generate in both domain and centralized locations

## 🛠️ Available Components

| Component | Platforms | Description |
|-----------|-----------|-------------|
| **navbar** | Mobile + Desktop | Navigation with platform-specific behavior |
| **footer** | Mobile + Desktop | Responsive footer with domain links |
| **card** | Mobile + Desktop | Content card with touch/hover optimization |
| **svg-card** | Mobile + Desktop | Icon-enhanced card component |
| **ticker** | Mobile only | Scrolling announcement ticker |

### Mobile-Specific Features
- Hamburger menu navigation (navbar)
- Integrated ticker component
- Touch-friendly 44px minimum targets
- Single-column responsive layouts
- Gesture-based interactions

### Desktop-Specific Features  
- Horizontal navigation (navbar)
- Advanced hover effects
- Multi-column layouts
- Keyboard accessibility
- Search functionality

## 🎨 Domain Themes

### Dev Domain (Blue Theme)
- Primary: `#3b82f6`
- Focus: Development tools and interfaces
- Style: Professional, technical

### Server Domain (Green Theme)
- Primary: `#22c55e` 
- Focus: Backend services and APIs
- Style: Reliable, performance-focused

### WWW Domain (Purple Theme)
- Primary: `#a855f7`
- Focus: Public web presence
- Style: Creative, engaging

## 🔧 Build System Commands

### Individual Component Builds
```bash
# Basic build
./build/build.sh --component navbar --platform both --domain all

# Domain-specific
./build/build.sh --component footer --platform mobile --domain dev

# With validation
./build/build.sh --component card --platform both --domain all --validate

# Watch mode (auto-rebuild on changes)
./build/build.sh --component navbar --platform both --domain dev --watch
```

### Batch Operations
```bash
# Build all components
./build/build-all.sh

# Domain-specific batch
./build/build-all.sh --domain dev --validate

# Verbose output
./build/build-all.sh --verbose
```

## 📱 Responsive Breakpoints

The system uses a mobile-first approach:

```css
/* Mobile styles (default) */
.component { /* Mobile styles */ }

/* Desktop styles */
@media (min-width: 769px) {
  .component { /* Desktop overrides */ }
}
```

**Key Breakpoint**: 768px (iPad Mini width)
- **Mobile**: ≤768px
- **Desktop**: >768px

## 🎛️ Configuration

### Component Configuration (`build/components.json`)
```json
{
  "components": {
    "navbar": {
      "platforms": ["mobile", "desktop"],
      "dependencies": {
        "mobile": ["ticker.js"],
        "desktop": []
      }
    }
  }
}
```

### Tailwind Configuration (`build/tailwind.config.js`)
Enhanced with:
- Domain-specific color palettes
- Touch-friendly utilities
- Component base classes
- Animation keyframes

## 🚦 Build Process Flow

```
1. Template Loading
   └── components/global.c/<platform>/<component>.js

2. Style Application  
   ├── <domain>/<domain>.styles/<domain>-styles.css
   └── <domain>/<domain>.styles/<domain>.tailwind.css

3. Path Resolution
   └── Update domain-specific URLs and links

4. Header Injection
   └── Add build metadata and timestamps

5. Dual Output Generation
   ├── <domain>/components/<domain>.c/<platform>.c/
   └── components/<domain>.c/<platform>/

6. Validation (optional)
   └── Syntax checking and structure validation

7. Manifest Update
   └── Log build status and metadata
```

## 🧪 Example Usage

### Initialize Mobile Navbar
```javascript
const navbar = new MobileNavbar({
  logoText: 'Ascend Institute',
  showTicker: true,
  tickerText: 'Latest updates and announcements'
});
```

### Initialize Desktop Navbar
```javascript
const navbar = new DesktopNavbar({
  logoText: 'Ascend Institute', 
  showSearch: true
});
```

### Create Card Grid
```javascript
const cards = MobileCard.createGrid([
  {
    title: 'GremlinGPT',
    description: 'AI-powered automation system',
    linkUrl: '/gremlingpt'
  },
  // ... more cards
], '#card-container');
```

## 📊 Component Manifest

The build system tracks:
- Component dependencies
- Build timestamps  
- Platform support
- Domain deployments
- Build success/failure rates

Check manifest: `build/component-manifest.json`

## 🔍 Validation & Testing

### Syntax Validation
```bash
# Validate generated JavaScript
node -c path/to/component.js

# Build with validation
./build/build.sh --component navbar --platform both --domain all --validate
```

### Manual Testing
Open example files to test components:
- `components/global.c/mobile/navbar-example.html`
- `components/global.c/desktop/navbar-example.html`

## 🤝 Contributing

1. **Component Development**: Add templates to `components/global.c/`
2. **Style Enhancement**: Update domain styles in `<domain>/<domain>.styles/`
3. **Build System**: Modify scripts in `build/`
4. **Documentation**: Update relevant README files

See [CONTRIBUTING.md](About%20Us/CONTRIBUTING.md) for detailed guidelines.

## 📖 Documentation

- **Build System**: [build/README.md](build/README.md)
- **Components**: [components/global.c/README.md](components/global.c/README.md)
- **Code of Conduct**: [About Us/CODE_OF_CONDUCT.md](About%20Us/CODE_OF_CONDUCT.md)
- **Contributing**: [About Us/CONTRIBUTING.md](About%20Us/CONTRIBUTING.md)

## 🔗 Related Projects

- **GremlinGPT**: AI automation system
- **Sovereign Stack**: Self-hosting infrastructure
- **Financial Autonomy**: Educational resources

## 📄 License

See [LICENSE.md](LICENSE.md) for license information.

## 🆘 Support

For issues, questions, or feature requests:

1. Check the [build system documentation](build/README.md)
2. Review [troubleshooting guide](build/README.md#troubleshooting)
3. Create an issue in the repository
4. Follow [contributing guidelines](About%20Us/CONTRIBUTING.md)

---

**Built with ❤️ for digital sovereignty by the Ascend Institute team.**