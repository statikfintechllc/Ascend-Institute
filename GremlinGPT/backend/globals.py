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
# CENTRALIZED IMPORT MANAGEMENT FOR ALL GREMLINGPT MODULES
# All modules should import their dependencies from here to ensure consistency

# ========================================================================================
# STANDARD LIBRARY IMPORTS - Always available
# ========================================================================================
import os
import sys
import json
import time
import logging
import asyncio
import threading
import pathlib
import datetime
import collections
import subprocess
import tempfile
import traceback
import hashlib
import shutil
import signal
import uuid
import math
import random
import re
import ast
import argparse
import typing
import dataclasses
import enum
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

# ========================================================================================
# THIRD-PARTY IMPORTS - With fallbacks for missing packages
# ========================================================================================

# TOML Configuration
try:
    import toml
    HAS_TOML = True
except ImportError:
    HAS_TOML = False
    toml = None

# Flask Web Framework
try:
    import flask
    from flask import Flask, Blueprint, request, jsonify, render_template
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    flask = request = jsonify = render_template = None
    # Mock Flask components for non-web environments
    class MockFlask:
        def __init__(self, name): pass
        def route(self, *args, **kwargs): 
            def decorator(f): return f
            return decorator
    class MockBlueprint:
        def __init__(self, name, import_name): 
            self.name = name
            self.deferred_functions = []
        def route(self, rule, **options):
            def decorator(f):
                self.deferred_functions.append((rule, f, options))
                return f
            return decorator
    Flask = MockFlask
    Blueprint = MockBlueprint

# Scientific Computing
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    pd = None

# HTTP Requests
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None

# Async HTTP
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    aiohttp = None

# Natural Language Processing
try:
    import nltk
    from nltk.tokenize import word_tokenize
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False
    nltk = word_tokenize = None

# Machine Learning
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None

try:
    import transformers
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    transformers = None

# Task Scheduling
try:
    import schedule
    HAS_SCHEDULE = True
except ImportError:
    HAS_SCHEDULE = False
    schedule = None

# Testing
try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False
    pytest = None

# Web Automation
try:
    from playwright.async_api import async_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    async_playwright = None

# ========================================================================================
# PROJECT CONFIGURATION AND PATHS
# ========================================================================================

# Add current directory to Python path for relative imports
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

# Configuration paths
CONFIG_PATH = str(project_root / "config" / "config.toml")
MEMORY_JSON = str(project_root / "config" / "memory.json")

def load_config():
    """Load configuration with fallback for missing dependencies"""
    try:
        if HAS_TOML and toml and os.path.exists(CONFIG_PATH):
            return toml.load(CONFIG_PATH)
        else:
            return get_default_config()
    except Exception as e:
        return get_default_config()

def get_default_config():
    """Provide default configuration when toml is not available"""
    return {
        "system": {"name": "GremlinGPT", "mode": "alpha", "debug": True, "log_level": "INFO"},
        "paths": {
            "base_dir": ".", "data_dir": "$ROOT/data/", "models_dir": "$ROOT/nlp_engine/",
            "checkpoints_dir": "$ROOT/run/checkpoints/", "log_file": "$ROOT/data/logs/runtime.log",
            "vector_store_path": "$ROOT/memory/vector_store/", "faiss_path": "$ROOT/memory/vector_store/faiss/",
            "chroma_path": "$ROOT/memory/vector_store/chroma/", "faiss_index_file": "$ROOT/memory/vector_store/faiss/faiss_index.index",
            "chroma_db": "$ROOT/memory/vector_store/chroma/chroma.sqlite3", "local_index_path": "$ROOT/memory/local_index/documents/",
            "local_db": "$ROOT/memory/local_index/documents.db", "metadata_db": "$ROOT/memory/local_index/metadata.db"
        },
        "hardware": {"use_ram": True, "use_cpu": True, "use_gpu": False, "gpu_device": [0], "multi_gpu": False},
        "nlp": {"tokenizer_model": "bert-base-uncased", "embedder_model": "bert-base-uncased", "transformer_model": "bert-base-uncased", "embedding_dim": 768, "confidence_threshold": 0.5},
        "agent": {"max_tasks": 100, "task_retry_limit": 3, "log_agent_output": True},
        "scraper": {"browser_profile": "scraper/profiles/chromium_profile", "scrape_interval_sec": 30, "max_concurrent_scrapers": 1},
        "memory": {"vector_backend": "faiss", "embedding_format": "float32", "auto_index": True, "index_chunk_size": 128},
        "loop": {"fsm_tick_delay": 0.5, "planner_interval": 60, "mutation_watch_interval": 10, "planner_enabled": True, "mutation_enabled": True, "self_training_enabled": True},
        "roles": {"planner": "planner_agent", "executor": "tool_executor", "trainer": "feedback_loop", "kernel": "code_mutator"}
    }

