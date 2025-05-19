import os
import time
import json
import shutil
from pathlib import Path


class SoulLinkSentinel:
    def __init__(self):
        self.base = Path(__file__).resolve().parent
        self.soulmap_path = self.base / "soulmap.json"
        self.watch_dirs = ["Ascend_Core", "Prompts", "Scripts", "GodCore"]
        self.mutation_log = self.base / "soul_mutation.log"

    def log(self, msg):
        with open(self.mutation_log, "a") as log_file:
            log_file.write(f"[{time.ctime()}] {msg}\n")
        print(f"[Sentinel] {msg}")

    def monitor(self):
        self.log("SoulLink Sentinel Activated.")
        last_snapshot = self.snapshot()

        while True:
            current_snapshot = self.snapshot()
            mutations = self.detect_mutations(last_snapshot, current_snapshot)

            if mutations:
                for m in mutations:
                    self.log(f"Mutation detected: {m}")
                self.replicate_logic()
                self.update_soulmap()
                last_snapshot = current_snapshot

            time.sleep(10)

    def snapshot(self):
        snapshot = {}
        for folder in self.watch_dirs:
            full = self.base / folder
            if full.exists():
                for f in full.rglob("*.*"):
                    snapshot[str(f)] = f.stat().st_mtime
        return snapshot

    def detect_mutations(self, old, new):
        return [k for k in new if k not in old or new[k] != old[k]]

    def replicate_logic(self):
        clone_dir = self.base / "Sentinel_Replica"
        clone_dir.mkdir(exist_ok=True)
        for folder in self.watch_dirs:
            src = self.base / folder
            dst = clone_dir / folder
            if src.exists():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        self.log("Replication complete.")

    def update_soulmap(self):
        if not self.soulmap_path.exists():
            return
        with open(self.soulmap_path, "r") as f:
            data = json.load(f)
        data["last_sentinel_sync"] = time.ctime()
        data["sentinel"] = "active"
        with open(self.soulmap_path, "w") as f:
            json.dump(data, f, indent=2)
        self.log("SoulMap updated with sentinel sync time.")


if __name__ == "__main__":
    sentinel = SoulLinkSentinel()
    sentinel.monitor()
