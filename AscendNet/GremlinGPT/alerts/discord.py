# alerts/discord.py

import os
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(message: str) -> bool:
    """
    Sends a message to a Discord channel via webhook.
    Returns True if successful, False otherwise.
    """
    if not DISCORD_WEBHOOK_URL:
        print("[discord.py] No DISCORD_WEBHOOK_URL found in environment.")
        return False

    payload = {
        "content": f"**[GremlinGPT Alert]**\n{message}"
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            return True
        else:
            print(f"[discord.py] Failed to send alert: {response.status_code}")
            return False
    except Exception as e:
        print(f"[discord.py] Exception occurred: {e}")
        return False
