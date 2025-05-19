import os
import sys
import time
import logging
import traceback
import requests
from pathlib import Path
from multiprocessing import Process
import psutil
from core.model_interface import auto_remediate_failed_tasks
from langgraph_core import build_gremlin_graph

# === Optional advanced modules ===
try:
    import ray

    ray.init(ignore_reinit_error=True)
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# === Paths & Config ===
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
DASHBOARD_HEARTBEAT_URL = os.getenv(
    "DASHBOARD_HEARTBEAT_URL", "http://localhost:5000/heartbeat"
)

# === Core System ===
from core.decision import decision_node
from core.model_interface import ask_model
from core.docker_runner import run_code_in_docker
from memory.vector_memory import recall_context, store_context
from memory.planning_memory import log_plan, get_pending_plans
from memory.task_journal import log_task_event
from alerts.discord import send_discord_alert
from alerts.telegram import send_telegram_alert
from tools import tool_registry

# Optional instance orchestration
try:
    from tools.instance_orchestrator import maybe_spawn_instance
except ImportError:
    maybe_spawn_instance = lambda task: None  # placeholder

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Optional GPU Ray Tasks ===
@ray.remote(num_gpus=1)
def remote_tool_run(name, params):
    return tool_registry[name](**params)


@ray.remote(num_gpus=1)
def remote_docker_run(code):
    return run_code_in_docker(code)


# === Task Execution Logic ===
def handle_task(task):
    try:
        logger.info(f"Processing task: {task['task']}")
        context = recall_context(task["task"])
        action = decision_node(task["task"], context)

        if action["type"] == "tool":
            if GPU_AVAILABLE:
                result = ray.get(
                    remote_tool_run.remote(action["name"], action["params"])
                )
            else:
                result = tool_registry[action["name"]](**action["params"])

        elif action["type"] == "code":
            if GPU_AVAILABLE:
                result = ray.get(remote_docker_run.remote(action["code"]))
            else:
                result = run_code_in_docker(action["code"])

        elif action["type"] == "shell":
            result = os.popen(action["command"]).read()

        elif action["type"] == "quantum":
            result = "[TODO] Quantum task placeholder."

        else:
            result = "[UNKNOWN] Invalid action type."

        store_context(task["task"], result)
        log_plan(task["task"], task.get("reason", "no-reason"), outcome="completed")
        log_task_event(task["task"], "completed", str(result))
        send_discord_alert(f"[COMPLETE] '{task['task']}' → {result}")
        send_telegram_alert(f"[COMPLETE] '{task['task']}' → {result}")

    except Exception as e:
        err = traceback.format_exc()
        log_task_event(task["task"], "error", str(e))
        log_plan(task["task"], task.get("reason", "unknown"), outcome="error")
        logger.error(f"[FAILURE] {task['task']} errored: {err}")
        send_discord_alert(f"[ERROR] '{task['task']}' → {e}")
        send_telegram_alert(f"[ERROR] '{task['task']}' → {e}")
        maybe_spawn_instance(task)


# Right after handling tasks:
auto_remediate_failed_tasks()

gremlin_graph = build_gremlin_graph()


def handle_task(task):
    try:
        logger.info(f"Processing task: {task['task']}")
        context = recall_context(task["task"])
        action = decision_node(task["task"], context)

        # === Agent Decision Execution ===
        if action["type"] == "agent":
            logger.info("[Agent Mode] Executing via LangGraph")
            result = gremlin_graph.run(task["task"])

        # === Tool Dispatch ===
        elif action["type"] == "tool":
            result = tool_registry[action["name"]](**action["params"])

        # === Code Execution ===
        elif action["type"] == "code":
            result = run_code_in_docker(action["code"])

        # === Shell Execution ===
        elif action["type"] == "shell":
            result = os.popen(action["command"]).read()

        # === Fallback
        else:
            result = "[UNKNOWN] Action type not understood."

        # Log + Persist Outcome
        store_context(task["task"], result)
        log_plan(task["task"], task.get("reason", "unknown"), outcome="completed")
        send_discord_alert(f"Task '{task['task']}' complete: {result}")
        send_telegram_alert(f"Task '{task['task']}' complete: {result}")

    except Exception as e:
        logger.error(f"[FAILURE] {task['task']} blew up: {e}")
        send_discord_alert(f"[ERROR] Task failed: {e}")
        send_telegram_alert(f"[ERROR] Task failed: {e}")
        log_plan(task["task"], task.get("reason", "unknown"), outcome="error")


# === Main Loop ===
def gremlin_loop():
    logger.info("[GremlinGPT] Loop initialized.")
    while True:
        try:
            # Send heartbeat to dashboard
            try:
                requests.post(DASHBOARD_HEARTBEAT_URL, json={"status": "alive"})
            except Exception as ping_err:
                logger.warning(f"[Heartbeat] Dashboard ping failed: {ping_err}")

            # RAM Check
            if psutil.virtual_memory().percent > 90:
                logger.warning("[System] Memory high. Sleeping...")
                time.sleep(30)
                continue

            tasks = get_pending_plans()
            if not tasks:
                logger.info("[System] No tasks. Idling...")
                time.sleep(30)
                continue

            for task in tasks:
                handle_task(task)

            time.sleep(5)

        except Exception as loop_error:
            err = traceback.format_exc()
            logger.error(f"[LOOP ERROR] {err}")
            send_discord_alert(f"[LOOP FAIL] {loop_error}")
            send_telegram_alert(f"[LOOP FAIL] {loop_error}")
            time.sleep(30)


# Right after handling tasks:
auto_remediate_failed_tasks()

# === Optional Threaded Version ===
def start_gremlin_loop_threaded():
    p = Process(target=gremlin_loop)
    p.start()
    return p


if __name__ == "__main__":
    gremlin_loop()
