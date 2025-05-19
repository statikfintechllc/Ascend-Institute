from transformers import AutoModel
import torch
from backend.globals import CFG
from nlp_engine.tokenizer import tokenizer

MODEL = CFG["nlp"]["transformer_model"]
model = AutoModel.from_pretrained(MODEL)
model.eval()


def encode(text):
    tokens = tokenizer(
        text, return_tensors="pt", truncation=True, padding=True
    )
    with torch.no_grad():
        output = model(**tokens)
    return output.last_hidden_state.mean(dim=1).squeeze().numpy()
