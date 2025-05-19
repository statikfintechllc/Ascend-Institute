import os
import toml
import json
from pathlib import Path
from loguru import logger

# Load configs
CONFIG_PATH = "config/config.toml"
MEMORY_JSON = "config/memory_settings.json"


def load_config():
    return toml.load(CONFIG_PATH)


def load_memory_config():
    with open(MEMORY_JSON) as f:
        return json.load(f)


CFG = load_config()
MEM = load_memory_config()

# Expand paths
def resolve_path(p):
    p = p.replace("$ROOT", str(BASE_DIR))
    return os.path.expanduser(p)


BASE_DIR = Path(os.path.expanduser(CFG["paths"]["base_dir"])).resolve()
DATA_DIR = resolve_path(CFG["paths"]["data_dir"])
MODELS_DIR = resolve_path(CFG["paths"]["models_dir"])
CHECKPOINTS_DIR = resolve_path(CFG["paths"]["checkpoints_dir"])
LOG_FILE = resolve_path(CFG["paths"]["log_file"])

# Logging (runtime.log setup)
logger.add(LOG_FILE, rotation="1 MB", retention="5 days", enqueue=True)
logger.info("[GLOBALS] Configuration loaded and logger initialized.")

# Hardware
HARDWARE = {
    "use_ram": CFG["hardware"].get("use_ram", True),
    "use_cpu": CFG["hardware"].get("use_cpu", True),
    "use_gpu": CFG["hardware"].get("use_gpu", False),
    "gpu_device": CFG["hardware"].get("gpu_device", [0]),
    "multi_gpu": CFG["hardware"].get("multi_gpu", False),
}

# NLP settings
NLP = {
    "tokenizer_model": CFG["nlp"]["tokenizer_model"],
    "embedder_model": CFG["nlp"]["embedder_model"],
    "transformer_model": CFG["nlp"]["transformer_model"],
    "embedding_dim": CFG["nlp"]["embedding_dim"],
    "confidence_threshold": CFG["nlp"]["confidence_threshold"],
}

# Agent
AGENT = {
    "max_tasks": CFG["agent"]["max_tasks"],
    "task_retry_limit": CFG["agent"]["task_retry_limit"],
    "log_agent_output": CFG["agent"]["log_agent_output"],
}

# Scraper
SCRAPER = {
    "profile": CFG["scraper"]["browser_profile"],
    "interval": CFG["scraper"]["scrape_interval_sec"],
    "max_concurrent": CFG["scraper"]["max_concurrent_scrapers"],
}

# Memory settings
MEMORY = {
    "vector_backend": CFG["memory"]["vector_backend"],
    "embedding_format": CFG["memory"]["embedding_format"],
    "auto_index": CFG["memory"]["auto_index"],
    "index_chunk_size": CFG["memory"]["index_chunk_size"],
}

# Runtime mode
SYSTEM = {
    "name": CFG["system"]["name"],
    "mode": CFG["system"]["mode"],
    "offline": CFG["system"]["offline"],
    "debug": CFG["system"]["debug"],
    "log_level": CFG["system"]["log_level"],
}
