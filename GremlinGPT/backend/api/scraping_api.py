from flask import request, jsonify
from agent_core.task_queue import enqueue_task


def scrape_url():
    data = request.get_json()
    url = data.get("url")
    if url:
        task = {"type": "scrape", "target": url}
        enqueue_task(task)
        return jsonify({"status": "queued", "task": task})
    return jsonify({"error": "No URL provided"}), 400
