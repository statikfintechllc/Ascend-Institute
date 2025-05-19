# runtime/cron_scheduler.py

import schedule
import time
import logging
from runtime.runner import run

logging.basicConfig(
    filename="logs/gremlin_cron.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def start_scheduler():
    logging.info("Starting GremlinGPT scheduler...")

    # Run every 15 minutes
    schedule.every(15).minutes.do(scheduled_run)

    while True:
        try:
            schedule.run_pending()
        except Exception as e:
            logging.error(f"[SCHEDULER ERROR] {e}")
        time.sleep(5)


def scheduled_run():
    logging.info("Scheduled run triggered.")
    try:
        run()
    except Exception as e:
        logging.error(f"[Scheduled run failed] {e}")
