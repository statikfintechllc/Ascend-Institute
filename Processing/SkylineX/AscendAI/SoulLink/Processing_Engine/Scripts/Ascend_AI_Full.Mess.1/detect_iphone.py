
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def detect_iphone():
    print("[] Searching for nearby iPhones...")
        output = subprocess.check_output(["bluetoothctl", "scan", "on"], universal_newlines=True)
        for line in output.split("\n"):
            if "iPhone" in line:
                iphone_mac = line.split()[2]
                print(f"[] iPhone detected: {iphone_mac}")
                return iphone_mac
        print(f"[] Error detecting iPhone: {e}")
    return None

if __name__ == '__main__':
    detect_iphone()