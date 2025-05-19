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
                dom = await get_dom_html(task['target'])
                store_scrape_to_memory(task['target'], dom)
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
