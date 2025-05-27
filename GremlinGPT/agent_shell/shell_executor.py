# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import subprocess
import shlex
import json
from datetime import datetime
from pathlib import Path
from memory.vector_store.embedder import package_embedding
from backend.globals import logger

LOG_PATH = Path("run/logs/shell_log.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

SAFE_COMMANDS = [
    "ls",
    "pwd",
    "whoami",
    "echo",
    "ps",
    "top",
    "df",
    "free",
    "uptime",
    "uname",
    "cat",
    "grep",
    "find",
]


def run_shell_command(cmd: str) -> str:
    parsed = shlex.split(cmd)

    if not parsed:
        logger.warning("[SHELL] Empty or invalid command.")
        return "[DENIED] Empty command"

    if parsed[0] not in SAFE_COMMANDS:
        logger.warning(f"[SHELL] Unsafe command blocked: {parsed[0]}")
        return f"[DENIED] Unsafe command: {parsed[0]}"

    try:
        result = subprocess.run(parsed, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip() or result.stderr.strip()

        meta = {
            "origin": "shell_executor",
            "command": cmd,
            "timestamp": datetime.utcnow().isoformat(),
            "watermark": "source:GremlinGPT",
        }

        package_embedding(cmd + "\n" + output, meta=meta)

        with open(LOG_PATH, "a") as log:
            log.write(
                json.dumps(
                    {
                        "timestamp": meta["timestamp"],
                        "command": cmd,
                        "output": output,
                    }
                )
                + "\n"
            )

        logger.info(f"[SHELL] Executed: {cmd}")
        return output

    except Exception as e:
        logger.error(f"[SHELL] Execution error: {e}")
        return f"[ERROR] {e}"
