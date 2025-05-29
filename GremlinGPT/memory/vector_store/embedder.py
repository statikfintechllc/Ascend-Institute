#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import os
import shutil
import uuid
import json
from datetime import datetime

import numpy as np
from sentence_transformers import SentenceTransformer
from backend.globals import MEM
from loguru import logger

# Load embedding model and paths from system config
model = SentenceTransformer(MEM["embedding"]["model"])
MEMORY_DIR = MEM["storage"]["vector_store_path"]
INDEX_DB = MEM["storage"]["metadata_db"]
LOCAL_INDEX_PATH = os.path.join(MEM["storage"]["local_index_path"], "documents")
os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(LOCAL_INDEX_PATH, exist_ok=True)

memory_vectors = {}

# --- Core Embedding Functions ---

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
            "source": meta.get("source", "system"),
            "model": MEM["embedding"]["model"],
            "created": datetime.utcnow().isoformat(),
            "replaceable": True,
        },
    }
    memory_vectors[emb_id] = embedding
    _write_to_disk(embedding)
    logger.info(f"[EMBEDDER] Stored embedding: {emb_id}")
    return embedding

def inject_watermark(origin="unknown"):
    text = f"Watermark from {origin} @ {datetime.utcnow().isoformat()}"
    vector = embed_text(text)
    meta = {"origin": origin, "timestamp": datetime.utcnow().isoformat()}
    return package_embedding(text, vector, meta)

def archive_plan(vector_path="data/nlp_training_sets/auto_generated.jsonl"):
    if not os.path.exists(vector_path):
        return None
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    archive = f"GremlinGPT/docs/planlog_{timestamp}.jsonl"
    shutil.copyfile(vector_path, archive)
    return archive

def auto_commit(file_path):
    if not file_path:
        return
    os.system(f"git add {file_path}")
    os.system(f'git commit -m "[autocommit] Planner log update: {file_path}"')

def get_all_embeddings(limit=50):
    # Return all loaded or cached vectors; auto-refresh if empty
    if not memory_vectors:
        _load_from_disk()
    return list(memory_vectors.values())[:limit]

def get_embedding_by_id(emb_id):
    # Return a single embedding by ID
    if emb_id in memory_vectors:
        return memory_vectors[emb_id]
    _load_from_disk()
    return memory_vectors.get(emb_id, None)

def _write_to_disk(embedding):
    path = os.path.join(LOCAL_INDEX_PATH, f"{embedding['id']}.json")
    with open(path, "w") as f:

