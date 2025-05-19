from transformers import AutoTokenizer
from backend.globals import CFG

MODEL = CFG["nlp"]["tokenizer_model"]
tokenizer = AutoTokenizer.from_pretrained(MODEL)


def tokenize(text):
    return tokenizer.tokenize(text)
