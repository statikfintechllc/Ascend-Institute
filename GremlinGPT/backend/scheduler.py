import schedule
import time
from backend.globals import logger, LOOP

from self_training.trainer import trigger_retrain
from agents.planner_agent import enqueue_next
from self_mutation_watcher.watcher import scan_and_diff


def start_scheduler():
    retrain_interval = LOOP.get("planner_interval", 15)
    mutation_interval = LOOP.get("mutation_watch_interval", 5)
    plan_interval = LOOP.get("planner_interval", 10)

    logger.info("[SCHEDULER] Initializing scheduler...")

    if LOOP.get("self_training_enabled", True):
        schedule.every(retrain_interval).minutes.do(trigger_retrain)
        logger.success(
            f"[SCHEDULER] Self-training scheduled every {retrain_interval} min"
        )

    if LOOP.get("planner_enabled", True):
        schedule.every(plan_interval).seconds.do(enqueue_next)
        logger.success(
            f"[SCHEDULER] Planner enqueue scheduled every {plan_interval} sec"
        )

    if LOOP.get("mutation_watch_enabled", True):
        schedule.every(mutation_interval).seconds.do(scan_and_diff)
        logger.success(
            f"[SCHEDULER] Mutation scan scheduled every {mutation_interval} sec"
        )

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.warning("[SCHEDULER] Manual interrupt — exiting.")
            break
        except Exception as e:
            logger.error(f"[SCHEDULER] Scheduler loop error: {e}")
            time.sleep(3)
