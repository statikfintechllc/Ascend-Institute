from bs4 import BeautifulSoup

def extract_dom_structure(html):
    soup = BeautifulSoup(html, "lxml")
    body = soup.body
    links = [a['href'] for a in soup.find_all("a", href=True)]
    text = soup.get_text(separator="\n")
    return {"links": links, "text": text[:2000]}  # Limit for safety

