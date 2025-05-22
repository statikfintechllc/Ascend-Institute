#!/usr/bin/env python3

import subprocess
import os
import logging
import time
import threading
from pathlib import Path

# === Config ===
MONITOR_INTERVAL = 30  # Seconds between health checks
MATRIX_NAME = "ascend_matrix.py"
DASHBOARD_ENDPOINT = "https://api.ascend-dashboard.ai/deploy"
LOOP_FOLDER = "Ascend_AI_Basic_Loops"
LOG_FOLDER = "logs"
REQUIRED_AGENTS = ["automation_module.py", "Alpha_Point_Ascension.py"]
FINAL_GOAL = "Final_Goal.txt"

# === Setup Logging ===
os.makedirs(LOG_FOLDER, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_FOLDER, "supervisor.log"),
    level=logging.INFO,
    format="%(asctime)s [SUPERVISOR]: %(message)s",
)

# === Function: Is process running? ===
def is_process_alive(process_name):
    result = subprocess.run(["pgrep", "-f", process_name], capture_output=True)
    return bool(result.stdout)


# === Function: Restart Matrix if crashed ===
def restart_matrix_if_crashed():
    while True:
        if not is_process_alive(MATRIX_NAME):
            logging.warning(f"{MATRIX_NAME} not running. Restarting...")
            subprocess.Popen(["python3", MATRIX_NAME])
        time.sleep(MONITOR_INTERVAL)


# === Function: Validate Final_Goal priority ===
def validate_goal_file():
    if not os.path.exists(FINAL_GOAL):
        logging.warning("Final_Goal.txt missing.")
        return
    with open(FINAL_GOAL, "r") as f:
        content = f.read()
        if "dashboard" not in content.lower():
            logging.warning("Dashboard priority not found in Final_Goal.txt")
        else:
            logging.info("Dashboard found in Final_Goal.txt")


# === Function: Check dashboard health ===
def check_dashboard():
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", DASHBOARD_ENDPOINT],
            capture_output=True,
            text=True,
        )
        if result.stdout.strip() != "200":
            logging.warning(f"Dashboard health check failed: {result.stdout.strip()}")
        else:
            logging.info("Dashboard endpoint healthy.")
    except Exception as e:
        logging.error(f"Dashboard check error: {e}")


# === Function: Loop folder check ===
def verify_loops_present():
    loops = list(Path(LOOP_FOLDER).glob("*.py"))
    if not loops:
        logging.warning("No loops found in loop directory.")
    else:
        logging.info(f"{len(loops)} loop scripts present.")


# === Function: Agent sanity check ===
def verify_agents_exist():
    for agent in REQUIRED_AGENTS:
        if not os.path.exists(agent):
            logging.error(f"Required agent missing: {agent}")
        else:
            logging.info(f"Verified agent exists: {agent}")


# === Supervisor Main Loop ===
def supervisor_loop():
    logging.info("Ascend Supervisor Agent activated.")
    while True:
        verify_agents_exist()
        verify_loops_present()
        check_dashboard()
        validate_goal_file()
        time.sleep(MONITOR_INTERVAL * 2)  # Longer loop for heavier checks


# === Launch ===
def main():
    threading.Thread(target=restart_matrix_if_crashed, daemon=True).start()
    threading.Thread(target=supervisor_loop, daemon=True).start()
    while True:
        time.sleep(60)  # Keep main thread alive while daemons run


if __name__ == "__main__":
    main()
