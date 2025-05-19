import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def update_emotion(n_clicks, user_input):
    if n_clicks:
        return ascend_dashboard.analyze_emotion(user_input)
    return "Waiting for input..."


if __name__ == "__main__":
    update_emotion()
