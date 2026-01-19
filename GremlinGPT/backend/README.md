# Backend Module

The `backend` module serves as the core server infrastructure for GremlinGPT, providing API endpoints, request routing, state management, and system coordination services.

## Components

### 🌐 server.py
**Main Application Server**
- Flask-based web server for API endpoints and dashboard
- NLTK data path configuration and natural language processing setup
- WebSocket broadcasting for real-time communication
- Graceful server startup and shutdown handling
- Integration with frontend dashboard and external API consumers

### 🔄 router.py
**API Route Management**
- Dynamic API route registration and verification
- Route backup and failover mechanisms
- Endpoint health monitoring and status reporting
- RESTful API design patterns and middleware integration
- Request/response logging and metrics collection

### ⏰ scheduler.py
**Task Scheduling System**
- Background task scheduling using APScheduler
- Integration with core loop operations and agent coordination
- Self-training pipeline scheduling and execution
- Planner agent coordination and task distribution
- Mutation watcher scheduling for system evolution
- Signal handling for graceful shutdown

### 🌍 globals.py
**Global Configuration Management**
- TOML configuration file loading and validation
- Memory configuration management and JSON handling
- Path resolution with project-relative addressing
- Environment variable integration and override support
- Critical configuration error handling and recovery
- Dashboard backend URL management

### 💾 state_manager.py
**System State Persistence**
- State snapshot creation and restoration
- System checkpoint management
- Configuration state tracking and validation
- Recovery mechanisms for system restarts
- State consistency verification and repair

### 📁 Subdirectories

#### api/
**API Endpoint Implementations**
- Individual API route handlers and business logic
- Request validation and response formatting
- Authentication and authorization middleware
- Rate limiting and request throttling

#### interface/
**UI Interface Components**
- Dashboard interface templates and static assets
- WebSocket handlers for real-time updates
- Frontend-backend communication protocols
- User interface state management

#### utils/
**Backend Utilities**
- Helper functions for backend operations
- Common middleware and decorators
- Request/response transformation utilities
- Backend-specific validation functions

## Architecture

The backend module follows a modular, service-oriented architecture:

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Server      │────│     Router      │────│      API        │
│   (Flask App)   │    │  (Route Mgmt)   │    │   (Endpoints)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Scheduler     │    │  State Manager  │    │    Globals      │
│  (Background)   │    │  (Persistence)  │    │ (Configuration) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Operation Flow

1. **Initialization**: Globals loads configuration, server initializes Flask app
2. **Route Registration**: Router dynamically registers API endpoints
3. **Service Startup**: Scheduler starts background tasks and agent coordination
4. **Request Handling**: Server processes incoming requests via registered routes
5. **State Management**: State manager maintains system consistency and checkpoints
6. **Background Operations**: Scheduler coordinates long-running tasks and agent activities

## API Endpoints

The backend provides RESTful APIs for:
- **System Control**: Start/stop operations, health checks
- **Agent Management**: Agent registration, task assignment, status monitoring
- **Trading Operations**: Market data, signal processing, order management
- **Memory Operations**: Knowledge storage, retrieval, vector search
- **Training Pipeline**: Model training, data processing, validation
- **Real-time Communication**: WebSocket endpoints for live updates

## Configuration

Key configuration parameters managed by globals.py:
- Server host/port settings
- Database connection strings
- API rate limiting parameters
- Logging levels and output destinations
- Security keys and authentication settings
- External service integration endpoints

## Logging

Structured logging with component-specific log files:
- Server operations: `data/logs/backend/server.log`
- Router activity: `data/logs/backend/router.log`
- Scheduler events: `data/logs/backend/scheduler.log`
- Global config: `data/logs/backend/globals.log`
- State management: `data/logs/backend/state_manager.log`

## Security

The backend implements multiple security layers:
- Request validation and sanitization
- Rate limiting and DDoS protection
- Authentication token management
- CORS policy enforcement
- Input validation and SQL injection prevention
- Secure configuration handling

## Performance

Optimized for:
- **High Throughput**: Concurrent request processing
- **Low Latency**: Efficient route lookup and response generation
- **Scalability**: Horizontal scaling with load balancer support
- **Reliability**: Graceful error handling and automatic recovery
- **Monitoring**: Comprehensive metrics and health checking

## Integration

The backend integrates with:
- **Frontend**: Dashboard UI and real-time updates
- **Agent Core**: Task distribution and coordination
- **NLP Engine**: Natural language processing requests
- **Memory System**: Knowledge storage and retrieval
- **Trading Core**: Financial operations and market data
- **External APIs**: Third-party service integration
