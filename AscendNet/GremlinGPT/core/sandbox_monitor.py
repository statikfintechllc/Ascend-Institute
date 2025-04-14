# sandbox_monitor.py

import docker
import psutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

class ContainerMonitor:
    def __init__(self):
        self.client = docker.from_env()

    def monitor_containers(self):
        containers = self.client.containers.list()
        for container in containers:
            stats = container.stats(stream=False)
            cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
            mem_usage = stats['memory_stats']['usage']
            logger.info(f"Container {container.name}: CPU {cpu_usage}, Memory {mem_usage}")

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logger.info(f"File modified: {event.src_path}")

def start_monitoring():
    monitor = ContainerMonitor()
    monitor.monitor_containers()

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()