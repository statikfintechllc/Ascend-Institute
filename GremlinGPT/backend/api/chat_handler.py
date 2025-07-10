# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# # GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion. v5 :: Module Integrity Directive

from flask import request, jsonify, has_request_context
from backend.interface import commands
from nlp_engine.tokenizer import tokenize
from nlp_engine.transformer_core import encode
from agent_core.task_queue import enqueue_task
from memory.vector_store import embedder
from memory.log_history import log_event
from loguru import logger
from datetime import datetime


def chat(user_input=None):
    if has_request_context():
        data = request.get_json()
        user_input = data.get("message", "").strip()
    elif user_input is not None:
        user_input = user_input.strip()
    else:
        logger.warning("[CHAT] No input provided to chat()")
        # Always return dict outside Flask for CLI
        return {"error": "No input provided"}, 400

    if not user_input:
        logger.warning("[CHAT] Empty input received.")
        resp = {"error": "Empty input"}
        return jsonify(resp), 400 if has_request_context() else (resp, 400)

    tokens = tokenize(user_input)
    vector = encode(user_input)
    task = commands.parse_command(user_input)
    result = commands.execute_command(task)

    embedder.package_embedding(
        text=user_input,
        vector=vector,
        meta={
            "origin": "chat_handler",
            "type": task.get("type", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_input,
            "watermark": "source:GremlinGPT",
        },
    )

    log_event("chat", "parsed", {"input": user_input, "task_type": task["type"]})

    if task["type"] == "unknown":
        logger.warning(
            f"[CHAT] Fallback NLP task for unrecognized command: {user_input}"
        )
        enqueue_task({"type": "nlp", "text": user_input})

    response = {
        "response": f"Command interpreted as: {task['type']}",
        "tokens": tokens,
        "result": result,
        "message": f"Command interpreted as: {task['type']}",
    }
    # Return Flask response if inside a request, else dict for CLI
    return jsonify(response) if has_request_context() else response
