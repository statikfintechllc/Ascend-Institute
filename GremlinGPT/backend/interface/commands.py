# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────
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

# backend/interface/commands.py

from agent_core.task_queue import enqueue_task, reprioritize
from backend.globals import CFG
from loguru import logger
from nlp_engine.parser import parse_nlp
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from datetime import datetime

WATERMARK = "source:GremlinGPT"
ORIGIN = "commands_interface"


def parse_command(cmd_text):
    parsed = parse_nlp(cmd_text)
    route = parsed.get("route", "unknown")

    if "scrape" in cmd_text:
        return {"type": "scrape", "target": cmd_text.split()[-1]}
    elif "scan" in cmd_text:
        return {"type": "signal_scan"}
    elif "train" in cmd_text:
        return {"type": "self_train"}
    elif route == "code":
        return {"type": "shell", "command": cmd_text}
    elif route == "finance":
        return {"type": "nlp", "text": cmd_text}
    else:
        return {"type": "unknown", "payload": cmd_text}


def execute_command(cmd):
    if cmd["type"] in ["scrape", "signal_scan", "self_train", "nlp", "shell"]:
        enqueue_task(cmd)

        if CFG["agent"].get("log_agent_output", True):
            logger.info(f"[COMMAND] Queued: {cmd}")

        # === Embed the command for memory tracking ===
        text = cmd.get("target") or cmd.get("text") or str(cmd)
        summary = f"Command executed: {cmd['type']}"

        vector = embed_text(text)
        package_embedding(
            text=summary,
            vector=vector,
            meta={
                "type": cmd["type"],
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
    Adjust the priority of a task using task_queue.reprioritize.
    """
    try:
        result = reprioritize(task_id, new_priority)
        if result:
            logger.info(f"[COMMAND] Task {task_id} reprioritized to {new_priority}")
        else:
            logger.warning(f"[COMMAND] Failed to reprioritize task: {task_id}")
        return result
    except Exception as e:
        logger.error(f"[COMMAND] Priority update failed: {e}")
        return False
