# !/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import sys
import traceback

try:
    from tokenizer import Tokenizer  # Your actual tokenizer
    from transformer_core import TransformerCore  # Your real core model
except ImportError as e:
    print(f"[NLP_CHECK] ImportError: {e}", file=sys.stderr)
    sys.exit(1)

def nlp_internal_check():
    try:
        # Simple English test phrase
        test_phrase = "This is a test of the GremlinGPT NLP engine."
        # Instantiate your tokenizer (adjust class name if needed)
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(test_phrase)
        assert isinstance(tokens, list) and len(tokens) > 0, "Tokenization failed"

        # Instantiate your transformer (adjust class name if needed)
        model = TransformerCore()
        result = model.forward(tokens)
        assert result is not None, "Transformer forward failed"

        print("NLP Internal Check: ✅")
    except Exception as ex:
        print("[NLP_CHECK] Error:", ex, file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    nlp_internal_check()