def resolve_path(p):
    """Resolve paths with $ROOT replacement"""
    return os.path.expanduser(p.replace("$ROOT", str(project_root)))

# Load configuration
CFG = load_config()

# Initialize logging
try:
    from utils.logging_config import setup_module_logger
    logger = setup_module_logger("backend", "globals")
    HAS_LOGGER = True
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("backend.globals")
    HAS_LOGGER = False

# ========================================================================================
# CENTRALIZED MODULE IMPORTS WITH SAFE FALLBACKS
# ========================================================================================

def safe_import_function(module_path, function_name, fallback=None):
    """Safely import a function from a module with fallback"""
    try:
        module_parts = module_path.split('.')
        module = __import__(module_path, fromlist=[function_name])
        return getattr(module, function_name, fallback)
    except Exception as e:
        logger.debug(f"[GLOBALS] Failed to import {module_path}.{function_name}: {e}")
        return fallback

def safe_import_class(module_path, class_name, fallback=None):
    """Safely import a class from a module with fallback"""
    try:
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name, fallback)
    except Exception as e:
        logger.debug(f"[GLOBALS] Failed to import {module_path}.{class_name}: {e}")
        return fallback

def safe_import_module(module_path, fallback=None):
    """Safely import an entire module with fallback"""
    try:
        return __import__(module_path, fromlist=[''])
    except Exception as e:
        logger.debug(f"[GLOBALS] Failed to import module {module_path}: {e}")
        return fallback

# ========================================================================================
# CORE SYSTEM MODULES
# ========================================================================================

# Core loop and system management
boot_loop = safe_import_function('core.loop', 'boot_loop')
build_tree = safe_import_function('core.snapshot', 'build_tree')
verify_snapshot = safe_import_function('core.snapshot', 'verify_snapshot')
rollback = safe_import_function('core.snapshot', 'rollback')
snapshot_file = safe_import_function('core.snapshot', 'snapshot_file')
sha256_file = safe_import_function('core.snapshot', 'sha256_file')

# State management
save_state = safe_import_function('backend.state_manager', 'save_state')
load_state = safe_import_function('backend.state_manager', 'load_state')

# Router and backend utilities
register_routes = safe_import_function('backend.router', 'register_routes')
route_task = safe_import_function('backend.router', 'route_task')

# ========================================================================================
# NLP ENGINE MODULES
# ========================================================================================

# Tokenization and text processing
clean_text = safe_import_function('nlp_engine.tokenizer', 'clean_text')
tokenize = safe_import_function('nlp_engine.tokenizer', 'tokenize')
diff_texts = safe_import_function('nlp_engine.diff_engine', 'diff_texts')
diff_files = safe_import_function('nlp_engine.diff_engine', 'diff_files')
get_pos_tags = safe_import_function('nlp_engine.pos_tagger', 'get_pos_tags')
classify_intent = safe_import_function('nlp_engine.parser', 'classify_intent')
extract_code_entities = safe_import_function('nlp_engine.parser', 'extract_code_entities')
detect_financial_terms = safe_import_function('nlp_engine.parser', 'detect_financial_terms')
parse_nlp = safe_import_function('nlp_engine.parser', 'parse_nlp')
encode = safe_import_function('nlp_engine.transformer_core', 'encode')

# NLP Classes
ChatSession = safe_import_class('nlp_engine.chat_session', 'ChatSession')
MiniMultiHeadAttention = safe_import_class('nlp_engine.mini_attention', 'MiniMultiHeadAttention')

# ========================================================================================
# AGENT CORE MODULES
# ========================================================================================

# FSM and task management
fsm_loop = safe_import_function('agent_core.fsm', 'fsm_loop')
get_fsm_status = safe_import_function('agent_core.fsm', 'get_fsm_status')
step_fsm = safe_import_function('agent_core.fsm', 'step_fsm')
reset_fsm = safe_import_function('agent_core.fsm', 'reset_fsm')
fsm_inject_task = safe_import_function('agent_core.fsm', 'fsm_inject_task')

