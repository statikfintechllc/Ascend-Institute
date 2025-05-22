import time
import json
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.globals import CFG
from self_training.generate_dataset import extract_training_data
from self_training.mutation_engine import mutate_dataset
from memory.vector_store.embedder import package_embedding, embed_text, inject_watermark
from mini_attention import MiniMultiHeadAttention
from datetime import datetime
import numpy as np

LOG_DIR = CFG["paths"].get("data_dir", "data/") + "logs/"
OUTPUT_PATH = (
    CFG["paths"].get("data_dir", "data/") + "nlp_training_sets/mutated_dataset.json"
)
WATERMARK = "source:GremlinGPT"
TAG = "trainer_module"

attention = MiniMultiHeadAttention(embed_dim=64, num_heads=4)


class LogEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".log"):
            logger.info("[TRAINER] Log updated. Triggering retraining...")
            trigger_retrain()


def trigger_retrain():
    # Extract logs and mutate into new dataset
    raw = extract_training_data(LOG_DIR)
    mutated = mutate_dataset(raw)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(mutated, f, indent=2)
    logger.success(f"[TRAINER] Dataset mutation complete → {OUTPUT_PATH}")

    # === Simulate attention training behavior ===
    dummy_input = np.random.rand(8, 64)
    out, weights = attention.forward(dummy_input)

    embed_text_summary = f"Trainer activated attention w/ {attention.num_heads} heads | out shape: {out.shape}"
    vector = embed_text(embed_text_summary)

    package_embedding(
        text=embed_text_summary,
        vector=vector,
        meta={
            "origin": TAG,
            "event": "trainer::attention_trace",
            "timestamp": datetime.utcnow().isoformat(),
            "shape": str(out.shape),
            "watermark": WATERMARK,
        },
    )

    # Inject post-train memory watermark
    inject_watermark(origin="trainer::retrain")


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
