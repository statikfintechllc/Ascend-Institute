#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

import logging
from datetime import datetime
from backend.globals import CFG
from pathlib import Path
import json
import uuid
from typing import Union

log_dir = CFG.get("paths", {}).get("log_dir")
if not log_dir or not isinstance(log_dir, str):
    raise RuntimeError("Missing or invalid 'log_dir' in CFG['paths']")
ERROR_LOG_FILE = Path(log_dir) / "task_errors.jsonl"

# Configure logger for error logging
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
if not error_logger.handlers:
    fh = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.ERROR)
    class JsonlFormatter(logging.Formatter):
        def format(self, record):
            return record.getMessage()
    fh.setFormatter(JsonlFormatter())
    error_logger.addHandler(fh)

def log_error(task: dict, error: Union[Exception, str], source: str = "unknown"):
    """
    Logs structured, agent-aligned error with traceability for GremlinFSM.
    Supports console output and persistent JSONL storage.
    """

    trace_id = str(uuid.uuid4())
    task_type = task.get("type", "unknown")

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent": source,
        "task_type": task_type,
        "task_payload": task,
        "error": str(error),
        "severity": "error",
        "trace_id": trace_id,
    }

    # Log to terminal
    print(f"[ERROR_LOG] [{trace_id}] {task_type} failed — {error}")

    # Persist to file using logging
    try:
        error_logger.error(json.dumps(record))
    except Exception as e:
        print(f"[ERROR_LOG] Failed to persist log: {e}")
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
