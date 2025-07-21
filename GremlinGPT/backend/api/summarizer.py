# backend/api/summarizer.py
# Refactored to use centralized imports from backend.globals

from backend.globals import logger

def summarize_text(text):
    """Stub summarizer: returns the first 128 characters with ellipsis if too long."""
    if not isinstance(text, str):
        logger.warning("summarize_text received non-string input")
        return ""
    logger.debug(f"Summarizing text of length {len(text)}")
    return text[:128] + ("..." if len(text) > 128 else "")
