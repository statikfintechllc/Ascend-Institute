from loguru import logger


def log_error(task, error):
    logger.error(f"[ERROR_LOG] Task {task['type']} failed. Reason: {error}")
