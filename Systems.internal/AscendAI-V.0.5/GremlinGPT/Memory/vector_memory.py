import os
import sys
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
MEMORY_PATH = ROOT_DIR / "memory" / "vector_store"
os.makedirs(MEMORY_PATH, exist_ok=True)

VECTOR_INDEX_FILE = MEMORY_PATH / "index.faiss"
TEXT_STORE_FILE = MEMORY_PATH / "texts.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight and fast
dimension = 384  # Output dimension for this model
index = faiss.IndexFlatL2(dimension)

# Load existing memory if it exists
if VECTOR_INDEX_FILE.exists() and TEXT_STORE_FILE.exists():
    print("[VectorMemory] Loading memory...")
    with open(TEXT_STORE_FILE, "rb") as f:
        stored_texts = pickle.load(f)
    faiss.read_index(str(VECTOR_INDEX_FILE))
else:
    stored_texts = []


def store_context(text: str):
    """Embed and store text in vector DB."""
    global stored_texts, index
    embedding = model.encode([text])
    index.add(embedding)
    stored_texts.append(text)

    with open(TEXT_STORE_FILE, "wb") as f:
        pickle.dump(stored_texts, f)
    faiss.write_index(index, str(VECTOR_INDEX_FILE))


def recall_context(query: str, k: int = 3):
    """Return top-k similar text snippets from memory."""
    if not stored_texts:
        return ""

    query_vec = model.encode([query])
    D, I = index.search(query_vec, k)
    results = [stored_texts[i] for i in I[0] if i < len(stored_texts)]
    return "\n---\n".join(results)
