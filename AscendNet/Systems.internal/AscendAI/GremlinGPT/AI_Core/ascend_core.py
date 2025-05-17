import os
import sys
import traceback
import importlib
import logging
import json
import time

from AI_Core.memory_manager import MemoryManager
from AI_Core.error_handling import ErrorHandler
from AI_Core.executor import Executor
from AI_Core.task_execution import TaskExecution
from AI_Core.module_manager import ModuleManager
from AI_Core.prompt_engine import PromptEngine

# === LOGGING ===
log_path = os.path.expanduser("~/AscendNet/GremlinGPT/Logs/execution.log")
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("GremlinGPT")

# === INIT CORE COMPONENTS ===
memory = MemoryManager()
errors = ErrorHandler()
executor = Executor()
tasker = TaskExecution()
modules = ModuleManager()
prompt_gen = PromptEngine()

def initialize_system():
    logger.info("Initializing GremlinGPT Runtime Loop")
    modules.load_all()
    memory.load_short_term()
    memory.load_long_term()
    logger.info("System initialization complete")

def run_main_loop():
    while True:
        try:
            task = memory.get_next_task()
            if not task:
                logger.info("No pending tasks. Sleeping.")
                time.sleep(10)
                continue

            prompt = prompt_gen.build_prompt(task)
            logger.info(f"[TASK] Running prompt: {prompt[:120]}...")
            code = executor.generate_code(prompt)

            result = executor.execute_code(code)
            logger.info(f"[RESULT] {str(result)[:150]}")

            memory.store_result(task, code, result)
            errors.reset_error(task)

        except Exception as e:
            logger.error(traceback.format_exc())
            errors.log_failure(str(e))
            memory.mark_task_failed(str(e))
            time.sleep(5)

if __name__ == "__main__":
    initialize_system()
    run_main_loop()

