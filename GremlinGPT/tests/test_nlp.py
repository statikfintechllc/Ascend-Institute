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

# tests/test_nlp.py

from nlp_engine.tokenizer import tokenize
from nlp_engine.pos_tagger import get_pos_tags
from nlp_engine.transformer_core import encode
from nlp_engine.diff_engine import vector_diff
import numpy as np


def test_tokenizer():
    tokens = tokenize("Run GremlinGPT on boot.")
    assert "Run" in tokens


def test_pos():
    tags = get_pos_tags("Run the agent task.")
    assert any(tag[1] for tag in tags)


def test_encode_and_diff():
    vec1 = encode("Test vector one.")
    vec2 = encode("Test vector two.")
    assert isinstance(vec1, np.ndarray)
    assert isinstance(vec2, np.ndarray)
    assert vec1.shape == vec2.shape

    score = vector_diff("Test vector one.", "Test vector two.")
    assert 0 <= score <= 1
