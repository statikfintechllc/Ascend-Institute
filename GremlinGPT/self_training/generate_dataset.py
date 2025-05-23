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

# self_training/generate_dataset.py

import os
import json
import time
import uuid
import schedule
from datetime import datetime
from pathlib import Path
from agent_core.task_queue import enqueue_task
from self_training.feedback_loop import inject_feedback

WATERMARK = "source:GremlinGPT"
KEYWORDS = ["FAIL", "LOW_CONF", "INVALID", "delta", "error", "retry", "timeout", "null"]

ROOT_DIR = "run/logs"
OUTPUT_FILE = "data/nlp_training_sets/auto_generated.jsonl"
LINEAGE_TAG = str(uuid.uuid4())
CONFIDENCE_THRESHOLD = 0.4  # Reserved for future use


def extract_training_data(root_dir=ROOT_DIR, output_file=OUTPUT_FILE):
    entries = []
    root = Path(root_dir)

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                if any(keyword in line.upper() for keyword in KEYWORDS):
                    cleaned = line.strip()
                    if 15 < len(cleaned) < 1000:
                        entry = {
                            "input": cleaned,
                            "output": "TBD",
                            "source_file": str(path),
                            "line": i + 1,
                            "timestamp": datetime.utcnow().isoformat(),
                            "meta": {
                                "watermark": WATERMARK,
                                "length": len(cleaned),
                                "lineage_id": LINEAGE_TAG,
                                "type": path.suffix or "text",
                            },
                        }
                        entries.append(entry)

        except Exception as e:
            print(f"[EXTRACTOR] Failed to process {path}: {e}")

    if entries:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")

        print(f"[DATASET] Extracted {len(entries)} entries → {output_file}")

        # Queue self-training with lineage context
        enqueue_task(
            {
                "type": "self_train",
                "meta": {
                    "reason": "auto_generated_dataset",
                    "lineage_id": LINEAGE_TAG,
                    "source": "dataset_scheduler",
                },
            }
        )
        inject_feedback()
        print("[DATASET] Self-train task injected.")
    else:
        print("[DATASET] No matching entries found.")

    return entries


def schedule_extraction(interval_min=10):
    schedule.every(interval_min).minutes.do(extract_training_data)
    print(f"[SCHEDULER] Training extraction scheduled every {interval_min} min.")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    schedule_extraction()
