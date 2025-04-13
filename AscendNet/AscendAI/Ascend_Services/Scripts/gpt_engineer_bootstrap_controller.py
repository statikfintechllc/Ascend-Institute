
import os
import subprocess
import time
import random
import traceback

SCRIPTS_DIR = "./Scripts"
LOG_FILE = "./bootstrap_log.txt"
RETRY_LIMIT = 3
MUTATION_RECORD = {}

def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{time.ctime()}] {message}\n")
    print(message)

def run_script(script_path):
    try:
        result = subprocess.run(["python3", script_path], capture_output=True, timeout=60)
        if result.returncode == 0:
            log(f"✅ SUCCESS: {script_path}")
            return True
        else:
            log(f"❌ FAIL: {script_path} | {result.stderr.decode()}")
            return False
    except Exception as e:
        log(f"⚠️ ERROR: {script_path} | {e}")
        return False

def mutate_script_order(scripts):
    # Random shuffle based on last run result to encourage new patterns
    log("♻️ Mutating script execution order...")
    random.shuffle(scripts)
    return scripts

def run_all_scripts():
    log("🚀 Starting GPT-Engineer Bootstrap Controller")
    scripts = [os.path.join(SCRIPTS_DIR, f) for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py")]
    retry_tracker = {script: 0 for script in scripts}
    
    scripts = mutate_script_order(scripts)

    for _ in range(3):  # 3 mutation rounds
        for script in scripts:
            if retry_tracker[script] >= RETRY_LIMIT:
                log(f"🚫 Max retries exceeded for: {script}")
                continue

            success = run_script(script)
            if not success:
                retry_tracker[script] += 1
                time.sleep(2)
        scripts = mutate_script_order(scripts)
    log("✅ Bootstrap process complete.")

if __name__ == "__main__":
    run_all_scripts()
