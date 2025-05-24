# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

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

# backend/server.py

from flask import Flask
from flask_socketio import SocketIO
from backend.router import register_routes
from loguru import logger
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config["SECRET_KEY"] = "gremlin_secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Register all REST endpoints
register_routes(app)

logger.add("run/logs/runtime.log", rotation="1 MB")


@app.route("/")
def index():
    return {"message": "GremlinGPT Backend Running."}


if __name__ == "__main__":
    logger.info("[BACKEND] Starting GremlinGPT backend server.")
    socketio.run(app, host="0.0.0.0", port=5050)
