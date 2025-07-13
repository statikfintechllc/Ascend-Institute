# backend/api/summarizer.py  # type: ignore

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.logging_config import setup_module_logger

logger = setup_module_logger('backend', 'summarizer')

def summarize_text(text):
    """Stub summarizer: returns the first 128 characters with ellipsis if too long."""
    if not isinstance(text, str):
        logger.warning("summarize_text received non-string input")
        return ""
    logger.debug(f"Summarizing text of length {len(text)}")
    return text[:128] + ("..." if len(text) > 128 else "")
