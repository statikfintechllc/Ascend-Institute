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

# nlp_engine/mini_attention.py

import numpy as np
from datetime import datetime
from memory.vector_store.embedder import package_embedding, embed_text
from memory.log_history import log_event
from self_training.feedback_loop import inject_feedback

WATERMARK = "source:GremlinGPT"
MODULE = "mini_attention"


class MiniMultiHeadAttention:
    def __init__(self, embed_dim, num_heads=4, scale=True):
        assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = scale

        # Initialize projection weights
        self.W_q = np.random.randn(num_heads, embed_dim, self.head_dim) * 0.02
        self.W_k = np.random.randn(num_heads, embed_dim, self.head_dim) * 0.02
        self.W_v = np.random.randn(num_heads, embed_dim, self.head_dim) * 0.02
        self.W_out = np.random.randn(num_heads * self.head_dim, embed_dim) * 0.02

    def _softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)

    def _apply_mask(self, scores, mask=None):
        if mask is not None:
            scores = np.where(mask, scores, -1e9)
        return scores

    def _combine_heads(self, heads):
        return heads.transpose(1, 0, 2).reshape(heads.shape[1], -1)

    def forward(self, X, mask=None):
        """
        Args:
            X: (seq_len, embed_dim)
            mask: (seq_len, seq_len) boolean
        Returns:
            output: (seq_len, embed_dim)
            weights: (num_heads, seq_len, seq_len)
        """
      # seq_len = X.shape[0] # Unused currently
        head_outputs = []
        all_weights = []

        for h in range(self.num_heads):
            Q = X @ self.W_q[h]
            K = X @ self.W_k[h]
            V = X @ self.W_v[h]

            scores = Q @ K.T
            if self.scale:
                scores = scores / np.sqrt(self.head_dim)

            scores = self._apply_mask(scores, mask)
            weights = self._softmax(scores)
            output = weights @ V

            head_outputs.append(output)
            all_weights.append(weights)

        combined = self._combine_heads(np.array(head_outputs))
        final_output = combined @ self.W_out

        self._log_attention_event(X, final_output, all_weights)

        return final_output, np.array(all_weights)

    def _log_attention_event(self, input_tensor, output_tensor, weights):
        timestamp = datetime.utcnow().isoformat()
        info = {
            "origin": MODULE,
            "event": "forward_pass",
            "watermark": WATERMARK,
            "timestamp": timestamp,
            "shape_input": input_tensor.shape,
            "shape_output": output_tensor.shape,
            "num_heads": self.num_heads,
        }

        # Log to system memory and logs
        log_event(MODULE, "attention_forward", info)
        summary = (
    f"Attention pass: {self.num_heads} heads | "
    f"in={input_tensor.shape} out={output_tensor.shape}"
)
        vector = embed_text(summary)
        package_embedding(text=summary, vector=vector, meta=info)

        # Training signal hint
        inject_feedback()


# === Example Run ===
if __name__ == "__main__":
    np.random.seed(42)
    dummy_input = np.random.rand(8, 64)  # 8 tokens, 64-dimensional embeddings

    attention = MiniMultiHeadAttention(embed_dim=64, num_heads=4)

    # Example: causal mask
    causal_mask = np.tril(np.ones((8, 8))).astype(bool)

    out, attn_weights = attention.forward(dummy_input, mask=causal_mask)

    print(f"Output shape: {out.shape}")
    print(f"Attention shape: {attn_weights.shape}")
