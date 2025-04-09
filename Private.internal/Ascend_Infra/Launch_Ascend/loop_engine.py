import subprocess
import time
import os
import logging
from pathlib import Path
import json

# Directories
LOOP_FOLDER = "Ascend_AI_Basic_Loops"
LOG_FOLDER = "logs"
MEMORY_FILE = "ascend_memory.jsonl"

# Ensure log directory exists
os.makedirs(LOG_FOLDER, exist_ok=True)

# Dictionary to keep track of loop processes
loop_processes = {}

def launch_loop(loop_path):
    """Launch a loop script as a subprocess and log its output."""
    loop_name = loop_path.stem
    log_path = os.path.join(LOG_FOLDER, f"{loop_name}.log")
    with open(log_path, "a") as log_file:
        process = subprocess.Popen(
            ["python3", str(loop_path)],
            stdout=log_file,
            stderr=log_file
        )
    return process

def monitor_loops():
    """Monitor and restart loops as necessary."""
    while True:
        for loop_path in Path(LOOP_FOLDER).glob("*.py"):
            loop_name = loop_path.name
            if loop_name not in loop_processes or loop_processes[loop_name].poll() is not None:
                logging.info(f"Launching or restarting loop: {loop_name}")
                loop_processes[loop_name] = launch_loop(loop_path)
        time.sleep(10)

def main():
    """Main function to set up logging and start monitoring loops."""
    logging.basicConfig(
        filename=os.path.join(LOG_FOLDER, "loop_engine.log"),
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]: %(message)s'
    )
    logging.info("Loop Engine started.")
    monitor_loops()

if __name__ == "__main__":
    main()
