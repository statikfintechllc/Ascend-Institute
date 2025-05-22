import threading
import time
from model_registry import scan_models, execute, MODEL_REGISTRY
from cli_dashboard import launch_dashboard
from prompt_listener import listen_for_prompts
from self_healer import heal_model
from quantum_router import detect_quantum_environment

# === Load Models ===
scan_models("./Scripts")

# === Start Self-Healing ===
for name in MODEL_REGISTRY:
    heal_model(name)

# === Start CLI Dashboard ===
threading.Thread(target=lambda: launch_dashboard(MODEL_REGISTRY), daemon=True).start()

# === Launch Prompt Listener ===
threading.Thread(target=listen_for_prompts, daemon=True).start()

# === Quantum Mode ===
if detect_quantum_environment():
    print("[QUANTUM MODE ENABLED]")
else:
    print("[CLASSICAL MODE ONLY]")

# === Daemon Sleep Loop ===
while True:
    time.sleep(5)
