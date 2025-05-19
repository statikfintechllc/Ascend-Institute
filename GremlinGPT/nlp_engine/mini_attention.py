import numpy as np


def local_attention_score(embeddings):
    attention_weights = np.dot(embeddings, embeddings.T)
    norm = np.linalg.norm(attention_weights, axis=1)
    return norm.tolist()
