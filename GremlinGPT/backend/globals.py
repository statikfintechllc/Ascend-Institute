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

import os
from pathlib import Path

# Try importing optional dependencies with fallbacks
try:
    import toml
    HAS_TOML = True
except ImportError:
    HAS_TOML = False
    toml = None

try:
    from utils.logging_config import setup_module_logger
    # Initialize module-specific logger
    logger = setup_module_logger("backend", "globals")
    HAS_LOGGER = True
except ImportError:
    # Fallback logger
    import logging
    logger = logging.getLogger("backend.globals")
    HAS_LOGGER = False

# === CONFIGURATION PATHS ===
CONFIG_PATH = str(Path(__file__).parent.parent / "config" / "config.toml")
MEMORY_JSON = str(Path(__file__).parent.parent / "config" / "memory.json")


def load_config():
    """Load configuration with fallback for missing dependencies"""
    try:
        if HAS_TOML and toml:
            return toml.load(CONFIG_PATH)
        else:
            logger.warning("[GLOBALS] toml not available, using default config")
            return get_default_config()
    except Exception as e:
        logger.critical(f"[GLOBALS] Failed to load TOML config: {e}")
        return get_default_config()

def get_default_config():
    """Provide default configuration when toml is not available"""
    return {
        "system": {"name": "GremlinGPT", "mode": "alpha", "debug": True, "log_level": "INFO"},
        "paths": {
            "base_dir": ".",
            "data_dir": "$ROOT/data/",
            "models_dir": "$ROOT/nlp_engine/",
            "checkpoints_dir": "$ROOT/run/checkpoints/",
            "log_file": "$ROOT/data/logs/runtime.log",
            "vector_store_path": "$ROOT/memory/vector_store/",
            "faiss_path": "$ROOT/memory/vector_store/faiss/",
            "chroma_path": "$ROOT/memory/vector_store/chroma/",
            "faiss_index_file": "$ROOT/memory/vector_store/faiss/faiss_index.index",
            "chroma_db": "$ROOT/memory/vector_store/chroma/chroma.sqlite3",
            "local_index_path": "$ROOT/memory/local_index/documents/",
            "local_db": "$ROOT/memory/local_index/documents.db",
            "metadata_db": "$ROOT/memory/local_index/metadata.db"
        },
        "hardware": {"use_ram": True, "use_cpu": True, "use_gpu": False, "gpu_device": [0], "multi_gpu": False},
        "nlp": {"tokenizer_model": "bert-base-uncased", "embedder_model": "bert-base-uncased", "transformer_model": "bert-base-uncased", "embedding_dim": 768, "confidence_threshold": 0.5},
        "agent": {"max_tasks": 100, "task_retry_limit": 3, "log_agent_output": True},
        "scraper": {"browser_profile": "scraper/profiles/chromium_profile", "scrape_interval_sec": 30, "max_concurrent_scrapers": 1},
        "memory": {"vector_backend": "faiss", "embedding_format": "float32", "auto_index": True, "index_chunk_size": 128},
        "loop": {"fsm_tick_delay": 0.5, "planner_interval": 60, "mutation_watch_interval": 10, "planner_enabled": True, "mutation_enabled": True, "self_training_enabled": True},
        "roles": {"planner": "planner_agent", "executor": "tool_executor", "trainer": "feedback_loop", "kernel": "code_mutator"}
    }

# Load the configuration
CFG = load_config()

def resolve_path(p):
    """Resolve paths with $ROOT replacement"""
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


# Memory configuration placeholder 
MEM = {}

# === COMPREHENSIVE MODULE IMPORTS ===
# Import all classes and functions from GremlinGPT modules to fix import failures

# Add current directory to Python path for relative imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

def safe_import_function(module_name, function_name):
    """Safely import a function from a module"""
    try:
        module = __import__(module_name, fromlist=[function_name])
        return getattr(module, function_name, None)
    except Exception:
        return None

def safe_import_class(module_name, class_name):
    """Safely import a class from a module"""
    try:
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name, None)
    except Exception:
        return None

# Core utilities - highest priority for fixing import issues
try:
    from utils.logging_config import setup_module_logger, get_module_logger, create_all_module_loggers
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

try:
    from backend.state_manager import save_state, load_state
    STATE_MANAGER_AVAILABLE = True
except ImportError:
    STATE_MANAGER_AVAILABLE = False
    save_state = load_state = None

# Core system modules - essential for system operation
boot_loop = safe_import_function('core.loop', 'boot_loop')
build_tree = safe_import_function('core.snapshot', 'build_tree')
verify_snapshot = safe_import_function('core.snapshot', 'verify_snapshot')
rollback = safe_import_function('core.snapshot', 'rollback')
snapshot_file = safe_import_function('core.snapshot', 'snapshot_file')
sha256_file = safe_import_function('core.snapshot', 'sha256_file')

