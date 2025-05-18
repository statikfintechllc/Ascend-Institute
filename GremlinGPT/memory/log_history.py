# memory/log_history.py

import os
import json
from pathlib import Path
from datetime import datetime
from backend.globals import logger

HISTORY_DIR = Path("data/logs/history/")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_FILE = HISTORY_DIR / "gremlin_exec_log.jsonl"

def log_event(event_type, task_type, details, status="ok", meta=None):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "task": task_type,
        "status": status,
        "details": details,
        "meta": meta or {}
    }

    try:
        with open(HISTORY_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
        logger.info(f"[HISTORY] Logged {event_type} :: {task_type}")
    except Exception as e:
        logger.error(f"[HISTORY] Failed to log: {e}")

def load_history(n=50):
    """Returns the last n events from log history"""
    try:
        with open(HISTORY_FILE, "r") as f:
            lines = f.readlines()
        return [json.loads(line) for line in lines[-n:]]
    except FileNotFoundError:
        return []
    except Exception as e:
        logger.error(f"[HISTORY] Load failed: {e}")
        return []

# CLI test
if __name__ == "__main__":
    log_event("exec", "scrape", {"outcome": "5 tickers pulled"}, status="success")
    log_event("exec", "nlp", {"answer": "support/resistance identified"}, status="ok")
    print(load_history(2))
