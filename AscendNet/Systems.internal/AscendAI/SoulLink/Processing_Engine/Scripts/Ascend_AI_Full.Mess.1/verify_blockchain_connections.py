
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def verify_blockchain_connections():
    """Ensures AI has direct access to all integrated blockchains."""
    for chain, connection in blockchains.items():
        if connection.is_connected():
            logging.info(f" Connected to {chain.upper()} Blockchain")
            logging.error(f" Connection Failed: {chain.upper()}")

if __name__ == '__main__':
    verify_blockchain_connections()