# NLP Engine - critical for language processing
clean_text = safe_import_function('nlp_engine.tokenizer', 'clean_text')
tokenize = safe_import_function('nlp_engine.tokenizer', 'tokenize')
diff_texts = safe_import_function('nlp_engine.diff_engine', 'diff_texts')
diff_files = safe_import_function('nlp_engine.diff_engine', 'diff_files')
# Skip nlp_check due to runtime dependencies
# log_nlp_out = safe_import_function('nlp_engine.nlp_check', 'log_nlp_out')
# nlp_internal_check = safe_import_function('nlp_engine.nlp_check', 'nlp_internal_check')
get_pos_tags = safe_import_function('nlp_engine.pos_tagger', 'get_pos_tags')
classify_intent = safe_import_function('nlp_engine.parser', 'classify_intent')
extract_code_entities = safe_import_function('nlp_engine.parser', 'extract_code_entities')
detect_financial_terms = safe_import_function('nlp_engine.parser', 'detect_financial_terms')
parse_nlp = safe_import_function('nlp_engine.parser', 'parse_nlp')
encode = safe_import_function('nlp_engine.transformer_core', 'encode')

# NLP Classes
ChatSession = safe_import_class('nlp_engine.chat_session', 'ChatSession')
MiniMultiHeadAttention = safe_import_class('nlp_engine.mini_attention', 'MiniMultiHeadAttention')

# Trading Core - essential for trading functionality  
repair_signal_index = safe_import_function('trading_core.signal_generator', 'repair_signal_index')
generate_signals = safe_import_function('trading_core.signal_generator', 'generate_signals')
get_signal_history = safe_import_function('trading_core.signal_generator', 'get_signal_history')
apply_signal_rules = safe_import_function('trading_core.rules_engine', 'apply_signal_rules')
estimate_batch = safe_import_function('trading_core.tax_estimator', 'estimate_batch')
estimate_tax = safe_import_function('trading_core.tax_estimator', 'estimate_tax')
get_live_penny_stocks = safe_import_function('trading_core.stock_scraper', 'get_live_penny_stocks')
simulate_technical_indicators = safe_import_function('trading_core.stock_scraper', 'simulate_technical_indicators')
route_scraping = safe_import_function('trading_core.stock_scraper', 'route_scraping')
simulate_fallback = safe_import_function('trading_core.stock_scraper', 'simulate_fallback')

# Agent system - critical for autonomous operations
evaluate_task = safe_import_function('agent_core.heuristics', 'evaluate_task')
log_error = safe_import_function('agent_core.error_log', 'log_error')
JsonlFormatter = safe_import_class('agent_core.error_log', 'JsonlFormatter')
TaskQueue = safe_import_class('agent_core.task_queue', 'TaskQueue')
enqueue_task = safe_import_function('agent_core.task_queue', 'enqueue_task')
get_all_tasks = safe_import_function('agent_core.task_queue', 'get_all_tasks')

# Agent classes
AgentCoordinator = safe_import_class('agents.agent_coordinator', 'AgentCoordinator')
get_agent_coordinator = safe_import_function('agents.agent_coordinator', 'get_agent_coordinator')
DataAnalystAgent = safe_import_class('agents.data_analyst_agent', 'DataAnalystAgent')
AnomalyReport = safe_import_class('agents.data_analyst_agent', 'AnomalyReport')
get_data_analyst_agent = safe_import_function('agents.data_analyst_agent', 'get_data_analyst_agent')
LearningGoal = safe_import_class('agents.learning_agent', 'LearningGoal')
PerformanceMetric = safe_import_class('agents.learning_agent', 'PerformanceMetric')
LearningAgent = safe_import_class('agents.learning_agent', 'LearningAgent')
get_learning_agent = safe_import_function('agents.learning_agent', 'get_learning_agent')

# Self Training - important for system improvement
is_valid_python = safe_import_function('self_training.mutation_engine', 'is_valid_python')
mutate_dataset = safe_import_function('self_training.mutation_engine', 'mutate_dataset')
extract_training_data = safe_import_function('self_training.generate_dataset', 'extract_training_data')
hash_entry = safe_import_function('self_training.generate_dataset', 'hash_entry')
schedule_extraction = safe_import_function('self_training.generate_dataset', 'schedule_extraction')
generate_datasets = safe_import_function('self_training.generate_dataset', 'generate_datasets')
LogEventHandler = safe_import_class('self_training.trainer', 'LogEventHandler')

