import os
import subprocess

def main():
    print("[+] Building llama-cpp-python with CUDA...")
    env = os.environ.copy()
    env["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
    env["FORCE_CMAKE"] = "1"
    subprocess.run(["pip", "install", "--no-cache-dir", "--force-reinstall", "llama-cpp-python"], check=True, env=env)
