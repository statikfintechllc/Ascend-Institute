
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def run_command(command):
    """Executes a system command and prints output."""
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f" Error executing: {command}\n{process.stderr}")
        sys.exit(1)

if __name__ == '__main__':
    run_command()