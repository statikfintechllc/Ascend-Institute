import schedule
import time
from core import main


def run_scheduler():
    schedule.every(10).minutes.do(main.run)

    while True:
        schedule.run_pending()
        time.sleep(1)
