# agent_core/tool_executor.py

import asyncio
from datetime import datetime
from scraper.scraper_loop import get_dom_html
from nlp_engine.transformer_core import encode
from memory.vector_store.embedder import package_embedding
from trading_core.signal_generator import generate_signals
from self_training.feedback_loop import inject_feedback
from agent_shell.shell_executor import run_shell_command
from tools.reward_model import evaluate_result, log_reward
from memory.log_history import log_event
from backend.globals import logger


def execute_tool(task):
    task_type = task.get("type")
    target = task.get("target", "")
    meta = task.get("meta", {})

    try:
        logger.info(f"[TOOL] Executing task: {task_type}")

        if task_type == "scrape":
            dom = asyncio.run(get_dom_html(target))
            preview = dom[:100]
            log_event(
                "exec", task_type, {"preview": preview}, status="success", meta=meta
            )
            return {"scraped": preview}

        elif task_type == "signal_scan":
            signals = generate_signals()
            log_event(
                "exec", task_type, {"signals": signals}, status="success", meta=meta
            )
            return signals

        elif task_type == "nlp":
            vec = encode(target)
            vector_list = vec.tolist()
            meta_embed = {
                "origin": "tool_executor",
                "task_type": "nlp",
                "timestamp": datetime.utcnow().isoformat(),
            }
            package_embedding(target, vec, meta_embed)
            log_event(
                "exec", task_type, {"embedded": True}, status="success", meta=meta_embed
            )
            return {"embedding": vector_list}

        elif task_type == "self_train":
            inject_feedback()
            log_event(
                "exec", task_type, {"triggered": True}, status="success", meta=meta
            )
            return {"trained": True}

        elif task_type == "shell":
            output = run_shell_command(task["command"])
            preview = output[:500]
            reward = evaluate_result("shell", preview)
            log_reward(reward)
            log_event(
                "exec",
                task_type,
                {"shell_preview": preview},
                status="success",
                meta=reward,
            )
            return {"shell_result": preview}

        else:
            logger.error(f"[TOOL] Unknown task type: {task_type}")
            log_event(
                "exec",
                task_type,
                {"error": "Unknown task type"},
                status="error",
                meta=meta,
            )
            raise ValueError("Unknown task type")

    except Exception as e:
        logger.error(f"[TOOL] Execution error for {task_type}: {e}")
        log_event("exec", task_type, {"error": str(e)}, status="failure", meta=meta)
        return {"error": str(e), "success": False}
