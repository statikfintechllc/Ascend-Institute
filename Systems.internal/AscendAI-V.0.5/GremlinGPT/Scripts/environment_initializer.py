#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

ENV_DIR = "/home/statiksmoke8/miniconda3/envs"

# Maps each environment to its required packages
ENV_DEFS = {
    "ai-core": [
        "torch",
        "transformers",
        "bitsandbytes",
        "accelerate",
        "deepspeed",
        "flash-attn",
        "xformers",
        "llama-cpp-python",
        "sentence-transformers",
        "pytorch-lightning",
        "optimum",
        "scipy",
        "numpy",
    ],
    "starcoder-wrapper": ["huggingface_hub", "transformers", "auto-gptq", "einops"],
    "nanogpt-wrapper": ["numpy", "datasets", "tiktoken"],
    "ai-agents": [
        "crewai",
        "langchain==0.0.293",
        "langgraph",
        "openai",
        "autogpt",
        "babyagi",
        "tiktoken",
        "pydantic",
        "tenacity",
    ],
    "vector-db": ["chromadb", "faiss-cpu", "weaviate-client"],
    "dashboard-ui": [
        "streamlit",
        "gradio",
        "dash",
        "panel",
        "flask",
        "fastapi",
        "uvicorn",
        "voila",
        "gunicorn",
    ],
    "quantum-research": [
        "qiskit",
        "qiskit-aer",
        "qiskit-ibmq-provider",
        "cirq",
        "pennylane",
        "azure-quantum",
        "braket",
    ],
    "finops": [
        "ib_insync",
        "alpaca-trade-api",
        "ccxt",
        "ta-lib",
        "finta",
        "quantstats",
        "backtrader",
        "bt",
        "pandas",
        "matplotlib",
        "yfinance",
        "zipline-reloaded",
    ],
    "stealth-core": [
        "watchdog",
        "pyinotify",
        "pyxhook",
        "getmac",
        "psutil",
        "loguru",
        "shodan",
    ],
    "surveillance-stack": [
        "opencv-python",
        "mediapipe",
        "face_recognition",
        "cvzone",
        "pyaudio",
        "pyttsx3",
        "gTTS",
        "SpeechRecognition",
        "PyAV",
    ],
    "ml-ops-deploy": [
        "docker",
        "kubernetes",
        "sagemaker",
        "mlflow",
        "bentoml",
        "onnx",
        "tritonclient",
        "torchserve",
    ],
    "netsec-tools": [
        "aircrack-ng",
        "bettercap",
        "nmap",
        "wireshark",
        "tcpdump",
        "mitmproxy",
        "macchanger",
        "reaver",
        "hydra",
        "john",
    ],
    "telemetry-ops": [
        "loguru",
        "fluentd",
        "filebeat",
        "elastic-apm",
        "opentelemetry",
        "graypy",
    ],
    "intel-recon": [
        "shodan",
        "whois",
        "python-whois",
        "theHarvester",
        "sublist3r",
        "spyse",
        "censys",
    ],
    "darknet-interface": ["stem", "onionshare", "flask-sock"],
    "ai-eval": [
        "torchmetrics",
        "evaluate",
        "datasets",
        "seqeval",
        "scikit-learn",
        "wandb",
    ],
    "code-fuzz": ["hypothesis", "afl", "fuzzingbook", "mutmut", "pytest"],
    "base-dev": [
        "pip",
        "setuptools",
        "wheel",
        "build",
        "httpx",
        "poetry",
        "pipdeptree",
        "pre-commit",
        "virtualenv",
    ],
}


def create_env(env_name, packages):
    print(f"\n[+] Creating environment: {env_name}")
    try:
        subprocess.run(
            ["conda", "create", "-y", "-n", env_name, "python=3.11"] + packages,
            check=True,
        )
        subprocess.run(
            ["conda", "env", "export", "-n", env_name],
            check=True,
            stdout=open(f"{ENV_DIR}/{env_name}.yml", "w"),
        )
        print(f"[✓] Environment '{env_name}' initialized successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to create env: {env_name}")
        print(e)


def main():
    print("Initializing all GremlinGPT Conda environments...")
    for env, pkgs in ENV_DEFS.items():
        create_env(env, pkgs)

    print("\n[✓] All environments have been processed.")


if __name__ == "__main__":
    if not Path(ENV_DIR).exists():
        os.makedirs(ENV_DIR)
    main()