# Task queue operations
enqueue_task = safe_import_function('agent_core.task_queue', 'enqueue_task')
get_all_tasks = safe_import_function('agent_core.task_queue', 'get_all_tasks')
fetch_task = safe_import_function('agent_core.task_queue', 'fetch_task')
reprioritize = safe_import_function('agent_core.task_queue', 'reprioritize')
TaskQueue = safe_import_class('agent_core.task_queue', 'TaskQueue')

# Heuristics and error handling
evaluate_task = safe_import_function('agent_core.heuristics', 'evaluate_task')
log_error = safe_import_function('agent_core.error_log', 'log_error')
JsonlFormatter = safe_import_class('agent_core.error_log', 'JsonlFormatter')

# ========================================================================================
# TRADING CORE MODULES  
# ========================================================================================

# Signal generation and trading
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

# ========================================================================================
# MEMORY SYSTEM MODULES
# ========================================================================================

# Vector store and embeddings
embed_text = safe_import_function('memory.vector_store.embedder', 'embed_text')
inject_watermark = safe_import_function('memory.vector_store.embedder', 'inject_watermark')
package_embedding = safe_import_function('memory.vector_store.embedder', 'package_embedding')
get_all_embeddings = safe_import_function('memory.vector_store.embedder', 'get_all_embeddings')
repair_index = safe_import_function('memory.vector_store.embedder', 'repair_index')
search_memory = safe_import_function('memory.vector_store.embedder', 'search_memory')

# Memory logging and history
log_event = safe_import_function('memory.log_history', 'log_event')
load_history = safe_import_function('memory.log_history', 'load_history')

# ========================================================================================
# SELF-TRAINING MODULES
# ========================================================================================

# Mutation and feedback
is_valid_python = safe_import_function('self_training.mutation_engine', 'is_valid_python')
mutate_dataset = safe_import_function('self_training.mutation_engine', 'mutate_dataset')
extract_training_data = safe_import_function('self_training.generate_dataset', 'extract_training_data')
hash_entry = safe_import_function('self_training.generate_dataset', 'hash_entry')
schedule_extraction = safe_import_function('self_training.generate_dataset', 'schedule_extraction')
generate_datasets = safe_import_function('self_training.generate_dataset', 'generate_datasets')

# Feedback loop functions
tag_event = safe_import_function('self_training.feedback_loop', 'tag_event')
check_trigger = safe_import_function('self_training.feedback_loop', 'check_trigger')
inject_feedback = safe_import_function('self_training.feedback_loop', 'inject_feedback')
clear_trigger = safe_import_function('self_training.feedback_loop', 'clear_trigger')

# Training classes
LogEventHandler = safe_import_class('self_training.trainer', 'LogEventHandler')

# ========================================================================================
# SCRAPER MODULES
# ========================================================================================

# DOM and web scraping
extract_dom_structure = safe_import_function('scraper.dom_navigator', 'extract_dom_structure')
store_scrape_to_memory = safe_import_function('scraper.page_simulator', 'store_scrape_to_memory')
run_search_and_scrape = safe_import_function('scraper.web_knowledge_scraper', 'run_search_and_scrape')

# STT and TWS scrapers
parse_stt_data = safe_import_function('scraper.stt_scraper', 'parse_stt_data')
locate_stt_paths = safe_import_function('scraper.stt_scraper', 'locate_stt_paths')
safe_scrape_stt = safe_import_function('scraper.stt_scraper', 'safe_scrape_stt')
locate_tws_files = safe_import_function('scraper.tws_scraper', 'locate_tws_files')
parse_tws_json = safe_import_function('scraper.tws_scraper', 'parse_tws_json')
safe_scrape_tws = safe_import_function('scraper.tws_scraper', 'safe_scrape_tws')

# ========================================================================================
# AGENT MODULES
# ========================================================================================

