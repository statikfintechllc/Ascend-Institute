#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive

from loguru import logger
from datetime import datetime
from backend.globals import CFG
from pathlib import Path
import json
import uuid

ERROR_LOG_FILE = Path(CFG["paths"]["log_dir"]) / "task_errors.jsonl"
ERROR_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_error(task: dict, error: Exception | str, source: str = "unknown"):
    """
    Logs structured, agent-aligned error with traceability for GremlinFSM.
    Supports console output and persistent JSONL storage.
    """

    trace_id = str(uuid.uuid4())
    task_type = task.get("type", "unknown")

    record = {
        "id": trace_id,
        "timestamp": datetime.utcnow().isoformat(),
        "agent": source,
        "task_type": task_type,
        "task_payload": task,
        "error": str(error),
        "severity": "error",
    }

    # Log to terminal
    logger.error(f"[ERROR_LOG] [{trace_id}] {task_type} failed — {error}")

    # Persist to file
    try:
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        logger.warning(f"[ERROR_LOG] Failed to persist log: {e}")
