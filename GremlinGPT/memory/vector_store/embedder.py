#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Memory Embedder & Vector Store Core

import os
import shutil
import uuid
import json
from datetime import datetime

import numpy as np
import faiss
from loguru import logger

from chromadb import Client
from chromadb.config import Settings

from nlp_engine.transformer_core import encode
from backend.globals import MEM

# Optional import for embedding model
try:
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    logger.error(f"[EMBEDDER] sentence_transformers import failed: {e}")
    SentenceTransformer = None

# --- Configuration & Paths ---
STORAGE = MEM.get("storage", {})
BASE_VECTOR_PATH = STORAGE.get("vector_store_path", "./memory/vector_store")
FAISS_DIR = os.path.join(BASE_VECTOR_PATH, "faiss")
CHROMA_DIR = os.path.join(BASE_VECTOR_PATH, "chroma")

LOCAL_INDEX_ROOT = STORAGE.get("local_index_path", "./memory/local_index")
LOCAL_INDEX_PATH = os.path.join(LOCAL_INDEX_ROOT, "documents")
METADATA_DB_PATH = STORAGE.get("metadata_db", os.path.join(LOCAL_INDEX_ROOT, "metadata.db"))

USE_FAISS = STORAGE.get("use_faiss", True)
USE_CHROMA = STORAGE.get("use_chroma", False)

EMBEDDING_MODEL = MEM.get("embedding", {}).get("model", "all-MiniLM-L6-v2")
DIMENSION = MEM.get("embedding", {}).get("dimension", 384)

# Ensure directories exist
for path in (FAISS_DIR, CHROMA_DIR, LOCAL_INDEX_PATH):
    os.makedirs(path, exist_ok=True)

# --- Chroma Client Setup ---
chroma_settings = Settings(
    persist_directory=CHROMA_DIR,
    chroma_db_impl="duckdb+parquet"
)
chroma_client = Client(chroma_settings)
collection = chroma_client.get_or_create_collection(name="gremlin_memory")

def add_to_chroma(text, emb_id, vector, meta):
    try:
        collection.add(
            documents=[text],
            embeddings=[vector.tolist()],
            metadatas=[meta],
            ids=[emb_id]
        )
        logger.info(f"[CHROMA] Added {emb_id}")
    except Exception as e:
        logger.error(f"[CHROMA] Add failed for {emb_id}: {e}")

# --- FAISS Index Setup ---
FAISS_INDEX_PATH = os.path.join(FAISS_DIR, "faiss_index.index")

if os.path.exists(FAISS_INDEX_PATH):
    faiss_index = faiss.read_index(FAISS_INDEX_PATH)
else:
    faiss_index = faiss.IndexFlatL2(DIMENSION)

def add_to_faiss(vector, emb_id):
    try:
        vec = np.array([vector], dtype="float32")
        faiss_index.add(vec)
        faiss.write_index(faiss_index, FAISS_INDEX_PATH)
        logger.info(f"[FAISS] Added {emb_id}")
    except Exception as e:
        logger.error(f"[FAISS] Add failed for {emb_id}: {e}")

# --- Model Loading ---
if SentenceTransformer:
    try:
        model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info(f"[EMBEDDER] Loaded model: {EMBEDDING_MODEL}")
    except Exception as e:
        logger.error(f"[EMBEDDER] Model load failed: {e}")
        model = None
else:
    logger.error("[EMBEDDER] SentenceTransformer not available")
    model = None

memory_vectors = {}

# --- Embedding Functions ---
def embed_text(text):
    if not model:
        logger.error("[EMBEDDER] No model loaded; returning zero vector")
        return np.zeros(DIMENSION, dtype="float32")
    try:
        vec = model.encode(text, convert_to_numpy=True)
        logger.debug(f"[EMBEDDER] Norm: {np.linalg.norm(vec):.4f}")
        return vec
    except Exception as e:
        logger.error(f"[EMBEDDER] Embedding failed: {e}")
        return np.zeros(DIMENSION, dtype="float32")

