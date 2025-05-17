from sentence_transformers import util
import numpy as np

def cosine_similarity(a, b):
    return float(util.cos_sim(np.array(a), np.array(b))[0][0])

