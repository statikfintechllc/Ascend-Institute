# runtime/runner.py

import time
import traceback
import logging
from core.gremlin_loop import gremlin_loop
from alerts.discord import send_discord_alert
from alerts.telegram import send_telegram_alert

# Configure runtime logging
logging.basicConfig(
    filename="logs/gremlin_runtime.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def run():
    logging.info("Starting GremlinGPT runtime loop...")

    while True:
        try:
            gremlin_loop()
            logging.info("Loop iteration complete.")
        except Exception as e:
            error_msg = f"Gremlin crashed:\n{e}\n\n{traceback.format_exc()}"
            logging.error(error_msg)

            # Alert the humans
            send_discord_alert(error_msg)
            send_telegram_alert(error_msg)

            # Cooldown before retry
            time.sleep(30)

        # Wait a bit before starting next loop iteration
        time.sleep(10)
