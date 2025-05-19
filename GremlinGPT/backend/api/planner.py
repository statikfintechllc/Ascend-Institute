from flask import Blueprint, request, jsonify
from agent_core import task_queue
import networkx as nx
import time

planner_bp = Blueprint("planner", __name__)


@planner_bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = task_queue.global_queue.dump()
    G = nx.DiGraph()
    for idx, t in enumerate(tasks):
        G.add_node(idx, label=t["type"])
        if idx > 0:
            G.add_edge(idx - 1, idx)
    serialized = [
        {"name": t["type"], "state": "queued", "subtasks": []} for t in tasks
    ]
    return jsonify({"tasks": serialized})


@planner_bp.route("/api/mutation/ping", methods=["POST"])
def mutation_notify():
    message = request.json.get("message", "")
    return jsonify(
        {
            "status": "received",
            "timestamp": time.time(),
            "log": f"Mutation daemon: {message}",
        }
    )
