# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: utils/nltk_setup.py :: Module Integrity Directive
# Self-improving NLTK setup for GremlinGPT.
# This script is a component of the GremlinGPT system, under Alpha expansion.

import os
import nltk

def setup_nltk_data():
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "nltk_data")
    )
    fallback_dirs = ["/usr/local/share/nltk_data", base_dir]

    for path in fallback_dirs:
        nltk.data.path.append(path)

    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", download_dir=base_dir)

    return base_dir
