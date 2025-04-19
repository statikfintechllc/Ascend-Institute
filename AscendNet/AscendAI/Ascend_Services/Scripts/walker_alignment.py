#!/usr/bin/env python3

import os
import re
import datetime
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# === CONFIGURATION ===
ROOT_DIRS = ["./bootstrap", "./scripts", "./memory", "./core", "./tasks"]
LOG_FILE = "logs/walker_alignment.log"
FINAL_GOAL_FILE = "memory/final_goal.internal"
VECTOR_DB = "memory/vector_index.faiss"  # Optional if embedding DB is used
OCR_QUEUE = "task_queue/ask_monday.task"
CHUNK_SIZE = 500

# === EMBEDDER INIT ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# === LOAD FINAL GOAL ===
def load_final_goal():
    try:
        with open(FINAL_GOAL_FILE, "r") as f:
            return f.read()
    except Exception as e:
        return "[ERROR] Final goal file missing or corrupted."

final_goal_text = load_final_goal()
final_goal_vec = model.encode(final_goal_text)

# === WALK FUNCTION ===
def find_setup_files():
    found = []
    keywords = re.compile(r"(env|requirement|setup|install|init|directive|goal|boot|plan)", re.IGNORECASE)
    for root in ROOT_DIRS:
        for path in Path(root).rglob("*.*"):
            if path.suffix in [".sh", ".py", ".txt", ".md", ".yml", ".toml"]:
                try:
                    content = path.read_text(errors="ignore")
                    if keywords.search(content):
                        found.append((str(path), content))
                except Exception as e:
                    continue
    return found

# === COMPARE AGAINST GOAL ===
def rank_relevance(content):
    chunks = [content[i:i+CHUNK_SIZE] for i in range(0, len(content), CHUNK_SIZE)]
    scores = []
    for chunk in chunks:
        vec = model.encode(chunk)
        sim = util.pytorch_cos_sim(vec, final_goal_vec)[0][0].item()
        scores.append((chunk, sim))
    return sorted(scores, key=lambda x: x[1], reverse=True)

# === WRITE TASK TO MONDAY IF LOW ALIGNMENT ===
def escalate_to_monday(filepath, chunk, score):
    query = f"Alignment issue found in {filepath}:\n\n{chunk}\n\nScore: {score:.3f}\n\nHow should this be rewritten to match final_goal.internal?"
    with open(OCR_QUEUE, "a") as f:
        f.write(f"ask_monday: {query}\n")

# === LOG SYSTEM ===
def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

# === MAIN ===
def run_walker():
    log("Starting walker_alignment...")
    files = find_setup_files()
    log(f"Found {len(files)} setup-related files.")

    for filepath, content in files:
        relevance = rank_relevance(content)
        top_chunk, score = relevance[0]

        if score < 0.6:
            log(f"[LOW] {filepath} scored {score:.3f}. Escalating.")
            escalate_to_monday(filepath, top_chunk, score)
        else:
            log(f"[OK] {filepath} relevance score: {score:.3f}")

    log("Walker complete.")

# === EXECUTE ===
if __name__ == "__main__":
    run_walker()