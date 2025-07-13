# GremlinGPT Logging Structure

This directory contains all GremlinGPT system logs organized by category for easy navigation and debugging.

## Directory Structure

```text
data/logs/
├── system/           # System-level logs
│   ├── runtime.log      # Main system runtime log
│   ├── bootstrap.log    # System startup log
│   └── install.log      # Installation process log
├── services/         # Service output logs (.out files)
│   ├── backend.out      # Backend service output
│   ├── frontend.out     # Frontend service output
│   ├── nlp.out         # NLP engine service output
│   ├── memory.out      # Memory system service output
│   ├── fsm.out         # FSM agent service output
│   ├── scraper.out     # Scraper service output
│   ├── trainer.out     # Training service output
│   └── ngrok.out       # Ngrok tunnel service output
├── modules/          # Individual module logs (organized by module)
│   ├── backend/        # Backend module logs
│   ├── core/          # Core system logs
│   ├── nlp_engine/    # NLP engine logs
│   ├── memory/        # Memory system logs
│   ├── scraper/       # Scraper logs
│   ├── trading_core/  # Trading system logs
│   ├── agents/        # Agent system logs
│   ├── executors/     # Executor logs
│   ├── tools/         # Tools logs
│   ├── utils/         # Utilities logs
│   ├── self_mutation_watcher/  # Mutation watcher logs
│   └── self_training/ # Self-training logs
├── applications/     # Application-specific logs
│   ├── task_errors.jsonl    # Task error logs (JSON format)
│   └── tests/              # Test logs
└── archives/        # Archived/rotated logs
```

## Log Types

### System Logs (`system/`)
- **runtime.log**: Main application runtime events and errors
- **bootstrap.log**: System startup sequence and initialization
- **install.log**: Installation process, dependency setup, configuration

### Service Logs (`services/`)  
- Service output logs (`.out` files) from process managers
- Contain stdout/stderr from running services
- Useful for diagnosing service startup issues

### Module Logs (`modules/`)
- Individual module logs with structured logging
- Each module has its own subdirectory
- Rotating logs with timestamps
- Include INFO, WARNING, ERROR, DEBUG levels

### Application Logs (`applications/`)
- Application-specific data logs
- Task queues, error tracking, data processing logs
- Structured data logs (JSON, JSONL formats)

## Log Rotation

- Individual module logs rotate at 10MB
- Logs are retained for 30 days
- Archives are moved to `archives/` directory
- Service logs (.out files) are managed by process managers

## Permissions

All log files are created with 644 permissions:
- Owner: read/write
- Group: read  
- Others: read

## Viewing Logs

### Via Dashboard CLI
```bash
./utils/dash_cli.sh
# Select option 4 for organized log viewing
```

### Via Command Line
```bash
# View recent system logs
tail -f data/logs/system/runtime.log

# View module logs
tail -f data/logs/backend/backend.log

# View service outputs
tail -f data/logs/services/backend.out

# Search across all logs
grep -r "ERROR" data/logs/

# View structured logs
cat data/logs/applications/task_errors.jsonl | jq '.'
```

### Via systemd (for service logs)
```bash
# View service logs
journalctl -u gremlin -f

# View recent logs
journalctl -u gremlin -n 100
```

## Troubleshooting

### Log File Not Found
- Check if the module/service is running
- Verify permissions on log directories
- Check if logging is properly configured in the module

### Disk Space Issues  
- Logs rotate automatically at 10MB
- Check `archives/` directory for old logs
- Manually clean archives if needed: `rm -rf data/logs/archives/*`

### Permission Issues
- All logs should be 644 (readable by all, writable by owner)
- Log directories should be 755
- Run: `find data/logs -type f -exec chmod 644 {} \;`

## Integration

This logging structure integrates with:
- **Dashboard CLI**: Organized log viewing interface
- **systemd service**: Journal logging for service management  
- **Log rotation**: Automatic cleanup and archival
- **Monitoring**: Structured logs for external monitoring tools
