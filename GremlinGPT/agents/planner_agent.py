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
    logger.info(f"[{AGENT_NAME}] Found {len(current)} task(s) in queue.")
    return current

def analyze_rewards(threshold=0.4):
    top = top_rewarded_tasks(n=10)
    logger.info(f"[{AGENT_NAME}] Top reward signals:")
    for t in top:
        logger.info(f"  - {t['task']} [Score: {t['reward']}] Reason: {t['reason']}")
    # Filter low confidence signals to reprocess
    weak_signals = [t for t in top if t['reward'] < threshold]
    return top, weak_signals

def plan_next_task():
    top, weak = analyze_rewards()

    # Prefer retrying low-reward tasks with intelligent fallback
    if weak:
        choice = weak[0]["task"]
        reason = "reprocessing_low_confidence"
    elif top:
        choice = random.choices(
            [t["task"] for t in top],
            weights=[t["reward"] for t in top],
            k=1
        )[0]
        reason = "reward_guided"
    else:
        choice = "scrape"
        reason = "fallback_scrape"

    planned = {
        "type": choice,
        "meta": {
            "source": AGENT_NAME,
            "timestamp": datetime.utcnow().isoformat(),
            "strategy": reason
        }
    }

    # Semantic memory embedding of the planned task
    text_desc = f"Planned task: {choice} via {reason}"
    vector = embedder.embed_text(text_desc)
    embedder.package_embedding(
        text=text_desc,
        vector=vector,
        meta={
            "agent": AGENT_NAME,
            "task_type": choice,
            "reason": reason,
            "timestamp": planned["meta"]["timestamp"]
        }
    )

    logger.info(f"[{AGENT_NAME}] Planned next task: {choice} [{reason}]")
    return planned

def enqueue_next():
    task = plan_next_task()
    global_queue.enqueue(task)
    logger.success(f"[{AGENT_NAME}] Enqueued task: {task['type']}")

def planner_loop(cycles=3):
    logger.info(f"[{AGENT_NAME}] Starting planner loop with {cycles} cycles.")
    for _ in range(cycles):
        enqueue_next()

if __name__ == "__main__":
    planner_loop(3)
