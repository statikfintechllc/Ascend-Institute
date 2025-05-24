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

# backend/router.py

from backend.api import chat_handler, memory_api, scraping_api, planner


def register_routes(app):
    app.add_url_rule("/api/chat", view_func=chat_handler.chat, methods=["POST"])
    app.add_url_rule("/api/memory/graph", view_func=memory_api.graph, methods=["GET"])
    app.add_url_rule("/api/scrape", view_func=scraping_api.scrape_url, methods=["POST"])
    app.add_url_rule("/api/agent/tasks", view_func=planner.list_tasks, methods=["GET"])
    app.add_url_rule(
        "/api/trading/signals", view_func=planner.get_signals, methods=["GET"]
    )
    app.add_url_rule(
        "/api/tasks/priority", view_func=planner.set_task_priority, methods=["POST"]
    )  # NEW
