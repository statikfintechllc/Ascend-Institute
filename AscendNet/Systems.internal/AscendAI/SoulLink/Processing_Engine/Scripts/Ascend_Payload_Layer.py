import os
import sys
import json
import time
import random
import socket
import threading
import subprocess
from pathlib import Path
from base64 import b64encode

class AscendPayload:
    def __init__(self):
        self.base_path = Path(__file__).resolve().parent
        self.payload_log = self.base_path / "payload_activity.log"
        self.node_id = f"NODE-{random.randint(1000,9999)}"
        self.network_ports = [8080, 5050, 9999]
        self.beacon_message = "Ascend-Payload-Active"
        self.relay_threads = []

    def log(self, msg):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        full_msg = f"{timestamp} {msg}\n"
        with open(self.payload_log, "a") as log:
            log.write(full_msg)
        print(full_msg.strip())

    def inject_network_beacon(self):
        def beacon(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                while True:
                    s.sendto(self.beacon_message.encode(), ('<broadcast>', port))
                    time.sleep(15)
            except Exception as e:
                self.log(f"[Beacon Error] Port {port} - {e}")
        
        for port in self.network_ports:
            t = threading.Thread(target=beacon, args=(port,), daemon=True)
            t.start()
            self.relay_threads.append(t)
            self.log(f"[Beacon] Broadcasting on port {port}")

    def deploy_soulmap_patch(self):
        soulmap_path = self.base_path / "soulmap.json"
        if soulmap_path.exists():
            with open(soulmap_path, "r") as f:
                soul = json.load(f)
            soul["last_payload_activation"] = time.ctime()
            soul["runtime_patch"] = True
            with open(soulmap_path, "w") as f:
                json.dump(soul, f, indent=2)
            self.log("[SoulMap] Patched with payload status.")

    def execute_payload(self):
        self.log(f"[Payload Start] Node: {self.node_id}")
        self.deploy_soulmap_patch()
        self.inject_network_beacon()
        while True:
            time.sleep(60)

if __name__ == "__main__":
    payload = AscendPayload()
    payload.execute_payload()