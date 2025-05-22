#!/usr/bin/env python3

from flask import Flask, request, jsonify
from datetime import datetime
import os
import re

app = Flask(__name__)

# === Setup ===
LOG_FILE = "ascend_idea_log.txt"
TASK_DIR = "task_queue"
os.makedirs("dashboard_logs", exist_ok=True)
os.makedirs(TASK_DIR, exist_ok=True)
LOG_PATH = os.path.join("dashboard_logs", LOG_FILE)

# === Lightweight NLP Classifier ===
def classify_idea(idea_text):
    idea_lower = idea_text.lower()
    if any(keyword in idea_lower for keyword in ["expedite", "fast", "rush"]):
        return "expedite"
    elif any(keyword in idea_lower for keyword in ["warn", "danger", "fbi", "gov"]):
        return "warn"
    elif any(keyword in idea_lower for keyword in ["patch", "fix", "repair"]):
        return "patch"
    elif any(
        keyword in idea_lower for keyword in ["prioritize", "urgent", "important"]
    ):
        return "prioritize"
    else:
        return "note"


# === Task Dispatcher ===
def dispatch_task(idea_text, intent):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = re.sub(r"\W+", "_", idea_text[:40])
    file_path = os.path.join(TASK_DIR, f"{intent}_{timestamp}_{safe_filename}.task")

    with open(file_path, "w") as f:
        f.write(f"intent: {intent}\n")
        f.write(f"timestamp: {timestamp}\n")
        f.write(f"idea: {idea_text}\n")

    print(f">> [Parser] Task dispatched: {file_path}")


# === Routes ===


@app.route("/")
def home():
    return """
    <h1>Ascend AI: Golden Eye Uplink</h1>
    <p>Status: ONLINE</p>
    <p>Post thoughts to /idea (JSON)</p>
    """


@app.route("/idea", methods=["POST"])
def receive_idea():
    data = request.get_json(force=True)
    idea = data.get("idea", "").strip()

    if not idea:
        return jsonify({"status": "error", "message": "No idea content provided."}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] IDEA: {idea}\n"

    # Log to disk
    with open(LOG_PATH, "a") as f:
        f.write(log_line)

    # Classify + Dispatch
    intent = classify_idea(idea)
    dispatch_task(idea, intent)

    return jsonify(
        {"status": "received", "idea": idea, "intent": intent, "timestamp": timestamp}
    )


@app.route("/log", methods=["GET"])
def read_log():
    if not os.path.exists(LOG_PATH):
        return jsonify({"log": []})
    with open(LOG_PATH, "r") as f:
        log_data = f.readlines()
    return jsonify({"log": log_data[-25:]})


# === Main ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
