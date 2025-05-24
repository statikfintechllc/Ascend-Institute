# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────
#!/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# agent_shell/shell_executor.py

import subprocess
import shlex
import json
from datetime import datetime
from pathlib import Path
from memory.vector_store.embedder import package_embedding

LOG_PATH = Path("~/AscendNet/GremlinGPT/logs/shell_log.jsonl")
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

    if parsed[0] not in SAFE_COMMANDS:
        return f"[DENIED] Unsafe command: {parsed[0]}"

    try:
        result = subprocess.run(parsed, capture_output=True, text=True, timeout=10)
        output = result.stdout.strip() or result.stderr.strip()
        package_embedding(cmd + "\n" + output, source="shell")

        with open(LOG_PATH, "a") as log:
            log.write(
                json.dumps(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "command": cmd,
                        "output": output,
                    }
                )
                + "\n"
            )

        return output
    except Exception as e:
        return f"[ERROR] {e}"
