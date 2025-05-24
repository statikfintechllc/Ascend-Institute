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

# memory/vector_store/embedder.py

import os
import shutil
import uuid
import json
from datetime import datetime

import numpy as np
from sentence_transformers import SentenceTransformer
from backend.globals import MEM
from loguru import logger

model = SentenceTransformer(MEM["embedding"]["model"])

MEMORY_DIR = MEM["storage"]["vector_store_path"]
INDEX_DB = MEM["storage"]["metadata_db"]
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
            "replaceable": True,
        },
    }
    memory_vectors[emb_id] = embedding
    _write_to_disk(embedding)
    logger.info(f"[EMBEDDER] Stored embedding: {emb_id}")
    return embedding


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


def get_all_embeddings(limit=10):
    return list(memory_vectors.values())[:limit]


def _write_to_disk(embedding):
    index_path = os.path.join(MEM["storage"]["local_index_path"], "documents")
    os.makedirs(index_path, exist_ok=True)
    path = os.path.join(index_path, f"{embedding['id']}.json")
    with open(path, "w") as f:
        json.dump(embedding, f, indent=2)
