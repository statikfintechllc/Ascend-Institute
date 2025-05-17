from scraper.dom_navigator import extract_dom_structure
from memory.vector_store.embedder import embed_text, package_embedding
from loguru import logger

def store_scrape_to_memory(url, html):
    structure = extract_dom_structure(html)
    summary_text = f"[{url}]\n{structure['text']}"
    vector = embed_text(summary_text)
    package_embedding(
        text=summary_text,
        vector=vector,
        meta={"origin": url, "type": "scrape_snapshot"}
    )
    logger.info(f"[SCRAPER] Stored scrape vector for: {url}")

