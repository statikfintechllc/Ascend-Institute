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

# nlp_engine/semantic_score.py

import re
import nltk
from nltk.tokenize import word_tokenize
from backend.globals import logger

# Ensure tokenizer models are present
nltk.download("punkt", quiet=True)


def clean_text(text):
    """
    Normalize input by removing excess whitespace and illegal chars.
    """
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # Remove non-ASCII
    return text.strip()


def split_sentences(text):
    """
    Lightweight sentence segmentation for context-aware parsing.
    """
    return re.split(r"(?<=[.!?])\s+", text)


def tokenize(text):
    try:
        cleaned = clean_text(text)
        tokens = word_tokenize(cleaned)
        logger.debug(f"[TOKENIZER] Tokenized {len(tokens)} tokens.")
        return tokens
    except Exception as e:
        logger.error(f"[TOKENIZER] Failed to tokenize: {e}")
        return []
