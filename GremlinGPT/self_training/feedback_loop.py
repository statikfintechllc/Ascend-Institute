import os
import json
from datetime import datetime
from loguru import logger
from pathlib import Path

# Paths
LOG_PATH = Path("data/logs/")
TRIGGER_FILE = Path("run/checkpoints/retrain_trigger.json")
LOG_PATH.mkdir(parents=True, exist_ok=True)

def inject_feedback():
    logger.info("[FEEDBACK] Mutation event detected — scheduling retrain.")
    trigger = {
        "trigger": "mutation_watcher",
        "time": datetime.utcnow().isoformat(),
        "note": "Auto-diff-based training cycle",
    }
    try:
        with open(TRIGGER_FILE, "w") as f:
            json.dump(trigger, f, indent=2)
        logger.success(f"[FEEDBACK] Retrain trigger saved → {TRIGGER_FILE}")
    except Exception as e:
        logger.error(f"[FEEDBACK] Failed to save retrain trigger: {e}")

def check_trigger():
    exists = TRIGGER_FILE.exists()
    logger.debug(f"[FEEDBACK] Trigger file exists: {exists}")
    return exists

def clear_trigger():
    if TRIGGER_FILE.exists():
        TRIGGER_FILE.unlink()
        logger.info("[FEEDBACK] Retrain trigger cleared.")

