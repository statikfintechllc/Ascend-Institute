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
PATCH_LOG = "./patch_feedback.json"
RETRY_LIMIT = 3


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
    versions[path] = {"hash": hash_file(path), "timestamp": time.ctime()}
    with open(VERSIONS_FILE, "w") as f:
        json.dump(versions, f, indent=2)


def auto_generate_patch(script_path, error_log):
    if not os.path.exists(PATCH_DIR):
        os.makedirs(PATCH_DIR)

    prompt = f"Fix this Python error for the script {script_path}:\n{error_log}\nProvide only corrected Python code:"
    result = patch_gen(prompt, max_new_tokens=200)[0]["generated_text"]

    patch_path = os.path.join(PATCH_DIR, f"patch_{os.path.basename(script_path)}")
    with open(patch_path, "w") as f:
        f.write(result)
    log(f"🛠️ Patch generated for {script_path} → {patch_path}")
    return patch_path


def apply_patch(script_path, patch_path):
    try:
        with open(patch_path, "r") as patch_file:
            fixed_code = patch_file.read()
        with open(script_path, "w") as target_file:
            target_file.write(fixed_code)
        log(f"✅ Patch applied to {script_path}")
    except Exception as e:
        log(f"❌ Failed to apply patch to {script_path}: {e}")


def record_patch_feedback(script_path, outcome):
    feedback = {}
    if os.path.exists(PATCH_LOG):
        with open(PATCH_LOG, "r") as f:
            feedback = json.load(f)
    feedback_entry = feedback.get(script_path, {"success": 0, "fail": 0})
    if outcome == "success":
        feedback_entry["success"] += 1
    else:
        feedback_entry["fail"] += 1
    feedback[script_path] = feedback_entry
    with open(PATCH_LOG, "w") as f:
        json.dump(feedback, f, indent=2)


def run_script_with_tracking(script_path, retries):
    try:
        result = subprocess.run(
            ["python3", script_path], capture_output=True, timeout=60
        )
        if result.returncode == 0:
            log(f"✅ SUCCESS: {script_path}")
            save_success_version(script_path)
            record_patch_feedback(script_path, "success")
            return True
        else:
            error_text = result.stderr.decode()
            log(f"❌ FAIL: {script_path} | {error_text}")
            record_patch_feedback(script_path, "fail")
            if retries >= 2:
                patch_path = auto_generate_patch(script_path, error_text)
                apply_patch(script_path, patch_path)
            return False
    except Exception as e:
        log(f"⚠️ ERROR: {script_path} | {e}")
        record_patch_feedback(script_path, "fail")
        if retries >= 2:
            patch_path = auto_generate_patch(script_path, str(e))
            apply_patch(script_path, patch_path)
        return False


def run_all_scripts():
    log("🚀 Executing /Scripts/ with intelligent self-repair")
    retry_tracker = {}
    scripts = [
        os.path.join(SCRIPTS_DIR, f)
        for f in os.listdir(SCRIPTS_DIR)
        if f.endswith(".py")
    ]

    for i in range(3):  # 3 mutation rounds
        for script in scripts:
            retry_tracker.setdefault(script, 0)
            if retry_tracker[script] >= RETRY_LIMIT:
                continue
            success = run_script_with_tracking(script, retry_tracker[script])
            if not success:
                retry_tracker[script] += 1


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
    required_dirs = [
        SCRIPTS_DIR,
        PROMPTS_DIR,
        "./Core",
        "./Dashboard",
        "./Quantum",
        "./Security",
        PATCH_DIR,
    ]
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
    run_all_scripts()
    run_bootstrap_controller()
    activate_ascend_core()
    log(
        "✅ All systems launched. Ascend is now building, repairing, and evolving recursively."
    )
    log("====================================\n")


if __name__ == "__main__":
    start()
