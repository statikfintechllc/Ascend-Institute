# GremlinGPT/core/loop.py

import time
from agent_core import fsm
from self_training.feedback_loop import check_trigger, clear_trigger
from backend.globals import logger

def boot_loop():
    logger.info("[LOOP] Starting recursive FSM loop...")
    while True:
        try:
            if check_trigger():
                logger.info("[LOOP] Triggered retrain from feedback loop.")
                clear_trigger()

            fsm.fsm_loop()
            time.sleep(5)

        except KeyboardInterrupt:
            logger.warning("[LOOP] Manual interrupt. Stopping.")
            break
        except Exception as e:
            logger.error(f"[LOOP] Exception: {e}")
            time.sleep(2)

if __name__ == "__main__":
    boot_loop()
