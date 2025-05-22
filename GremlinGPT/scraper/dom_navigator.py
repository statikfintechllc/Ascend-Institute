from bs4 import BeautifulSoup
from loguru import logger
from collections import Counter


def extract_dom_structure(html):
    """
    Extracts structured DOM metadata, links, semantic blocks, and top text from HTML.
    """
    """
    This enhances what goes into memory or NLP for semantic tagging.
    """
    soup = BeautifulSoup(html, "lxml")
    body = soup.body

    if not body:
        logger.warning("[DOM NAVIGATOR] No <body> tag found in HTML.")
        return {"links": [], "text": "", "tags": {}, "nodes": []}

    # Extract anchor links
    links = [a["href"] for a in soup.find_all("a", href=True)]

    # Node type frequency (for insight into page structure)
    tag_counts = Counter(tag.name for tag in soup.find_all())

    # Top-level semantic blocks (e.g., headers, articles, nav)
    semantic_tags = ["header", "nav", "main", "section", "article", "footer"]
    nodes = []

    for tag in semantic_tags:
        elems = soup.find_all(tag)
        for elem in elems:
            content = elem.get_text(strip=True)
            if len(content) > 20:  # Only meaningful content
                nodes.append(
                    {
                        "type": tag,
                        "text": content[:500],  # Truncate per node
                        "length": len(content),
                    }
                )

    # Full body text (limited for memory safety)
    full_text = soup.get_text(separator="\n", strip=True)

    result = {
        "links": links,
        "text": full_text[:2000],  # Limit body preview
        "tags": dict(tag_counts),
        "nodes": nodes,
    }

    logger.info(
        f"[DOM NAVIGATOR] Parsed HTML: {len(links)} links, "
        f"{len(nodes)} semantic nodes, {len(full_text)} chars of text."
    )

    return result


# CLI/Debug Usage
if __name__ == "__main__":
    with open("example_page.html", "r") as f:
        html = f.read()
    summary = extract_dom_structure(html)
    print(summary)
