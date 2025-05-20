from agent_core.task_queue import enqueue_task
from backend.globals import CFG
from loguru import logger


def parse_command(cmd_text):
    if "scrape" in cmd_text:
        return {"type": "scrape", "target": cmd_text.split()[-1]}
    elif "scan" in cmd_text:
        return {"type": "signal_scan"}
    elif "train" in cmd_text:
        return {"type": "self_train"}
    return {"type": "unknown", "payload": cmd_text}


def execute_command(cmd):
    if cmd["type"] in ["scrape", "signal_scan", "self_train"]:
        enqueue_task(cmd)
        if CFG["agent"]["log_agent_output"]:
            logger.info(f"[COMMAND] Queued: {cmd}")
        return {"status": "queued", "task": cmd}
    else:
        return {"status": "error", "message": "Unknown command."}

def update_task_priority(task_id, new_priority):
    from agent_core.task_queue import task_queue, task_meta, task_status
    for level in task_queue:
        for task in list(task_queue[level]):
            if task["id"] == task_id:
                task_queue[level].remove(task)
                task["priority"] = new_priority
                task_meta[task_id]["priority"] = new_priority
                task_queue[new_priority].append(task)
                task_status[task_id] = "reprioritized"
                return True
    return False
