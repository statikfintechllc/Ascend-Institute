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

# backend/api/chat_handler.py

from flask import request, jsonify
from backend.interface import commands
from nlp_engine.tokenizer import tokenize
from nlp_engine.transformer_core import encode
from agent_core.task_queue import enqueue_task
from memory.vector_store.embedder import package_embedding
from loguru import logger


def chat():
    data = request.get_json()
    user_input = data.get("text", "")

    tokens = tokenize(user_input)
    vector = encode(user_input)

    task = commands.parse_command(user_input)
    result = commands.execute_command(task)

    package_embedding(
        text=user_input,
        vector=vector,
        meta={"from": "chat", "type": task["type"], "user_intent": user_input},
    )

    # Use enqueue_task directly if unrecognized for fallback logging
    if task["type"] == "unknown":
        logger.warning(f"[CHAT] Unrecognized input: {user_input}")
        enqueue_task({"type": "nlp", "text": user_input})

    return jsonify(
        {
            "response": f"Command interpreted as: {task['type']}",
            "tokens": tokens,
            "result": result,
        }
    )
