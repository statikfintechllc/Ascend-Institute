
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def step(self, action):
        reward = np.random.randn()
        return self.state, reward, False, {}
    def reset(self):
        return self.state

if __name__ == '__main__':
    step()