import re
import nltk
from nltk.tokenize import word_tokenize
from backend.globals import logger

# Ensure tokenizer models are present
nltk.download("punkt", quiet=True)


def clean_text(text):
    """
    Normalize input by removing excess whitespace and illegal chars.
    """
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)  # Remove non-ASCII
    return text.strip()


def split_sentences(text):
    """
    Lightweight sentence segmentation for context-aware parsing.
    """
    return re.split(r"(?<=[.!?])\s+", text)


def tokenize(text):
    try:
        cleaned = clean_text(text)
        tokens = word_tokenize(cleaned)
        logger.debug(f"[TOKENIZER] Tokenized {len(tokens)} tokens.")
        return tokens
    except Exception as e:
        logger.error(f"[TOKENIZER] Failed to tokenize: {e}")
        return []