# Agent coordinators and specialized agents
AgentCoordinator = safe_import_class('agents.agent_coordinator', 'AgentCoordinator')
get_agent_coordinator = safe_import_function('agents.agent_coordinator', 'get_agent_coordinator')
DataAnalystAgent = safe_import_class('agents.data_analyst_agent', 'DataAnalystAgent')
AnomalyReport = safe_import_class('agents.data_analyst_agent', 'AnomalyReport')
get_data_analyst_agent = safe_import_function('agents.data_analyst_agent', 'get_data_analyst_agent')
LearningGoal = safe_import_class('agents.learning_agent', 'LearningGoal')
PerformanceMetric = safe_import_class('agents.learning_agent', 'PerformanceMetric')
LearningAgent = safe_import_class('agents.learning_agent', 'LearningAgent')
get_learning_agent = safe_import_function('agents.learning_agent', 'get_learning_agent')

# ========================================================================================
# EXECUTOR MODULES
# ========================================================================================

# Command and shell executors
run_shell_command = safe_import_function('executors.shell_executor', 'run_shell_command')
# execute_tool = safe_import_function('executors.tool_executor', 'execute_tool')  # Skip due to scraper_loop import
execute_tool = None  # Placeholder to avoid import issues

# ========================================================================================
# TOOLS AND UTILITIES
# ========================================================================================

# Reward model and evaluation
evaluate_with_diff = safe_import_function('tools.reward_model', 'evaluate_with_diff')
top_rewarded_tasks = safe_import_function('tools.reward_model', 'top_rewarded_tasks')
log_reward = safe_import_function('tools.reward_model', 'log_reward')
evaluate_result = safe_import_function('tools.reward_model', 'evaluate_result')
get_reward_feed = safe_import_function('tools.reward_model', 'get_reward_feed')

# ========================================================================================
# BACKEND API MODULES
# ========================================================================================

# API handlers
chat = safe_import_function('backend.api.chat_handler', 'chat')
graph = safe_import_function('backend.api.memory_api', 'graph')
set_task_priority = safe_import_function('backend.api.planner', 'set_task_priority')
list_tasks = safe_import_function('backend.api.planner', 'list_tasks')
get_signals = safe_import_function('backend.api.planner', 'get_signals')
mutation_notify = safe_import_function('backend.api.planner', 'mutation_notify')
summarize_text = safe_import_function('backend.api.summarizer', 'summarize_text')

# ========================================================================================
# UTILITY MODULES
# ========================================================================================

# Logging and setup utilities
if HAS_LOGGER:
    setup_module_logger = safe_import_function('utils.logging_config', 'setup_module_logger')
    get_module_logger = safe_import_function('utils.logging_config', 'get_module_logger')
    create_all_module_loggers = safe_import_function('utils.logging_config', 'create_all_module_loggers')
else:
    setup_module_logger = get_module_logger = create_all_module_loggers = None

# ========================================================================================
# PATH CONFIGURATION
# ========================================================================================

# Resolve and set up paths
BASE_DIR = resolve_path(CFG["paths"].get("base_dir", "."))
DATA_DIR = resolve_path(CFG["paths"].get("data_dir", "data"))
MODELS_DIR = resolve_path(CFG["paths"].get("models_dir", "models"))
CHECKPOINTS_DIR = resolve_path(CFG["paths"].get("checkpoints_dir", "run/checkpoints"))
LOG_FILE = resolve_path(CFG["paths"].get("log_file", "data/logs/runtime.log"))

# Memory & Vector Store Paths
VECTOR_STORE_PATH = resolve_path(CFG["paths"].get("vector_store_path", "$ROOT/memory/vector_store/"))
FAISS_PATH = resolve_path(CFG["paths"].get("faiss_path", "$ROOT/memory/vector_store/faiss/"))
CHROMA_PATH = resolve_path(CFG["paths"].get("chroma_path", "$ROOT/memory/vector_store/chroma/"))
FAISS_INDEX_FILE = resolve_path(CFG["paths"].get("faiss_index_file", "$ROOT/memory/vector_store/faiss/faiss_index.index"))
CHROMA_DB = resolve_path(CFG["paths"].get("chroma_db", "$ROOT/memory/vector_store/chroma/chroma.sqlite3"))
LOCAL_INDEX_PATH = resolve_path(CFG["paths"].get("local_index_path", "$ROOT/memory/local_index/documents/"))
LOCAL_DB = resolve_path(CFG["paths"].get("local_db", "$ROOT/memory/local_index/documents.db"))
METADATA_DB_PATH = resolve_path(CFG["paths"].get("metadata_db", "$ROOT/memory/local_index/metadata.db"))

