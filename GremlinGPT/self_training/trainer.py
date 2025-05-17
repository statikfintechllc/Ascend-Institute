from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from self_training.generate_dataset import extract_training_data
from self_training.mutation_engine import mutate_dataset
from backend.globals import CFG
from loguru import logger
import time

LOG_DIR = "data/logs/"

class LogEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".log"):
            logger.info("[TRAINER] Log updated. Triggering retraining...")
            trigger_retrain()

def trigger_retrain():
    raw = extract_training_data(LOG_DIR)
    mutated = mutate_dataset(raw)
    with open("data/nlp_training_sets/mutated_dataset.json", "w") as f:
        import json
        json.dump(mutated, f, indent=2)
    logger.info("[TRAINER] Mutation + data regeneration complete.")

def watch_logs():
    observer = Observer()
    observer.schedule(LogEventHandler(), path=LOG_DIR, recursive=False)
    observer.start()
    logger.info("[TRAINER] Watching logs for retraining...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_logs()

