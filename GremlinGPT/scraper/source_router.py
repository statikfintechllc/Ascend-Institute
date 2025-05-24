# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────
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

# scraper/source_router.py

import asyncio
import psutil
import threading
import time
from loguru import logger
from scraper.tws_scraper import safe_scrape_tws
from scraper.stt_scraper import safe_scrape_stt
from scraper.playwright_scraper import safe_scrape_web
from scraper.page_simulator import store_scrape_to_memory

_last_scraped = []


def detect_apps():
    procs = [p.name().lower() for p in psutil.process_iter()]
    return {
        "tws": any("tws" in p for p in procs),
        "stt": any("stockstotrade" in p for p in procs),
    }


def route_scraping():
    try:
        apps = detect_apps()
        logger.info(f"[SCRAPER] Active sources: {apps}")

        if apps["tws"]:
            return safe_scrape_tws()
        elif apps["stt"]:
            return safe_scrape_stt()
        else:
            return safe_scrape_web()
    except Exception as e:
        logger.warning(f"[SCRAPER] Routing failed: {e}")
        return []


def periodic_refresh(interval_sec=5):
    global _last_scraped
    while True:
        try:
            data = route_scraping()
            _last_scraped = data
        except Exception as e:
            logger.error(f"[SCRAPER] Loop error: {e}")
        time.sleep(interval_sec)


def get_live_snapshot():
    return _last_scraped


def start_scraper_loop():
    logger.info("[SCRAPER] Starting refresh loop.")
    t = threading.Thread(target=periodic_refresh, daemon=True)
    t.start()
