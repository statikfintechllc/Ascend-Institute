import time
import schedule
from rich.console import Console
from datetime import datetime

from agent_core.task_queue import TaskQueue, reprioritize, promote_old_tasks
from agent_core.tool_executor import execute_tool
from agent_core.heuristics import evaluate_task
from agent_core.error_log import log_error
from agents.planner_agent import enqueue_next

from backend import globals as G
from memory.log_history import log_event
from self_mutation_watcher.watcher import scan_and_diff
from self_mutation_watcher.mutation_daemon import run_daemon

FSM_STATE = "IDLE"
console = Console()
task_queue = TaskQueue(retry_limit=G.AGENT["task_retry_limit"])
tick_delay = G.CFG.get("loop", {}).get("fsm_tick_delay", 0.5)


def fsm_loop():
    global FSM_STATE
    FSM_STATE = "RUNNING"
    tick_time = datetime.utcnow().isoformat()
    console.log(f"[FSM] Tick start @ {tick_time}")

    try:
        promote_old_tasks()
    except Exception as e:
        console.log(f"[FSM] Priority escalation failed: {e}")

    while not task_queue.is_empty():
        task = task_queue.get_next()
        if not task:
            FSM_STATE = "IDLE"
            break

        log_event("fsm", "task_start", {"task": task}, status="begin")

        try:
            if evaluate_task(task):
                result = execute_tool(task)
                console.log(f"[FSM] {task['type']} => {result}")
                log_event("fsm", "task_exec", {"task": task, "result": result})
            else:
                console.log(f"[FSM] Skipped: {task}")
                log_event("fsm", "task_skipped", {"task": task}, status="skip")
        except Exception as e:
            log_error(task, e)
            task_queue.retry(task)
            log_event("fsm", "task_error", {"task": task, "error": str(e)}, status="fail")

            # Priority escalation for repeatedly failing tasks
            tid = task.get("id")
            retries = task_queue.task_meta.get(tid, {}).get("retries", 0)
            if retries >= 2:
                reprioritize(tid, "high")
                console.log(f"[FSM] Reprioritized failing task {tid} to HIGH")

        try:
            scan_and_diff()
        except Exception as e:
            console.log(f"[FSM] Diff scan error: {e}")
            log_event("fsm", "diff_error", {"error": str(e)}, status="warn")

        time.sleep(tick_delay)

    # Autonomous planner injection
    if task_queue.is_empty():
        console.log("[FSM] Queue empty — invoking planner to enqueue new task.")
        try:
            enqueue_next()
        except Exception as e:
            console.log(f"[FSM] Planner enqueue failed: {e}")

    FSM_STATE = "IDLE"
    console.log("[FSM] Queue cleared.")
    log_event("fsm", "loop_complete", {}, status="idle")


def run_schedule():
    run_daemon()
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
