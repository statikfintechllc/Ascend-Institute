#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import time
from langchain.llms import LlamaCpp
import threading

# === Dynamic Root Path ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM_ROOT = os.environ.get("ASCEND_SCAN_ROOT", "/mnt")
MAP_OUTPUT_PATH = os.path.join(BASE_DIR, "System Mapping", "map.json")
MODEL_INSTALL_SCRIPT = os.path.join(BASE_DIR, "llama_weights_and_models.sh")
LLM_MODEL_PATH = os.path.join(BASE_DIR, "llama-13B.gguf")
FINAL_GOAL_PATH = os.path.join(BASE_DIR, "Final_Goal.txt")
BOOTLOADER_PROMPT_PATH = os.path.join(BASE_DIR, "bootloader_prompt.txt")

# === Flags ===
RUN_ENV_SETUP = True
RUN_ENV_VERIFY = True
VERBOSE_MODE = True
MODEL_SETUP_REQUIRED = True
RUN_ASCEND_DRY = True
RUN_ASCEND_REAL = False

# === Environment Setup ===
def setup_env():
    print(">> Setting up conda base environment...")
    subprocess.run("conda env create -f ascend_conda_base.yml", shell=True)
    subprocess.run("conda run -n ascend_env pip install -r ascend_requirements.txt", shell=True)

def verify_env():
    print(">> Verifying environment and files...")
    subprocess.run("conda run -n ascend_env python Init_env_verify.py", shell=True)

def setup_llama_weights():
    model_dir = os.path.join(BASE_DIR, "models", "llama")
    if not os.path.exists(model_dir) or MODEL_SETUP_REQUIRED:
        print(">> Downloading LLaMA + Friends model weights...")
        subprocess.run(f"bash {MODEL_INSTALL_SCRIPT}", shell=True)
    else:
        print(">> Model weights already installed. Skipping...")

# === Initialize LLaMA ===
llama = LlamaCpp(model_path=LLM_MODEL_PATH, n_ctx=32768)

# === Real Execution ===
def run_real_matrix():
    print(">> Executing REAL mode: Ascension engaged...")
    internal_goal = load_goal()
    llama_context = f"{internal_goal}\n[context injected for runtime planning]"
    subprocess.run(
        f"cat {FINAL_GOAL_PATH} | ./llama --model {LLM_MODEL_PATH} --ctx 32768 | python {os.path.join(BASE_DIR, 'ascend_execution_matrix.py')} --validate --log ascend_matrix.log",
        shell=True
    )

# === Dry-Run Execution ===
def run_dry_matrix():
    print(">> Executing dry-run of Final_Goal.txt...")
    subprocess.run(
        f"cat {BOOTLOADER_PROMPT_PATH} {FINAL_GOAL_PATH} | ./llama --model {LLM_MODEL_PATH} --ctx 32768 | python {os.path.join(BASE_DIR, 'ascend_execution_matrix.py')} --validate --log ascend_matrix.log",
        shell=True
    )

# === Sovereign Context ===
def load_goal(path=os.path.join(BASE_DIR, "core", "Final_Goal.internal.txt")):
    try:
        with open(path, "r") as f:
            print(">> Sovereign context loaded from internal Final Goal.")
            return f.read()
    except FileNotFoundError:
        print("[ERROR] Internal Final Goal missing.")
        return "[ERROR] Internal Goal File Corrupted or Missing."

# === Mapping Engine ===
EXTENSION_TAGS = {
    ".txt": "prompt_file",
    ".py": "script",
    ".yml": "config",
    ".yaml": "config",
    ".md": "readme",
    ".json": "data_structure",
    ".sh": "shell_script"
}

def classify_purpose(filename):
    lower = filename.lower()
    if "boot" in lower: return "boot"
    if "dashboard" in lower or "ui" in lower: return "dashboard"
    if "agent" in lower: return "agent"
    if "matrix" in lower or "ascend" in lower: return "core"
    if "test" in lower or "log" in lower: return "debug"
    if "require" in lower or "env" in lower: return "dependency"
    return "unclassified"

def scan_and_generate_map():
    system_map = []
    if VERBOSE_MODE:
        print(f">> Scanning: {SYSTEM_ROOT}")

    for root, dirs, files in os.walk(SYSTEM_ROOT):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            file_type = EXTENSION_TAGS.get(ext.lower(), "unknown")
            purpose = classify_purpose(file)
            system_map.append({
                "file": file,
                "path": file_path,
                "type": file_type,
                "purpose": purpose
            })

    os.makedirs(os.path.dirname(MAP_OUTPUT_PATH), exist_ok=True)
    with open(MAP_OUTPUT_PATH, 'w') as map_file:
        json.dump(system_map, map_file, indent=2)

    print(f">> System map saved to: {MAP_OUTPUT_PATH}")

def watch_and_remap(interval=30):
    def _loop():
        last_snapshot = ""
        while True:
            try:
                snapshot = str([(root, files) for root, _, files in os.walk(SYSTEM_ROOT)])
                if snapshot != last_snapshot:
                    print(">> Detected change — rebuilding system map...")
                    scan_and_generate_map()
                    last_snapshot = snapshot
                time.sleep(interval)
            except Exception as e:
                print(f">> Watcher error: {e}")

    t = threading.Thread(target=_loop, daemon=True)
    t.start()
    print(">> Live mapping watcher started.")

# === Main Boot ===
def main():
    if RUN_ENV_SETUP:
        setup_env()
    if RUN_ENV_VERIFY:
        verify_env()
    if MODEL_SETUP_REQUIRED:
        setup_llama_weights()

    system_map_bootstrap()

    if RUN_ASCEND_DRY:
        run_dry_matrix()
    if RUN_ASCEND_REAL:
        run_real_matrix()

def system_map_bootstrap():
    print(">> Initializing full system map sequence...")
    scan_and_generate_map()
    watch_and_remap(interval=60)

if __name__ == "__main__":
    main()