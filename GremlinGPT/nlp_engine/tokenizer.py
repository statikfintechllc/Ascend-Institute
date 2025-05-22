import re
from transformers import AutoTokenizer
from backend.globals import CFG, logger
import nltk

# Fallback for tokenizer if HuggingFace load fails
nltk.download("punkt", quiet=True)

# Configurable tokenizer
MODEL = CFG["nlp"].get("tokenizer_model", "bert-base-uncased")
text = re.sub(r"\s+", " ", text)
text = re.sub(r"[^\x00-\x7F]+", "", text)
text = clean_text(text)

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    logger.success(f"[TOKENIZER] Loaded: {MODEL}")
except Exception as e:
    logger.warning(f"[TOKENIZER] Failed to load {MODEL}. Falling back to nltk: {e}")
    tokenizer = None


def clean_text(text):
    """
    Clean and normalize text input before tokenization.
    """
    return text.strip()


def tokenize(text):
    if tokenizer:
        tokens = tokenizer.tokenize(text)
    else:
        from nltk.tokenize import word_tokenize

        tokens = word_tokenize(text)

    logger.debug(f"[TOKENIZER] Token count: {len(tokens)}")
    return tokens
