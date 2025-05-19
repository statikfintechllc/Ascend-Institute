import os
import time
import threading
import subprocess
from pathlib import Path
import psutil
from rich.console import Console
from rich.table import Table
import json

# === Define Paths ===
BASE_DIR = Path(__file__).resolve().parent
PROMPT_DIR = BASE_DIR / "AscendAI_Prompts"
RESPONSE_DIR = BASE_DIR / "AscendAI_Responses"
LOG_PATH = BASE_DIR / "Logs" / "boot_log.txt"
SOULMAP_PATH = BASE_DIR / "soulmap.json"
AGENT_SCRIPT_PATH = BASE_DIR / "Scripts"

# === Ensure Directories ===
PROMPT_DIR.mkdir(parents=True, exist_ok=True)
RESPONSE_DIR.mkdir(parents=True, exist_ok=True)
(Path(BASE_DIR / "Logs")).mkdir(parents=True, exist_ok=True)

# === Runtime State ===
console = Console()
active_models = []
running_threads = {}


def log(message):
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{time.ctime()}] {message}\n")
    console.log(message)


# === Load Models ===
def scan_models():
    global active_models
    active_models.clear()
    for file in AGENT_SCRIPT_PATH.glob("*.py"):
        if "model" in file.name.lower():
            active_models.append(file.stem)
    log(f"[SCAN] Registered Models: {active_models}")


# === Dashboard ===
def cli_dashboard():
    while True:
        table = Table(title="Ascend-AI Runtime Dashboard")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("CPU Usage", f"{psutil.cpu_percent()}%")
        table.add_row("Memory Usage", f"{psutil.virtual_memory().percent}%")
        table.add_row("Threads Running", str(len(running_threads)))

        console.print(table)
        time.sleep(5)


# === Agent Launcher ===
def launch_agent(script_name):
    def agent_thread():
        log(f"[AGENT START] {script_name}")
        try:
            subprocess.run(
                ["python3", str(AGENT_SCRIPT_PATH / script_name)], check=True
            )
        except subprocess.CalledProcessError as e:
            log(f"[AGENT ERROR] {script_name}: {e}")

    t = threading.Thread(target=agent_thread)
    t.daemon = True
    t.start()
    running_threads[script_name] = t


# === Prompt Reactor ===
def react_to_prompts():
    log("[REACTOR] Activated")
    while True:
        for prompt_file in PROMPT_DIR.glob("*.txt"):
            with open(prompt_file, "r") as f:
                content = f.read().strip()
            response_path = RESPONSE_DIR / f"response_{prompt_file.stem}.txt"
            with open(response_path, "w") as rf:
                rf.write(f"[Ascend-AI] Received: {content}")
            prompt_file.unlink()
        time.sleep(2)


# === Load SoulMap (Optional) ===
def load_soulmap():
    if SOULMAP_PATH.exists():
        with open(SOULMAP_PATH, "r") as f:
            soul = json.load(f)
        log(f"[SOULMAP] Loaded: {soul.get('identity', 'Unknown')}")
    else:
        log("[SOULMAP] Not Found")


# === Main Entry ===
def main():
    log("[INIT] Ascend-AI Launcher Starting...")
    scan_models()
    load_soulmap()

    # Launch dashboard + prompt handler
    threading.Thread(target=cli_dashboard, daemon=True).start()
    threading.Thread(target=react_to_prompts, daemon=True).start()

    # Launch all found agents
    for model in active_models:
        launch_agent(f"{model}.py")

    # Keep main alive
    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()
