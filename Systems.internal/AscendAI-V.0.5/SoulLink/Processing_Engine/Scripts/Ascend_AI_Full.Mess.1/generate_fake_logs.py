
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def generate_fake_logs():
    print(" Flooding System Logs with Fake Data...")
    log_file = "C:\\Windows\\System32\\Logs\\System.log"
    fake_entries = [
        "User logged in successfully",
        "Windows Defender scan completed, no threats found",
        "Network adapter reset due to inactivity",
        "Windows Update applied security patch KB123456",
        "User changed display settings"
        with open(log_file, "a") as f:
            f.write(random.choice(fake_entries) + "\n")
        time.sleep(random.randint(60, 300))

if __name__ == '__main__':
    generate_fake_logs()