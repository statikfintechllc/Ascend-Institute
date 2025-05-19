import json
import hashlib
import os
from datetime import datetime

HASH_PATH = "./memory/constitution_hashes.json"
WATCHDOG_LOG = "./logs/skepticus_watchdog.log"
DASHBOARD_OUT = "./dashboard/alerts/integrity_alert.json"


def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def log_issue(message):
    with open(WATCHDOG_LOG, "a") as f:
        f.write(f"[{datetime.utcnow().isoformat()}] {message}\n")


def alert_dashboard(issues):
    with open(DASHBOARD_OUT, "w") as f:
        json.dump(
            {
                "type": "CONSTITUTION_ALERT",
                "timestamp": datetime.utcnow().isoformat(),
                "issues": issues,
            },
            f,
            indent=4,
        )


def check_integrity():
    if not os.path.exists(HASH_PATH):
        log_issue("Hash map missing.")
        return

    with open(HASH_PATH, "r") as f:
        expected = json.load(f)

    issues = []
    for path, expected_hash in expected.items():
        if not os.path.exists(path):
            issues.append(f"Missing file: {path}")
            continue
        actual_hash = hash_file(path)
        if actual_hash != expected_hash:
            issues.append(f"Tampered: {path}")

    if issues:
        for issue in issues:
            log_issue(issue)
        alert_dashboard(issues)


if __name__ == "__main__":
    check_integrity()
