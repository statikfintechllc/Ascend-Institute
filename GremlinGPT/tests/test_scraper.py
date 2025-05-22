import asyncio
from scraper.playwright_handler import get_dom_html
from scraper.dom_navigator import extract_dom_structure
from scraper.page_simulator import store_scrape_to_memory

TEST_URL = "https://example.com"


def test_scraper_pipeline():
    html = asyncio.run(get_dom_html(TEST_URL))
    assert "<html" in html.lower()

    parsed = extract_dom_structure(html)
    assert "text" in parsed and len(parsed["text"]) > 0

    store_scrape_to_memory(TEST_URL, html)
