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

# nlp_engine/pos_tagger.py

import nltk
from nltk import pos_tag, word_tokenize
from datetime import datetime
from loguru import logger

from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark

nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

WATERMARK = "source:GremlinGPT"
ORIGIN = "pos_tagger"


def get_pos_tags(text):
    try:
        tokens = word_tokenize(text)
        tags = pos_tag(tokens)

        # Create compact summary
        summary = f"POS tagging: {len(tokens)} tokens | Example: {tags[:3]}"
        vector = embed_text(summary)

        package_embedding(
            text=summary,
            vector=vector,
            meta={
                "origin": ORIGIN,
                "timestamp": datetime.utcnow().isoformat(),
                "token_count": len(tokens),
                "watermark": WATERMARK,
            },
        )
        inject_watermark(origin=ORIGIN)

        return tags

    except Exception as e:
        logger.error(f"[POS_TAGGER] Failed to tag input: {e}")
        return []
