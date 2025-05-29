# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from flask import Blueprint, request, jsonify
from agent_core.fsm import (
    fsm_loop,
    get_fsm_status,
    step_fsm,
    reset_fsm,
    inject_task as fsm_inject_task,
)
from agent_core.task_queue import TaskQueue
from backend.api.chat_handler import chat
from backend.api.memory_api import graph as memory_graph
from backend.api.planner import list_tasks, mutation_notify, set_task_priority
from backend.api.scraping_api import scrape_url
from memory.vector_store.embedder import get_memory_graph
from trading_core.signal_generator import generate_signals

api_blueprint = Blueprint("api", __name__)

# --- Core Chat / NLP ---
@api_blueprint.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = chat(user_input)
    return jsonify({"response": response})


# --- FSM Operations ---
@api_blueprint.route("/api/fsm/status", methods=["GET"])
def api_fsm_status():
    status = get_fsm_status()
    return jsonify({"fsm_status": status})


@api_blueprint.route("/api/fsm/tick", methods=["POST"])
def api_fsm_tick():
    result = fsm_loop(tick_once=True)
    return jsonify({"tick_result": result})


@api_blueprint.route("/api/fsm/step", methods=["POST"])
def api_fsm_step():
    result = step_fsm()
    return jsonify({"step_result": result})


@api_blueprint.route("/api/fsm/reset", methods=["POST"])
def api_fsm_reset():
    result = reset_fsm()
    return jsonify({"reset_result": result})


@api_blueprint.route("/api/fsm/inject", methods=["POST"])
def api_fsm_inject():
    data = request.get_json()
    task = data.get("task")
    result = fsm_inject_task(task)
    return jsonify({"inject_result": result})


# --- Task Queue & Planner ---
@api_blueprint.route("/api/agent/tasks", methods=["GET", "POST"])
def api_agent_tasks():
    tq = TaskQueue()
    if request.method == "POST":
        task_data = request.get_json()
        task_desc = task_data.get("task")
        result = tq.enqueue(task_desc)
        return jsonify({"enqueued": result})
    tasks = tq.get_all_tasks()
    return jsonify({"tasks": tasks})


@api_blueprint.route("/api/agent/planner", methods=["GET"])
def api_agent_planner():
    tasks = list_tasks()
    return jsonify({"planner_tasks": tasks})


@api_blueprint.route("/api/agent/planner/mutate", methods=["POST"])
def api_planner_mutate():
    data = request.get_json()
    notify = mutation_notify(data)
    return jsonify({"mutate_notify": notify})


@api_blueprint.route("/api/agent/planner/priority", methods=["POST"])
def api_planner_priority():
    data = request.get_json()
    task_id = data.get("task_id")
    priority = data.get("priority")
    result = set_task_priority(task_id, priority)
    return jsonify({"set_priority": result})


# --- Memory Graph ---
@api_blueprint.route("/api/memory/graph", methods=["GET"])
def api_memory_graph():
    graph = get_memory_graph()
    return jsonify(graph)


# --- State Manager ---
@api_blueprint.route("/api/state/save", methods=["POST"])
def api_save_state():
    from backend.state_manager import save_state

    result = save_state()
    return jsonify({"save_result": result})


@api_blueprint.route("/api/state/load", methods=["GET"])
def api_load_state():
    from backend.state_manager import load_state

    result = load_state()
    return jsonify({"load_result": result})


# --- Trading Signals ---
@api_blueprint.route("/api/trading/signals", methods=["GET"])
def api_trading_signals():
    signals = generate_signals()
    return jsonify({"signals": signals})


# --- Scraping / Web ---
@api_blueprint.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing 'url'"}), 400
    result = scrape_url(url)
    return jsonify({"scrape_result": result})


# --- Extend with more agent/tools as needed below ---
