import time
import threading
from loguru import logger
from self_mutation_watcher.watcher import scan_and_diff
import requests

SCAN_INTERVAL_MIN = 5
NOTIFY_DASHBOARD = True
DASHBOARD_ENDPOINT = "http://localhost:5050/api/mutation/ping"

def notify_dashboard(message):
    try:
        if NOTIFY_DASHBOARD:
            requests.post(DASHBOARD_ENDPOINT, json={"message": message})
    except Exception as e:
        logger.warning(f"[WATCHER] Dashboard notification failed: {e}")

def mutation_loop():
    logger.info("[WATCHER] Mutation Daemon Started.")
    while True:
        try:
            scan_and_diff()
            notify_dashboard("Self-mutation scan complete.")
        except Exception as e:
            logger.error(f"[WATCHER] Loop error: {e}")
        time.sleep(SCAN_INTERVAL_MIN * 60)

def run_daemon():
    t = threading.Thread(target=mutation_loop, daemon=True)
    t.start()
