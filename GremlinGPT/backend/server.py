# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

from flask import Flask
from flask_socketio import SocketIO
from backend.router import register_routes
from loguru import logger
from backend.globals import CFG
import eventlet
import os

eventlet.monkey_patch()

# App and SocketIO Initialization
app = Flask(__name__)
app.config["SECRET_KEY"] = CFG.get("backend", {}).get("secret_key", "gremlin_secret")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# Route Registration
register_routes(app)

# Log Setup
LOG_DIR = CFG.get("paths", {}).get("log_dir", "run/logs")
os.makedirs(LOG_DIR, exist_ok=True)
logger.add(f"{LOG_DIR}/runtime.log", rotation="1 MB")


# Base API Checkpoint
@app.route("/")
def index():
    return {"message": "GremlinGPT Backend Running."}


# Boot Entry
if __name__ == "__main__":
    host = CFG.get("backend", {}).get("host", "0.0.0.0")
    port = CFG.get("backend", {}).get("port", 5050)

    logger.info(f"[BACKEND] Starting GremlinGPT backend on {host}:{port}")
    socketio.run(app, host=host, port=port)
