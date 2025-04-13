import os
import sys
import time
import logging
from pathlib import Path

# Add the root directory to sys.path for module imports
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from core.decision import decision_node
from core.model_interface import ask_model
from core.docker_runner import run_code_in_docker
from memory.vector_memory import recall_context, store_context
from memory.planning_memory import log_plan, get_pending_plans
from alerts.discord import send_discord_alert
from alerts.telegram import send_telegram_alert
from tools import tool_registry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def gremlin_loop():
    logger.info("Starting GremlinGPT loop.")
    while True:
        try:
            # Retrieve pending plans
            pending_tasks = get_pending_plans()
            for task in pending_tasks:
                logger.info(f"Processing task: {task['task']}")
                # Recall context related to the task
                context = recall_context(task['task'])
                # Decide on action
                action = decision_node(task['task'], context)
                # Execute action
                if action['type'] == 'tool':
                    result = tool_registry[action['name']](**action['params'])
                elif action['type'] == 'code':
                    result = run_code_in_docker(action['code'])
                else:
                    result = "Unknown action type."
                # Store result in context
                store_context(task['task'], result)
                # Send alerts
                send_discord_alert(f"Task '{task['task']}' completed with result: {result}")
                send_telegram_alert(f"Task '{task['task']}' completed with result: {result}")
                # Update task status
                log_plan(task['task'], task['reason'], outcome='completed')
            time.sleep(60)  # Wait before next iteration
        except Exception as e:
            logger.error(f"Error in GremlinGPT loop: {e}")
            send_discord_alert(f"Error in GremlinGPT loop: {e}")
            send_telegram_alert(f"Error in GremlinGPT loop: {e}")
            time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    gremlin_loop()
