from flask import jsonify
from memory.vector_store.embedder import get_all_embeddings
from backend.globals import MEM


def graph():
    data = get_all_embeddings(limit=MEM["search"]["default_top_k"])
    return jsonify(data)
