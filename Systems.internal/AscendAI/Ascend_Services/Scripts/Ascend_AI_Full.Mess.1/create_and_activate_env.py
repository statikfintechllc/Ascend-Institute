
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def create_and_activate_env():
    """Creates and activates the Conda environment."""
    envs_output = subprocess.run(["conda", "env", "list"], capture_output=True, text=True)
    if CONDA_ENV_NAME not in envs_output.stdout:
        print(f" Creating Conda environment: {CONDA_ENV_NAME} with Python {PYTHON_VERSION}...")
        run_command(f"conda create --name {CONDA_ENV_NAME} python={PYTHON_VERSION} -y")
    print(f" Activating Conda environment: {CONDA_ENV_NAME}...")
    if sys.platform == "win32":
        activate_cmd = f"conda activate {CONDA_ENV_NAME} && python {sys.argv[0]}"
        os.system(activate_cmd)
        sys.exit(0)
        os.execvp("bash", ["bash", "-c", f"conda activate {CONDA_ENV_NAME} && python {sys.argv[0]}"])

if __name__ == '__main__':
    create_and_activate_env()