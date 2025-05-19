from difflib import unified_diff
from nlp_engine.semantic_score import semantic_similarity
from nlp_engine.transformer_core import encode_text
import numpy as np


def diff_texts(old: str, new: str):
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
    delta = float(np.linalg.norm(encode_text(old) - encode_text(new)))
    return {
        "diff_lines": lines,
        "semantic_score": sem_score,
        "embedding_delta": delta,
    }


def diff_files(file_a: str, file_b: str):
    with open(file_a) as f1, open(file_b) as f2:
        return diff_texts(f1.read(), f2.read())
