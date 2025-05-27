# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import asyncio
import time
from scraper.playwright_handler import get_dom_html
from scraper.page_simulator import store_scrape_to_memory
from backend.globals import CFG, logger
from agent_core.task_queue import fetch_task
from memory.log_history import log_event
from datetime import datetime

MODULE = "scraper_loop"


async def run_scraper():
    logger.info(f"[{MODULE.upper()}] Autonomous loop engaged.")
    interval = CFG["scraper"].get("scrape_interval_sec", 10)

    while True:
        loop_start = time.time()
        tick_time = datetime.utcnow().isoformat()
        log_event(MODULE, "tick_start", {"timestamp": tick_time})

        task = fetch_task("scrape")

        if task:
            logger.info(f"[{MODULE.upper()}] Acquired task: {task}")
            try:
                dom = await get_dom_html(task["target"])
                store_scrape_to_memory(task["target"], dom)
                logger.success(f"[{MODULE.upper()}] Stored scrape snapshot from {task['target']}")
                log_event(MODULE, "task_complete", {"target": task["target"]}, status="success")
            except Exception as e:
                logger.error(f"[{MODULE.upper()}] Scrape failed: {e}")
                log_event(MODULE, "task_error", {"error": str(e)}, status="fail")
        else:
            logger.debug(f"[{MODULE.upper()}] No pending scrape task.")

        elapsed = time.time() - loop_start
        logger.debug(f"[{MODULE.upper()}] Cycle completed in {elapsed:.2f} sec.")
        await asyncio.sleep(interval)


if __name__ == "__main__":
    asyncio.run(run_scraper())
