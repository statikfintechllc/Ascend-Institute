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

# Setup Logging
logging.basicConfig(
    filename='ascend_matrix.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

if not os.path.exists("approved_tasks.jsonl"):
    with open("approved_tasks.jsonl", "w") as f:
        f.write("")

# Constants
MAX_TASK_ITERATIONS = 10
THROTTLE_INTERVAL = 2
DRY_RUN_MODE = False
DANGEROUS_PATTERNS = [r"rm\s+-rf", r"sudo.*shutdown", r"mkfs.*", r"format", r"dd if=.* of=.*", r":\(\)\{:\|:&\};:"]
task_counter = {}
gpg = gnupg.GPG()

# Environment Verification
def verify_environment():
    subprocess.run('conda activate ascendenv', shell=True)

# Dangerous Pattern Scan
def sanitize_task(task):
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, task):
            logging.warning(f"Dangerous pattern detected: {task}")
            return False
    return True

# Signature Verification
def verify_signature(task, signature):
    verified = gpg.verify_data(signature, task.encode())
    if not verified.valid:
        logging.error("Invalid task signature.")
        return False
    return True

# Script Integrity Check
def verify_script_integrity(script_path, expected_checksum):
    with open(script_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    if file_hash != expected_checksum:
        logging.error(f"Checksum mismatch: {script_path}")
        return False
    return True

# Update Checksum CLI Tool
def update_checksum(script_path):
    with open(script_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    manifest_path = ".matrix_manifest"
    with open(manifest_path, "a") as mf:
        mf.write(f"{script_path}: {file_hash}\n")
    logging.info(f"Checksum updated for {script_path}")

# Dry Run Mode
def dry_run(task):
    logging.info(f"[DRY RUN] Task: {task}")

# Dockerized Sandbox
def sandbox_task(task):
    client = docker.from_env()
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

# Backup System
def create_backup(files=['Final_Goal.txt', 'ascend_matrix.log', 'configs']):
    backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    for file in files:
        subprocess.run(["cp", "-r", file, backup_dir])
    logging.info(f"Backup created at {backup_dir}")
    return backup_dir

# Rollback
def rollback_from_backup(backup_dir):
    for file in os.listdir(backup_dir):
        subprocess.run(["cp", "-r", f"{backup_dir}/{file}", "."])
    logging.info(f"Rollback restored from {backup_dir}")

# Dashboard API Hook
def push_to_dashboard(event):
    try:
        with open("ascend_matrix.log", "rb") as log_file:
            data = {
                "timestamp": str(datetime.now()),
                "event": event,
                "log": log_file.read().decode(errors='ignore')
            }
        subprocess.run(["curl", "-X", "POST", "http://localhost:5000/dashboard", "-d", json.dumps(data)])
    except Exception as e:
        logging.warning(f"Dashboard push failed: {e}")

# Approval Handler
def await_human_approval(task_meta):
    approval_file = f"approval_required/{int(time.time())}.json"
    with open(approval_file, "w") as f:
        json.dump(task_meta, f)

    logging.info(f"[AWAITING APPROVAL] {task_meta['intent']} — Awaiting iPhone signal")

    while not os.path.exists("approved/" + os.path.basename(approval_file)):
        time.sleep(1)

    logging.info(f"[APPROVED] {task_meta['intent']}")

# Core Task Executor
def execute_task(task, signature):
    if DRY_RUN_MODE:
        dry_run(task)
        return

    if not verify_signature(task, signature):
        logging.error("Task signature check failed.")
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
        return

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
        agent_script = interpretation['script']
        logging.info(f"Launching agent: {agent_script}")
        subprocess.run(["python3", agent_script])

    else:
        logging.warning(f"Unknown interpretation type: {interpretation}")

# Memory Tools
def log_approved_task(task):
    with open("approved_tasks.jsonl", "a") as f:
        f.write(json.dumps({"task": task}) + "\n")

def is_task_whitelisted(task):
    with open("approved_tasks.jsonl", "r") as f:
        for line in f:
            approved = json.loads(line)
            if approved["task"] == task:
                return True
    return False

def compose_agent(goal_json):
    agent_id = f"agent_{int(time.time())}"
    template_path = f"agent_templates/{goal_json['intent']}.tpl"
    with open(template_path, 'r') as tpl:
        code = tpl.read().replace("{{INTENT}}", goal_json['intent'])
    output_file = f"agents/{agent_id}.py"
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
    with open("goal_memory.jsonl", "a") as f:
        f.write(json.dumps(memory) + "\n")

# Main
def main_execution_matrix():
    verify_environment()
    backup_dir = create_backup()
    llama_cmd = "cat Final_Goal.txt | ./llama --model llama-13B.gguf --ctx 32768"
    result = subprocess.run(llama_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("LLaMA model failed.")
        rollback_from_backup(backup_dir)
        return
    tasks = result.stdout.splitlines()
    with open('llama_output.sig', 'r') as sig_file:
        signatures = sig_file.readlines()
    for task, signature in zip(tasks, signatures):
        execute_task(task.strip(), signature.strip())
        time.sleep(THROTTLE_INTERVAL)
    sandbox_task("python automation_module.py llama_output.txt")

if __name__ == '__main__':
    main_execution_matrix()
