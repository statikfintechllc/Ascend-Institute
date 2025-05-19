import psutil
import random


def evaluate_task(task):
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    entropy = random.random()

    return cpu < 80 and mem < 85 and entropy > 0.1
