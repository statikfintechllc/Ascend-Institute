import requests
from bs4 import BeautifulSoup
import trafilatura
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor
from core.model_interface import ask_model

HEADERS = {
    "User-Agent": "Mozilla/5.0 (GremlinGPT Scraper 1.0)"
}

def fetch_raw_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return response.text
    except Exception as e:
        return f"[Error fetching raw HTML from {url}]: {str(e)}"

def parse_with_bs4(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def parse_with_trafilatura(html):
    return trafilatura.extract(html)

def parse_with_newspaper(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"[Newspaper3k failed]: {str(e)}"

def summarize(text, max_chars=4000):
    trimmed = text[:max_chars]
    prompt = f"Summarize the following content for a general user:\n\n{trimmed}"
    return ask_model(prompt)

def scrape_and_summarize_single(url):
    html = fetch_raw_html(url)
    if not html:
        return f"[Empty HTML for {url}]"

    content = (
        parse_with_trafilatura(html) or
        parse_with_newspaper(url) or
        parse_with_bs4(html)
    )

    if not content or len(content.strip()) < 100:
        return f"[Failed to extract usable content from {url}]"

    summary = summarize(content)
    return f"[SUMMARY from {url}]\n{summary}\n"

def scrape_multiple(urls, parallel_limit=4):
    with ThreadPoolExecutor(max_workers=parallel_limit) as executor:
        results = list(executor.map(scrape_and_summarize_single, urls))
    return "\n\n".join(results)

# Entrypoint for GremlinGPT's toolset
def scrape_web(input_data):
    """Input can be a single URL or a list of URLs."""
    if isinstance(input_data, str):
        input_data = [input_data]
    return scrape_multiple(input_data)
