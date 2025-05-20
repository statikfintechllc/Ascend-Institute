from flask import Blueprint, request, jsonify
from agent_core.task_queue import reprioritize
from agent_core import task_queue
import networkx as nx
import time
from loguru import logger

planner_bp = Blueprint("planner", __name__)


@planner_bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = task_queue.global_queue.dump()
    logger.info(f"[PLANNER_API] Returning {len(tasks)} queued tasks.")

    # Build a DAG for visualization (e.g., frontend graph support)
    G = nx.DiGraph()
    for idx, t in enumerate(tasks):
        G.add_node(idx, label=t["type"])
        if idx > 0:
            G.add_edge(idx - 1, idx)

    serialized = [
        {
            "name": t["type"],
            "state": "queued",
            "subtasks": [],
            "meta": t.get("meta", {}),
        }
        for t in tasks
    ]

    return jsonify({"tasks": serialized})


@planner_bp.route("/api/mutation/ping", methods=["POST"])
def mutation_notify():
    message = request.json.get("message", "No message provided")
    logger.debug(f"[PLANNER_API] Mutation daemon ping received: {message}")
    return jsonify(
        {
            "status": "received",
            "timestamp": time.time(),
            "log": f"Mutation daemon: {message}",
        }
    )

@planner_bp.route("/api/tasks/priority", methods=["POST"])
def set_task_priority():
    data = request.get_json()
    task_id = data.get("id")
    new_priority = data.get("priority")

    if not task_id or not new_priority:
        return jsonify({"error": "Missing 'id' or 'priority'"}), 400

    success = reprioritize(task_id, new_priority)
    return jsonify({
        "updated": success,
        "task_id": task_id,
        "new_priority": new_priority
    })
