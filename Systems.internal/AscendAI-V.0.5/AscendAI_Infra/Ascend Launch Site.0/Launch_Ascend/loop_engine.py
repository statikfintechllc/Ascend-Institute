import subprocess
import time
import os
import logging
from pathlib import Path
import threading

# Directories
LOOP_FOLDER = "Ascend_AI_Basic_Loops"
LOG_FOLDER = "logs"
MEMORY_FILE = "ascend_memory.jsonl"
MATRIX_INTERVAL = 300  # 5 minutes

# Ensure log directory exists
os.makedirs(LOG_FOLDER, exist_ok=True)


def launch_matrix():
    subprocess.run(["python3", "ascend_matrix.py"])


def main():
    logging.basicConfig(
        filename=os.path.join(LOG_FOLDER, "loop_engine.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
    )
    logging.info("Loop Engine started.")

    # Start the matrix thread
    matrix_thread = threading.Thread(target=launch_matrix, daemon=True)
    matrix_thread.start()

    # Monitor loops
    monitor_loops()


# Dictionary to track subprocesses
loop_processes = {}
matrix_thread = None
last_matrix_time = 0


def launch_loop(loop_path):
    """Launch a loop script as a subprocess and log its output."""
    loop_name = loop_path.stem
    log_path = os.path.join(LOG_FOLDER, f"{loop_name}.log")
    with open(log_path, "a") as log_file:
        process = subprocess.Popen(
            ["python3", str(loop_path)], stdout=log_file, stderr=log_file
        )
    return process


def run_matrix_background():
    """Fire up ascend_matrix.py in a background thread."""

    def matrix_task():
        logging.info("[MATRIX] Activating ascend_matrix.py")
        subprocess.run(["python3", "ascend_matrix.py"])

    global matrix_thread
    if matrix_thread is None or not matrix_thread.is_alive():
        matrix_thread = threading.Thread(target=matrix_task, daemon=True)
        matrix_thread.start()
    else:
        logging.info("[MATRIX] Already running; skipping new launch.")


def monitor_loops():
    """Monitor and restart loops as necessary."""
    global last_matrix_time
    while True:
        for loop_path in Path(LOOP_FOLDER).glob("*.py"):
            loop_name = loop_path.name
            if (
                loop_name not in loop_processes
                or loop_processes[loop_name].poll() is not None
            ):
                logging.info(f"[LOOP] Launching/restarting: {loop_name}")
                loop_processes[loop_name] = launch_loop(loop_path)

        # Auto-trigger the Matrix every X seconds
        if time.time() - last_matrix_time > MATRIX_INTERVAL:
            run_matrix_background()
            last_matrix_time = time.time()

        time.sleep(10)


def main():
    """Start loop monitoring and Matrix execution."""
    logging.basicConfig(
        filename=os.path.join(LOG_FOLDER, "loop_engine.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
    )
    logging.info("[ENGINE] Loop Engine initialized.")
    monitor_loops()


if __name__ == "__main__":
    main()
