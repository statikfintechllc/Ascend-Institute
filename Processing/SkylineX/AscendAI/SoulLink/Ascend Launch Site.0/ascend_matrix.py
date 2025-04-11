#!/usr/bin/env python3

import subprocess
import gnupg
import os
import time
import re
import logging
import shutil
import hashlib
import docker
import json
from datetime import datetime
from ascend_execution_matrix import interpret_task

# === Dynamic Base Path ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Logging ===
LOG_FILE = os.path.join(BASE_DIR, 'ascend_matrix.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

# === Boot State Files ===
APPROVED_TASKS_PATH = os.path.join(BASE_DIR, "approved_tasks.jsonl")
SIGNATURE_FILE = os.path.join(BASE_DIR, "llama_output.sig")
LLAMA_OUTPUT_FILE = os.path.join(BASE_DIR, "llama_output.txt")
GOAL_MEMORY_FILE = os.path.join(BASE_DIR, "goal_memory.jsonl")

if not os.path.exists(APPROVED_TASKS_PATH):
    with open(APPROVED_TASKS_PATH, "w") as f:
        f.write("")

# Constants
MAX_TASK_ITERATIONS = 10
THROTTLE_INTERVAL = 2
DRY_RUN_MODE = False
DANGEROUS_PATTERNS = [r"rm\s+-rf", r"sudo.*shutdown", r"mkfs.*", r"format", r"dd if=.* of=.*", r":\(\)\{:\|:&\};:"]
task_counter = {}
gpg = gnupg.GPG()

def verify_environment():
    subprocess.run('conda activate ascendenv', shell=True)

def sanitize_task(task):
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, task):
            logging.warning(f"Dangerous pattern detected: {task}")
            return False
    return True

def verify_signature(task, signature_path):
    try:
        with open(signature_path, 'rb') as sig_file:
            verified = gpg.verify_data(sig_file, task.encode())
        if not verified.valid:
            logging.error("Invalid task signature.")
            return False
        return True
    except Exception as e:
        logging.error(f"Signature verification failed: {e}")
        return False

