#!/usr/bin/env python3
#Run commands

#1
conda env create -f ascend_conda_base.yml
conda activate ascend_env

pip install -r ascend_requirements.txt

#!/usr/bin/env python3

import subprocess
import os
import sys

# === Config Flags ===
RUN_ENV_SETUP = True
RUN_ENV_VERIFY = True
RUN_ASCEND_DRY = True
RUN_ASCEND_REAL = False  # <- Flip to True when the Matrix awakens
SOULLINK_PATH = "./SoulLink"  # Optional soul-scanning directory

# === Step 1: Environment Setup ===
def setup_env():
    print(">> Setting up conda base environment...")
    subprocess.run("conda env create -f ascend_conda_base.yml", shell=True)
    subprocess.run("conda activate ascend_env", shell=True)
    subprocess.run("pip install -r ascend_requirements.txt", shell=True)

# === Step 2: Verify Everything Exists ===
def verify_env():
    print(">> Verifying environment and files...")
    subprocess.run("python Init_env_verify.py", shell=True)

# === Step 3: Run Dry Execution Through Matrix ===
def run_dry_matrix():
    print(">> Executing dry-run of Final_Goal.txt...")
    subprocess.run(
        "cat Final_Goal.txt | ./llama --model llama-13B.gguf --ctx 32768 | python ascend_execution_matrix.py --validate --dry-run --log ascend_matrix.log",
        shell=True
    )

# === Step 4: Full Fire ===
def run_real_matrix():
    print(">> Executing REAL mode: Ascension engaged...")
    subprocess.run(
        "cat Final_Goal.txt | ./llama --model llama-13B.gguf --ctx 32768 | python ascend_execution_matrix.py --validate --log ascend_matrix.log",
        shell=True
    )

# === Optional SoulLink Directory Crawl ===
def parse_soullink_directory():
    if os.path.exists(SOULLINK_PATH):
        print(f">> Parsing SoulLink directory: {SOULLINK_PATH}")
        for root, dirs, files in os.walk(SOULLINK_PATH):
            for file in files:
                print(f"  - Found: {os.path.join(root, file)}")
    else:
        print(">> SoulLink directory not found... yet.")

# === Main Logic ===
def main():
    if RUN_ENV_SETUP:
        setup_env()
    if RUN_ENV_VERIFY:
        verify_env()
    if RUN_ASCEND_DRY:
        run_dry_matrix()
    if RUN_ASCEND_REAL:
        run_real_matrix()
    parse_soullink_directory()

if __name__ == '__main__':
    main()
#4
#Unlock After Expansion and integration of decentralized cloud and computing

conda env create -f ascendenv.yml
conda activate ascendenv