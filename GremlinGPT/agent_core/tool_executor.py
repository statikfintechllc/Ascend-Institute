#─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
#─────────────────────────────────────────────────────────────
#!/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# agent_core/tool_executor.py

import asyncio
from datetime import datetime
from scraper.scraper_loop import get_dom_html
from nlp_engine.transformer_core import encode
from memory.vector_store.embedder import package_embedding, inject_watermark
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
    timestamp = datetime.utcnow().isoformat()

    try:
        logger.info(f"[TOOL] Executing task: {task_type}")

        if task_type == "scrape":
            dom = asyncio.run(get_dom_html(target))
            preview = dom[:100]
            result = {"scraped": preview}
            reward = evaluate_result(task_type, preview)
            log_reward(reward)
            vector = encode(preview)
            package_embedding(
                preview, vector, {"task": task_type, "timestamp": timestamp}
            )
            inject_watermark(origin="tool::scrape")
            log_event(
                "exec", task_type, {"preview": preview}, status="success", meta=reward
            )
            return result

        elif task_type == "signal_scan":
            signals = generate_signals()
            result = {"signals": signals}
            reward = evaluate_result(task_type, str(signals))
            log_reward(reward)
            vector = encode(str(signals))
            package_embedding(
                str(signals), vector, {"task": task_type, "timestamp": timestamp}
            )
            inject_watermark(origin="tool::signal_scan")
            log_event(
                "exec", task_type, {"signals": signals}, status="success", meta=reward
            )
            return result

        elif task_type == "nlp":
            vec = encode(target)
            vector_list = vec.tolist()
            package_embedding(
                target,
                vec,
                {
                    "origin": "tool_executor",
                    "task_type": task_type,
                    "timestamp": timestamp,
                },
            )
            inject_watermark(origin="tool::nlp")
            result = {"embedding": vector_list}
            reward = evaluate_result(task_type, target)
            log_reward(reward)
            log_event(
                "exec", task_type, {"embedded": True}, status="success", meta=reward
            )
            return result

        elif task_type == "self_train":
            inject_feedback()
            inject_watermark(origin="tool::self_train")
            result = {"trained": True}
            log_event(
                "exec",
                task_type,
                result,
                status="success",
                meta={"timestamp": timestamp},
            )
            return result

        elif task_type == "shell":
            output = run_shell_command(task["command"])
            preview = output[:500]
            reward = evaluate_result(task_type, preview)
            log_reward(reward)
            vector = encode(preview)
            package_embedding(
                preview, vector, {"task": task_type, "timestamp": timestamp}
            )
            inject_watermark(origin="tool::shell")
            result = {"shell_result": preview}
            log_event("exec", task_type, result, status="success", meta=reward)
            return result

        else:
            error_msg = f"Unknown task type: {task_type}"
            logger.error(f"[TOOL] {error_msg}")
            log_event(
                "exec", task_type, {"error": error_msg}, status="error", meta=meta
            )
            raise ValueError(error_msg)

    except Exception as e:
        logger.error(f"[TOOL] Execution error for {task_type}: {e}")
        log_event("exec", task_type, {"error": str(e)}, status="failure", meta=meta)
        return {"error": str(e), "success": False}
