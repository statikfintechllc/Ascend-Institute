import time
from agent_core import fsm
from backend.globals import logger, CFG
from self_training.feedback_loop import check_trigger, clear_trigger
from memory.log_history import log_event
from datetime import datetime


def boot_loop():
    logger.info("[LOOP] Starting recursive FSM control engine...")
    tick_interval = CFG.get("loop", {}).get("tick_interval_sec", 5)
    cycle_count = 0

    while True:
        try:
            cycle_count += 1
            loop_time = datetime.utcnow().isoformat()
            logger.info(f"[LOOP] Tick #{cycle_count} @ {loop_time}")

            if check_trigger():
                logger.info("[LOOP] Retrain trigger detected → scheduling learning phase.")
                log_event("loop", "trigger", {"origin": "feedback"}, status="queued")
                clear_trigger()

            # Core execution
            fsm.fsm_loop()

            log_event("loop", "fsm_cycle", {"tick": cycle_count}, status="complete")
            time.sleep(tick_interval)

        except KeyboardInterrupt:
            logger.warning("[LOOP] Manual interrupt received. Halting system.")
            break

        except Exception as e:
            logger.error(f"[LOOP] Loop exception: {e}")
            log_event("loop", "exception", {"error": str(e)}, status="fail")
            time.sleep(3)


if __name__ == "__main__":
    boot_loop()
