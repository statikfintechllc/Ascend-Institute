# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# # GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion. v5 :: Module Integrity Directive

from flask import request, jsonify
from backend.interface import commands
from nlp_engine.tokenizer import tokenize
from nlp_engine.transformer_core import encode_text
from agent_core.task_queue import enqueue_task
from memory.vector_store.embedder import package_embedding
from memory.log_history import log_event
from loguru import logger
from datetime import datetime


def chat(user_input=None):
    if user_input is None:
        data = request.get_json()
        user_input = data.get("message", "").strip()
    else:
        user_input = user_input.strip()

    if not user_input:
        logger.warning("[CHAT] Empty input received.")
        return jsonify({"error": "Empty input"}), 400

    tokens = tokenize(user_input)
    vector = encode_text(user_input)

    task = commands.parse_command(user_input)
    result = commands.execute_command(task)

    package_embedding(
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

    return jsonify(
        {
            "response": f"Command interpreted as: {task['type']}",
            "tokens": tokens,
            "result": result,
        }
    )
