import toml
import json
import os

CONFIG_PATH = "config/config.toml"
MEMORY_JSON = "config/memory_settings.json"

def load_config():
    return toml.load(CONFIG_PATH)

def load_memory_config():
    with open(MEMORY_JSON) as f:
        return json.load(f)

CFG = load_config()
MEM = load_memory_config()

