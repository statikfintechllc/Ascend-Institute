# agents/planner_agent.py

from agent_core.task_queue import global_queue
from tools.reward_model import top_rewarded_tasks
from memory.vector_store import embedder
from backend.globals import logger
from datetime import datetime
import random

AGENT_NAME = "planner_agent"

def inspect_task_queue():
    current = global_queue.dump()
    logger.info(f"[{AGENT_NAME}] Found {len(current)} task(s) queued.")
    return current

def analyze_rewards():
    top = top_rewarded_tasks(n=5)
    logger.info(f"[{AGENT_NAME}] Top historical rewards:")
    for t in top:
        logger.info(f"  - {t['task']} ({t['reward']}) => {t['reason']}")
    return top

def plan_next_task():
    """Plans next task based on reward feedback and heuristics."""
    top = analyze_rewards()
    history_types = [r["task"] for r in top]

    # Select one with weighted randomness
    if history_types:
        choice = random.choices(history_types, weights=[r["reward"] for r in top], k=1)[0]
    else:
        choice = "scrape"

    planned = {
        "type": choice,
        "meta": {
            "source": AGENT_NAME,
            "timestamp": datetime.utcnow().isoformat()
        }
    }
    logger.info(f"[{AGENT_NAME}] Planning next task: {choice}")
    return planned

def enqueue_next():
    task = plan_next_task()
    global_queue.enqueue(task)
    logger.success(f"[{AGENT_NAME}] Enqueued task: {task['type']}")

def planner_loop(cycles=3):
    logger.info(f"[{AGENT_NAME}] Starting planner loop for {cycles} cycles.")
    for _ in range(cycles):
        enqueue_next()

if __name__ == "__main__":
    planner_loop(3)
