#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: FSM Core & Module Integrity Directive

import numpy as np
from datetime import datetime
from memory.vector_store.embedder import package_embedding, embed_text
from memory.log_history import log_event
from self_training.feedback_loop import inject_feedback

WATERMARK = "source:GremlinGPT"
MODULE = "mini_attention"

class MiniMultiHeadAttention:
    """
    Production-grade, traceable, multi-head self-attention module, fully integrated with
    GremlinGPT system memory, feedback, and event logging.
    """

    def __init__(self, embed_dim, num_heads=4, scale=True, seed=None):
        assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.scale = scale

        # Allow deterministic initialization for traceability/testing
        if seed is not None:
            np.random.seed(seed)

        # Initialize projection weights (Kaiming-like, small variance)
        self.W_q = np.random.randn(num_heads, embed_dim, self.head_dim) * (2.0 / np.sqrt(embed_dim))
        self.W_k = np.random.randn(num_heads, embed_dim, self.head_dim) * (2.0 / np.sqrt(embed_dim))
        self.W_v = np.random.randn(num_heads, embed_dim, self.head_dim) * (2.0 / np.sqrt(embed_dim))
        self.W_out = np.random.randn(num_heads * self.head_dim, embed_dim) * (2.0 / np.sqrt(embed_dim))

    def _softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)

    def _apply_mask(self, scores, mask=None):
        if mask is not None:
            # Set masked positions to a large negative value for softmax
            scores = np.where(mask, scores, -1e9)
        return scores

    def _combine_heads(self, heads):
        # heads: (num_heads, seq_len, head_dim) -> (seq_len, num_heads * head_dim)
        return heads.transpose(1, 0, 2).reshape(heads.shape[1], -1)

    def forward(self, X, mask=None):
        """
        Args:
            X: (seq_len, embed_dim)
            mask: (seq_len, seq_len) boolean or None
        Returns:
            output: (seq_len, embed_dim)
            weights: (num_heads, seq_len, seq_len)
        """
        seq_len = X.shape[0]
        head_outputs = []
        all_weights = []

        for h in range(self.num_heads):
            Q = X @ self.W_q[h]  # (seq_len, head_dim)
            K = X @ self.W_k[h]  # (seq_len, head_dim)
            V = X @ self.W_v[h]  # (seq_len, head_dim)

            scores = Q @ K.T  # (seq_len, seq_len)
            if self.scale:
                scores = scores / np.sqrt(self.head_dim)

            scores = self._apply_mask(scores, mask)
            weights = self._softmax(scores)
            output = weights @ V  # (seq_len, head_dim)

            head_outputs.append(output)
            all_weights.append(weights)

        # Stack heads: (num_heads, seq_len, head_dim)
        head_outputs = np.stack(head_outputs, axis=0)
        all_weights = np.stack(all_weights, axis=0)

        combined = self._combine_heads(head_outputs)  # (seq_len, embed_dim)
        final_output = combined @ self.W_out  # (seq_len, embed_dim)

        self._log_attention_event(X, final_output, all_weights, mask)

        return final_output, all_weights

    def _log_attention_event(self, input_tensor, output_tensor, weights, mask):
        timestamp = datetime.utcnow().isoformat()
        info = {
            "origin": MODULE,
            "event": "forward_pass",
            "watermark": WATERMARK,
            "timestamp": timestamp,
            "shape_input": input_tensor.shape,
            "shape_output": output_tensor.shape,
            "num_heads": self.num_heads,
            "mask_applied": mask is not None,
        }

        # Log to system memory and logs
        log_event(MODULE, "attention_forward", info)
        summary = (
            f"MiniAttention: {self.num_heads} heads | "
            f"in={input_tensor.shape} out={output_tensor.shape} mask={mask is not None}"
        )
        vector = embed_text(summary)
        package_embedding(text=summary, vector=vector, meta=info)

        # Training signal hint
        inject_feedback()

    def repair_weights(self):
        """
        Reload/reinitialize weights in case of detection of corruption or failed shapes.
        """
        self.W_q = np.random.randn(self.num_heads, self.embed_dim, self.head_dim) * (2.0 / np.sqrt(self.embed_dim))
        self.W_k = np.random.randn(self.num_heads, self.embed_dim, self.head_dim) * (2.0 / np.sqrt(self.embed_dim))
        self.W_v = np.random.randn(self.num_heads, self.embed_dim, self.head_dim) * (2.0 / np.sqrt(self.embed_dim))
        self.W_out = np.random.randn(self.num_heads * self.head_dim, self.embed_dim) * (2.0 / np.sqrt(self.embed_dim))
        log_event(MODULE, "weights_repair", {
            "origin": MODULE,
            "timestamp": datetime.utcnow().isoformat(),
            "event": "repair_weights"
        })


# === Example Run ===
if __name__ == "__main__":
    np.random.seed(42)
    dummy_input = np.random.rand(8, 64)  # 8 tokens, 64-dimensional embeddings

    attention = MiniMultiHeadAttention(embed_dim=64, num_heads=4, scale=True, seed=42)

    # Example: causal mask (lower triangle: allow attending to current and previous tokens)
    causal_mask = np.tril(np.ones((8, 8))).astype(bool)

    out, attn_weights = attention.forward(dummy_input, mask=causal_mask)

    print(f"Output shape: {out.shape}")
    print(f"Attention shape: {attn_weights.shape}")

    # Test repair_weights
    attention.repair_weights()
    print("Weights repaired and reinitialized.")
