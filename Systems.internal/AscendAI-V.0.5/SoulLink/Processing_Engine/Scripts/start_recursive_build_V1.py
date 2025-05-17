
import os
import time
import subprocess
import hashlib
import json
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

PROMPTS_DIR = "./prompts"
SCRIPTS_DIR = "./Scripts"
BOOTSTRAP_CONTROLLER = "./gpt_engineer_bootstrap_controller.py"
LOG_FILE = "./ascend_recursive_build_log.txt"
PATCH_DIR = "./Patches"
VERSIONS_FILE = "./ascend_success_versions.json"

# Load AI model for patch generation
def load_patch_generator():
    tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoder")
    model = AutoModelForCausalLM.from_pretrained("bigcode/starcoder")
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

patch_gen = load_patch_generator()

def log(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{time.ctime()}] {message}\n")
    print(message)

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def save_success_version(path):
    if not os.path.exists(VERSIONS_FILE):
        versions = {}
    else:
        with open(VERSIONS_FILE, "r") as f:
            versions = json.load(f)
    versions[path] = {
        "hash": hash_file(path),
        "timestamp": time.ctime()
    }
    with open(VERSIONS_FILE, "w") as f:
        json.dump(versions, f, indent=2)

def run_script_with_tracking(script_path):
    try:
        result = subprocess.run(["python3", script_path], capture_output=True, timeout=60)
        if result.returncode == 0:
            log(f"✅ SUCCESS: {script_path}")
            save_success_version(script_path)
            return True
        else:
            error_text = result.stderr.decode()
            log(f"❌ FAIL: {script_path} | {error_text}")
            auto_generate_patch(script_path, error_text)
            return False
    except Exception as e:
        log(f"⚠️ ERROR: {script_path} | {e}")
        auto_generate_patch(script_path, str(e))
        return False

def auto_generate_patch(script_path, error_log):
    if not os.path.exists(PATCH_DIR):
        os.makedirs(PATCH_DIR)

    prompt = f"Fix this Python error for the script {script_path}:\n{error_log}\nProvide only corrected Python code:"
    result = patch_gen(prompt, max_new_tokens=200)[0]["generated_text"]

    patch_path = os.path.join(PATCH_DIR, f"patch_{os.path.basename(script_path)}")
    with open(patch_path, "w") as f:
        f.write(result)
    log(f"🛠️ Patch generated for {script_path} → {patch_path}")

def run_bootstrap_controller():
    if os.path.exists(BOOTSTRAP_CONTROLLER):
        log("🚀 Launching GPT-Engineer Bootstrap Controller")
        subprocess.run(["python3", BOOTSTRAP_CONTROLLER])
    else:
        log("❌ Bootstrap controller not found!")

def run_all_prompts():
    log("📚 Executing all prompt logic inside /prompts/")
    for file in os.listdir(PROMPTS_DIR):
        if file.endswith(".txt"):
            path = os.path.join(PROMPTS_DIR, file)
            log(f"🧠 Processing Prompt File: {file}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                print(content[:500] + "...")  # Preview content

def validate_structure():
    log("🧱 Validating and auto-fixing core Ascend directory structure")
    required_dirs = [SCRIPTS_DIR, PROMPTS_DIR, "./Core", "./Dashboard", "./Quantum", "./Security", PATCH_DIR]
    for d in required_dirs:
        os.makedirs(d, exist_ok=True)

def activate_ascend_core():
    log("🔥 Activating Ascend Core Recursive Engine")
    if os.path.exists("./ascend_ai_self_evolution.py"):
        subprocess.Popen(["python3", "./ascend_ai_self_evolution.py"])
    if os.path.exists("./ascend_ai_decentralized_expander.py"):
        subprocess.Popen(["python3", "./ascend_ai_decentralized_expander.py"])

def start():
    log("====================================")
    log("🌐 Ascend Recursive Build Starting")
    validate_structure()
    run_all_prompts()
    run_bootstrap_controller()
    activate_ascend_core()
    log("✅ All systems launched. Ascend is now building itself recursively.")
    log("====================================\n")

if __name__ == "__main__":
    start()
