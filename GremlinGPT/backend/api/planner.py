# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion. v5 :: Module Integrity Directive

from flask import Blueprint, request, jsonify
from agent_core.task_queue import reprioritize
from agent_core import task_queue
from memory.log_history import log_event
from loguru import logger
import networkx as nx
from datetime import datetime

planner_bp = Blueprint("planner", __name__)


@planner_bp.route("/tasks", methods=["GET"])
def list_tasks():
    """Returns all queued tasks and a simple DAG view."""
    queue_data = task_queue.global_queue.dump()
    flat_list = []
    count = 0

    for level in ["high", "normal", "low"]:
        for task in queue_data[level]:
            count += 1
            flat_list.append({
                "name": task["type"],
                "state": "queued",
                "priority": level,
                "meta": task.get("meta", {}),
            })

    logger.info(f"[PLANNER_API] Found {count} tasks in queue.")
    log_event("planner_api", "task_list_fetch", {"count": count}, status="ok")

    # Optional graph structure (for frontend)
    G = nx.DiGraph()
    for idx, t in enumerate(flat_list):
        G.add_node(idx, label=t["name"])
        if idx > 0:
            G.add_edge(idx - 1, idx)

    return jsonify({"tasks": flat_list, "timestamp": datetime.utcnow().isoformat()})


@planner_bp.route("/api/mutation/ping", methods=["POST"])
def mutation_notify():
    """Receives ping from mutation daemon."""
    message = request.json.get("message", "No message provided")
    logger.debug(f"[PLANNER_API] Mutation ping: {message}")
    log_event("planner_api", "mutation_ping", {"message": message}, status="pong")

    return jsonify({
        "status": "received",
        "timestamp": datetime.utcnow().isoformat(),
        "log": f"Mutation daemon: {message}",
        "watermark": "source:GremlinGPT"
    })


@planner_bp.route("/api/tasks/priority", methods=["POST"])
def set_task_priority():
    """Adjusts task priority by ID."""
    data = request.get_json()
    task_id = data.get("id")
    new_priority = data.get("priority")

    if not task_id or not new_priority:
        logger.warning("[PLANNER_API] Priority update failed: missing ID or priority.")
        return jsonify({"error": "Missing 'id' or 'priority'"}), 400

    success = reprioritize(task_id, new_priority)
    log_event("planner_api", "priority_update", {
        "task_id": task_id,
        "new_priority": new_priority,
        "success": success,
    }, status="updated" if success