# ========================================================================================
# CONFIGURATION DICTIONARIES
# ========================================================================================

# Hardware configuration
HARDWARE = {
    "use_ram": CFG.get("hardware", {}).get("use_ram", True),
    "use_cpu": CFG.get("hardware", {}).get("use_cpu", True),
    "use_gpu": CFG.get("hardware", {}).get("use_gpu", False),
    "gpu_device": CFG.get("hardware", {}).get("gpu_device", [0]),
    "multi_gpu": CFG.get("hardware", {}).get("multi_gpu", False),
}

# NLP configuration
NLP = {
    "tokenizer_model": CFG["nlp"].get("tokenizer_model", "bert-base-uncased"),
    "embedder_model": CFG["nlp"].get("embedder_model", "bert-base-uncased"),
    "transformer_model": CFG["nlp"].get("transformer_model", "bert-base-uncased"),
    "embedding_dim": CFG["nlp"].get("embedding_dim", 768),
    "confidence_threshold": CFG["nlp"].get("confidence_threshold", 0.5),
}

# Agent configuration
AGENT = {
    "max_tasks": CFG["agent"].get("max_tasks", 100),
    "task_retry_limit": CFG["agent"].get("task_retry_limit", 3),
    "log_agent_output": CFG["agent"].get("log_agent_output", True),
}

# Scraper configuration
SCRAPER = {
    "profile": CFG["scraper"].get("browser_profile", "scraper/profiles/chromium_profile"),
    "interval": CFG["scraper"].get("scrape_interval_sec", 30),
    "max_concurrent": CFG["scraper"].get("max_concurrent_scrapers", 1),
}

# Memory configuration
MEMORY = {
    "vector_backend": CFG["memory"].get("dashboard_selected_backend", CFG["memory"].get("vector_backend", "faiss")),
    "embedding_format": CFG["memory"].get("embedding_format", "float32"),
    "auto_index": CFG["memory"].get("auto_index", True),
    "index_chunk_size": CFG["memory"].get("index_chunk_size", 128),
}

# System configuration
SYSTEM = {
    "name": CFG["system"].get("name", "GremlinGPT"),
    "mode": CFG["system"].get("mode", "alpha"),
    "offline": CFG["system"].get("offline", False),
    "debug": CFG["system"].get("debug", False),
    "log_level": CFG["system"].get("log_level", "INFO"),
}

# Loop configuration
LOOP = {
    "fsm_tick_delay": CFG.get("loop", {}).get("fsm_tick_delay", 0.5),
    "planner_interval": CFG.get("loop", {}).get("planner_interval", 60),
    "mutation_watch_interval": CFG.get("loop", {}).get("mutation_watch_interval", 10),
    "planner_enabled": CFG.get("loop", {}).get("planner_enabled", True),
    "mutation_enabled": CFG.get("loop", {}).get("mutation_enabled", True),
    "self_training_enabled": CFG.get("loop", {}).get("self_training_enabled", True),
}

# Role assignments
ROLES = CFG.get("roles", {
    "planner": "planner_agent", "executor": "tool_executor", 
    "trainer": "feedback_loop", "kernel": "code_mutator",
})

# Memory placeholder for runtime state
MEM = {}

# ========================================================================================
# DASHBOARD BACKEND MANAGEMENT
# ========================================================================================

def set_dashboard_backend(backend):
    """Update the dashboard selected backend in config and memory"""
    global MEMORY
    if backend in ["faiss", "chroma"]:
        MEMORY["vector_backend"] = backend
        CFG["memory"]["dashboard_selected_backend"] = backend
        try:
            if HAS_TOML and toml:
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

# ========================================================================================
# COMPREHENSIVE EXPORTS
# ========================================================================================

