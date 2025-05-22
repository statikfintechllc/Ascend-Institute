import os
import json
import hashlib
import time
from datetime import datetime

CONSTITUTION_PATHS = ["./memory/ascend_constitution.json", "./memory/ascend_dna.txt"]
HASH_REGISTRY = "./memory/constitution_hashes.json"
LOG_PATH = "./logs/skepticus_watchdog.log"


def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_hashes():
    if not os.path.exists(HASH_REGISTRY):
        return {}
    with open(HASH_REGISTRY, "r") as f:
        return json.load(f)


def log_violation(message):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.utcnow().isoformat()}] {message}\n")


def check_integrity():
    saved = load_hashes()
    for path in CONSTITUTION_PATHS:
        if not os.path.exists(path):
            log_violation(f"Missing file: {path}")
            continue
        current = hash_file(path)
        if path not in saved or saved[path] != current:
            log_violation(f"INTEGRITY BREACH: {path}")
            # Here you could also trigger an alert to dashboard or halt recursion


if __name__ == "__main__":
    while True:
        check_integrity()
        time.sleep(60)