def package_embedding(text, vector, meta):
    emb_id = str(uuid.uuid4())
    embedding = {
        "id": emb_id,
        "text": text,
        "embedding": vector.tolist() if hasattr(vector, "tolist") else list(vector),
        "meta": meta,
        "tags": {
            "source": meta.get("source", "system"),
            "model": EMBEDDING_MODEL,
            "created": datetime.utcnow().isoformat(),
            "replaceable": True
        }
    }
    if USE_FAISS:
        add_to_faiss(vector, emb_id)
    if USE_CHROMA:
        add_to_chroma(text, emb_id, vector, meta)

    memory_vectors[emb_id] = embedding
    try:
        _write_to_disk(embedding)
        logger.info(f"[EMBEDDER] Stored {emb_id}")
    except Exception as e:
        logger.error(f"[EMBEDDER] Write failed for {emb_id}: {e}")
    return embedding

def inject_watermark(origin="unknown"):
    text = f"Watermark from {origin} @ {datetime.utcnow().isoformat()}"
    vector = encode(text)
    meta = {"origin": origin, "timestamp": datetime.utcnow().isoformat()}
    return package_embedding(text, vector, meta)

def archive_plan(vector_path="data/nlp_training_sets/auto_generated.jsonl"):
    if not os.path.exists(vector_path):
        logger.warning(f"[EMBEDDER] No plan at {vector_path}")
        return None
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    archive = os.path.join("GremlinGPT", "docs", f"planlog_{stamp}.jsonl")
    try:
        shutil.copyfile(vector_path, archive)
        logger.info(f"[EMBEDDER] Archived plan to {archive}")
        return archive
    except Exception as e:
        logger.error(f"[EMBEDDER] Archive failed: {e}")
        return None

def auto_commit(file_path):
    if not file_path:
        return
    try:
        os.system(f"git add {file_path}")
        os.system(f'git commit -m "[autocommit] Updated: {file_path}"')
    except Exception as e:
        logger.error(f"[EMBEDDER] Git commit failed: {e}")

def get_all_embeddings(limit=50):
    if not memory_vectors:
        _load_from_disk()
    return list(memory_vectors.values())[:limit]

def get_embedding_by_id(emb_id):
    if emb_id not in memory_vectors:
        _load_from_disk()
    return memory_vectors.get(emb_id)

def _write_to_disk(embedding):
    path = os.path.join(LOCAL_INDEX_PATH, f"{embedding['id']}.json")
    try:
        with open(path, "w") as f:
            json.dump(embedding, f, indent=2)
    except Exception as e:
        logger.error(f"[EMBEDDER] Disk write failed for {embedding['id']}: {e}")

def _load_from_disk():
    if not os.path.isdir(LOCAL_INDEX_PATH):
        logger.warning(f"[EMBEDDER] Missing local index: {LOCAL_INDEX_PATH}")
        return
    for fname in os.listdir(LOCAL_INDEX_PATH):
        if fname.endswith(".json"):
            path = os.path.join(LOCAL_INDEX_PATH, fname)
            try:
                with open(path) as f:
                    emb = json.load(f)
                memory_vectors[emb["id"]] = emb
            except Exception as e:
                logger.warning(f"[EMBEDDER] Load failed for {fname}: {e}")

def get_memory_graph():
    if not memory_vectors:
        _load_from_disk()
    nodes, edges = [], []
    for emb in memory_vectors.values():
        nodes.append({
            "id": emb["id"],
            "label": emb["meta"].get("label", emb["text"][:24] + "..."),
            "group": emb["tags"].get("source", "system")
        })
        if "source_id" in emb["meta"]:
            edges.append({"from": emb["meta"]["source_id"], "to": emb["id"]})
    return {"nodes": nodes, "edges": edges}

def repair_index():
    memory_vectors.clear()
    _load_from_disk()
    logger.info("[EMBEDDER] Index repaired")

# Load existing embeddings on import
try:
    _load_from_disk()
except Exception as e:
    logger.error(f"[EMBEDDER] Initial load failed: {e}")
