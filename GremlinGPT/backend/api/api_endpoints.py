# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: backend/api/api_endpoints.py :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import flask
from agent_core.fsm import (
    fsm_loop,
    get_fsm_status,
    step_fsm,
    reset_fsm,
    inject_task as fsm_inject_task,
)
# Importing necessary modules for the API
from agent_core.task_queue import TaskQueue
from backend.api.chat_handler import chat
from backend.api.memory_api import graph as memory_graph
from backend.api.planner import list_tasks, mutation_notify, set_task_priority
from backend.api.scraping_api import scrape_url
from memory.vector_store.embedder import get_memory_graph
from trading_core.signal_generator import generate_signals
from nlp_engine.chat_session import ChatSession

# Create Flask Blueprint for API
api_blueprint = flask.Blueprint("api", __name__)

# In-memory session store (for demo; use Redis or DB for production)
_sessions = {}


# --- Core Chat / NLP ---
@api_blueprint.route("/api/chat", methods=["POST"])
def api_chat():
    data = flask.request.get_json()
    user_input = data.get("message", "")
    response = chat(user_input)
    return flask.jsonify({"response": response})


@api_blueprint.route("/api/chat/session", methods=["POST"])
def api_chat_session():
    data = flask.request.get_json()
    user_input = data.get("message", "")
    session_id = data.get("session_id")
    user_id = data.get("user_id", "api_user")
    feedback = data.get("feedback")
    # Retrieve or create session
    if session_id and session_id in _sessions:
        session = _sessions[session_id]
    else:
        session = ChatSession(user_id=user_id)
        _sessions[session.session_id] = session
        session_id = session.session_id
    result = session.process_input(user_input, feedback=feedback)
    result["session_id"] = session_id
    return flask.jsonify(result)


# --- FSM Operations ---
@api_blueprint.route("/api/fsm/status", methods=["GET"])
def api_fsm_status():
    status = get_fsm_status()
    return flask.jsonify({"fsm_status": status})


@api_blueprint.route("/api/fsm/tick", methods=["POST"])
def api_fsm_tick():
    result = fsm_loop()  # Remove tick_once param
    return flask.jsonify({"tick_result": result})


@api_blueprint.route("/api/fsm/step", methods=["POST"])
def api_fsm_step():
    result = step_fsm()
    return flask.jsonify({"step_result": result})


@api_blueprint.route("/api/fsm/reset", methods=["POST"])
def api_fsm_reset():
    result = reset_fsm()
    return flask.jsonify({"reset_result": result})


@api_blueprint.route("/api/fsm/inject", methods=["POST"])
def api_fsm_inject():
    data = flask.request.get_json()
    task = data.get("task")
    result = fsm_inject_task(task)
    return flask.jsonify({"inject_result": result})


# --- Task Queue & Planner ---
@api_blueprint.route("/api/agent/tasks", methods=["GET", "POST"])
def api_agent_tasks():
    tq = TaskQueue()
    if flask.request.method == "POST":
        task_data = flask.request.get_json()
        task_desc = task_data.get("task")
        result = tq.enqueue_task(task_desc)
        return flask.jsonify({"enqueued": result})
    tasks = tq.get_all_tasks()
    return flask.jsonify({"tasks": tasks})


@api_blueprint.route("/api/agent/planner", methods=["GET"])
def api_agent_planner():
    tasks = list_tasks()
    return flask.jsonify({"planner_tasks": tasks})


@api_blueprint.route("/api/agent/planner/mutate", methods=["POST"])
def api_planner_mutate():
    return mutation_notify()

@api_blueprint.route("/api/agent/planner/priority", methods=["POST"])
def api_planner_priority():
    return set_task_priority()


# --- Memory Graph ---
@api_blueprint.route("/api/memory/graph", methods=["GET"])
def api_memory_graph():
    graph = get_memory_graph()
    return flask.jsonify(graph)


# --- State Manager ---
@api_blueprint.route("/api/state/save", methods=["POST"])
def api_save_state():
    from backend.state_manager import save_state

    # save_state likely needs a state argument; pass an empty dict as placeholder
    result = save_state({})
    return flask.jsonify({"save_result": result})


@api_blueprint.route("/api/state/load", methods=["GET"])
def api_load_state():
    from backend.state_manager import load_state

    result = load_state()
    return flask.jsonify({"load_result": result})


# --- Trading Signals ---
@api_blueprint.route("/api/trading/signals", methods=["GET"])
def api_trading_signals():
    signals = generate_signals()
    return flask.jsonify({"signals": signals})


# --- Scraping / Web ---
@api_blueprint.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = flask.request.get_json()
    url = data.get("url")
    if not url:
        return flask.jsonify({"error": "Missing 'url'"}), 400
    result = scrape_url(url)
    return flask.jsonify({"scrape_result": result})


# --- Extend with more agent/tools as needed below ---
