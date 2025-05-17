
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def test_tor_connection():
    """Validates TOR connection by checking IP address."""
        response = requests.get("http://check.torproject.org")
        if "Congratulations" in response.text:
            logging.info(" TOR Network Successfully Connected")
            logging.warning(" TOR Connection Failed.")
        logging.error(f" Error Testing TOR Connection: {e}")

if __name__ == '__main__':
    test_tor_connection()