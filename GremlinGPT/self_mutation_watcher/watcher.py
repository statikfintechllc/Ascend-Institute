# self_mutation_watcher/watcher.py

import hashlib
from pathlib import Path
from datetime import datetime
from difflib import unified_diff

from memory.vector_store.embedder import embed_text, package_embedding
from self_training.feedback_loop import inject_feedback
from core.kernel import apply_patch
from agents.planner_agent import enqueue_next
from loguru import logger

WATCH_PATHS = [
    "agent_core/fsm.py",
    "agent_core/heuristics.py",
    "trading_core/rules_engine.py",
]

SNAPSHOT_DIR = Path("run/checkpoints/code_snapshots/")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def get_snapshot_path(file_path):
    filename = Path(file_path).name
    return SNAPSHOT_DIR / f"{filename}.snapshot"


def load_snapshot(file_path):
    snap_path = get_snapshot_path(file_path)
    return snap_path.read_text() if snap_path.exists() else ""


def save_snapshot(file_path, content):
    snap_path = get_snapshot_path(file_path)
    snap_path.write_text(content)


def generate_diff(old, new):
    lines = list(
        unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile="before",
            tofile="after",
            lineterm="",
        )
    )
    return "\n".join(lines)


def scan_and_diff():
    logger.info("[WATCHER] Scanning for code changes...")
    for file_path in WATCH_PATHS:
        try:
            with open(file_path, "r") as f:
                current = f.read()

            previous = load_snapshot(file_path)
            if current != previous:
                logger.success(f"[WATCHER] Detected change in: {file_path}")
                diff = generate_diff(previous, current)
                vector = embed_text(diff)

                package_embedding(
                    text=diff,
                    vector=vector,
                    meta={
                        "origin": "self_mutation_watcher",
                        "file": file_path,
                        "type": "code_diff",
                        "line_count": len(diff.splitlines()),
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                )

                inject_feedback()

                # Auto-apply current version as patch for traceability
                apply_patch(file_path, current, reason="mutation_observed")

                # Schedule planner to re-infer a new task
                enqueue_next()

                save_snapshot(file_path, current)
        except Exception as e:
            logger.error(f"[WATCHER] Failed to process {file_path}: {e}")


if __name__ == "__main__":
    scan_and_diff()
