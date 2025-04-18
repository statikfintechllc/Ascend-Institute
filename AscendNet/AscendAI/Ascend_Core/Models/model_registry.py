import os
import importlib.util
import logging
from datetime import datetime

# ================== CONFIG ==================
MODEL_BASE_PATH = os.path.expanduser("~/AscendAI/AscendNet/AscendAI/Ascend_Core/Models/")
LOGGING_LEVEL = logging.INFO
# ============================================

# Configure logging
logging.basicConfig(level=LOGGING_LEVEL, format="[%(levelname)s] %(message)s")

# Quantum detection -- safe and drama-free
QUANTUM_LIBS = ["qiskit", "pennylane", "cirq", "braket"]

def check_quantum_libs():
    for lib in QUANTUM_LIBS:
        try:
            __import__(lib)
            logging.info(f"[QUANTUM] {lib} detected.")
            return True
        except ImportError:
            continue
    return False

quantum_mode = check_quantum_libs()

# This is the holy ledger of loaded models
MODEL_REGISTRY = {}

# ================== CORE FUNCTIONS ==================

def load_model_module(file_path):
    name = os.path.splitext(os.path.basename(file_path))[0]
    try:
        spec = importlib.util.spec_from_file_location(name, file_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        MODEL_REGISTRY[name] = {
            "call": getattr(mod, "call_model", None),
            "load": getattr(mod, "load_model", None),
            "validate": getattr(mod, "validate_model", None),
            "test": getattr(mod, "test_model", None),
            "module": mod,
            "score": 100,  # Default trust
            "quantum": getattr(mod, "use_quantum", False),
            "last_loaded": datetime.utcnow().isoformat()
        }
        logging.info(f"[MODEL] {name} loaded successfully.")
    except Exception as e:
        logging.error(f"[ERROR] Failed to load model {name}: {e}")

def scan_models(base_folder=MODEL_BASE_PATH):
    logging.info(f"[SCAN] Scanning models in {base_folder}...")
    if not os.path.isdir(base_folder):
        logging.error(f"[SCAN] Directory not found: {base_folder}")
        return
    for root, _, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                load_model_module(os.path.join(root, file))

def validate_models():
    failed_models = []
    for name, meta in MODEL_REGISTRY.items():
        validator = meta.get("validate")
        if callable(validator):
            try:
                valid = validator()
                if not valid:
                    logging.warning(f"[VALIDATE] Model {name} failed validation.")
                    failed_models.append(name)
            except Exception as e:
                logging.warning(f"[VALIDATE] Exception while validating {name}: {e}")
                failed_models.append(name)
        else:
            logging.info(f"[VALIDATE] Model {name} has no validate() method. Skipping.")

    for name in failed_models:
        del MODEL_REGISTRY[name]
        logging.info(f"[REGISTRY] Model {name} removed due to failed validation.")

    logging.info(f"[VALIDATE] Validation complete. {len(MODEL_REGISTRY)} models remaining.")

# ================== EXECUTION & FUSION ==================

def select_best_model(task="default"):
    valid_models = [name for name, m in MODEL_REGISTRY.items() if callable(m["call"]) and m["score"] > 60]
    sorted_models = sorted(valid_models, key=lambda x: MODEL_REGISTRY[x]["score"], reverse=True)
    return sorted_models[0] if sorted_models else None

def fusion_output(prompt, models):
    outputs = []
    for name in models:
        try:
            result = MODEL_REGISTRY[name]["call"](prompt)
            outputs.append(f"[{name}]: {result}")
        except Exception as e:
            logging.warning(f"[FUSION] Model {name} failed: {e}")
    return "\n---\n".join(outputs)

def execute(prompt, model=None):
    if model and model in MODEL_REGISTRY:
        try:
            return MODEL_REGISTRY[model]["call"](prompt)
        except Exception as e:
            logging.warning(f"[EXEC] Primary model {model} failed: {e}")

    fallback = select_best_model()
    if fallback:
        try:
            return MODEL_REGISTRY[fallback]["call"](prompt)
        except Exception as e:
            logging.warning(f"[EXEC] Fallback model failed: {e}")

    # Last resort: ensemble
    top_models = list(MODEL_REGISTRY.keys())[:2]
    logging.info("[EXEC] Using ensemble fallback.")
    return fusion_output(prompt, top_models)

def cli():
    parser = argparse.ArgumentParser(
        description="Model Registry CLI -- Command your models like a true sovereign overlord."
    )
    parser.add_argument("--scan", action="store_true", help="Scan and load models from registry path")
    parser.add_argument("--validate", action="store_true", help="Run validate() on all models")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--prompt", type=str, help="Prompt to run with selected model")
    parser.add_argument("--model", type=str, help="Specify model name to execute prompt")
    parser.add_argument("--fusion", nargs="+", help="Run fusion output across multiple models")
    parser.add_argument("--quantum", action="store_true", help="Check if quantum mode is active")

    args = parser.parse_args()

    if args.scan:
        scan_models()
    if args.validate:
        validate_models()
    if args.list:
        print("Available Models:", list(MODEL_REGISTRY.keys()))
    if args.quantum:
        print("Quantum Mode:", "ENABLED" if quantum_mode else "DISABLED")
    if args.prompt:
        if args.fusion:
            print("[FUSION OUTPUT]")
            print(fusion_output(args.prompt, args.fusion))
        else:
            print("[EXECUTION RESULT]")
            print(execute(args.prompt, args.model))

if __name__ == "__main__":
    scan_models()
    validate_models()
    print("Available Models:", list(MODEL_REGISTRY.keys()))
    cli()