__all__ = [
    # Standard library modules
    'os', 'sys', 'json', 'time', 'logging', 'asyncio', 'threading', 'pathlib', 'datetime',
    'collections', 'subprocess', 'tempfile', 'traceback', 'hashlib', 'shutil', 'signal',
    'uuid', 'math', 'random', 're', 'ast', 'argparse', 'typing', 'dataclasses', 'enum',
    'timedelta', 'timezone', 'defaultdict', 'Counter', 'Dict', 'List', 'Optional', 'Any', 'Union',
    
    # Third-party modules (when available)
    'flask', 'Flask', 'Blueprint', 'request', 'jsonify', 'render_template',
    'np', 'pd', 'requests', 'aiohttp', 'nltk', 'word_tokenize', 'torch', 'transformers',
    'schedule', 'pytest', 'async_playwright', 'toml',
    
    # Configuration and paths
    'CFG', 'logger', 'resolve_path', 'CONFIG_PATH', 'MEMORY_JSON',
    'BASE_DIR', 'DATA_DIR', 'MODELS_DIR', 'CHECKPOINTS_DIR', 'LOG_FILE',
    'VECTOR_STORE_PATH', 'FAISS_PATH', 'CHROMA_PATH', 'FAISS_INDEX_FILE', 'CHROMA_DB',
    'LOCAL_INDEX_PATH', 'LOCAL_DB', 'METADATA_DB_PATH',
    'HARDWARE', 'NLP', 'AGENT', 'SCRAPER', 'MEMORY', 'SYSTEM', 'LOOP', 'ROLES', 'MEM',
    
    # Core system functions
    'boot_loop', 'build_tree', 'verify_snapshot', 'rollback', 'snapshot_file', 'sha256_file',
    'save_state', 'load_state', 'register_routes', 'route_task',
    
    # NLP functions and classes
    'clean_text', 'tokenize', 'diff_texts', 'diff_files', 'get_pos_tags', 'classify_intent',
    'extract_code_entities', 'detect_financial_terms', 'parse_nlp', 'encode',
    'ChatSession', 'MiniMultiHeadAttention',
    
    # Agent core functions and classes
    'fsm_loop', 'get_fsm_status', 'step_fsm', 'reset_fsm', 'fsm_inject_task',
    'enqueue_task', 'get_all_tasks', 'fetch_task', 'reprioritize', 'TaskQueue',
    'evaluate_task', 'log_error', 'JsonlFormatter',
    
    # Trading functions
    'repair_signal_index', 'generate_signals', 'get_signal_history', 'apply_signal_rules',
    'estimate_batch', 'estimate_tax', 'get_live_penny_stocks', 'simulate_technical_indicators',
    'route_scraping', 'simulate_fallback',
    
    # Memory functions
    'embed_text', 'inject_watermark', 'package_embedding', 'get_all_embeddings', 'repair_index',
    'search_memory', 'log_event', 'load_history',
    
    # Self-training functions and classes
    'is_valid_python', 'mutate_dataset', 'extract_training_data', 'hash_entry',
    'schedule_extraction', 'generate_datasets', 'tag_event', 'check_trigger',
    'inject_feedback', 'clear_trigger', 'LogEventHandler',
    
    # Scraper functions
    'extract_dom_structure', 'store_scrape_to_memory', 'run_search_and_scrape',
    'parse_stt_data', 'locate_stt_paths', 'safe_scrape_stt', 'locate_tws_files',
    'parse_tws_json', 'safe_scrape_tws',
    
    # Agent classes and functions
    'AgentCoordinator', 'get_agent_coordinator', 'DataAnalystAgent', 'AnomalyReport',
    'get_data_analyst_agent', 'LearningGoal', 'PerformanceMetric', 'LearningAgent',
    'get_learning_agent',
    
    # Executor functions
    'run_shell_command', 'execute_tool',
    
    # Tools and utilities
    'evaluate_with_diff', 'top_rewarded_tasks', 'log_reward', 'evaluate_result',
    'get_reward_feed',
    
    # Backend API functions
    'chat', 'graph', 'set_task_priority', 'list_tasks', 'get_signals', 'mutation_notify',
    'summarize_text',
    
    # Utility functions
    'setup_module_logger', 'get_module_logger', 'create_all_module_loggers',
    
    # Dashboard management
    'set_dashboard_backend', 'get_dashboard_backend',
    
    # Safe import helpers
    'safe_import_function', 'safe_import_class', 'safe_import_module',
    
    # Availability flags
    'HAS_TOML', 'HAS_FLASK', 'HAS_NUMPY', 'HAS_PANDAS', 'HAS_REQUESTS', 'HAS_AIOHTTP',
    'HAS_NLTK', 'HAS_TORCH', 'HAS_TRANSFORMERS', 'HAS_SCHEDULE', 'HAS_PYTEST',
    'HAS_PLAYWRIGHT', 'HAS_LOGGER'
]

logger.info(f"[GLOBALS] Centralized import management loaded successfully. {len(__all__)} items exported.")
