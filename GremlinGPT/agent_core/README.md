# Agent Core Module

The `agent_core` module is the foundational component of GremlinGPT's autonomous agent system. It provides the core infrastructure for agent management, task orchestration, state management, and error handling.

## Components

### 🤖 agent_profiles.py
**Agent Configuration & Profile Management**
- Loads and manages agent profiles from YAML configuration
- Defines agent capabilities, specializations, and behavioral parameters
- Provides agent configuration lookup and validation
- Supports dynamic agent profile updates

### 📋 task_queue.py
**Production Task Queue System**
- Implements prioritized task queue with high/normal/low priority levels
- Provides task scheduling, escalation, and lifecycle management
- Supports task persistence and recovery across system restarts
- Handles task status tracking and completion monitoring
- Features automatic task aging and priority promotion

### 🔄 fsm.py
**Finite State Machine Core**
- Implements the main state machine orchestrating agent behavior
- Manages state transitions and agent lifecycle
- Coordinates task execution across multiple agents
- Provides system health monitoring and recovery mechanisms
- Handles scheduled operations and system maintenance

### ⚡ heuristics.py
**Performance & Resource Heuristics**
- Provides system performance monitoring and analysis
- Implements resource usage optimization heuristics
- Calculates system load and capacity metrics
- Supports dynamic resource allocation decisions
- Monitors CPU, memory, and system resource utilization

### 📊 error_log.py
**Centralized Error Management**
- Implements structured error logging and tracking
- Provides error categorization and severity analysis
- Supports error recovery and escalation workflows
- Maintains error history and pattern analysis
- Generates error reports and system health metrics

### 📁 agent_profiles.yaml
**Agent Configuration File**
- YAML-based agent profile definitions
- Defines agent capabilities, roles, and permissions
- Configures agent interaction patterns and workflows
- Supports multi-agent coordination parameters

## Architecture

The agent_core module follows a modular, event-driven architecture:

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FSM Core      │────│   Task Queue    │────│   Heuristics    │
│   (Orchestrator)│    │   (Scheduler)   │    │   (Monitor)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Agent Profiles  │    │   Error Log     │    │   External      │
│ (Configuration) │    │   (Monitoring)  │    │   Agents        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Operation Flow

1. **Initialization**: FSM loads agent profiles and initializes task queue
2. **Task Reception**: Tasks are received and queued with appropriate priority
3. **Agent Selection**: FSM selects appropriate agents based on profiles and heuristics
4. **Task Execution**: Tasks are distributed to agents for execution
5. **Monitoring**: System monitors performance, errors, and resource usage
6. **Recovery**: Error handling and system recovery mechanisms activate as needed

## Logging

All components use structured logging with module-specific log files:
- System logs: `data/logs/agent_core/`
- Individual component logs for debugging and monitoring
- Centralized error tracking in `data/logs/applications/task_errors.jsonl`

## Integration

The agent_core module integrates with:
- **Backend**: Server coordination and API endpoints
- **NLP Engine**: Natural language processing for task interpretation
- **Memory**: Long-term memory and knowledge storage
- **Trading Core**: Financial trading operations and signals
- **Executors**: Code and shell execution environments

## Configuration

Key configuration parameters:
- Agent profiles: `agent_core/agent_profiles.yaml`
- Task queue persistence: `run/checkpoints/task_queue.json`
- Logging configuration: Via `utils/logging_config.py`
- Error thresholds and escalation rules

## Performance

The agent_core module is optimized for:
- **Low Latency**: Sub-second task queue operations
- **High Throughput**: Concurrent task processing
- **Fault Tolerance**: Graceful degradation and recovery
- **Scalability**: Support for multiple agent instances
- **Resource Efficiency**: Minimal memory and CPU overhead
