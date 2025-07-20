#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Centralized Logging Configuration

import os
import sys
from pathlib import Path
from loguru import logger

# Define custom logging level 'log_history'
logger.level("log_history", no=25, color="<yellow>", icon="📝")

# Define custom logging level 'globals'
logger.level("globals", no=30, color="<blue>", icon="🌐")

# Define custom logging level 'task_queue'
logger.level("task_queue", no=20, color="<cyan>", icon="📋")

# Define custom logging level 'state_manager'
logger.level("state_manager", no=25, color="<magenta>", icon="🗂")

# Define custom logging level 'orchestrator'
logger.level("orchestrator", no=30, color="<green>", icon="🔄")

# Define custom logging level 'data_analyst'
logger.level("data_analyst", no=35, color="<yellow>", icon="📊")

# Define custom logging level 'trading_strategist'
logger.level("trading_strategist", no=40, color="<red>", icon="📈")

# Define custom logging level 'learning_agent'
logger.level("learning_agent", no=45, color="<blue>", icon="📘")

# Define custom logging level 'coordinator'
logger.level("coordinator", no=50, color="<magenta>", icon="🤝")

# Define custom logging level 'integration'
logger.level("integration", no=55, color="<cyan>", icon="🔗")

# Base logging directory - use project directory instead of home
project_root = Path(__file__).parent.parent
BASE_LOG_DIR = project_root / "data" / "logs"

def setup_module_logger(module_name, param2="INFO"):
    """
    Setup dedicated logger for a specific module
    
    Args:
        module_name (str): Name of the module (e.g., 'backend', 'nlp_engine', 'scraper')
        param2 (str): Either log_level (DEBUG, INFO, WARNING, ERROR, CRITICAL) 
                     or submodule_name (for backward compatibility)
    
    Returns:
        logger: Configured logger instance
    """
    # Determine if param2 is a log level or submodule name
    valid_log_levels = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
    if param2.upper() in valid_log_levels:
        log_level = param2.upper()
        submodule = None
    else:
        # Backward compatibility: param2 is submodule name
        log_level = "INFO"
        submodule = param2
    
    # Ensure log directory exists
    module_log_dir = BASE_LOG_DIR / module_name
    module_log_dir.mkdir(parents=True, exist_ok=True)
    
    # Set proper permissions
    os.chmod(str(module_log_dir), 0o755)
    
    # Configure module-specific log file (include submodule if provided)
    if submodule:
        log_file = module_log_dir / f"{module_name}_{submodule}.log"
    else:
        log_file = module_log_dir / f"{module_name}.log"
    
    # Remove existing handlers for this module to avoid duplicates
    logger.remove()
    
    # Add module-specific file handler
    logger.add(
        str(log_file),
        rotation="10 MB",
        retention="30 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}",
        enqueue=True,
        backtrace=True,
        diagnose=True
    )
    
    # Add console handler for development
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # Set file permissions
    if log_file.exists():
        os.chmod(str(log_file), 0o644)
    
    logger.info(f"[LOGGING] Module logger initialized for {module_name} -> {log_file}")
    return logger

def get_module_logger(module_name, log_level="INFO"):
    """
    Get or create a logger for a specific module
    
    Args:
        module_name (str): Name of the module
        log_level (str): Logging level
    
    Returns:
        logger: Configured logger instance
    """
    return setup_module_logger(module_name, log_level)

def create_all_module_loggers():
    """
    Create loggers for all major system modules
    """
    modules = [
        'backend', 'nlp_engine', 'memory', 'scraper', 'agents', 
        'trading_core', 'tools', 'core', 'executors', 'self_training',
        'self_mutation_watcher', 'utils', 'tests', 'frontend'
    ]
    
    for module in modules:
        setup_module_logger(module)
    
    logger.success(f"[LOGGING] Initialized loggers for {len(modules)} modules")

if __name__ == "__main__":
    create_all_module_loggers()
