
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def mimic_human_behavior():
    print(" Mimicking Human Behavior...")
        time.sleep(random.uniform(1, 5))  # Random delays
        text = "Hello, I am not AI."
        typo_text = ''.join([char if random.random() > 0.05 else random.choice("abcdefghijklmnopqrstuvwxyz") for char in text])
        pyautogui.write(typo_text, interval=random.uniform(0.1, 0.5))  # Type with typos
        x, y = random.randint(100, 900), random.randint(100, 600)
        pyautogui.moveTo(x, y, duration=random.uniform(0.5, 2))  # Move mouse randomly

if __name__ == '__main__':
    mimic_human_behavior()