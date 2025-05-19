import os
import hashlib
import json
import datetime

VERSION_TRACKER_PATH = "./ModelRegistry/version_history.json"
VERSION_DIR = "./ModelRegistry"
REUSE_DIR = "./ReusableModules"


def init_registry():
    os.makedirs(VERSION_DIR, exist_ok=True)
    os.makedirs(REUSE_DIR, exist_ok=True)
    if not os.path.exists(VERSION_TRACKER_PATH):
        with open(VERSION_TRACKER_PATH, "w") as f:
            json.dump({}, f, indent=2)


def hash_model(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def register_model(model_name, file_path, context_note=""):
    init_registry()
    model_hash = hash_model(file_path)
    timestamp = datetime.datetime.now().isoformat()

    with open(VERSION_TRACKER_PATH, "r") as f:
        registry = json.load(f)

    version_id = f"{model_name}_{timestamp}"
    registry[version_id] = {
        "model_name": model_name,
        "timestamp": timestamp,
        "hash": model_hash,
        "context": context_note,
        "path": file_path,
    }

    with open(VERSION_TRACKER_PATH, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"✅ Model registered: {version_id}")
    return version_id


def reuse_module(module_path):
    if not os.path.exists(module_path):
        print(f"❌ Module {module_path} not found.")
        return

    file_name = os.path.basename(module_path)
    target = os.path.join(REUSE_DIR, file_name)
    with open(module_path, "r") as f:
        code = f.read()

    # Check if already saved
    if os.path.exists(target):
        with open(target, "r") as tf:
            if tf.read() == code:
                print("✅ Module already stored. Skipping duplicate.")
                return

    with open(target, "w") as f:
        f.write(code)
    print(f"♻️ Reusable Module Stored: {file_name}")


def mutate_module(module_path, mutation_prompt, generator):
    with open(module_path, "r") as f:
        current_code = f.read()

    prompt = f"""Mutate the following module to improve:
- Defense (resilience to failure)
- Accuracy (less hallucination)
- Scalability (multi-device or cloud)
- Speed (inference + execution)
- AI Intelligence (dynamic thinking)

INSTRUCTIONS: {mutation_prompt}

MODULE:
{current_code}

Return only the updated Python code:
"""
    result = generator(prompt, max_new_tokens=300)[0]["generated_text"]

    with open(module_path, "w") as f:
        f.write(result)

    print(f"🧬 Mutated & Updated: {module_path}")


def get_version_history():
    if not os.path.exists(VERSION_TRACKER_PATH):
        print("⚠️ No model version history found.")
        return {}
    with open(VERSION_TRACKER_PATH, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    init_registry()
    print("📦 Model Versioning Engine Initialized.")
