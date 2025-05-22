from flask import request, jsonify
from agent_core.task_queue import enqueue_task
from nlp_engine.transformer_core import encode
from memory.vector_store.embedder import package_embedding
from datetime import datetime
from core.snapshot import snapshot_file


def scrape_url():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    timestamp = datetime.utcnow().isoformat()
    _, lineage_meta = snapshot_file(
        "scraper/scraper_loop.py", label="api_scrape_request", return_meta=True
    )

    # Embed request for vector trace
    vector = encode(url)
    package_embedding(
        text=url,
        vector=vector,
        meta={
            "from": "scraper_api",
            "type": "scrape_request",
            "timestamp": timestamp,
            "target_url": url,
            **lineage_meta,
        },
    )

    task = {
        "type": "scrape",
        "target": url,
        "meta": {
            "source": "scraper_api",
            "timestamp": timestamp,
            "lineage": lineage_meta.get("lineage_id", "none"),
        },
    }

    enqueue_task(task)
    return jsonify({"status": "queued", "task": task})
