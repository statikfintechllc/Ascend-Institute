# agent_core/fsm.py

import os
import time
import shutil
import schedule
from rich.console import Console
from datetime import datetime
from agent_core.task_queue import TaskQueue, reprioritize, promote_old_tasks
from agent_core.tool_executor import execute_tool
from agent_core.heuristics import evaluate_task
from agent_core.error_log import log_error
from agents.planner_agent import enqueue_next
from backend import globals as G
from memory.vector_store.embedder import inject_watermark
from memory.log_history import log_event
from self_mutation_watcher.watcher import scan_and_diff
from self_mutation_watcher.mutation_daemon import run_daemon
from tools.generate_dataset import generate_datasets

FSM_STATE = "IDLE"
console = Console()
task_queue = TaskQueue(retry_limit=G.AGENT["task_retry_limit"])
tick_delay = G.CFG.get("loop", {}).get("fsm_tick_delay", 0.5)


def archive_dataset(output_path):
    if not os.path.exists(output_path):
        return
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    archive_name = f"GremlinGPT/docs/dataset_dump_{timestamp}.jsonl"
    shutil.copyfile(output_path, archive_name)
    console.log(f"[FSM] Dataset backup created → {archive_name}")


def auto_commit(backup_file):
    try:
        os.system(f"git add {backup_file}")
        os.system(f'git commit -m "[autocommit] Dataset updated by FSM loop"')
        console.log("[FSM] Autocommit completed.")
    except Exception as e:
        console.log(f"[FSM] Git autocommit failed: {e}")


def auto_push():
    try:
        branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
        push_cmd = f"git push origin {branch}"
        result = os.system(push_cmd)
        if result == 0:
            console.log(f"[FSM] Git pushed to origin/{branch}.")
        else:
            console.log(f"[FSM] Git push failed with exit code: {result}")
    except Exception as e:
        console.log(f"[FSM] Git push error: {e}")


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
            log_event(
                "fsm", "task_error", {"task": task, "error": str(e)}, status="fail"
            )

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

    if task_queue.is_empty():
        console.log("[FSM] Queue empty — invoking planner to enqueue new task.")
        try:
            enqueue_next()
        except Exception as e:
            console.log(f"[FSM] Planner enqueue failed: {e}")

        try:
            inject_watermark(origin="fsm_loop")
            console.log("[FSM] Memory watermark injected.")
        except Exception as e:
            console.log(f"[FSM] Watermark injection failed: {e}")

        dataset_path = "data/nlp_training_sets/auto_generated.jsonl"
        try:
            generate_datasets(root_dir=".", output_file=dataset_path)
            console.log("[FSM] Training dataset updated.")
            archive_dataset(dataset_path)
            auto_commit(f"GremlinGPT/docs/dataset_dump_*.jsonl")

            if G.CFG.get("git", {}).get("auto_push", False):
                auto_push()
        except Exception as e:
            console.log(f"[FSM] Dataset generation failed: {e}")

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
