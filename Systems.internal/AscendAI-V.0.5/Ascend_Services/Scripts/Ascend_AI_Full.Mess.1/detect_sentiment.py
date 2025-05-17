
import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import torch
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)


def detect_sentiment(text):
    """AI processes and detects sentiment in financial news."""
    tokenizer = transformers.AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = transformers.AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    sentiment_score = torch.softmax(outputs.logits, dim=1).detach().numpy()
    logging.info(f" AI Sentiment Analysis Score: {sentiment_score}")

if __name__ == '__main__':
    detect_sentiment()