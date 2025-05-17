import json
import os

class SoulCore:
    def __init__(self, config_path="config/soulmap.json"):
        self.config_path = config_path
        self.identity = {}

    def load_identity(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.identity = json.load(f)
            print("Soul identity loaded.")
        else:
            print("soulmap.json missing.")
