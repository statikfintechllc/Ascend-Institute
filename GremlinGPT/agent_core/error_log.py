# !/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from loguru import logger
from datetime import datetime
from backend.globals import CFG
from pathlib import Path
import json

ERROR_LOG_FILE = Path(CFG["paths"]["log_dir"]) / "task_errors.jsonl"
ERROR_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_error(task, error):
    """
    Logs structured error for a failed task.
    Supports console + file persistence.
    """
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "task_type": task.get("type", "unknown"),
        "task_payload": task,
        "error": str(error),
    }

    # Log to terminal
    logger.error(f"[ERROR_LOG] Task '{record['task_type']}' failed — {error}")

    # Append to file
    try:
        with open(ERROR_LOG_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        logger.warning(f"[ERROR_LOG] Failed to persist error log: {e}")
