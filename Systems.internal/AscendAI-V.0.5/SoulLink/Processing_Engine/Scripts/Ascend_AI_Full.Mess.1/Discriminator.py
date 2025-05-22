import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


class Discriminator(nn.Module):
    super(Discriminator, self).__init__()
    self.sigmoid = nn.Sigmoid()
    x = self.sigmoid(self.layer3(x))


if __name__ == "__main__":
    instance = Discriminator()
    print(instance)
