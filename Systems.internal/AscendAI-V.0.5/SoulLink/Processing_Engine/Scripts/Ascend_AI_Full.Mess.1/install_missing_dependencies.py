import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def install_missing_dependencies():
    """Automatically installs missing Python libraries before execution."""
    for lib in REQUIRED_LIBRARIES:
        try:
            __import__(lib)
        except ImportError:
            print(f" Missing {lib}. Installing now...")
            run_command(f"pip install {lib}")


if __name__ == "__main__":
    install_missing_dependencies()
