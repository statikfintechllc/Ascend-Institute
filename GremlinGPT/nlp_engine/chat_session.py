# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: nlp_engine/chat_session.py :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# GremlinGPT v1.0.3 :: nlp_engine/chat_session.py
# Self-improving chat session manager for GremlinGPT.
# Handles dialog state, memory, feedback, and learning integration.


from datetime import datetime
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from memory.log_history import log_event
from nlp_engine.tokenizer import tokenize
from nlp_engine.semantic_score import reasoned_similarity
from agent_core.fsm import inject_task
from backend.api.chat_handler import chat as backend_chat


class ChatSession:


    def __init__(self, user_id=None):
        self.user_id = user_id or "anon"
        self.history = []  # List of (user, bot, meta)
        self.created = datetime.utcnow().isoformat()
        self.session_id = f"chat_{self.user_id}_{self.created}"
        self.memory_trace = []


    def process_input(self, user_input, context=None, feedback=None):
        # Tokenize and embed
        tokens = tokenize(user_input)
        vector = embed_text(user_input)
        package_embedding(
            text=user_input,
            vector=vector,
            meta={
                "origin": "chat_session",
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": self.user_id,
                "session_id": self.session_id,
                "token_count": len(tokens),
            },
        )
        inject_watermark(origin="chat_session")
        # Call backend chat handler for response
        bot_response = backend_chat(user_input)
        # Ensure output is always a string
        if isinstance(bot_response, str):
            pass
        elif isinstance(bot_response, dict):
            bot_response = str(bot_response.get("response", next(iter(bot_response.values()), "")))
        elif isinstance(bot_response, tuple):
            # Flask may return (dict, status)
            val = bot_response[0]
            if isinstance(val, dict):
                bot_response = str(val.get("response", next(iter(val.values()), "")))
            else:
                bot_response = str(val)
        else:
            bot_response = str(bot_response)
        # Optionally, reason about similarity to previous turns
        explanation = None
        if self.history:
            prev_user, prev_bot, _ = self.history[-1]
            sim = reasoned_similarity(prev_user, user_input)
            explanation = sim.get("explanation")
        # Log event
        log_event(
            "chat_session", "turn", {
                "user_input": user_input,
                "bot_response": bot_response,
                "tokens": tokens,
                "explanation": explanation,
                "feedback": feedback,
                "session_id": self.session_id,
            }
        )
        # Store in history
        self.history.append((user_input, bot_response, {"explanation": explanation, "feedback": feedback}))
        # Optionally inject feedback for learning
        if feedback:
            inject_task({"type": "feedback", "input": user_input, "feedback": feedback})
        return {
            "response": bot_response,
            "explanation": explanation,
            "tokens": tokens,
            "session_id": self.session_id,
        }


    def get_history(self):
        return self.history

# For API/CLI usage
__all__ = ["ChatSession"]
