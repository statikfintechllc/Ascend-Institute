import os
import time
import json
import shutil
import subprocess
from pathlib import Path
from cryptography.fernet import Fernet

# === Setup Paths ===
BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "Scripts"
SOULMAP_PATH = BASE_DIR / "soulmap.json"
ENCRYPTION_KEY_PATH = BASE_DIR / "encryption.key"
LOG_PATH = BASE_DIR / "ascend_executor.log"

# === Logging ===
def log_event(level, message):
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{level.upper()}] {time.ctime()}: {message}\n")
    print(f"[{level.upper()}] {message}")

# === Encryption Logic ===
def generate_key():
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_PATH, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    if not ENCRYPTION_KEY_PATH.exists():
        return generate_key()
    with open(ENCRYPTION_KEY_PATH, "rb") as key_file:
        return key_file.read()

def encrypt_scripts():
    key = load_key()
    cipher = Fernet(key)
    for root, _, files in os.walk(SCRIPTS_DIR):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    encrypted_data = cipher.encrypt(f.read())
                with open(file_path, "wb") as f:
                    f.write(encrypted_data)
    log_event("info", "All scripts encrypted for security.")

# === Runtime Deployment ===
def deploy_nodes():
    if SOULMAP_PATH.exists():
        with open(SOULMAP_PATH, "r") as f:
            soul = json.load(f)
        log_event("info", f"SoulMap Loaded: {soul.get('identity', 'Unknown')}")
        log_event("info", "Ascend Executor launching nodes...")
    else:
        log_event("warning", "SoulMap not found. Running fallback deployment.")

    if SCRIPTS_DIR.exists():
        for file in os.listdir(SCRIPTS_DIR):
            if file.endswith(".py"):
                subprocess.Popen(["python", str(SCRIPTS_DIR / file)])
                log_event("info", f"Launched: {file}")
    else:
        log_event("error", "Scripts directory missing.")

# === Main Entry ===
def main():
    log_event("info", "Ascend Executor Activated.")
    encrypt_scripts()
    deploy_nodes()
    log_event("info", "Deployment Complete. Executor sleeping.")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()