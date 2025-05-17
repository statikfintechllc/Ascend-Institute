import requests
import json
from core.model_interface import ask_model

HEADERS = {
    "User-Agent": "GremlinGPT-Agent/1.0"
}

def query_api(input_data):
    """
    Expects either:
    - A string URL (e.g., 'https://api.coindesk.com/v1/bpi/currentprice.json')
    - A dictionary with optional method, headers, and body
    """

    if isinstance(input_data, str):
        url = input_data
        method = "GET"
        headers = HEADERS
        payload = None
    elif isinstance(input_data, dict):
        url = input_data.get("url")
        method = input_data.get("method", "GET").upper()
        headers = input_data.get("headers", HEADERS)
        payload = input_data.get("body", None)
    else:
        return "[query_api] Invalid input format."

    try:
        response = requests.request(method, url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        pretty = json.dumps(data, indent=2)

        # Try to summarize if it's too big
        if len(pretty) > 4000:
            summary = ask_model(f"Summarize this API response:\n{pretty[:4000]}")
            return f"[API Response Summary]\n{summary}"
        else:
            return f"[API Response]\n{pretty}"

    except Exception as e:
        return f"[query_api Error] {str(e)}"
