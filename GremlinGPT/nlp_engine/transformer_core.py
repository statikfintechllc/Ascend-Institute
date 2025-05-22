from transformers import AutoModel, AutoTokenizer
import torch
from backend.globals import CFG, logger

# Load model and tokenizer from config
MODEL_NAME = CFG["nlp"].get("transformer_model", "bert-base-uncased")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    logger.success(f"[TRANSFORMER] Loaded model: {MODEL_NAME}")
except Exception as e:
    logger.error(f"[TRANSFORMER] Failed to load model '{MODEL_NAME}': {e}")
    tokenizer = None
    model = None


def encode_text(text):
    """
    Encodes text into a semantic vector using the transformer model.
    Returns a numpy array representation.
    """


if not tokenizer or not model:
    logger.warning("[TRANSFORMER] No model loaded. Returning zeros.")
    return torch.zeros(768).numpy()

try:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    vector = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return vector
except Exception as e:
    logger.error(f"[TRANSFORMER] Encoding failed: {e}")
    return torch.zeros(768).numpy()
