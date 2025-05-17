#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import time
from langchain.llms import LlamaCpp
import threading

# === Config Flags ===
RUN_ENV_SETUP = True
RUN_ENV_VERIFY = True
VERBOSE_MODE = True
MODEL_SETUP_REQUIRED = True  # Flip to False after models are installed once
MODEL_INSTALL_SCRIPT = "./llama_weights_and_models.sh"
RUN_ASCEND_DRY = True
RUN_ASCEND_REAL = False  # <- Flip this when the Matrix awakens
# === Corrected Constants ===
SYSTEM_ROOT = "/mnt"  # Actual root scan directory
OUTPUT_MAP_PATH = "/mnt/SkylineX/AscendAI/System Mapping/map.json"  # Fixed path

# === Step 1: Environment Setup ===
def setup_env():
    print(">> Setting up conda base environment...")
    subprocess.run("conda env create -f ascend_conda_base.yml", shell=True)
    subprocess.run("conda run -n ascend_env pip install -r ascend_requirements.txt", shell=True)

# === Step 2: Verify Everything Exists ===
def verify_env():
    print(">> Verifying environment and files...")
    subprocess.run("conda run -n ascend_env python Init_env_verify.py", shell=True)

# === Step 3: Download & Install Model Weights ===
def setup_llama_weights():
    if not os.path.exists("models/llama") or MODEL_SETUP_REQUIRED:
        print(">> Downloading LLaMA + Friends model weights...")
        subprocess.run(f"bash {MODEL_INSTALL_SCRIPT}", shell=True)
    else:
        print(">> Model weights already installed. Skipping...")
        
# === Initialize LLaMA ===
llm_model_path = 'llama-13B.gguf'
llama = LlamaCpp(model_path=llm_model_path, n_ctx=32768)

# === Step 4: Sovereign Boot + Real Fire ===
def run_real_matrix():
    print(">> Executing REAL mode: Ascension engaged...")

    internal_goal = load_goal()
    llama_context = f"{internal_goal}\n[context injected for runtime planning]"

    # Optional future context injection to engine
    # llama_engine.load_context(llama_context)

    subprocess.run(
        "cat Final_Goal.txt | ./llama --model llama-13B.gguf --ctx 32768 | python ascend_execution_matrix.py --validate --log ascend_matrix.log",
        shell=True
    )
    
    # === Step 5: Dry Matrix Execution ===
def run_dry_matrix():
    print(">> Executing dry-run of Final_Goal.txt...")
    subprocess.run(
        "cat bootloader_prompt.txt Final_Goal.txt | ./llama --model llama-13B.gguf --ctx 32768 | python ascend_execution_matrix.py --validate --log ascend_matrix.log",
        shell=True
    )

# === Sovereign Core Context Loader ===
def load_goal(path="/core/Final_Goal.internal.txt"):
    try:
        with open(path, "r") as f:
            print(">> Sovereign context loaded from internal Final Goal.")
            return f.read()
    except FileNotFoundError:
        print("[ERROR] Internal Final Goal missing.")
        return "[ERROR] Internal Goal File Corrupted or Missing."

# === File Classification ===
def system_map_bootstrap():
    print(">> Initializing full system map sequence...")
    scan_and_generate_map()
    watch_and_remap(interval=60)
    
EXTENSION_TAGS = {
    ".txt": "prompt_file",
    ".py": "script",
    ".yml": "config",
    ".yaml": "config",
    ".md": "readme",
    ".json": "data_structure",
    ".sh": "shell_script"
}

# === Purpose Heuristics ===
def classify_purpose(filename):
    lower = filename.lower()
    if "boot" in lower: return "boot"
    if "dashboard" in lower or "ui" in lower: return "dashboard"
    if "agent" in lower: return "agent"
    if "matrix" in lower or "ascend" in lower: return "core"
    if "test" in lower or "log" in lower: return "debug"
    if "require" in lower or "env" in lower: return "dependency"
    return "unclassified"

# === Mapping Logic ===
def scan_and_generate_map():
    system_map = []
    if VERBOSE_MODE: print(f">> Scanning: {SYSTEM_ROOT}")
    
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

    os.makedirs(os.path.dirname(OUTPUT_MAP_PATH), exist_ok=True)
    with open(OUTPUT_MAP_PATH, 'w') as map_file:
        json.dump(system_map, map_file, indent=2)

    print(f">> System map saved to: {OUTPUT_MAP_PATH}")

# === Live Monitor (Watcher) ===
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
    
# === Main Routine ===
def main():
    # 1. Generate instructions
    llama_output = generate_instructions('Final_Goal.txt')
    
# === Main Boot Sequence ===
def main():
    if RUN_ENV_SETUP:
        setup_env()
    if RUN_ENV_VERIFY:
        verify_env()
    if MODEL_SETUP_REQUIRED:
        setup_llama_weights()
    
    # Map the system once at the start
    system_map_bootstrap()
    
    if RUN_ASCEND_DRY:
        run_dry_matrix()
    if RUN_ASCEND_REAL:
        run_real_matrix()
# === Run Scan + Watch
# === Run Boot Sequence ===
if __name__ == "__main__":
    main()
