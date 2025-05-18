# core/snapshot.py

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
from nlp_engine.diff_engine import diff_texts
from memory.vector_store.embedder import embed_text, package_embedding
from backend.globals import logger

SNAPSHOT_ROOT = Path("run/checkpoints/snapshots/")
SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def build_tree(directory):
    tree = {}
    for root, _, files in os.walk(directory):
        for f in files:
            full_path = Path(root) / f
            rel_path = str(full_path.relative_to(directory))
            try:
                tree[rel_path] = sha256_file(full_path)
            except Exception as e:
                logger.warning(f"[SNAPSHOT] Could not hash {rel_path}: {e}")
    return tree

def snapshot_file(file_path, label="manual"):
    file = Path(file_path)
    if not file.exists():
        logger.error(f"[SNAPSHOT] {file} does not exist.")
        return

    content = file.read_text()
    hash_val = hashlib.sha256(content.encode()).hexdigest()
    time_stamp = datetime.utcnow().isoformat()
    snap_name = f"{file.stem}_{label}_{time_stamp}.snap"
    snap_path = SNAPSHOT_ROOT / snap_name

    with open(snap_path, "w") as f:
        json.dump({
            "path": str(file),
            "hash": hash_val,
            "timestamp": time_stamp,
            "label": label,
            "code": content
        }, f, indent=2)

    logger.success(f"[SNAPSHOT] Saved {snap_name}")
    return snap_path

def rollback(file_path, snapshot_file):
    with open(snapshot_file, "r") as f:
        data = json.load(f)

    old_code = data["code"]
    new_code = Path(file_path).read_text()

    if old_code == new_code:
        logger.info("[SNAPSHOT] File already matches snapshot.")
        return

    # Embed diff before overwrite
    diff = diff_texts(new_code, old_code)
    diff_text = "\n".join(diff["diff_lines"])
    vector = embed_text(diff_text)

    package_embedding(
        text=diff_text,
        vector=vector,
        meta={
            "origin": "snapshot",
            "file": file_path,
            "type": "rollback",
            "semantic_score": diff["semantic_score"],
            "embedding_delta": diff["embedding_delta"],
            "timestamp": datetime.utcnow().isoformat()
        }
    )

    Path(file_path).write_text(old_code)
    logger.warning(f"[SNAPSHOT] Rolled back {file_path} using {snapshot_file}")

# CLI usage
if __name__ == "__main__":
    src = "agent_core/tool_executor.py"
    snap = snapshot_file(src, label="test")
    rollback(src, snap)
