# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import re
import nltk
from nltk.tokenize import word_tokenize
from backend.globals import logger

# Ensure necessary NLTK resources are available
nltk.download("punkt", quiet=True)

ENGINE_NAME = "semantic_score"


def clean_text(text: str) -> str:
    """
    Strips non-ASCII chars, compresses whitespace.
    """
    try:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\x00-\x7F]+", "", text)  # remove non-ASCII
        return text.strip()
    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Text cleaning failed: {e}")
        return text


def split_sentences(text: str):
    """
    Lightweight sentence segmentation.
    """
    try:
        return re.split(r"(?<=[.!?])\s+", text)
    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Sentence split failed: {e}")
        return [text]


def tokenize(text: str):
    """
    Tokenizes input text after cleaning.
    """
    try:
        cleaned = clean_text(text)
        tokens = word_tokenize(cleaned)
        logger.debug(f"[{ENGINE_NAME}] Tokenized {len(tokens)} tokens.")
        return tokens
    except Exception as e:
        logger.error(f"[{ENGINE_NAME}] Tokenization failed: {e}")
        return []
