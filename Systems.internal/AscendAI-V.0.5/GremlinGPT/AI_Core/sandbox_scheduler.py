# sandbox_scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def schedule_task(func, trigger, **kwargs):
    scheduler.add_job(func, trigger, **kwargs)
    logger.info(f"Scheduled task {func.__name__} with trigger {trigger}")


def start_scheduler():
    scheduler.start()
    logger.info("Scheduler started")
