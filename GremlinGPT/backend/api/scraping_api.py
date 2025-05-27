# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion. v5 :: Module Integrity Directive

from flask import request, jsonify
from agent_core.task_queue import enqueue_task
from nlp_engine.transformer_core import encode
from memory.vector_store.embedder import package_embedding
from memory.log_history import log_event
from core.snapshot import snapshot_file
from datetime import datetime
from loguru import logger


def scrape_url():
    data = request.get_json()
    url = data.get("url")

    if not url:
        logger.warning("[SCRAPE_API] No URL provided.")
        return jsonify({"error": "No URL provided"}), 400

    timestamp = datetime.utcnow().isoformat()
    logger.info(f"[SCRAPE_API] Scrape requested for: {url}")

    # === Create snapshot of scraper logic before enqueue (trace lineage)
    snap_result = snapshot_file("scraper/scraper_loop.py", label="api_scrape_request", return_meta=True)
    _, lineage_meta = snap_result if snap_result else (None, {})

    # === Embed URL intent into memory
    vector = encode(url)
    package_embedding(
        text=url,
        vector=vector,
        meta={
            "origin": "scraping_api",
            "type": "scrape_request",
            "target_url": url,
            "timestamp": timestamp,
            "watermark": "source:GremlinGPT",
            **lineage_meta,
        },
    )

    task = {
        "type": "scrape",
        "target": url,
        "meta": {
            "source": "scraping_api",
            "timestamp": timestamp,
            "lineage": lineage_meta.get("lineage_id", "none"),
        },
    }

    enqueue_task(task)
    log_event("api", "scrape_request", task, status="queued")

    return jsonify(
        {
            "status": "queued",
            "task": task,
            "trace": {
                "snapshot": lineage_meta.get("lineage_id", "n/a"),
                "timestamp": timestamp,
            },
        }
    )
