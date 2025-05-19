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

def analyze_rewards():
    top = top_rewarded_tasks(n=5)
    logger.info(f"[{AGENT_NAME}] Top reward signals:")
    for t in top:
        logger.info(f"  - {t['task']} [Score: {t['reward']}] Reason: {t['reason']}")
    return top

def plan_next_task():
    top = analyze_rewards()
    history_types = [r["task"] for r in top]

    if history_types:
        choice = random.choices(history_types, weights=[r["reward"] for r in top], k=1)[0]
        logger.debug(f"[{AGENT_NAME}] Selected based on reward heuristic: {choice}")
    else:
        choice = "scrape"
        logger.debug(f"[{AGENT_NAME}] Default fallback task used: {choice}")

    planned = {
        "type": choice,
        "meta": {
            "source": AGENT_NAME,
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    # Semantic memory embedding of the planned task
    vector = embedder.embed_text(f"Planned task: {choice}")
    embedder.package_embedding(
        text=f"Planned task: {choice}",
        vector=vector,
        meta={
            "agent": AGENT_NAME,
            "task_type": choice,
            "reason": "reward-guided",
            "timestamp": planned["meta"]["timestamp"]
        }
    )

    logger.info(f"[{AGENT_NAME}] Planned next task: {choice}")
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
