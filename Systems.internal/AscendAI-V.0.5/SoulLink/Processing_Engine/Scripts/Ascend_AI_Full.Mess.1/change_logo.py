
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def change_logo(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if file_path:
            global LOGO_PATH
            LOGO_PATH = file_path
            log_event("info", f"User changed logo to {LOGO_PATH}")
    def save_name(self):
        global AI_NAME
        AI_NAME = self.name_entry.get()
        log_event("info", f"User changed AI name to {AI_NAME}")

if __name__ == '__main__':
    change_logo()