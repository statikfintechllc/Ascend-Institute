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

# backend/api/memory_api.py

from flask import jsonify
from memory.vector_store.embedder import get_all_embeddings
from backend.globals import MEM
from loguru import logger


def graph():
    try:
        limit = MEM["search"].get("default_top_k", 10)
        records = get_all_embeddings(limit=limit)

        response = {
            "count": len(records),
            "results": records,
            "meta": {
                "limit": limit,
                "source": "vector_store",
                "embedding_dim": MEM["embedding_dim"],
                "similarity_threshold": MEM["search"].get("similarity_threshold", 0.75),
            },
        }

        logger.info(f"[MEMORY_API] Returning {len(records)} embeddings.")
        return jsonify(response)

    except Exception as e:
        logger.error(f"[MEMORY_API] Failed to generate graph data: {e}")
        return jsonify({"error": "Failed to load memory graph", "details": str(e)}), 500
