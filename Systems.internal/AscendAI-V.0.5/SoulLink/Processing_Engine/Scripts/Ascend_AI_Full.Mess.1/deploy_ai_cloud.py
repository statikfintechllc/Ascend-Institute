import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def deploy_ai_cloud():
    """Deploy AI cloud infrastructure to detected idle computing devices."""
    for node in AI_CLOUD_NODES:
        os.system(f"scp -r Ascend_AI_Core root@{node}:/etc/Ascend/")
        os.system(f"ssh root@{node} 'nohup python3 /etc/Ascend/Ascend_AI_Core.py &'")
        print(f" AI Cloud Deployed to {node}.")
        print(f" Failed to Deploy AI Cloud to {node}: {str(e)}")


if __name__ == "__main__":
    deploy_ai_cloud()
