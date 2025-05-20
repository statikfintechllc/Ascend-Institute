# agents/planner_agent.py

from agent_core.task_queue import global_queue, reprioritize
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
    weak_signals = [t for t in top if t['reward'] < threshold]
    return top, weak_signals

def adjust_priorities(weak_signals):
    """
    Reprioritize queued tasks that match weak signal types.
    """
    queue = global_queue.dump()
    affected_types = {w['task'] for w in weak_signals}
    count = 0

    for level in queue:
        for task in queue[level]:
            tid = task.get("id")
            if task["type"] in affected_types:
                if reprioritize(tid, "high"):
                    logger.debug(f"[{AGENT_NAME}] Boosted priority of task {tid}")
                    count += 1
    if count:
        logger.info(f"[{AGENT_NAME}] Reprioritized {count} tasks due to low confidence.")

def plan_next_task():
    top, weak = analyze_rewards()
    adjust_priorities(weak)

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

    desc = f"Planned task: {choice} via {reason}"
    vector = embedder.embed_text(desc)
    embedder.package_embedding(
        text=desc,
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
