#─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
#─────────────────────────────────────────────────────────────
#!/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# agent_core/task_queue.py

from collections import deque, defaultdict
import uuid
import json
from pathlib import Path
from backend.globals import logger
from datetime import datetime, timedelta

QUEUE_FILE = Path("run/checkpoints/task_queue.json")
ESCALATION_THRESHOLD_SEC = 120


def promote_old_tasks():
    now = datetime.utcnow()
    threshold = timedelta(seconds=ESCALATION_THRESHOLD_SEC)

    for level, next_level in [("low", "normal"), ("normal", "high")]:
        to_promote = []
        for task in list(task_queue[level]):
            tid = task.get("id")
            if not tid or tid not in task_meta:
                continue
            timestamp = datetime.fromisoformat(task_meta[tid]["timestamp"])
            if now - timestamp > threshold:
                to_promote.append(task)
                task_queue[level].remove(task)
                task_meta[tid]["priority"] = next_level
                logger.info(f"[ESCALATION] Promoted task {tid} to {next_level}")

        for task in to_promote:
            task_queue[next_level].append(task)
    _save_snapshot()


# Priority buckets
task_queue = {"high": deque(), "normal": deque(), "low": deque()}

task_status = {}
task_meta = defaultdict(dict)


def _save_snapshot():
    try:
        snapshot = {
            "queue": {k: list(v) for k, v in task_queue.items()},
            "status": task_status,
            "meta": task_meta,
        }
        with open(QUEUE_FILE, "w") as f:
            json.dump(snapshot, f, indent=2, default=str)
        logger.debug("[TASK_QUEUE] Snapshot saved.")
    except Exception as e:
        logger.error(f"[TASK_QUEUE] Snapshot save failed: {e}")


def _load_snapshot():
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE, "r") as f:
                data = json.load(f)
                for level in task_queue:
                    task_queue[level].clear()
                    task_queue[level].extend(data.get("queue", {}).get(level, []))
                task_status.update(data.get("status", {}))
                task_meta.update(data.get("meta", {}))
            logger.info("[TASK_QUEUE] Queue restored from snapshot.")
        except Exception as e:
            logger.warning(f"[TASK_QUEUE] Failed to load queue snapshot: {e}")


def enqueue_task(task):
    task_id = str(uuid.uuid4())
    task["id"] = task_id
    priority = task.get("priority", "normal").lower()

    if priority not in task_queue:
        logger.warning(
            f"[TASK_QUEUE] Invalid priority '{priority}', defaulting to normal."
        )
        priority = "normal"

    task_queue[priority].append(task)
    task_status[task_id] = "queued"
    task_meta[task_id] = {
        "type": task["type"],
        "priority": priority,
        "timestamp": datetime.utcnow().isoformat(),
        "retries": 0,
    }
    logger.debug(f"[TASK_QUEUE] Enqueued ({priority}): {task['type']} ({task_id})")
    _save_snapshot()


def reprioritize(task_id, new_priority):
    """
    Move a task to a new priority bucket by task ID.
    """
    if new_priority not in task_queue:
        logger.error(f"[TASK_QUEUE] Invalid target priority: {new_priority}")
        return False

    for level in ["high", "normal", "low"]:
        for task in list(task_queue[level]):
            if task.get("id") == task_id:
                task_queue[level].remove(task)
                task["priority"] = new_priority
                task_queue[new_priority].append(task)
                task_meta[task_id]["priority"] = new_priority
                task_status[task_id] = "reprioritized"
                logger.info(f"[TASK_QUEUE] Task {task_id} moved to {new_priority}")
                _save_snapshot()
                return True

    logger.warning(f"[TASK_QUEUE] Task ID {task_id} not found in any queue.")
    return False


def fetch_task(task_type=None):
    for level in ["high", "normal", "low"]:
        for _ in range(len(task_queue[level])):
            task = task_queue[level].popleft()
            if not task_type or task["type"] == task_type:
                task_status[task["id"]] = "running"
                return task
            task_queue[level].append(task)
    return None


def retry(task):
    tid = task.get("id")
    if tid:
        task_meta[tid]["retries"] += 1
        task_status[tid] = "retried"
        priority = task_meta[tid].get("priority", "normal")
        task_queue[priority].append(task)
        logger.warning(f"[TASK_QUEUE] Retried ({priority}): {tid}")
        _save_snapshot()


def get_all_tasks():
    return [
        {
            "id": k,
            "type": task_meta[k]["type"],
            "status": task_status[k],
            "priority": task_meta[k].get("priority", "normal"),
            "retries": task_meta[k].get("retries", 0),
            "timestamp": task_meta[k].get("timestamp"),
        }
        for k in task_status
    ]


def update_task_status(task_id, status):
    task_status[task_id] = status
    logger.debug(f"[TASK_QUEUE] {task_id} => {status}")
    _save_snapshot()


def dump():
    """Returns all queued tasks, grouped by priority"""
    return {
        "high": list(task_queue["high"]),
        "normal": list(task_queue["normal"]),
        "low": list(task_queue["low"]),
    }


# Cold boot restore
_load_snapshot()
