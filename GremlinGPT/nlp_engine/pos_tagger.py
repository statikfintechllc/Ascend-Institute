import nltk
from nltk import pos_tag, word_tokenize
from datetime import datetime
from loguru import logger

from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark

nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)

WATERMARK = "source:GremlinGPT"
ORIGIN = "pos_tagger"


def get_pos_tags(text):
    try:
        tokens = word_tokenize(text)
        tags = pos_tag(tokens)

        # Create compact summary
        summary = f"POS tagging: {len(tokens)} tokens | Example: {tags[:3]}"
        vector = embed_text(summary)

        package_embedding(
            text=summary,
            vector=vector,
            meta={
                "origin": ORIGIN,
                "timestamp": datetime.utcnow().isoformat(),
                "token_count": len(tokens),
                "watermark": WATERMARK,
            },
        )
        inject_watermark(origin=ORIGIN)

        return tags

    except Exception as e:
        logger.error(f"[POS_TAGGER] Failed to tag input: {e}")
        return []
