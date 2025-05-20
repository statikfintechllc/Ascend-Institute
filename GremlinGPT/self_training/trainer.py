# trainer.py

import time
import json
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.globals import CFG
from self_training.generate_dataset import extract_training_data
from self_training.mutation_engine import mutate_dataset

LOG_DIR = CFG["paths"].get("data_dir", "data/") + "logs/"
OUTPUT_PATH = (
    CFG["paths"].get("data_dir", "data/") + "nlp_training_sets/mutated_dataset.json"
)


class LogEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".log"):
            logger.info("[TRAINER] Log updated. Triggering retraining...")
            trigger_retrain()


def trigger_retrain():
    raw = extract_training_data(LOG_DIR)
    mutated = mutate_dataset(raw)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(mutated, f, indent=2)
    logger.info(f"[TRAINER] Mutation + data regeneration complete → {OUTPUT_PATH}")


def watch_logs():
    observer = Observer()
    observer.schedule(LogEventHandler(), path=LOG_DIR, recursive=False)
    observer.start()
    logger.info(f"[TRAINER] Watching logs at: {LOG_DIR}")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_logs()
