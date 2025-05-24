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

# nlp_engine/diff_engine.py

from difflib import unified_diff
from nlp_engine.semantic_score import semantic_similarity
from nlp_engine.transformer_core import encode_text
import numpy as np
from typing import Dict, List


def diff_texts(old: str, new: str, debug: bool = False) -> Dict:
    """
    Computes diff and semantic metrics between two strings.
    """
    if not old and not new:
        return {"diff_lines": [], "semantic_score": 1.0, "embedding_delta": 0.0}

    lines = list(
        unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile="before",
            tofile="after",
            lineterm="",
        )
    )

    sem_score = semantic_similarity(old, new)
    try:
        delta = float(np.linalg.norm(encode_text(old) - encode_text(new)))
    except Exception as e:
        delta = 0.0
        if debug:
            print(f"[DIFF_ENGINE] Embedding delta failed: {e}")

    return {
        "diff_lines": lines,
        "semantic_score": sem_score,
        "embedding_delta": delta,
    }


def diff_files(file_a: str, file_b: str) -> Dict:
    """
    Computes structured diff and semantic analysis between two file paths.
    """
    try:
        with open(file_a, "r", encoding="utf-8") as f1, open(
            file_b, "r", encoding="utf-8"
        ) as f2:
            return diff_texts(f1.read(), f2.read())
    except Exception as e:
        return {
            "diff_lines": [f"# ERROR: Could not diff files: {e}"],
            "semantic_score": 0.0,
            "embedding_delta": 0.0,
        }
