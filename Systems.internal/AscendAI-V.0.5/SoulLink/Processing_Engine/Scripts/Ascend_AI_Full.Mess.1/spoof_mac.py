import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def spoof_mac():
    """Randomizes the system MAC address for full anonymity."""
    os.system("ifconfig eth0 down")
    os.system("macchanger -r eth0")
    os.system("ifconfig eth0 up")
    logging.info(" MAC Address Spoofed")


if __name__ == "__main__":
    spoof_mac()
