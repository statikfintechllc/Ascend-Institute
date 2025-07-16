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
import sqlite3
import uuid
import json
import numpy as np # type: ignore
try:
    import faiss
except ImportError:
    try:
        import faiss_cpu as faiss  # type: ignore
    except ImportError as e:
        print(f"[EMBEDDER] faiss import failed: {e}")
        faiss = None
from datetime import datetime, timezone
from utils.logging_config import setup_module_logger

# Initialize module-specific logger
logger = setup_module_logger("memory") # type: ignore

# --- Resilient Imports ---
try:
    import chromadb  # type: ignore
except ImportError as e:
    logger.error(f"[EMBEDDER] chromadb import failed: {e}")
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer # type: ignore
except ImportError as e:
    logger.error(f"[EMBEDDER] sentence_transformers import failed: {e}")
    SentenceTransformer = None

try:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from backend.globals import MEM
    import toml
    CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/config.toml'))
    try:
        config = toml.load(CONFIG_PATH)
        memory_conf = config.get('memory', {})
        dashboard_selected_backend = memory_conf.get('dashboard_selected_backend', 'faiss')
    except Exception as e:
        logger.error(f"[EMBEDDER] Failed to load config.toml: {e}")
        dashboard_selected_backend = 'faiss'
except Exception as e:
    logger.error(f"[EMBEDDER] MEM import or type-check failed: {e}")
    MEM = {}

try:
    from nlp_engine.transformer_core import encode
except Exception:
    # fallback to a dummy encoder
    def encode(text):
        _ = text  # Access the parameter to avoid unused variable warning
        return np.zeros(MEM.get("embedding", {}).get("dimension", 384), dtype="float32")

# --- Configuration & Paths ---
storage_conf = MEM.get("storage", {})
if not isinstance(storage_conf, dict):
    logger.error("[EMBEDDER] storage config malformed; resetting to empty dict")
    storage_conf = {}

BASE_VECTOR_PATH = storage_conf.get("vector_store_path", "./memory/vector_store/")
FAISS_DIR        = storage_conf.get("faiss_path", os.path.join(BASE_VECTOR_PATH, "faiss/"))
CHROMA_DIR       = storage_conf.get("chroma_path", os.path.join(BASE_VECTOR_PATH, "chroma/"))
FAISS_INDEX_PATH = storage_conf.get("faiss_index_file", os.path.join(FAISS_DIR, "faiss_index.index"))
CHROMA_DB_PATH   = storage_conf.get("chroma_db", os.path.join(CHROMA_DIR, "chroma.sqlite3"))

LOCAL_INDEX_PATH = storage_conf.get("local_index_path", "./memory/local_index/documents/")
SQLITE_PATH      = storage_conf.get("local_db", "./memory/local_index/documents.db")

USE_LOCAL  = True
USE_FAISS  = storage_conf.get("use_faiss", True)
USE_CHROMA = storage_conf.get("use_chroma", False)

EMBED_MODEL = MEM.get("embedding", {}).get("model", "all-MiniLM-L6-v2")
DIMENSION   = MEM.get("embedding", {}).get("dimension", 384)

# Ensure paths exist
os.makedirs(LOCAL_INDEX_PATH, exist_ok=True)