# Memory system - essential for knowledge storage
log_event = safe_import_function('memory.log_history', 'log_event')
load_history = safe_import_function('memory.log_history', 'load_history')

# Tools and executors (skip problematic ones that import scraper_loop)
# execute_tool = safe_import_function('executors.tool_executor', 'execute_tool')  # Skip due to scraper_loop import
run_shell_command = safe_import_function('executors.shell_executor', 'run_shell_command')
evaluate_with_diff = safe_import_function('tools.reward_model', 'evaluate_with_diff')
top_rewarded_tasks = safe_import_function('tools.reward_model', 'top_rewarded_tasks')
log_reward = safe_import_function('tools.reward_model', 'log_reward')
evaluate_result = safe_import_function('tools.reward_model', 'evaluate_result')
get_reward_feed = safe_import_function('tools.reward_model', 'get_reward_feed')

# Runtime and CLI
cli_main = safe_import_function('run.cli', 'main')
trace_calls = safe_import_function('run.module_tracer', 'trace_calls')
is_importable = safe_import_function('run.module_tracer', 'is_importable')
GremlinGPTEcosystemLauncher = safe_import_class('run.unified_startup', 'GremlinGPTEcosystemLauncher')

# Scraper modules (skip problematic ones with sys.exit)
extract_dom_structure = safe_import_function('scraper.dom_navigator', 'extract_dom_structure')
store_scrape_to_memory = safe_import_function('scraper.page_simulator', 'store_scrape_to_memory')
run_search_and_scrape = safe_import_function('scraper.web_knowledge_scraper', 'run_search_and_scrape')
# Skip source_router due to import issues causing sys.exit
# periodic_refresh = safe_import_function('scraper.source_router', 'periodic_refresh')
# start_scraper_loop = safe_import_function('scraper.source_router', 'start_scraper_loop')
# detect_apps = safe_import_function('scraper.source_router', 'detect_apps')
# get_live_snapshot = safe_import_function('scraper.source_router', 'get_live_snapshot')

# STT and TWS scrapers
parse_stt_data = safe_import_function('scraper.stt_scraper', 'parse_stt_data')
locate_stt_paths = safe_import_function('scraper.stt_scraper', 'locate_stt_paths')
safe_scrape_stt = safe_import_function('scraper.stt_scraper', 'safe_scrape_stt')
locate_tws_files = safe_import_function('scraper.tws_scraper', 'locate_tws_files')
parse_tws_json = safe_import_function('scraper.tws_scraper', 'parse_tws_json')
safe_scrape_tws = safe_import_function('scraper.tws_scraper', 'safe_scrape_tws')

# Backend API functions (skip problematic ones that import scraper_loop)
chat = safe_import_function('backend.api.chat_handler', 'chat')
graph = safe_import_function('backend.api.memory_api', 'graph')
set_task_priority = safe_import_function('backend.api.planner', 'set_task_priority')
list_tasks = safe_import_function('backend.api.planner', 'list_tasks')
get_signals = safe_import_function('backend.api.planner', 'get_signals')
mutation_notify = safe_import_function('backend.api.planner', 'mutation_notify')
# scrape_router = safe_import_function('backend.api.scraping_api', 'scrape_router')  # Skip due to scraper_loop import
summarize_text = safe_import_function('backend.api.summarizer', 'summarize_text')
register_routes = safe_import_function('backend.router', 'register_routes')

# Mutation and self-monitoring
load_snapshot = safe_import_function('self_mutation_watcher.watcher', 'load_snapshot')
scan_and_diff = safe_import_function('self_mutation_watcher.watcher', 'scan_and_diff')
hash_file = safe_import_function('self_mutation_watcher.watcher', 'hash_file')
save_snapshot = safe_import_function('self_mutation_watcher.watcher', 'save_snapshot')
generate_diff = safe_import_function('self_mutation_watcher.watcher', 'generate_diff')

# === EXPORTS FOR EASY ACCESS ===
# Export commonly used items to fix import path issues
__all__ = [
    # Configuration
    'CFG', 'logger', 'resolve_path', 'DATA_DIR', 'MEM',
    # Paths  
    'BASE_DIR', 'MODELS_DIR', 'CHECKPOINTS_DIR', 'LOG_FILE',
    'VECTOR_STORE_PATH', 'FAISS_PATH', 'CHROMA_PATH', 'METADATA_DB_PATH',
    # Settings
    'HARDWARE', 'NLP', 'AGENT', 'SCRAPER', 'MEMORY', 'SYSTEM', 'LOOP', 'ROLES',
    # Functions
    'set_dashboard_backend', 'get_dashboard_backend', 'load_config', 'get_default_config'
]


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
