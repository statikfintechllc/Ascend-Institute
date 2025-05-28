# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import psutil
import random
from loguru import logger


def evaluate_task(task):
    """
    Evaluates whether a task should be executed based on system load and entropy.

    Args:
        task (dict): Task dictionary with at minimum a 'type' key.

    Returns:
        bool: True if the task should be processed, False otherwise.
    """
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    entropy = random.random()

    decision = cpu < 80 and mem < 85 and entropy > 0.1

    logger.debug(f"[HEURISTICS] Task={task.get('type')} | CPU={cpu} | MEM={mem} | RNG={entropy:.2f} | Decision={decision}")
    
    return decision