# SQLite setup
def ensure_sqlite_db():
    conn = sqlite3.connect(SQLITE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id TEXT PRIMARY KEY,
            text TEXT,
            embedding BLOB,
            meta TEXT,
            created TEXT,
            model TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

ensure_sqlite_db()

# Save embedding to SQLite
def save_to_sqlite(embedding):
    try:
        conn = sqlite3.connect(SQLITE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO embeddings (id, text, embedding, meta, created, model, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            embedding['id'],
            embedding['text'],
            json.dumps(embedding['embedding']),
            json.dumps(embedding['meta']),
            embedding['created'],
            embedding['model'],
            embedding['source']
        ))
        conn.commit()
        conn.close()
        logger.info(f"[SQLITE] Stored embedding {embedding['id']} in documents.db")
    except Exception as e:
        logger.error(f"[SQLITE] Failed to write to DB: {e}")


# _write_to_disk writes embedding to both JSON and SQLite
def ensure_db_setup():
    paths = [FAISS_DIR, CHROMA_DIR, LOCAL_INDEX_PATH]
    for path in paths:
        os.makedirs(path, exist_ok=True)

    # Ensure ChromaDB setup
    if chromadb:
        global chroma_client, collection
        chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        collection = chroma_client.get_or_create_collection(name="gremlin_memory")
        logger.info(f"[CHROMA] Initialized at {CHROMA_DIR}")

    # Ensure FAISS setup
    global faiss_index
    if faiss:
        if not os.path.exists(FAISS_INDEX_PATH):
            faiss_index = faiss.IndexFlatL2(DIMENSION)
            faiss.write_index(faiss_index, FAISS_INDEX_PATH)
            logger.info("[FAISS] Created new IndexFlatL2")
        else:
            faiss_index = faiss.read_index(FAISS_INDEX_PATH)
            logger.info(f"[FAISS] Loaded existing index from {FAISS_INDEX_PATH}")


def initialize_embedder():
    ensure_db_setup()
    try:
        _load_from_disk()
        logger.info("[EMBEDDER] Initial disk load complete")
    except Exception as e:
        logger.error(f"[EMBEDDER] Initial load failed: {e}")

# Call initialization at script start
if __name__ == '__main__':
    initialize_embedder()


def emb_id_to_int(emb_id):
    try:
        if isinstance(emb_id, int):
            return emb_id
        elif isinstance(emb_id, str) and emb_id.isdigit():
            return int(emb_id)
        else:
            return abs(hash(emb_id)) % (2**63)
    except Exception:
        return abs(hash(str(emb_id))) % (2**63)


# --- ChromaDB Setup ---
collection = None
chroma_client = None

if USE_CHROMA and chromadb:
    try:
        chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = chroma_client.get_or_create_collection(
            name="gremlin_memory",
            metadata={"description": "GremlinGPT memory store"},
        )
        logger.info(f"[CHROMA] Collection 'gremlin_memory' initialized at {CHROMA_DB_PATH}")
    except Exception as e:
        logger.error(f"[CHROMA] Initialization failed: {e}")
        collection = None
else:
    logger.info("[CHROMA] Skipped initialization; either disabled or chromadb not available")
    collection = None


def add_to_chroma(text, emb_id, vector, meta):
    if not collection:
        logger.warning(f"[CHROMA] Skipping add; collection not initialized")
        return

    try:
        vector_data = vector.tolist() if hasattr(vector, "tolist") else list(vector)
        meta = meta or {}

        collection.add(
            documents=[text],
            embeddings=[vector_data],
            metadatas=[meta],
            ids=[emb_id],
        )
        logger.info(f"[CHROMA] Added embedding {emb_id}")
    except Exception as e:
        logger.error(f"[CHROMA] Failed to add {emb_id}: {e}")


def add_to_faiss(vector, emb_id):
    if not faiss_index:
        logger.warning(f"[FAISS] Skipping add; index not available")
        return
    try:
        vec = np.array(vector, dtype="float32").reshape(1, -1)
        logger.info(f"[FAISS] Index type: {type(faiss_index)}")
        logger.debug(f"[FAISS] Index methods: {[m for m in dir(faiss_index) if 'add' in m]}")

        supports_ids = hasattr(faiss_index, 'add_with_ids') and callable(getattr(faiss_index, 'add_with_ids', None))

        if supports_ids:
            logger.info(f"[FAISS] Using add_with_ids method.")
            try:
                emb_id_int = emb_id_to_int(emb_id)
                vec_2d = np.array(vector, dtype="float32").reshape(1, -1)
                ids_array = np.array([emb_id_int], dtype="int64")
                logger.debug(f"[FAISS] add_with_ids vec shape: {vec_2d.shape}, emb_id_int: {emb_id_int}")
                faiss_index.add_with_ids(vec_2d, ids_array)  # type: ignore
                logger.info(f"[FAISS] Added {emb_id} with ID")
            except Exception as e:
                logger.warning(f"[FAISS] add_with_ids failed, falling back to add: {e}")
                supports_ids = False

        if not supports_ids:
            logger.info(f"[FAISS] Using add method (no ID support).")
            try:
                vec_2d = np.array(vector, dtype="float32").reshape(1, -1)
                logger.debug(f"[FAISS] add vec shape: {vec_2d.shape}")
                faiss_index.add(vec_2d)  # type: ignore
                logger.info(f"[FAISS] Added {emb_id} without ID")
            except Exception as e:
                logger.error(f"[FAISS] add failed: {e}")
                return
        faiss.write_index(faiss_index, FAISS_INDEX_PATH)  # type: ignore
        logger.info(f"[FAISS] Persisted index after adding {emb_id}")
    except Exception as e:
        logger.error(f"[FAISS] Add failed for {emb_id}: {e}")


def get_index_info():
    info = {}
    if 'faiss_index' in globals() and faiss_index:
        info['faiss_type'] = str(type(faiss_index))
        info['faiss_methods'] = dir(faiss_index)
    else:
        info['faiss_type'] = None
        info['faiss_methods'] = []

    if 'collection' in globals() and collection:
        info['chroma_type'] = str(type(collection))
        info['chroma_methods'] = dir(collection)
    else:
        info['chroma_type'] = None
        info['chroma_methods'] = []

    return info


def get_current_backend():
    global dashboard_selected_backend
    return dashboard_selected_backend


def set_backend(backend_name):
    global dashboard_selected_backend, USE_FAISS, USE_CHROMA

    if backend_name not in ['faiss', 'chromadb']:
        raise ValueError(f"Invalid backend: {backend_name}. Must be 'faiss' or 'chromadb'.")

    dashboard_selected_backend = backend_name
    USE_FAISS = backend_name == "faiss"
    USE_CHROMA = backend_name == "chromadb"

    try:
        import toml
        config = toml.load(CONFIG_PATH)
        if 'memory' not in config:
            config['memory'] = {}
        config['memory']['dashboard_selected_backend'] = backend_name

        with open(CONFIG_PATH, 'w') as f:
            toml.dump(config, f)

        logger.info(f"[EMBEDDER] Backend switched to: {backend_name}")
        return {"status": f"Backend switched to {backend_name}", "backend": backend_name}
    except Exception as e:
        logger.error(f"[EMBEDDER] Failed to update config: {e}")
        return {"error": f"Failed to update config: {e}", "backend": backend_name}


def get_backend_status():
    status = {
        "current_backend": dashboard_selected_backend,
        "faiss_available": faiss is not None and faiss_index is not None,
        "chromadb_available": chromadb is not None and collection is not None,
        "faiss_index_count": 0,
        "chroma_collection_count": 0
    }

    if status["faiss_available"]:
        try:
            status["faiss_index_count"] = faiss_index.ntotal  # type: ignore
        except Exception as e:
            logger.warning(f"[EMBEDDER] Failed to get FAISS count: {e}")

    if status["chromadb_available"]:
        try:
            if hasattr(collection, "count") and callable(collection.count):
                status["chroma_collection_count"] = collection.count()  # type: ignore
        except Exception as e:
            logger.warning(f"[EMBEDDER] Failed to get Chroma count: {e}")

    return status


# --- Model Loading (Resilient) ---
model = None
if SentenceTransformer:
    try:
        model = SentenceTransformer(EMBED_MODEL)
        logger.info(f"[EMBEDDER] Loaded model: {EMBED_MODEL}")
    except Exception as e:
        logger.error(f"[EMBEDDER] Model load failed: {e}")
        model = None
else:
    logger.error("[EMBEDDER] SentenceTransformer unavailable; using fallback")

memory_vectors = {}


# --- Core Embedding Functions ---
def embed_text(text):
    if not model:
        logger.error("[EMBEDDER] No model; returning zero-vector")
        return np.zeros(DIMENSION, dtype="float32")
    try:
        vec = model.encode(text, convert_to_numpy=True)
        logger.debug(f"[EMBEDDER] Embedding norm: {np.linalg.norm(vec):.4f}")
        return vec
    except Exception as e:
        logger.error(f"[EMBEDDER] Embedding failed: {e}")
        return np.zeros(DIMENSION, dtype="float32")


def package_embedding(text, vector, meta):
    emb_id = str(uuid.uuid4())
    
    if not isinstance(meta, dict):
        logger.warning(f"[EMBEDDER] meta not dict; got {type(meta)}; coercing")
        meta = {"source": str(meta)}
    
    embedding = {
        "id": emb_id,
        "text": text,
        "embedding": vector.tolist() if hasattr(vector, "tolist") else list(vector),
        "meta": meta,
        "created": datetime.now(timezone.utc).isoformat(),
        "source": meta.get("source", "system"),
        "model": EMBED_MODEL,
        "replaceable": True,
    }

    if USE_FAISS and faiss_index is not None:
        add_to_faiss(vector, emb_id)

    if USE_CHROMA and collection is not None:
        add_to_chroma(text, emb_id, vector, meta)

    if USE_LOCAL:
        try:
            _write_to_disk(embedding)
            save_to_sqlite(embedding)
            logger.info(f"[LOCAL] Stored embedding {emb_id} to disk and SQLite")
        except Exception as e:
            logger.error(f"[LOCAL] Write failed for {emb_id}: {e}")

    memory_vectors[emb_id] = embedding
    return embedding


def archive_plan(vector_path="data/nlp_training_sets/auto_generated.jsonl"):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    archive = os.path.join("GremlinGPT", "docs", f"planlog_{stamp}.jsonl")
    try:
        shutil.copyfile(vector_path, archive)
        logger.info(f"[EMBEDDER] Plan archived: {archive}")
        return archive
    except Exception as e:
        logger.error(f"[EMBEDDER] Archive failed: {e}")
        return None


def auto_commit(file_path):
    if not file_path or not os.path.exists(file_path):
        logger.warning(f"[EMBEDDER] auto_commit: invalid path {file_path}")
        return
    try:
        os.system(f"git add {file_path}")
        os.system(f'git commit -m "[autocommit] Updated: {file_path}"')
        logger.info(f"[EMBEDDER] auto_commit succeeded for {file_path}")
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
    try:
        path = os.path.join(LOCAL_INDEX_PATH, f"{embedding['id']}.json")
        with open(path, "w") as f:
            json.dump(embedding, f, indent=2)
    except Exception as e:
        logger.error(f"[EMBEDDER] Failed to write {embedding['id']} to disk: {e}")


def _load_from_disk():
    if not os.path.isdir(LOCAL_INDEX_PATH):
        logger.warning(f"[EMBEDDER] Local index missing: {LOCAL_INDEX_PATH}")
        return
    for fname in os.listdir(LOCAL_INDEX_PATH):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(LOCAL_INDEX_PATH, fname)
        try:
            with open(fpath, "r") as f:
                emb = json.load(f)
            memory_vectors[emb["id"]] = emb
        except Exception as e:
            logger.warning(f"[EMBEDDER] Failed to load {fname}: {e}")


def get_memory_graph():
    if not memory_vectors:
        _load_from_disk()
    nodes, edges = [], []
    for emb in memory_vectors.values():
        nodes.append({
            "id": emb["id"],
            "label": emb["meta"].get("label", emb["text"][:24] + "..."),
            "group": emb["meta"].get("source", "system"),
        })
        if "source_id" in emb["meta"]:
            edges.append({"from": emb["meta"]["source_id"], "to": emb["id"]})
    return {"nodes": nodes, "edges": edges}


def repair_index():
    memory_vectors.clear()
    _load_from_disk()
    logger.info("[EMBEDDER] Index repaired")


def inject_watermark(origin="unknown"):
    text = f"Watermark from {origin} @ {datetime.now(timezone.utc).isoformat()}"
    vector = embed_text(text)
    meta = {"origin": origin, "timestamp": datetime.now(timezone.utc).isoformat()}
    return package_embedding(text, vector, meta)


# --- Initial Load ---
try:
    _load_from_disk()
    logger.info("[EMBEDDER] Initial disk load complete")
except Exception as e:
    logger.error(f"[EMBEDDER] Initial load failed: {e}")
