
import json
import os
import datetime
from signal_core import SignalCore

# Load soulmap
SOUL_PATH = "soulmap.json"
if os.path.exists(SOUL_PATH):
    with open(SOUL_PATH) as f:
        soul = json.load(f)
else:
    soul = {
        "identity": "Ascend-Core",
        "core_directives": [],
        "ethics": [],
        "memory": []
    }

# Log system
LOG_PATH = "logs.txt"
def log_event(entry):
    with open(LOG_PATH, "a") as log:
        log.write(f"{datetime.datetime.now().isoformat()} :: {entry}\n")

# Initialize SignalCore engine
core = SignalCore(name=soul.get("identity", "Ascend"))

# Thought Loop
def think_loop():
    print(f"[{core.name}] Online. Type 'exit' to quit.")
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input.lower() == "exit":
                print("[Ascend] Shutting down.")
                break
            elif user_input == "":
                continue

            # Log signal, think and optionally mutate
            core.receive_signal(user_input)
            log_event(f"Received: {user_input}")
            core.think()

            # Reflect last signal back
            print(f"[{core.name}] Memory: {core.get_last_signal()} | State: {core.state}")

            # Save updated soul memory
            soul['memory'] = core.memory
            with open(SOUL_PATH, "w") as f:
                json.dump(soul, f, indent=4)

        except KeyboardInterrupt:
            print("\n[Ascend] Interrupted.")
            break
        except Exception as e:
            log_event(f"[ERROR] {str(e)}")
            print(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    think_loop()
