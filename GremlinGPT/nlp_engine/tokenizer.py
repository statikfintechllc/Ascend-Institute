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

# nlp_engine/tokenizer.py

import re
from transformers import AutoTokenizer
from backend.globals import CFG, logger
import nltk

# Fallback for tokenizer if HuggingFace load fails
nltk.download("punkt", quiet=True)

# Configurable tokenizer
MODEL = CFG["nlp"].get("tokenizer_model", "bert-base-uncased")


try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    logger.success(f"[TOKENIZER] Loaded: {MODEL}")
except Exception as e:
    logger.warning(f"[TOKENIZER] Failed to load {MODEL}. Falling back to nltk: {e}")
    tokenizer = None


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    """
    Clean and normalize text input before tokenization.
    """
    return text.strip()


def tokenize(text):
    text = clean_text(text)
    if tokenizer:
        tokens = tokenizer.tokenize(text)
    else:
        from nltk.tokenize import word_tokenize

        tokens = word_tokenize(text)

    logger.debug(f"[TOKENIZER] Token count: {len(tokens)}")
    return tokens
