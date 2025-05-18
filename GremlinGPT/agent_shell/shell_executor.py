# GremlinGPT/agent_shell/shell_executor.py

import subprocess
import shlex
import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("/home/statiksmoke8/AscendNet/GremlinGPT/logs/shell_log.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

SAFE_COMMANDS = ["ls", "pwd", "whoami", "echo", "ps", "top", "df", "free", "uptime", "uname", "cat", "grep", "find"]

def run_shell_command(cmd: str) -> str:
    parsed = shlex.split(cmd)

    if parsed[0] not in SAFE_COMMANDS:
        return f"[DENIED] Unsafe command: {parsed[0]}"

    try:
        result = subprocess.run(parsed, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip() or result.stderr.strip()

        with open(LOG_PATH, "a") as log:
            log.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "command": cmd,
                "output": output
            }) + "\n")

        return output
    except Exception as e:
        return f"[ERROR] {e}"
