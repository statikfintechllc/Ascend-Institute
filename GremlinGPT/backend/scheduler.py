import schedule
import time
from self_training.trainer import trigger_retrain
from rich import print


def start_scheduler():
    print("[SCHEDULER] Self-training every 15 minutes...")
    schedule.every(15).minutes.do(trigger_retrain)

    while True:
        schedule.run_pending()
        time.sleep(10)
