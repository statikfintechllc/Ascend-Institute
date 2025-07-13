# Utils Module

The `utils` module provides core utilities, configuration management, and shared functionality used throughout GremlinGPT.

## Components

### 📝 logging_config.py
**Centralized Logging Configuration**
- Structured logging setup and management
- Module-specific logger creation
- Log formatting and output configuration
- Log level management and filtering

### 🔧 dash_cli.sh
**Dashboard Command Line Interface**
- Interactive system management interface
- Log viewing and system monitoring
- Service control and management
- User-friendly system interaction

## Architecture

```text
┌─────────────────┐    ┌─────────────────┐
│ Logging Config  │────│   Dash CLI      │
│ (Infrastructure)│    │ (Interface)     │
└─────────────────┘    └─────────────────┘
         │                       │
         └───────────────────────┼
                                 │
                    ┌─────────────────┐
                    │   Shared Utils  │
                    │  (Common Funcs) │
                    └─────────────────┘
```

## Key Features

- **Centralized Configuration**: Single point of configuration management
- **Structured Logging**: Consistent logging across all modules
- **User Interface**: Intuitive command-line interaction
- **Shared Utilities**: Common functionality for all modules
