
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


class NASModel(nn.Module):
        super(NASModel, self).__init__()
        self.layer1 = nn.Linear(10, 50)
        self.layer2 = nn.Linear(50, 20)
        self.layer3 = nn.Linear(20, 1)
        self.activation = nn.ReLU()
        x = self.activation(self.layer1(x))
        x = self.activation(self.layer2(x))
        x = self.layer3(x)

if __name__ == '__main__':
    instance = NASModel()
    print(instance)