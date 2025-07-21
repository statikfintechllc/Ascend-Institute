#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: backend/api/api_endpoints.py :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

# Flask imports - will be imported via globals when available
try:
    import flask
    from flask import Blueprint
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    # Create mock classes for non-Flask environments
    class Blueprint:
        def __init__(self, name, import_name):
            self.name = name
            self.import_name = import_name
            self.deferred_functions = []
        def route(self, rule, **options):
            def decorator(f):
                self.deferred_functions.append((rule, f, options))
                return f
            return decorator
import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import everything from backend.globals for centralized dependency management
from backend.globals import *

# Create API blueprint
api_blueprint = Blueprint('api', __name__)

# Session storage for chat functionality
_sessions = {}

# === CHAT ENDPOINTS ===
@api_blueprint.route("/api/chat", methods=["POST"])
def api_chat():
    """Chat endpoint using centralized imports"""
    data = flask.request.get_json()
    user_input = data.get("message", "")
    session_id = data.get("session_id")
    user_id = data.get("user_id", "api_user")
    feedback = data.get("feedback")
    
    # Use ChatSession from centralized imports
    if session_id and session_id in _sessions:
        session = _sessions[session_id]
    else:
        if ChatSession:
            session = ChatSession(user_id=user_id)
            _sessions[session.session_id] = session
            session_id = session.session_id
        else:
            return flask.jsonify({"error": "ChatSession not available"}), 500
    
    try:
        result = session.process_input(user_input, feedback=feedback)
        result["session_id"] = session_id
        return flask.jsonify(result)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === FSM OPERATIONS ===
@api_blueprint.route("/api/fsm/status", methods=["GET"])
def api_fsm_status():
    """Get FSM status using centralized imports"""
    try:
        if get_fsm_status:
            status = get_fsm_status()
            return flask.jsonify({"fsm_status": status})
        else:
            return flask.jsonify({"fsm_status": "not_available"})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/fsm/tick", methods=["POST"])
def api_fsm_tick():
    """Trigger FSM tick using centralized imports"""
    try:
        if fsm_loop:
            result = fsm_loop()
            return flask.jsonify({"tick_result": result})
        else:
            return flask.jsonify({"error": "FSM not available"}), 500
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === TASK QUEUE & PLANNER ===
@api_blueprint.route("/api/agent/tasks", methods=["GET", "POST"])
def api_agent_tasks():
    """Task management using centralized imports"""
    try:
        if flask.request.method == "POST":
            task_data = flask.request.get_json()
            task_desc = task_data.get("task")
            if enqueue_task:
                result = enqueue_task(task_desc)
                return flask.jsonify({"enqueued": result})
            else:
                return flask.jsonify({"error": "Task queue not available"}), 500
        
        # GET request
        if get_all_tasks:
            tasks = get_all_tasks()
            return flask.jsonify({"tasks": tasks})
        else:
            return flask.jsonify({"tasks": []})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === MEMORY GRAPH ===
@api_blueprint.route("/api/memory/graph", methods=["GET"])
def api_memory_graph():
    """Memory graph endpoint using centralized imports"""
    try:
        # Use graph function from centralized imports if available
        if graph:
            result = graph()
            return flask.jsonify(result)
        else:
            return flask.jsonify({"nodes": [], "edges": [], "message": "Memory graph not available"})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === TRADING SIGNALS ===
@api_blueprint.route("/api/trading/signals", methods=["GET"])
def api_trading_signals():
    """Trading signals using centralized imports"""
    try:
        if generate_signals:
            signals = generate_signals()
            return flask.jsonify({"signals": signals})
        else:
            return flask.jsonify({"signals": [], "message": "Signal generator not available"})
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === SCRAPING ===
@api_blueprint.route("/api/scrape", methods=["POST"])
def api_scrape():
    """Scraping endpoint using centralized imports"""
    data = flask.request.get_json()
    url = data.get("url")
    if not url:
        return flask.jsonify({"error": "Missing 'url'"}), 400
    
    try:
        # Use scraping functions from centralized imports
        if route_scraping:
            result = route_scraping(url)
            return flask.jsonify({"scrape_result": result})
        else:
            return flask.jsonify({"error": "Scraper not available"}), 500
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === STATE MANAGEMENT ===
@api_blueprint.route("/api/state/save", methods=["POST"])
def api_save_state():
    """Save state using centralized imports"""
    try:
        if save_state:
            result = save_state({})
            return flask.jsonify({"save_result": result})
        else:
            return flask.jsonify({"error": "State manager not available"}), 500
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/state/load", methods=["GET"])
def api_load_state():
    """Load state using centralized imports"""
    try:
        if load_state:
            result = load_state()
            return flask.jsonify({"load_result": result})
        else:
            return flask.jsonify({"error": "State manager not available"}), 500
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === SYSTEM CONFIGURATION ===
@api_blueprint.route("/api/system/config", methods=["GET"])
def api_system_config():
    """System configuration using centralized imports"""
    try:
        # Use CFG from centralized imports
        return flask.jsonify(CFG)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_blueprint.route("/api/system/backend_select", methods=["POST"])
def api_system_backend_select():
    """Backend selection using centralized imports"""
    data = flask.request.get_json()
    backend = data.get("backend", "")
    if backend not in ["faiss", "chromadb"]:
        return flask.jsonify({"error": "Invalid backend. Use 'faiss' or 'chromadb'"}), 400
    
    try:
        if set_dashboard_backend:
            result = set_dashboard_backend(backend)
            return flask.jsonify({"success": result})
        else:
            return flask.jsonify({"error": "Backend selection not available"}), 500
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === UTILITY ENDPOINTS ===
@api_blueprint.route("/api/tools/text/summarize", methods=["POST"])
def api_tools_text_summarize():
    """Text summarization using centralized imports"""
    data = flask.request.get_json()
    text = data.get("text")
    if not text:
        return flask.jsonify({"error": "Missing 'text'"}), 400
    
    try:
        if summarize_text:
            summary = summarize_text(text)
            return flask.jsonify({"summary": summary})
        else:
            return flask.jsonify({"error": "Summarizer not available"}), 500
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


# === HEALTH CHECK ===
@api_blueprint.route("/api/health", methods=["GET"])
def api_health():
    """Health check endpoint"""
    return flask.jsonify({
        "status": "healthy",
        "version": "1.0.3",
        "imports_available": {
            "chat_session": ChatSession is not None,
            "fsm": fsm_loop is not None,
            "task_queue": enqueue_task is not None,
            "memory": graph is not None,
            "trading": generate_signals is not None,
            "scraping": route_scraping is not None,
            "state": save_state is not None,
        }
    })


# Export the blueprint for registration
__all__ = ['api_blueprint']