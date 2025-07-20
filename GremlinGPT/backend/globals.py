# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

# backend/globals.py

from backend.globals import CFG, logger, resolve_path, DATA_DIR, MEM

# Initialize module-specific logger
logger = get_module_logger("backend")

# === CONFIGURATION PATHS ===
CONFIG_PATH = str(Path(__file__).parent.parent / "config" / "config.toml")
MEMORY_JSON = str(Path(__file__).parent.parent / "config" / "memory.json")


def load_config():
    try:
        return toml.load(CONFIG_PATH)
    except Exception as e:
        logger.critical(f"[GLOBALS] Failed to load TOML config: {e}")
from backend.globals import CFG, logger, resolve_path, DATA_DIR, MEM
    project_root = Path(__file__).parent.parent.resolve()
    return os.path.expanduser(p.replace("$ROOT", str(project_root)))


BASE_DIR = resolve_path(CFG["paths"].get("base_dir", "."))
DATA_DIR = resolve_path(CFG["paths"].get("data_dir", "data"))
MODELS_DIR = resolve_path(CFG["paths"].get("models_dir", "models"))
CHECKPOINTS_DIR = resolve_path(CFG["paths"].get("checkpoints_dir", "run/checkpoints"))
LOG_FILE = resolve_path(CFG["paths"].get("log_file", "data/logs/runtime.log"))

# === MEMORY & VECTOR STORE PATHS ===
"""
Configuration-driven paths for memory, vector store, and metadata operations.
All modules should use these paths instead of hardcoded values.
"""
VECTOR_STORE_PATH = resolve_path(CFG["paths"].get("vector_store_path", "$ROOT/memory/vector_store/"))
FAISS_PATH = resolve_path(CFG["paths"].get("faiss_path", "$ROOT/memory/vector_store/faiss/"))
CHROMA_PATH = resolve_path(CFG["paths"].get("chroma_path", "$ROOT/memory/vector_store/chroma/"))
FAISS_INDEX_FILE = resolve_path(CFG["paths"].get("faiss_index_file", "$ROOT/memory/vector_store/faiss/faiss_index.index"))
CHROMA_DB = resolve_path(CFG["paths"].get("chroma_db", "$ROOT/memory/vector_store/chroma/chroma.sqlite3"))
LOCAL_INDEX_PATH = resolve_path(CFG["paths"].get("local_index_path", "$ROOT/memory/local_index/documents/"))
LOCAL_DB = resolve_path(CFG["paths"].get("local_db", "$ROOT/memory/local_index/documents.db"))

# === METADATA DATABASE PATH ===
"""
METADATA_DB_PATH: Central metadata store for the GremlinGPT system.
Used by all modules for:
  - Memory indexing and retrieval
  - Vector store metadata management
  - Training data provenance
  - Trading signal metadata
  - Scraper data annotation
  - Router decision tracking
  
All modules (API, router, training, trading, scraper, etc.) should import this
from backend.globals instead of using hardcoded paths.
"""
METADATA_DB_PATH = resolve_path(CFG["paths"].get("metadata_db", "$ROOT/memory/local_index/metadata.db"))


# === LOGGER INITIALIZATION ===
from utils.logging_config import setup_module_logger
logger = setup_module_logger("backend", "globals")


# === HARDWARE PREFERENCES ===
HARDWARE = {
    "use_ram": CFG.get("hardware", {}).get("use_ram", True),
    "use_cpu": CFG.get("hardware", {}).get("use_cpu", True),
    "use_gpu": CFG.get("hardware", {}).get("use_gpu", False),
    "gpu_device": CFG.get("hardware", {}).get("gpu_device", [0]),
    "multi_gpu": CFG.get("hardware", {}).get("multi_gpu", False),
}


# === NLP / EMBEDDING CONFIG ===
NLP = {
    "tokenizer_model": CFG["nlp"].get("tokenizer_model", "bert-base-uncased"),
    "embedder_model": CFG["nlp"].get("embedder_model", "bert-base-uncased"),
    "transformer_model": CFG["nlp"].get("transformer_model", "bert-base-uncased"),
    "embedding_dim": CFG["nlp"].get("embedding_dim", 768),
    "confidence_threshold": CFG["nlp"].get("confidence_threshold", 0.5),
}


# === AGENT TASK SETTINGS ===
AGENT = {
    "max_tasks": CFG["agent"].get("max_tasks", 100),
    "task_retry_limit": CFG["agent"].get("task_retry_limit", 3),
    "log_agent_output": CFG["agent"].get("log_agent_output", True),
}


# === SCRAPER CONFIG ===
SCRAPER = {
    "profile": CFG["scraper"].get(
        "browser_profile", "scraper/profiles/chromium_profile"
    ),
    "interval": CFG["scraper"].get("scrape_interval_sec", 30),
    "max_concurrent": CFG["scraper"].get("max_concurrent_scrapers", 1),
}


# === MEMORY ENGINE SETTINGS ===
MEMORY = {
    "vector_backend": CFG["memory"].get("dashboard_selected_backend", CFG["memory"].get("vector_backend", "faiss")),
    "embedding_format": CFG["memory"].get("embedding_format", "float32"),
    "auto_index": CFG["memory"].get("auto_index", True),
    "index_chunk_size": CFG["memory"].get("index_chunk_size", 128),
}


# === SYSTEM FLAGS ===
SYSTEM = {
    "name": CFG["system"].get("name", "GremlinGPT"),
    "mode": CFG["system"].get("mode", "alpha"),
    "offline": CFG["system"].get("offline", False),
    "debug": CFG["system"].get("debug", False),
    "log_level": CFG["system"].get("log_level", "INFO"),
}


# === LOOP TIMING / CONTROL ===
LOOP = {
    "fsm_tick_delay": CFG.get("loop", {}).get("fsm_tick_delay", 0.5),
    "planner_interval": CFG.get("loop", {}).get("planner_interval", 60),
    "mutation_watch_interval": CFG.get("loop", {}).get("mutation_watch_interval", 10),
    "planner_enabled": CFG.get("loop", {}).get("planner_enabled", True),
    "mutation_enabled": CFG.get("loop", {}).get("mutation_enabled", True),
    "self_training_enabled": CFG.get("loop", {}).get("self_training_enabled", True),
}


# === DASHBOARD BACKEND SELECTION ===
def set_dashboard_backend(backend):
    """Update the dashboard selected backend in config and memory"""
    global MEMORY
    if backend in ["faiss", "chroma"]:
        MEMORY["vector_backend"] = backend
        CFG["memory"]["dashboard_selected_backend"] = backend
        # Also update the config file
        try:
            with open(CONFIG_PATH, 'w') as f:
                toml.dump(CFG, f)
            logger.info(f"[GLOBALS] Dashboard backend updated to: {backend}")
            return True
        except Exception as e:
            logger.error(f"[GLOBALS] Failed to update backend: {e}")
            return False
    else:
        logger.error(f"[GLOBALS] Invalid backend: {backend}")
        return False

def get_dashboard_backend():
    """Get the current dashboard selected backend"""
    return MEMORY.get("vector_backend", "faiss")


# === AGENT ROLE ASSIGNMENTS ===
ROLES = CFG.get(
    "roles",
    {
        "planner": "planner_agent",
        "executor": "tool_executor",
        "trainer": "feedback_loop",
        "kernel": "code_mutator",
    },
)
