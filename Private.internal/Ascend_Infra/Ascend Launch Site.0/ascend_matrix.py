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

# Setup
logging.basicConfig(
    filename='ascend_matrix.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s'
)

gpg = gnupg.GPG()
DRY_RUN_MODE = False
THROTTLE_INTERVAL = 2
DANGEROUS_PATTERNS = [r"rm\s+-rf", r"sudo.*shutdown", r"mkfs.*", r"format", r"dd if=.* of=.*", r":\(\)\{:\|:&\};:"]
APPROVED_TASKS = "approved_tasks.jsonl"
SOFT_FAIL_LOG = "soft_fail_memory.jsonl"

# Ensure logs exist
for f in [APPROVED_TASKS, SOFT_FAIL_LOG]:
    if not os.path.exists(f):
        open(f, "w").close()

# ---------- SYSTEM PRIMITIVES ----------

def verify_environment():
    subprocess.run('conda activate ascendenv', shell=True)

def create_backup(files=['Final_Goal.txt', 'ascend_matrix.log', 'configs']):
    bdir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(bdir, exist_ok=True)
    for f in files:
        subprocess.run(["cp", "-r", f, bdir])
    logging.info(f"[BACKUP] Created at {bdir}")
    return bdir

def rollback(backup_dir):
    for f in os.listdir(backup_dir):
        subprocess.run(["cp", "-r", f"{backup_dir}/{f}", "."])
    logging.warning(f"[ROLLBACK] Reverted from {backup_dir}")

# ---------- TASK REVIEW + APPROVAL ----------

def sanitize_task(task):
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, task):
            logging.warning(f"[SANITIZE] Rejected dangerous task: {task}")
            return False
    return True

def verify_signature(task, sig_path):
    try:
        with open(sig_path, 'rb') as s:
            return gpg.verify_data(s, task.encode()).valid
    except Exception as e:
        logging.error(f"[SIGNATURE FAIL] {e}")
        return False

def is_task_whitelisted(task):
    with open(APPROVED_TASKS, "r") as f:
        return any(json.loads(line)["task"] == task for line in f)

def log_approved_task(task):
    with open(APPROVED_TASKS, "a") as f:
        f.write(json.dumps({"task": task, "time": str(datetime.now())}) + "\n")

def log_soft_fail(task, reason, meta):
    entry = {
        "timestamp": str(datetime.now()),
        "task": task,
        "reason": reason,
        "meta": meta
    }
    with open(SOFT_FAIL_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    logging.info(f"[SOFT FAIL] {reason}")

def escalate_task(task, meta, reason):
    ticket = {
        "timestamp": str(datetime.now()),
        "task": task,
        "intent": meta.get("intent"),
        "origin": meta.get("origin"),
        "risk": meta.get("risk"),
        "reason": reason
    }
    os.makedirs("approval_required", exist_ok=True)
    review_path = f"approval_required/{int(time.time())}.json"
    with open(review_path, "w") as f:
        json.dump(ticket, f, indent=4)
    logging.warning(f"[ESCALATE] Task sent for manual approval: {reason}")
    return review_path

def await_manual_approval(review_path):
    approval_path = "approved/" + os.path.basename(review_path)
    logging.info(f"[AWAITING HUMAN INPUT] {review_path}")
    while not os.path.exists(approval_path):
        time.sleep(2)
    logging.info(f"[APPROVED MANUALLY] {review_path}")

# ---------- EXECUTION ----------

def sandbox_task(command):
    try:
        docker.from_env().containers.run(
            'python:3.11-slim',
            f'/bin/bash -c "{command}"',
            detach=False,
            network_mode='none',
            pids_limit=100,
            read_only=True,
            remove=True
        )
        logging.info(f"[SANDBOX] Executed: {command}")
    except Exception as e:
        logging.error(f"[SANDBOX ERROR] {e}")

def run_shell(command, risky):
    if risky:
        sandbox_task(command)
    else:
        result = subprocess.run(command, shell=True, capture_output=True)
        log = result.stdout.decode() if result.returncode == 0 else result.stderr.decode()
        logging.info(f"[SHELL {'OK' if result.returncode == 0 else 'FAIL'}] {log}")

def run_agent(agent_script):
    try:
        subprocess.run(["python3", agent_script])
        logging.info(f"[AGENT] Launched: {agent_script}")
    except Exception as e:
        logging.error(f"[AGENT ERROR] {e}")

def execute_task(task, sig):
    if DRY_RUN_MODE:
        logging.info(f"[DRY RUN] {task}")
        return

    if not sanitize_task(task):
        log_soft_fail(task, "Blocked: Dangerous content", {})
        return

    meta = interpret_task(task)

    if not is_task_whitelisted(task) and meta.get("risk") in ["high", "critical"]:
        path = escalate_task(task, meta, "Not whitelisted and risky")
        await_manual_approval(path)
        log_approved_task(task)

    ttype = meta.get("type")
    if ttype == "shell":
        run_shell(meta.get("command", ""), meta.get("risk") == "high")
    elif ttype == "agent":
        run_agent(meta.get("script", "unknown.py"))
    else:
        log_soft_fail(task, "Unknown task type", meta)

# ---------- MAIN EXECUTION FLOW ----------

def main_execution_matrix():
    verify_environment()
    backup = create_backup()

    llama_cmd = "cat Final_Goal.txt | ./llama --model llama-13B.gguf --ctx 32768"
    res = subprocess.run(llama_cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        logging.error("[LLaMA FAIL] Fallback triggered.")
        rollback(backup)
        return

    tasks = res.stdout.splitlines()
    try:
        with open("llama_output.sig", "r") as sigfile:
            sigs = sigfile.readlines()
    except FileNotFoundError:
        logging.warning("[SIG MISSING] DRY RUN activated.")
        global DRY_RUN_MODE
        DRY_RUN_MODE = True
        sigs = [''] * len(tasks)

    if len(sigs) < len(tasks):
        logging.warning("[SIG COUNT MISMATCH] Continuing in DRY RUN.")
        DRY_RUN_MODE = True

    for task, sig in zip(tasks, sigs):
        execute_task(task.strip(), sig.strip())
        time.sleep(THROTTLE_INTERVAL)

    subprocess.run(["python3", "automation_module.py", "llama_output.txt"])

if __name__ == "__main__":
    main_execution_matrix()
