# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────
#!/usr/bin/env python3

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

# backend/globals.py

import os
import toml
import json
from pathlib import Path
from loguru import logger

# Paths to configuration files
CONFIG_PATH = "config/config.toml"
MEMORY_JSON = "config/memory_settings.json"

# Load config files
def load_config():
    return toml.load(CONFIG_PATH)


def load_memory_config():
    with open(MEMORY_JSON) as f:
        return json.load(f)


CFG = load_config()
MEM = load_memory_config()

# Root and derived paths
BASE_DIR = Path(os.path.expanduser(CFG["paths"]["base_dir"])).resolve()


def resolve_path(p):
    return os.path.expanduser(p.replace("$ROOT", str(BASE_DIR)))


DATA_DIR = resolve_path(CFG["paths"]["data_dir"])
MODELS_DIR = resolve_path(CFG["paths"]["models_dir"])
CHECKPOINTS_DIR = resolve_path(CFG["paths"]["checkpoints_dir"])
LOG_FILE = resolve_path(CFG["paths"]["log_file"])

# Runtime logging
logger.add(LOG_FILE, rotation="1 MB", retention="5 days", enqueue=True)
logger.info("[GLOBALS] Configuration loaded and logger initialized.")

# Hardware preferences
HARDWARE = {
    "use_ram": CFG["hardware"].get("use_ram", True),
    "use_cpu": CFG["hardware"].get("use_cpu", True),
    "use_gpu": CFG["hardware"].get("use_gpu", False),
    "gpu_device": CFG["hardware"].get("gpu_device", [0]),
    "multi_gpu": CFG["hardware"].get("multi_gpu", False),
}

# NLP and embedding settings
NLP = {
    "tokenizer_model": CFG["nlp"]["tokenizer_model"],
    "embedder_model": CFG["nlp"]["embedder_model"],
    "transformer_model": CFG["nlp"]["transformer_model"],
    "embedding_dim": CFG["nlp"]["embedding_dim"],
    "confidence_threshold": CFG["nlp"]["confidence_threshold"],
}

# Agent task settings
AGENT = {
    "max_tasks": CFG["agent"]["max_tasks"],
    "task_retry_limit": CFG["agent"]["task_retry_limit"],
    "log_agent_output": CFG["agent"]["log_agent_output"],
}

# Scraping configuration
SCRAPER = {
    "profile": CFG["scraper"]["browser_profile"],
    "interval": CFG["scraper"]["scrape_interval_sec"],
    "max_concurrent": CFG["scraper"]["max_concurrent_scrapers"],
}

# Memory engine config
MEMORY = {
    "vector_backend": CFG["memory"]["vector_backend"],
    "embedding_format": CFG["memory"]["embedding_format"],
    "auto_index": CFG["memory"]["auto_index"],
    "index_chunk_size": CFG["memory"]["index_chunk_size"],
}

# Runtime system flags
SYSTEM = {
    "name": CFG["system"]["name"],
    "mode": CFG["system"]["mode"],
    "offline": CFG["system"]["offline"],
    "debug": CFG["system"]["debug"],
    "log_level": CFG["system"]["log_level"],
}

# Loop control and timing
LOOP = {
    "fsm_tick_delay": CFG.get("loop", {}).get("fsm_tick_delay", 0.5),
    "planner_interval": CFG.get("loop", {}).get("planner_interval", 60),
    "mutation_enabled": CFG.get("loop", {}).get("mutation_enabled", True),
    "self_training_enabled": CFG.get("loop", {}).get("self_training_enabled", True),
}

# Agent role-specific identities (optional future use)
ROLES = CFG.get(
    "roles",
    {
        "planner": "planner_agent",
        "executor": "tool_executor",
        "trainer": "feedback_loop",
        "kernel": "code_mutator",
    },
)
