# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: nlp_engine/tokenizer.py :: Module Integrity Directive
# Self-improving tokenizer for GremlinGPT.
# This script is a component of the GremlinGPT system, under Alpha expansion.

# Refactored to use centralized imports from backend.globals
from backend.globals import (
    re, transformers, CFG, logger, datetime, nltk, 
    embed_text, package_embedding, inject_watermark
)

# Local project imports that can't be centralized
try:
    from utils.nltk_setup import setup_nltk_data
    NLTK_DATA_DIR = setup_nltk_data()
except ImportError:
    NLTK_DATA_DIR = None

# Try to get AutoTokenizer from transformers if available
try:
    if transformers:
        from transformers import AutoTokenizer
    else:
        AutoTokenizer = None
except ImportError:
    AutoTokenizer = None

WATERMARK = "source:GremlinGPT"
ORIGIN = "tokenizer"
MODEL = CFG["nlp"].get("tokenizer_model", "bert-base-uncased")


try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    logger.success(f"[TOKENIZER] Loaded: {MODEL}")
except Exception as e:
    logger.warning(f"[TOKENIZER] Failed to load {MODEL}. Falling back to nltk: {e}")
    tokenizer = None


def clean_text(text):
    """
    Normalizes whitespace and removes non-ASCII characters.
    """
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    return text.strip()


def tokenize(text):
    """
    Tokenizes input using HuggingFace tokenizer or NLTK fallback.
    Traces vector metadata for training and memory indexing.
    """
    text = clean_text(text)

    if tokenizer:
        tokens = tokenizer.tokenize(text)
    else:
        from nltk.tokenize import word_tokenize

        tokens = word_tokenize(text)

    logger.debug(f"[TOKENIZER] Token count: {len(tokens)}")

    # Memory trace
    summary = (
        f"Tokenized input: {len(tokens)} tokens from {MODEL if tokenizer else 'NLTK'}"
    )
    vector = embed_text(summary)

    package_embedding(
        text=summary,
        vector=vector,
        meta={
            "origin": ORIGIN,
            "timestamp": datetime.utcnow().isoformat(),
            "token_count": len(tokens),
            "fallback": tokenizer is None,
            "watermark": WATERMARK,
        },
    )

    inject_watermark(origin=ORIGIN)
    return tokens
