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

# scraper/scraper_loop.py

import asyncio
import time
from scraper.playwright_handler import get_dom_html
from scraper.page_simulator import store_scrape_to_memory
from backend.globals import CFG
from agent_core.task_queue import fetch_task
from loguru import logger


async def run_scraper():
    logger.info("[SCRAPER] Loop started.")
    while True:
        loop_start = time.time()
        task = fetch_task("scrape")

        if task:
            logger.info(f"[SCRAPER] New task: {task}")
            try:
                dom = await get_dom_html(task["target"])
                store_scrape_to_memory(task["target"], dom)
                logger.success(f"[SCRAPER] Stored DOM snapshot from {task['target']}")
            except Exception as e:
                logger.error(f"[SCRAPER] Error scraping {task['target']}: {e}")
        else:
            logger.debug("[SCRAPER] No scrape task available.")

        elapsed = time.time() - loop_start
        logger.debug(f"[SCRAPER] Loop cycle completed in {elapsed:.2f} sec.")
        await asyncio.sleep(CFG["scraper"]["scrape_interval_sec"])


if __name__ == "__main__":
    asyncio.run(run_scraper())
