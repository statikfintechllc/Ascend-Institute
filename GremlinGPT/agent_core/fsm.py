# agent_core/fsm.py

import time
import schedule
from rich.console import Console
from agent_core.task_queue import TaskQueue
from agent_core.tool_executor import execute_tool
from agent_core.heuristics import evaluate_task
from agent_core.error_log import log_error
from backend import globals as G
from self_mutation_watcher.watcher import scan_and_diff
from self_mutation_watcher.mutation_daemon import run_daemon

FSM_STATE = "IDLE"
console = Console()
task_queue = TaskQueue(retry_limit=G.AGENT["task_retry_limit"])


def fsm_loop():
    global FSM_STATE
    FSM_STATE = "RUNNING"
    console.log("[FSM] Loop started.")

    while not task_queue.is_empty():
        task = task_queue.get_next()
        if not task:
            FSM_STATE = "IDLE"
            break

        try:
            if evaluate_task(task):
                result = execute_tool(task)
                console.log(f"[FSM] {task['type']} => {result}")
            else:
                console.log(f"[FSM] Skipped: {task}")
        except Exception as e:
            log_error(task, e)
            task_queue.retry(task)

        try:
            scan_and_diff()
        except Exception as e:
            console.log(f"[FSM] Diff scan error: {e}")

        time.sleep(0.5)

    FSM_STATE = "IDLE"
    console.log("[FSM] Queue cleared.")


def run_schedule():
    run_daemon()  # Persistent mutation daemon thread
    schedule.every(30).seconds.do(fsm_loop)

    console.log("[FSM] Scheduler engaged.")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    task_queue.enqueue({"type": "scrape"})
    task_queue.enqueue({"type": "signal_scan"})
    task_queue.enqueue({"type": "nlp", "text": "What is support and resistance?"})
    run_schedule()
