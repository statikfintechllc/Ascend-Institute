# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

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

# scraper/web_knowledge_scraper.py

import os
import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from loguru import logger

from scraper.dom_navigator import extract_dom_structure
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark

WATERMARK = "source:GremlinGPT"
ORIGIN = "web_knowledge_scraper"


HEADERS = {
    "User-Agent": "GremlinGPT/4.0 (+https://gremlingpt.ai/bot)",
    "Accept-Language": "en-US,en;q=0.9",
}


async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=15) as response:
            if response.status == 200:
                return await response.text()
            else:
                logger.warning(f"[SCRAPER] Non-200 for {url}: {response.status}")
                return ""
    except Exception as e:
        logger.error(f"[SCRAPER] Failed to fetch {url}: {e}")
        return ""


async def scrape_web_knowledge(urls):
    results = []
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [fetch_html(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

    for url, html in zip(urls, pages):
        if not html:
            continue

        structure = extract_dom_structure(html)
        summary_text = f"[{url}]\n{structure['text']}"
        vector = embed_text(summary_text)

        package_embedding(
            text=summary_text,
            vector=vector,
            meta={
                "origin": ORIGIN,
                "timestamp": datetime.utcnow().isoformat(),
                "url": url,
                "tags": structure.get("tags", {}),
                "length": len(summary_text),
                "watermark": WATERMARK,
            },
        )
        inject_watermark(origin=ORIGIN)
        results.append(
            {
                "url": url,
                "summary": summary_text,
                "nodes": structure["nodes"],
                "links": structure["links"],
            }
        )
        logger.success(f"[SCRAPER] Embedded {url}")
    return results


def run_search_and_scrape(urls):
    return asyncio.run(scrape_web_knowledge(urls))


if __name__ == "__main__":
    test_urls = [
        "https://finance.yahoo.com/",
        "https://www.investing.com/news/stock-market-news",
    ]
    data = run_search_and_scrape(test_urls)
    with open("run/logs/sample_scrape.json", "w") as f:
        json.dump(data, f, indent=2)
    print("[SCRAPER] Sample scrape complete.")
