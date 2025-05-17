import subprocess
import os
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCKER_DIR = ROOT_DIR / "Docker"

DOCKER_IMAGE = "gremlingpt-runner"

def build_docker_image():
    print("[Docker] Building container...")
    subprocess.run([
        "docker", "build", "-t", DOCKER_IMAGE, str(DOCKER_DIR)
    ], check=True)

def run_code_in_docker(code_str: str) -> str:
    """Executes the given Python code string safely inside a Docker container."""
    temp_code_file = DOCKER_DIR / f"temp_{uuid.uuid4().hex}.py"

    # Save the code to a file inside the Docker build context
    with open(temp_code_file, "w") as f:
        f.write(code_str)

    try:
        result = subprocess.check_output([
            "docker", "run", "--rm", "-v", f"{DOCKER_DIR}:/app", DOCKER_IMAGE,
            "python", f"/app/{temp_code_file.name}"
        ], stderr=subprocess.STDOUT, timeout=20)

        output = result.decode("utf-8")

    except subprocess.CalledProcessError as e:
        output = f"[Docker Error]\n{e.output.decode('utf-8')}"
    except Exception as e:
        output = f"[Execution Failed]\n{str(e)}"
    finally:
        if temp_code_file.exists():
            os.remove(temp_code_file)

    return output
