# Backend API Module

The `backend/api` module contains all the API endpoint implementations and handlers for GremlinGPT's web services. These components provide RESTful API access to system functionality and real-time communication capabilities.

## Components

### 🌐 api_endpoints.py
**Main API Router & Endpoint Definitions**
- Central Flask blueprint registration and endpoint routing
- System control endpoints (start/stop/status/health)
- Task management and queue operations
- FSM state management and control
- Real-time WebSocket event handling
- Agent coordination and communication
- Trading signal processing and market data
- Memory graph visualization and data access

### 💬 chat_handler.py
**Natural Language Chat Interface**
- Processes user chat inputs and natural language commands
- Integrates with NLP engine for intent recognition
- Routes commands to appropriate system components
- Maintains conversation context and history
- Supports both synchronous and asynchronous responses
- Handles command parsing and validation
- Provides structured JSON responses for chat clients

### 🧠 memory_api.py
**Memory System API Interface**
- Vector store query and retrieval endpoints
- Memory graph visualization data
- Embedding search and similarity matching
- Knowledge base management operations
- Historical data access and archival
- Memory statistics and health monitoring
- Integration with vector databases (FAISS/Chroma)

### 📋 planner.py
**Task Planning & Agent Coordination API**
- Task queue management and prioritization
- Agent task assignment and distribution
- FSM state transition control
- Signal processing and routing
- Mutation event handling and responses
- Cross-agent communication protocols
- Task escalation and retry mechanisms

### 🕷️ scraping_api.py
**Web Scraping & Data Collection API**
- Dynamic web scraping endpoint routing
- Multi-method scraping strategy selection
- Content extraction and parsing
- Data validation and quality control
- Rate limiting and ethical scraping compliance
- Integration with multiple scraper backends
- Real-time scraping status and progress tracking

### 📝 summarizer.py
**Text Summarization Services**
- Text content summarization and compression
- Key information extraction
- Content length optimization
- Multi-format output support
- Performance-optimized stub implementation
- Future integration point for advanced NLP models

## Architecture

The API module follows RESTful design principles with modular endpoint organization:

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  API Endpoints  │────│  Chat Handler   │────│   Memory API    │
│   (Routing)     │    │    (NLP)        │    │   (Vector)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Planner      │    │  Scraping API   │    │   Summarizer    │
│ (Coordination)  │    │  (Collection)   │    │   (Processing)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Endpoint Categories

### System Control
- `GET /health` - System health check and status
- `POST /start` - Start GremlinGPT services
- `POST /stop` - Stop GremlinGPT services
- `GET /status` - Current system status and metrics

### Task Management
- `GET /tasks` - List current task queue
- `POST /tasks` - Add new task to queue
- `PUT /tasks/{id}` - Update task priority or status
- `DELETE /tasks/{id}` - Remove task from queue

### Chat & Communication
- `POST /chat` - Process natural language input
- `WebSocket /ws` - Real-time communication channel
- `GET /chat/history` - Retrieve chat history
- `POST /chat/command` - Execute direct commands

### Memory & Knowledge
- `GET /memory/graph` - Memory graph visualization data
- `POST /memory/search` - Vector similarity search
- `GET /memory/stats` - Memory system statistics
- `POST /memory/store` - Store new knowledge

### Scraping & Data
- `POST /scrape` - Initiate web scraping operation
- `GET /scrape/status/{id}` - Check scraping progress
- `GET /scrape/results/{id}` - Retrieve scraped data
- `POST /scrape/bulk` - Batch scraping operations

## Authentication & Security

- API key validation for external access
- Rate limiting per endpoint and client
- Input validation and sanitization
- CORS policy management
- Request/response logging and monitoring

## Response Formats

All endpoints return structured JSON responses with consistent formatting:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2025-07-13T12:00:00Z",
  "request_id": "uuid"
}
```

## Error Handling

- Standardized error codes and messages
- Graceful degradation for service failures
- Detailed error logging and tracking
- Client-friendly error responses
- Automatic retry mechanisms where appropriate

## Performance

- Asynchronous processing for long-running operations
- Response caching for frequently accessed data
- Connection pooling and resource management
- Request queuing and load balancing
- Comprehensive performance monitoring

## Integration

The API module integrates with:
- **Frontend Dashboard**: Real-time updates and control interface
- **Agent Core**: Task distribution and coordination
- **NLP Engine**: Natural language processing and understanding
- **Memory System**: Knowledge storage and retrieval
- **Scraper**: Web data collection and processing
- **Trading Core**: Market data and financial operations
