import os
import logging
import sys
from pathlib import Path
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

USE_OLLAMA = False  # Set to True to use Ollama instead of llama.cpp
from memory.task_journal import fetch_recent_logs

llm = None

if not USE_OLLAMA:
    try:
        from llama_cpp import Llama

        model_path = ROOT_DIR / "models" / "mistral-7b-instruct.gguf"
        if not model_path.exists():
            raise FileNotFoundError(f"[LLM LOAD] No model found at: {model_path}")

        llm = Llama(
            model_path=str(model_path), n_ctx=4096, n_gpu_layers=33, verbose=False
        )
        logging.info(f"[Model Interface] Loaded Mistral from {model_path}")

    except Exception as e:
        logging.error(f"[Model Interface] llama.cpp model load failed: {e}")
        llm = None


def ollama_query(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
        )
        return response.json()["response"]
    except Exception as e:
        logging.error(f"[Ollama Query Failed] {e}")
        return "[Model] Ollama backend unavailable."


def ask_model(prompt: str, max_tokens=512) -> str:
    print(f"[MODEL INPUT]\n{prompt}\n")

    # Check for similar past prompts
    recent_logs = fetch_recent_logs(limit=30)
    similar = [
        entry
        for entry in recent_logs
        if entry[2] == "error" and prompt[:25].lower() in entry[1].lower()
    ]

    if similar:
        warning_note = f"[MODEL WARNING] Similar failed task detected: '{similar[0][1]}'\nSkipping execution unless confirmed."
        print(warning_note)
        # You could route this back to the dashboard if needed
        try:
            requests.post(
                os.getenv("DASHBOARD_LOG_ENDPOINT", "http://localhost:5000/log"),
                json={"log": warning_note},
            )
        except Exception as dash_fail:
            logging.warning(f"[DASHBOARD POST FAIL] {dash_fail}")

    # Standard execution
    if USE_OLLAMA:
        return ollama_query(prompt)

    if llm:
        try:
            output = llm(
                f"[INST] {prompt} [/INST]",
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.95,
            )
            return output["choices"][0]["text"].strip()
        except Exception as e:
            logging.error(f"[LLM Error] {e}")
            return "[Model] Failed to respond from LLaMA."

    return "[Model] No model backend available."


from tools.self_edit import self_edit


def auto_remediate_failed_tasks():
    """Review failed logs and generate edits for broken tools/code."""
    failed = [entry for entry in fetch_recent_logs(50) if entry[2] == "error"]

    for log in failed:
        task_name = log[1].lower()
        detail = log[3]

        # Try to extract a matching filename from the log
        guessed_file = None
        for root, _, files in os.walk(ROOT_DIR / "tools"):
            for file in files:
                if (
                    file.endswith(".py")
                    and file.replace(".py", "").lower() in task_name
                ):
                    guessed_file = os.path.join(root, file)
                    break

        if guessed_file:
            print(f"[REMEDIATION] Attempting self-edit for {guessed_file}")
            instruction = f"Fix the following error automatically: {detail}"
            result = self_edit({"file_path": guessed_file, "instruction": instruction})
            print(f"[SELF-EDIT RESULT] {result}")
        else:
            print(
                f"[REMEDIATION SKIPPED] Could not determine file for task: {task_name}"
            )
