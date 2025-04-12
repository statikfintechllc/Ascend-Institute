
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def encrypt_files():
    cipher = Fernet(ENCRYPTION_KEY)
    for root, _, files in os.walk(AI_PATH):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    encrypted_data = cipher.encrypt(f.read())
                with open(file_path, "wb") as f:
                    f.write(encrypted_data)
    log_event("info", "All scripts encrypted for security.")

if __name__ == '__main__':
    encrypt_files()