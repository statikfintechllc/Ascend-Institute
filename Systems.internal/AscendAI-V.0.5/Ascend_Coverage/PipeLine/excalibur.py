import httpx
import random
import time
import sqlite3
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# === CONFIGURATION ===
TARGET_URL = "https://example.com/api/data"  # Replace with your scraped endpoint
HEADERS = {
    "User-Agent": UserAgent().random,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}
PROXIES = [
    "http://proxy1:port",
    "http://proxy2:port",
    # Use a rotating pool if you can afford it. Tor can be used if you're broke.
]

# === DATABASE SETUP ===
conn = sqlite3.connect("local_data.db")
cursor = conn.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS market_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    payload TEXT
)
"""
)
conn.commit()

# === HUMAN-LIKE DELAY ===
def human_delay(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))


# === STEALTH REQUEST FUNCTION ===
def stealth_request(url, headers, proxies=None):
    session = httpx.Client(http2=True, timeout=10.0, follow_redirects=True)

    if proxies:
        session.proxies = {
            "http://": random.choice(proxies),
            "https://": random.choice(proxies),
        }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except httpx.RequestError as e:
        print(f"Request failed: {e}")
        return None


# === PARSE + STORE ===
def save_payload(payload: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO market_data (timestamp, payload) VALUES (?, ?)",
        (timestamp, payload),
    )
    conn.commit()


# === MAIN LOOP ===
def run_scraper():
    while True:
        human_delay()
        headers = HEADERS.copy()
        headers["User-Agent"] = UserAgent().random  # Rotate every time

        raw_response = stealth_request(TARGET_URL, headers, PROXIES)
        if raw_response:
            # Optional parsing logic
            try:
                soup = BeautifulSoup(raw_response, "html.parser")
                cleaned_data = soup.get_text()[:500]  # Sample data
                print("Data:", cleaned_data)
                save_payload(raw_response)
            except Exception as e:
                print("Parsing failed:", e)

        # Random idle cycle
        human_delay(10, 30)


if __name__ == "__main__":
    run_scraper()
