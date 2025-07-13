# Core Module

The `core` module provides the fundamental execution engine and system kernel for GremlinGPT. It manages the main system loop, execution kernel, and state snapshot functionality that drives the autonomous operation of the entire system.

## Components

### 🔄 loop.py
**Main System Loop Engine**
- Implements the recursive FSM (Finite State Machine) control engine
- Manages the primary system tick cycle with configurable intervals
- Coordinates between agent_core FSM and system-wide operations
- Handles feedback loop integration and trigger monitoring
- Provides system lifecycle management and graceful shutdown
- Maintains cycle counting and performance metrics
- Integrates with memory logging for operational history

### ⚙️ kernel.py
**Code Execution & Writing Kernel**
- Implements the core code writing and execution engine
- Manages dynamic code generation and modification
- Provides file writing capabilities with backup and versioning
- Integrates with vector store for embedding and semantic analysis
- Handles diff generation for code changes and updates
- Supports feedback injection for continuous improvement
- Manages kernel-specific operations and metadata

### 📸 snapshot.py
**System State Snapshots**
- Creates comprehensive system state snapshots
- Implements file hashing and change detection
- Provides state versioning and checkpoint management
- Generates embeddings for snapshot content analysis
- Supports incremental and full system backups
- Manages snapshot metadata and indexing
- Enables system state comparison and rollback capabilities

## Architecture

The core module operates as the central nervous system of GremlinGPT:

```text
┌─────────────────┐
│   Main Loop     │
│   (Orchestrator)│
└─────────────────┘
         │
         ├─── FSM Control
         ├─── Feedback Monitoring  
         ├─── Memory Logging
         └─── Cycle Management
         │
┌─────────────────┐    ┌─────────────────┐
│     Kernel      │────│    Snapshot     │
│  (Execution)    │    │   (Persistence) │
└─────────────────┘    └─────────────────┘
         │                       │
         ├─── Code Writing        ├─── State Capture
         ├─── File Management     ├─── Change Detection
         ├─── Embedding Gen       ├─── Version Control
         └─── Diff Analysis       └─── Metadata Mgmt
```

## Operation Flow

### System Boot Sequence
1. **Loop Initialization**: Main loop starts with configuration loading
2. **FSM Activation**: Agent core FSM is initialized and activated
3. **Kernel Readiness**: Execution kernel prepares for code operations
4. **Snapshot Baseline**: Initial system state snapshot is created
5. **Tick Cycle Start**: Main loop begins regular tick operations

### Runtime Operation
1. **Tick Processing**: Each cycle processes pending operations
2. **FSM Coordination**: Agent core state machine execution
3. **Feedback Integration**: Continuous improvement feedback processing
4. **State Monitoring**: System health and performance tracking
5. **Snapshot Updates**: Periodic state snapshots for persistence

### Code Execution Flow
1. **Code Generation**: Kernel generates or modifies code
2. **Embedding Creation**: Vector embeddings for semantic analysis
3. **Diff Analysis**: Change detection and impact assessment
4. **Backup Creation**: Safe backup before modifications
5. **Execution**: Code writing and execution with monitoring

## Key Features

### 🔄 Loop Engine
- **Configurable Timing**: Adjustable tick intervals based on system load
- **Graceful Shutdown**: Clean termination with state preservation
- **Error Recovery**: Automatic recovery from loop failures
- **Performance Monitoring**: Cycle timing and throughput metrics
- **Memory Integration**: Event logging for system history

### ⚙️ Kernel Operations
- **Dynamic Code Writing**: Real-time code generation and modification
- **Version Control Integration**: Git-style change tracking
- **Semantic Analysis**: Vector-based code understanding
- **Backup Management**: Automatic backup creation and restoration
- **Feedback Integration**: Learning from execution outcomes

### 📸 Snapshot System
- **Incremental Snapshots**: Efficient change-only captures
- **Hash-based Detection**: Fast file change identification
- **Metadata Enrichment**: Rich snapshot descriptions and indexing
- **Vector Embeddings**: Semantic snapshot analysis
- **Rollback Capability**: State restoration from any snapshot

## Configuration

Key configuration parameters:
- **Loop Timing**: `loop.tick_interval_sec` - Main loop cycle interval
- **Snapshot Paths**: `run/checkpoints/snapshots/` - Snapshot storage location
- **Kernel Settings**: Code writing preferences and safety limits
- **Backup Policies**: Retention periods and storage limits

## Logging

Structured logging with core-specific log files:
- Main loop: `data/logs/core/loop.log`
- Kernel operations: `data/logs/core/kernel.log`
- Snapshot activities: `data/logs/core/snapshot.log`

## Performance

The core module is optimized for:
- **Low Overhead**: Minimal resource usage during idle cycles
- **High Reliability**: Fault-tolerant operation with recovery mechanisms
- **Scalable Operations**: Efficient handling of increasing system complexity
- **Real-time Response**: Sub-second response to system events
- **Memory Efficiency**: Optimized data structures and cleanup

## Integration

The core module integrates with:
- **Agent Core**: FSM coordination and task execution
- **Backend**: Server lifecycle and health monitoring
- **Memory**: Event logging and history management
- **NLP Engine**: Diff analysis and semantic understanding
- **Self Training**: Feedback loop integration and learning
- **Vector Store**: Embedding generation and storage

## Safety Features

- **Atomic Operations**: All-or-nothing code modifications
- **Backup Verification**: Integrity checking of backups
- **State Validation**: Snapshot consistency verification
- **Error Isolation**: Fault containment to prevent system corruption
- **Recovery Mechanisms**: Multiple levels of system recovery options
