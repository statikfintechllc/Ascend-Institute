from pathlib import Path
from datetime import datetime

LOG_DIR = Path("AscendAI_Logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def log(message: str):
    with open(LOG_DIR / "system.log", "a") as log_file:
        log_file.write(f"[{timestamp()}] {message}\n")


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    log("Ascend-AI Recursive Core Engine Initialized.")
    log("Waiting for external AI models to integrate...")


if __name__ == "__main__":
    main()
