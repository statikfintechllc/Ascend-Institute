
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def log_event(level, message):
    Logs messages with different severity levels.
    :param level: str - 'info', 'warning', 'error', 'critical'
    :param message: str - Message to log
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)

if __name__ == '__main__':
    log_event()