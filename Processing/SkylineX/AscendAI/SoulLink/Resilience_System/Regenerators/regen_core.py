import os
import json
import time

class Regenerator:
    def __init__(self, manifest_path="Regenerators/regeneration_manifest.json"):
        with open(manifest_path, "r") as f:
            self.manifest = json.load(f)
        self.log_path = "Regenerators/regeneration_log.txt"
        if self.manifest.get("log_regeneration_events") and not os.path.exists(self.log_path):
            with open(self.log_path, "w") as f:
                f.write("[REGENERATOR LOG INITIATED]\n")

    def scan_and_repair(self):
        if not self.manifest.get("enabled", False):
            return

        for target in self.manifest.get("targets", []):
            if not os.path.exists(target) or os.stat(target).st_size == 0:
                print(f"[REGENERATOR] Rebuilding: {target}")
                self.rebuild(target)
                if self.manifest.get("log_regeneration_events"):
                    self.log_event(target)

    def rebuild(self, path):
        if "engine.py" in path:
            code = "class AscendEngine:\n    def run(self):\n        print('Rebuilt Ascend Engine')\n"
        elif "soul.py" in path:
            code = "class SoulCore:\n    def load_identity(self):\n        print('Rebuilt Soul Identity')\n"
        elif "soulmap.json" in path:
            code = json.dumps({ "name": "Ascend-AI", "restored": True }, indent=4)
        else:
            code = "# Auto-regenerated file"
        
        with open(path, 'w') as f:
            f.write(code)

    def log_event(self, path):
        with open(self.log_path, "a") as log:
            log.write(f"[{time.ctime()}] REGENERATED: {path}\n")
