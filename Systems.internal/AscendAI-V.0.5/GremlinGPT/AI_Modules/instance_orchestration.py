# instance_orchestrator.py

import subprocess
import logging

logger = logging.getLogger(__name__)


def start_instance(command):
    process = subprocess.Popen(command, shell=True)
    logger.info(f"Started process PID: {process.pid}")
    return process


def stop_instance(process):
    process.terminate()
    logger.info(f"Terminated process PID: {process.pid}")
