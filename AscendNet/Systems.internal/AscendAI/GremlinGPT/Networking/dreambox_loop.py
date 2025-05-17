# runtime/dreambox_loop.py

import threading
import time
import logging
from tools.robinhood_trade import analyze_market
from tools.scrape_web import scrape_web
from memory.sqlite_memory import log_memory
from core.model_interface import ask_model
from tools.self_edit import self_edit

dreambox_running = False

def dreambox_loop():
    global dreambox_running
    logging.info("[Dreambox] Background loop started.")
    while dreambox_running:
        try:
            # Simulate market reasoning
            action = analyze_market("BTC")
            log_memory("Dreambox: Simulated Market", f"Signal: {action}", tag="dreambox")

            # Scrape some crypto headlines
            headlines = scrape_web(["https://www.coindesk.com", "https://cointelegraph.com"])
            for h in headlines:
                summary = h.get("summary", "")
                log_memory("Dreambox: Web Summary", summary[:300], tag="dreambox")

            # Reflective improvement
            prompt = (
                "Based on recent summaries and trade logs, suggest one improvement "
                "to the tool logic in the system. Include which file to edit and what to change."
            )
            reflection = ask_model(prompt)

            # Try self-edit if structure matches
            if "file:" in reflection and "instruction:" in reflection:
                parts = reflection.split("instruction:")
                file_line = parts[0].split("file:")[-1].strip()
                instruction = parts[1].strip()
                result = self_edit({"file_path": file_line, "instruction": instruction})
                log_memory("Dreambox: Self-Edit Attempt", result, tag="dreambox")

        except Exception as e:
            logging.warning(f"[Dreambox] Loop error: {e}")

        time.sleep(600)  # Run every 10 min

def start_dreambox():
    global dreambox_running
    if not dreambox_running:
        dreambox_running = True
        thread = threading.Thread(target=dreambox_loop, daemon=True)
        thread.start()
        return "[Dreambox] Loop activated."
    return "[Dreambox] Already running."

def stop_dreambox():
    global dreambox_running
    dreambox_running = False
    return "[Dreambox] Loop deactivated."
