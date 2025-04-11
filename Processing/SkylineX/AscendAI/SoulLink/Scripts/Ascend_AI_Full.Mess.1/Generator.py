
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


class Generator(nn.Module):
        super(Generator, self).__init__()
        self.layer3 = nn.Linear(20, 10)

if __name__ == '__main__':
    instance = Generator()
    print(instance)