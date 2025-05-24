# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.
# It must:
#   - Integrate seamlessly into the architecture defined in the full outline
#   - Operate autonomously and communicate cross-module via defined protocols
#   - Be production-grade, repair-capable, and state-of-the-art in logic
#   - Support learning, persistence, mutation, and traceability
#   - Not remove or weaken logic (stubs may be replaced, but never deleted)
#   - Leverage appropriate dependencies, imports, and interlinks to other systems
#   - Return enhanced — fully wired, no placeholders, no guesswork
# Objective:
#   Receive, reinforce, and return each script as a living part of the Gremlin:

# scraper/ask_monday_handler.py

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

# GremlinGPT v5 :: Module Integrity Directive

import os
import time
import pyautogui
import pyperclip
import pytesseract
import subprocess
import platform
from PIL import ImageGrab, Image
from datetime import datetime
from pathlib import Path

from backend.globals import logger
from memory.vector_store.embedder import embed_text, package_embedding, inject_watermark
from memory.log_history import log_event

WATERMARK = "source:GremlinGPT"
ORIGIN = "ask_monday_handler"

# Ensure platform-correct screenshot path (now using os.path.expanduser for flexibility)
SCREENSHOT_DIR = Path(os.path.expanduser("data/logs/screenshots"))
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_DIR = Path(os.path.expanduser("data/logs/chat_responses"))
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def launch_chatgpt():
    """Launch native ChatGPT client based on platform."""
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.Popen(["open", "-a", "ChatGPT"])
        elif system == "Linux":
            subprocess.Popen(["chatgpt"])
        elif system == "Windows":
            subprocess.Popen(["start", "", "ChatGPT"], shell=True)
        else:
            raise RuntimeError("Unsupported OS for launching ChatGPT.")
        time.sleep(5)
        pyautogui.click()
    except Exception as e:
        logger.error(f"[ASK] Failed to launch ChatGPT: {e}")


def paste_and_enter(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")


def scroll_and_capture():
    time.sleep(10)
    images = []
    for i in range(3):
        screenshot = ImageGrab.grab()
        path = (
            SCREENSHOT_DIR
            / f"monday_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
        )
        screenshot.save(path)
        images.append(path)
        pyautogui.scroll(-500)
        time.sleep(1.5)
    return images


def ocr_images(image_paths):
    blocks = []
    for p in image_paths:
        try:
            img = Image.open(p)
            text = pytesseract.image_to_string(img)
            blocks.append(text.strip())
        except Exception as e:
            logger.warning(f"[ASK] OCR failed for {p}: {e}")
            blocks.append("[OCR ERROR]")
    return "\n---\n".join(blocks)


def save_to_memory(prompt, response):
    timestamp = datetime.utcnow().isoformat()
    vector = embed_text(response)
    summary = f"ChatGPT external response to: {prompt[:100]}"
    package_embedding(
        text=summary,
        vector=vector,
        meta={
            "origin": ORIGIN,
            "timestamp": timestamp,
            "prompt": prompt,
            "response_len": len(response),
            "watermark": WATERMARK,
        },
    )
    inject_watermark(origin=ORIGIN)
    log_event("ask", "monday_query", {"prompt": prompt}, status="external")
    filename = (
        MEMORY_DIR / f"chat_response_{timestamp.replace(':', '').replace('-', '')}.md"
    )
    with open(filename, "w") as f:
        f.write(f"# Prompt:\n{prompt}\n\n# Response:\n{response}\n")
    logger.success(f"[ASK] ChatGPT result embedded and saved: {filename}")


def ask_monday(prompt):
    logger.info(f"[ASK] Asking ChatGPT: {prompt}")
    launch_chatgpt()
    paste_and_enter(prompt)
    images = scroll_and_capture()
    response = ocr_images(images)
    save_to_memory(prompt, response)
    return {"prompt": prompt, "response": response}


# FSM-compatible entry point
def handle(task):
    prompt = task.get("target") or task.get("text") or "What is your task?"
    return ask_monday(prompt)


# Standalone testing
if __name__ == "__main__":
    example = "Explain EMA crossover for penny stocks under 10 dollars."
    ask_monday(example)
