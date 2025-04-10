import json
import importlib
import time

class ChainExecutor:
    def __init__(self, manifest_path="Chains/chains_manifest.json", sequence_path="Chains/chain_sequence.json"):
        with open(manifest_path, "r") as f:
            self.manifest = json.load(f)
        with open(sequence_path, "r") as f:
            self.sequences = json.load(f)
        self.log_path = "Chains/chains_log.txt"

    def execute_chain(self, chain_name=None):
        if not self.manifest.get("enabled"):
            return

        chain = chain_name or self.manifest.get("default_chain")
        tasks = self.sequences.get(chain, [])

        for task in tasks:
            self.run_task(task)
            if self.manifest.get("log_execution"):
                self.log(task)

    def run_task(self, task):
        print(f"[CHAIN] Executing: {task['task']} from {task['module']}")
        try:
            mod = importlib.import_module(task["module"])
            if hasattr(mod, task["task"]):
                getattr(mod, task["task"])()
            else:
                print(f"[CHAIN] Task {task['task']} not found in {task['module']}")
        except Exception as e:
            print(f"[CHAIN ERROR] {e}")

    def log(self, task):
        with open(self.log_path, "a") as f:
            f.write(f"[{time.ctime()}] Executed: {task['task']} from {task['module']}
")

# Example:
# ce = ChainExecutor()
# ce.execute_chain("core_sequence")
