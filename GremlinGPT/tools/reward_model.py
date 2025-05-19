# tools/reward_model.py

import json
from datetime import datetime
from pathlib import Path
import numpy as np
from backend.globals import logger
from nlp_engine.semantic_score import semantic_similarity

LOG_HISTORY_DIR = Path("data/logs/")
REWARD_LOG = LOG_HISTORY_DIR / "rewards.jsonl"
REWARD_LOG.parent.mkdir(parents=True, exist_ok=True)

def evaluate_result(task_type, output_text, reference_text=None):
    """
    Assign reward/confidence based on output:
    - Uses semantic similarity and vector norms
    - Heuristic fallbacks for basic scoring
    """

    reward = 0.0
    confidence = 0.0
    reason = ""

    if reference_text:
        similarity = semantic_similarity(output_text, reference_text)
        delta = np.linalg.norm(np.array([similarity]) - np.array([1.0]))
        confidence = max(0.0, 1.0 - delta)
        reward = similarity
        reason = "semantic_match"
    else:
        if "error" in output_text.lower():
            reward = -0.3
            confidence = 0.2
            reason = "error_detected"
        elif len(output_text.strip()) > 40:
            reward = 0.6
            confidence = 0.7
            reason = "length_heuristic"
        else:
            reward = 0.3
            confidence = 0.5
            reason = "basic_pass"

    return {
        "task": task_type,
        "confidence": round(confidence, 4),
        "reward": round(reward, 4),
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
        "output": output_text[:300]
    }

def log_reward(record):
    try:
        with open(REWARD_LOG, "a") as f:
            f.write(json.dumps(record) + "\n")
        logger.info(f"[REWARD] Logged: {record['task']} [{record['reason']}]")
    except Exception as e:
        logger.error(f"[REWARD] Failed to log reward: {e}")

def top_rewarded_tasks(n=5):
    records = []
    try:
        with open(REWARD_LOG, "r") as f:
            for line in f:
                rec = json.loads(line.strip())
                records.append(rec)
    except FileNotFoundError:
        return []

    return sorted(records, key=lambda r: r["reward"], reverse=True)[:n]

if __name__ == "__main__":
    out = "Successfully scraped 5 stock tickers from Webull."
    ref = "Extract a list of tickers from a market page."
    rec = evaluate_result("scrape", out, ref)
    log_reward(rec)
    print(top_rewarded_tasks())
