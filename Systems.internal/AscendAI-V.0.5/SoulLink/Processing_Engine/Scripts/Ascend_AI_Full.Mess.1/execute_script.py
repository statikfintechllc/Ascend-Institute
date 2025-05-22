import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def execute_script(self, script_name):
    script_path = os.path.join(self.sandbox_path, script_name)
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
        log_event("info", f"Executed Sandbox Script: {script_name}")
        log_event("error", f"Script not found: {script_name}")


if __name__ == "__main__":
    execute_script()
