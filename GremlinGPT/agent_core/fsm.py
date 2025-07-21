#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: FSM Core & Module Integrity Directive

from backend.globals import (
    schedule, logging_config, nltk_setup, task_queue, heuristics, error_log, agent_profiles,
    planner_agent, backend_globals, backend_utils, router, scheduler, server, state_manager,
    git_ops, embedder, log_history, watcher, mutation_daemon, generate_dataset, kernel,
    CFG, logger, resolve_path, DATA_DIR, MEM
)

from backend.api.api_endpoints import *
from backend.router import route_task


NLTK_DATA_DIR = nltk_setup.setup_nltk_data() if nltk_setup else None

FSM_STATE = "IDLE"
console = None
task_queue = CFG["task_queue"] if "task_queue" in CFG else None
tick_delay = CFG.get("loop", {}).get("fsm_tick_delay", 0.5)
DATASET_PATH = resolve_path(CFG["paths"].get("dataset_path", "data/nlp_training_sets/auto_generated.jsonl"))
LOG_CRASH_PATH = resolve_path(CFG["paths"].get("log_crash_path", "data/logs/fsm_crash.log"))


def auto_push():
    return auto_commit()


def fsm_loop():
    return route_task("fsm_loop")


def run_schedule():
    return route_task("run_schedule")


if __name__ == "__main__":
    route_task("main")


def get_fsm_status():
    return route_task("get_fsm_status")


def reset_fsm():
    return route_task("reset_fsm")


def inject_task(task):
    return route_task("inject_task", task)
