# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

# Import everything from backend.globals for centralized dependency management
from backend.globals import (
    time, datetime, Path, sys, CFG, setup_module_logger, logging, 
    fsm, check_trigger, clear_trigger, log_event
)

# Initialize module-specific logger
if setup_module_logger:
    logger = setup_module_logger("core", "loop")
else:
    logger = logging.getLogger("core.loop")


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
                logger.info(
                    "[LOOP] Retrain trigger detected → scheduling learning phase."
                )
                log_event("loop", "trigger", {"origin": "feedback"}, status="queued")
                clear_trigger()

            # Core FSM execution
            try:
                result = fsm.fsm_loop()
                if result is None or (hasattr(result, "__len__") and len(result) == 0):
                    logger.info("[LOOP] No tasks available for FSM. Idling this tick.")
                else:
                    logger.info("[LOOP] FSM processed tasks or state.")
            except Exception as fsm_err:
                logger.warning(
                    f"[LOOP] FSM loop handled error (idle or empty queue is OK): {fsm_err}"
                )
                # Log as 'idle' instead of 'fail' if it's a known "no task" condition
                log_event(
                    "loop",
                    "fsm_idle",
                    {"tick": cycle_count, "error": str(fsm_err)},
                    status="idle",
                )
                time.sleep(tick_interval)
                continue

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