def verify_script_integrity(script_path, expected_checksum):
    with open(script_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    if file_hash != expected_checksum:
        logging.error(f"Checksum mismatch: {script_path}")
        return False
    return True

def update_checksum(script_path):
    with open(script_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    manifest_path = os.path.join(BASE_DIR, ".matrix_manifest")
    with open(manifest_path, "a") as mf:
        mf.write(f"{script_path}: {file_hash}\n")
    logging.info(f"Checksum updated for {script_path}")

def dry_run(task):
    logging.info(f"[DRY RUN] Task: {task}")

def sandbox_task(task):
    try:
        client = docker.from_env()
        client.images.pull('python:3.11-slim')
        container = client.containers.run(
            'python:3.11-slim',
            f'/bin/bash -c "{task}"',
            detach=True,
            network_mode='none',
            pids_limit=100,
            read_only=True
        )
        logging.info(f"Sandboxed task: Container {container.id}")
        container.wait()
        container.remove()
    except Exception as e:
        logging.error(f"Sandbox error: {e}")

def create_backup(files=['Final_Goal.txt', 'ascend_matrix.log', 'configs']):
    backup_dir = os.path.join(BASE_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(backup_dir, exist_ok=True)
    for file in files:
        src = os.path.join(BASE_DIR, file)
        subprocess.run(["cp", "-r", src, backup_dir])
    logging.info(f"Backup created at {backup_dir}")
    return backup_dir

def rollback_from_backup(backup_dir):
    for file in os.listdir(backup_dir):
        subprocess.run(["cp", "-r", os.path.join(backup_dir, file), BASE_DIR])
    logging.info(f"Rollback restored from {backup_dir}")

def push_to_dashboard(event):
    try:
        with open(LOG_FILE, "rb") as log_file:
            data = {
                "timestamp": str(datetime.now()),
                "event": event,
                "log": log_file.read().decode(errors='ignore')
            }
        subprocess.run([
            "curl", "-X", "POST", "http://localhost:5000/dashboard",
            "-d", json.dumps(data)
        ])
    except Exception as e:
        logging.warning(f"Dashboard push failed: {e}")

def await_human_approval(task_meta):
    approval_dir = os.path.join(BASE_DIR, "approval_required")
    approved_dir = os.path.join(BASE_DIR, "approved")
    os.makedirs(approval_dir, exist_ok=True)
    os.makedirs(approved_dir, exist_ok=True)

    approval_file = os.path.join(approval_dir, f"{int(time.time())}.json")
    with open(approval_file, "w") as f:
        json.dump(task_meta, f)

    logging.info(f"[AWAITING APPROVAL] {task_meta['intent']} — Awaiting iPhone signal")

    while not os.path.exists(os.path.join(approved_dir, os.path.basename(approval_file))):
        time.sleep(1)

    logging.info(f"[APPROVED] {task_meta['intent']}")

def execute_task(task, signature):
    if DRY_RUN_MODE:
        dry_run(task)
        return

    if not sanitize_task(task):
        logging.error("Task sanitization blocked execution.")
        return

    interpretation = interpret_task(task)
    meta = {
        "type": interpretation.get("type", "unknown"),
        "risk": interpretation.get("risk", "low"),
        "intent": interpretation.get("intent", "unknown"),
        "origin": interpretation.get("origin", "unknown"),
        "requires_approval": False
    }

    if not is_task_whitelisted(task) and meta["risk"] in ["high", "critical"]:
        meta["requires_approval"] = True

    if meta["requires_approval"]:
        push_to_dashboard(meta)
        await_human_approval(meta)
        log_approved_task(task)

    if meta["type"] == 'shell':
        command = interpretation["command"]
        if meta["risk"] == 'high':
            sandbox_task(command)
        else:
            result = subprocess.run(command, shell=True, capture_output=True)
            if result.returncode != 0:
                logging.error(f"Shell task failed: {result.stderr.decode()}")
            else:
                logging.info(f"Shell task success: {result.stdout.decode()}")

    elif meta["type"] == 'agent':
        agent_script = os.path.join(BASE_DIR, interpretation['script'])
        logging.info(f"Launching agent: {agent_script}")
        subprocess.run(["python3", agent_script])
    else:
        logging.warning(f"Unknown interpretation type: {interpretation}")

def log_approved_task(task):
    with open(APPROVED_TASKS_PATH, "a") as f:
        f.write(json.dumps({"task": task}) + "\n")

def is_task_whitelisted(task):
    with open(APPROVED_TASKS_PATH, "r") as f:
        for line in f:
            approved = json.loads(line)
            if approved["task"] == task:
                return True
    return False

def compose_agent(goal_json):
    agent_id = f"agent_{int(time.time())}"
    tpl_path = os.path.join(BASE_DIR, "agent_templates", f"{goal_json['intent']}.tpl")
    agents_dir = os.path.join(BASE_DIR, "agents")
    os.makedirs(agents_dir, exist_ok=True)

    if not os.path.exists(tpl_path):
        logging.error(f"No agent template for intent: {goal_json['intent']}")
        return None

    with open(tpl_path, 'r') as tpl:
        code = tpl.read().replace("{{INTENT}}", goal_json['intent'])

    output_file = os.path.join(agents_dir, f"{agent_id}.py")
    with open(output_file, 'w') as out:
        out.write(code)

    logging.info(f"Agent composed: {output_file}")
    return output_file

def log_goal_memory(task, result, interpretation):
    memory = {
        "timestamp": str(datetime.now()),
        "task": task,
        "result": result,
        "meta": interpretation
    }
    with open(GOAL_MEMORY_FILE, 'a') as f:
        f.write(json.dumps(memory) + "\n")

def main_execution_matrix():
    verify_environment()
    backup_dir = create_backup()

    try:
        with open(LLAMA_OUTPUT_FILE, 'r') as f:
            tasks = f.read().splitlines()
        logging.info(f"Loaded {len(tasks)} tasks from llama_output.txt")
    except FileNotFoundError:
        logging.error("llama_output.txt missing — aborting matrix execution.")
        rollback_from_backup(backup_dir)
        return

    try:
        with open(SIGNATURE_FILE, 'r') as sig_file:
            signatures = sig_file.readlines()
    except FileNotFoundError:
        logging.warning("No signature file found — enabling DRY RUN.")
        global DRY_RUN_MODE
        DRY_RUN_MODE = True
        signatures = [''] * len(tasks)

    if len(signatures) < len(tasks):
        logging.warning("Signature count mismatch — continuing in DRY RUN mode.")
        DRY_RUN_MODE = True

    for task, signature in zip(tasks, signatures):
        execute_task(task.strip(), signature.strip())
        time.sleep(THROTTLE_INTERVAL)

    automation_path = os.path.join(BASE_DIR, "automation_module.py")
    sandbox_task(f"python {automation_path} {LLAMA_OUTPUT_FILE}")

if __name__ == '__main__':
    main_execution_matrix()
