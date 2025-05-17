from memory.vector_store.embedder import embed_text, package_embedding
import json
from loguru import logger

def inject_feedback(filepath="data/nlp_training_sets/mutated_dataset.json"):
    with open(filepath, "r") as f:
        data = json.load(f)

    for item in data:
        vector = embed_text(item["mutation"])
        package_embedding(
            text=item["mutation"],
            vector=vector,
            meta={"source": "self_training", "type": "mutation"}
        )
        logger.info(f"[FEEDBACK] Embedded mutation: {item['mutation']}")

