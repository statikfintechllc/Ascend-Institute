import subprocess
from pathlib import Path
from datetime import datetime

# Optional: Uncomment if using OpenAI or local models
# import openai


def read_code_from_directory(path):
    return [Path(f).read_text() for f in Path(path).glob("*.py")]


def analyze_code_quality(code_list):
    # Use static analysis + benchmark logs + log weights
    return "Refactor inefficient loops, simplify logic, modularize NLP"


def select_best_model_for_task():
    # Choose based on the type of task
    return "starcoder"  # Replace with codet5, deepseek, etc.


def invoke_ai_model(model, prompt):
    if model == "starcoder":
        return call_local_starcoder(prompt)
    elif model == "codet5":
        return call_codet5_model(prompt)
    else:
        return call_fallback_model(prompt)


def validate_code(code):
    try:
        compile(code, "<string>", "exec")
        return True
    except Exception as e:
        log_error(e)
        return False


def deploy_code(code):
    Path("/AscendAI_Core/core_engine.py").write_text(code)


def rollback_and_log_failure():
    log("Rollback initiated due to failed optimization.")


def log_evolution(code):
    log_path = Path("/AscendAI_Logs/recursive_optimizations.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as log_file:
        log_file.write(f"\n\nNew Optimization @ {timestamp()}:\n{code}")


def log_error(error):
    with open("/AscendAI_Logs/optimization_errors.log", "a") as log_file:
        log_file.write(f"\n[{timestamp()}] {str(error)}")


def log(message):
    with open("/AscendAI_Logs/system.log", "a") as log_file:
        log_file.write(f"\n[{timestamp()}] {message}")


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# === MAIN LOOP ===
def recursive_self_optimization():
    while True:
        try:
            current_code = read_code_from_directory("/AscendAI_Core/")
            targets = analyze_code_quality(current_code)
            model = select_best_model_for_task()
            optimized_code = invoke_ai_model(model, prompt=targets)

            if validate_code(optimized_code):
                deploy_code(optimized_code)
                log_evolution(optimized_code)
            else:
                rollback_and_log_failure()

        except Exception as fail:
            log_error(fail)

        # Wait before next iteration
        import time

        time.sleep(600)  # 10 minutes
