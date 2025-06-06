# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from agent_core.task_queue import enqueue_task, reprioritize
from backend.globals import CFG
from nlp_engine.parser import parse_nlp
from loguru import logger
from datetime import datetime
from memory.vector_store.embedder import (
    embed_text,
    package_embedding,
    inject_watermark,
)

WATERMARK = "source:GremlinGPT"
ORIGIN = "commands_interface"


def parse_command(cmd_text):
    """
    Interprets freeform command text into structured task dictionaries.
    Uses NLP, pattern matching, and command routing heuristics.
    """
    parsed = parse_nlp(cmd_text)
    route = parsed.get("route", "unknown")

    lowered = cmd_text.lower()

    # Explicit command mappings
    if "scrape" in lowered and "http" in lowered:
        return {"type": "scrape", "target": cmd_text.split()[-1]}

    elif "scan" in lowered or "signal" in lowered:
        return {"type": "signal_scan"}

    elif "train" in lowered or "retrain" in lowered:
        return {"type": "self_train"}

    elif "shell" in lowered or route == "code":
        return {"type": "shell", "command": cmd_text}

    elif route == "finance":
        return {"type": "nlp", "text": cmd_text}

    else:
        return {"type": "unknown", "payload": cmd_text}


def execute_command(cmd):
    """
    Executes or enqueues task, and logs trace to vector memory for lineage.
    """
    task_type = cmd.get("type")

    if task_type in {"scrape", "signal_scan", "self_train", "nlp", "shell"}:
        enqueue_task(cmd)

        if CFG["agent"].get("log_agent_output", True):
            logger.info(f"[COMMAND] Task enqueued: {cmd}")

        # Prepare trace
        summary = f"Command executed: {task_type}"
        trace_text = (
            cmd.get("target") or cmd.get("message") or cmd.get("command") or str(cmd)
        )
        vector = embed_text(trace_text)

        package_embedding(
            text=summary,
            vector=vector,
            meta={
                "type": task_type,
                "timestamp": datetime.utcnow().isoformat(),
                "source": ORIGIN,
                "watermark": WATERMARK,
            },
        )

        inject_watermark(origin=ORIGIN)

        return {"status": "queued", "task": cmd}

    else:
        logger.warning(f"[COMMAND] Unknown command type: {cmd}")
        return {"status": "error", "message": "Unknown command."}


def update_task_priority(task_id, new_priority):
    """
    Adjusts task priority in runtime queue.
    """
    try:
        result = reprioritize(task_id, new_priority)
        if result:
            logger.info(f"[COMMAND] Reprioritized task {task_id} → {new_priority}")
        else:
            logger.warning(f"[COMMAND] Failed to reprioritize: {task_id}")
        return result
    except Exception as e:
        logger.error(f"[COMMAND] Priority update error: {e}")
        return False
