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
