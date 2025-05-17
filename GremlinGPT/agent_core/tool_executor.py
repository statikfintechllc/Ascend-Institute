from scraper.scraper_loop import get_dom_html
from nlp_engine.transformer_core import encode
from memory.vector_store.embedder import package_embedding
from trading_core.signal_generator import generate_signals
from self_training.feedback_loop import inject_feedback
import asyncio

def execute_tool(task):
    if task["type"] == "scrape":
        dom = asyncio.run(get_dom_html(task["target"]))
        return {"scraped": dom[:100]}

    elif task["type"] == "signal_scan":
        return generate_signals()

    elif task["type"] == "nlp":
        vector = encode(task["target"])
        return vector.tolist()

    elif task["type"] == "self_train":
        inject_feedback()
        return {"trained": True}

    else:
        raise ValueError("Unknown task type")

