import hashlib
import json
import os

CONSTITUTION_FILES = [
    "./memory/ascend_constitution.json",
    "./memory/ascend_dna.txt",
    "./prompts/skepticus_prompt.txt",
    "./prompts/secure_exec_prompt.txt"
]
OUTPUT = "./memory/constitution_hashes.json"

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def generate_hash_map():
    hash_map = {}
    for file in CONSTITUTION_FILES:
        if os.path.exists(file):
            hash_map[file] = hash_file(file)
    with open(OUTPUT, "w") as f:
        json.dump(hash_map, f, indent=4)
    print(f"[HASHMAP] Saved to {OUTPUT}")

if __name__ == "__main__":
    generate_hash_map()
