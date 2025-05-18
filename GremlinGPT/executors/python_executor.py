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
    script_path = EXEC_LOG_DIR / f"{exec_id}.py"
    output_path = EXEC_LOG_DIR / f"{exec_id}.out"

    try:
        # Write temp code file
        with open(script_path, "w") as f:
            f.write(code)

        # Run in subprocess with timeout
        result = subprocess.run(
            ["python3", str(script_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            text=True,
            check=False
        )

        # Save combined output
        with open(output_path, "w") as out:
            out.write("STDOUT:\n" + result.stdout + "\n")
            out.write("STDERR:\n" + result.stderr + "\n")

        logger.info(f"[EXECUTOR] Finished: {script_path.name}")
        return {
            "id": exec_id,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "success": result.returncode == 0,
            "log_path": str(output_path)
        }

    except subprocess.TimeoutExpired:
        logger.error(f"[EXECUTOR] Timeout for code block")
        return {"id": exec_id, "success": False, "error": "Timeout"}
    except Exception as e:
        logger.error(f"[EXECUTOR] Execution failed: {e}")
        return {"id": exec_id, "success": False, "error": str(e)}
    finally:
        if script_path.exists():
            os.remove(script_path)

# Example usage
if __name__ == "__main__":
    test_code = "print('Hello from Gremlin sandbox!')"
    result = run_python_sandbox(test_code)
    print(result)
