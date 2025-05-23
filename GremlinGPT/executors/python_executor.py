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

# executors/python_executor.py

import subprocess
import tempfile
import uuid
import os
from pathlib import Path
from backend.globals import logger

EXEC_LOG_DIR = Path("run/logs/executions/")
EXEC_LOG_DIR.mkdir(parents=True, exist_ok=True)


def run_python_sandbox(code, timeout=5):
    exec_id = str(uuid.uuid4())
    output_path = EXEC_LOG_DIR / f"{exec_id}.out"

    try:
        # Use a safe temporary file for execution
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            script_path = tmp.name

        # Execute safely with timeout
        result = subprocess.run(
            ["python3", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True,
            check=False,
        )

        # Save output to log
        with open(output_path, "w") as out:
            out.write("STDOUT:\n" + result.stdout + "\n")
            out.write("STDERR:\n" + result.stderr + "\n")

        logger.info(f"[EXECUTOR] Finished: {Path(script_path).name}")
        return {
            "id": exec_id,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "success": result.returncode == 0,
            "log_path": str(output_path),
        }

    except subprocess.TimeoutExpired:
        logger.error("[EXECUTOR] Timeout during execution")
        return {"id": exec_id, "success": False, "error": "Timeout"}

    except Exception as e:
        logger.error(f"[EXECUTOR] Execution failed: {e}")
        return {"id": exec_id, "success": False, "error": str(e)}

    finally:
        # Clean up the temp script
        if "script_path" in locals() and os.path.exists(script_path):
            os.remove(script_path)


# CLI test mode
if __name__ == "__main__":
    test_code = "print('Hello from Gremlin sandbox!')"
    result = run_python_sandbox(test_code)
    print(result)
