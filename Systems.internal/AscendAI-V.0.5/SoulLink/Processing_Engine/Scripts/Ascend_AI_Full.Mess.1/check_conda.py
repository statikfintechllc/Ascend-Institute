
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def check_conda():
    """Verifies if Conda is installed and accessible."""
        subprocess.run(["conda", "--version"], capture_output=True, text=True, check=True)
        print(" Conda is installed.")
    except FileNotFoundError:
        print(" Conda is not installed. Please install Conda before running this script.")

if __name__ == '__main__':
    check_conda()