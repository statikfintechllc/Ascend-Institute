import os
import uuid
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.globals import MEM
from loguru import logger
import json

model = SentenceTransformer(MEM['embedding']['model'])

MEMORY_DIR = MEM['storage']['vector_store_path']
INDEX_DB = MEM['storage']['metadata_db']
os.makedirs(MEMORY_DIR, exist_ok=True)

memory_vectors = {}

def embed_text(text):
    vec = model.encode(text, convert_to_numpy=True)
    norm = np.linalg.norm(vec)
    logger.debug(f"[EMBEDDER] Embedding norm: {norm:.4f}")
    return vec

def package_embedding(text, vector, meta):
    emb_id = str(uuid.uuid4())
    embedding = {
        "id": emb_id,
        "text": text,
        "embedding": vector.tolist(),
        "meta": meta,
        "tags": {
            "source": "bootstrap-prebuilt",
            "model": "MiniLM",
            "replaceable": True
        }
    }
    memory_vectors[emb_id] = embedding
    _write_to_disk(embedding)
    logger.info(f"[EMBEDDER] Stored embedding: {emb_id}")
    return embedding

def get_all_embeddings(limit=10):
    return list(memory_vectors.values())[:limit]

def _write_to_disk(embedding):
    index_path = os.path.join(MEM['storage']['local_index_path'], "documents")
    os.makedirs(index_path, exist_ok=True)
    path = os.path.join(index_path, f"{embedding['id']}.json")
    with open(path, "w") as f:
        json.dump(embedding, f, indent=2)
