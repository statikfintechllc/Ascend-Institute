import os
import logging
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

USE_OLLAMA = False  # Set to True to use Ollama instead of llama.cpp

if not USE_OLLAMA:
    from llama_cpp import Llama

try:
    model_path = ROOT_DIR / "models" / "mistral-7b-instruct.gguf"
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")

    llm = Llama(
        model_path=str(model_path),
        n_ctx=4096,
        n_gpu_layers=33,
        verbose=False
    )
    logging.info(f"[Model Interface] Loaded model at: {model_path}")

except Exception as e:
    logging.error(f"[Model Interface] Failed to load model: {e}")
    llm = None  # Optional: prevent everything from dying
else:
    import requests

    def ollama_query(prompt):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]

def ask_model(prompt: str, max_tokens=512) -> str:
    """Queries the local model and returns the response."""
    print(f"[MODEL INPUT]\n{prompt}\n")

    if USE_OLLAMA:
        return ollama_query(prompt)

    output = llm(
        f"[INST] {prompt} [/INST]",
        max_tokens=max_tokens,
        temperature=0.7,
        top_p=0.95,
    )
    return output["choices"][0]["text"].strip()
