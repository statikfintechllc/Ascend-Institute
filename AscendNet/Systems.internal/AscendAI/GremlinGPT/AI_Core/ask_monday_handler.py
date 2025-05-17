#!/usr/bin/env python3

import os
import time
import pyautogui
import pyperclip
import pytesseract
import subprocess
import platform
from PIL import ImageGrab
from datetime import datetime

# === DYNAMIC PATHS ===
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(ROOT_DIR, ".."))

TASK_FILE = os.path.join(BASE_DIR, "task_queue", "ask_monday.task")
LOG_FILE = os.path.join(BASE_DIR, "logs", "chat_log.txt")
MEMORY_DIR = os.path.join(BASE_DIR, "memory", "chat_responses")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "logs", "screenshots")

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# === UTILITY ===
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

# === TASK PARSER ===
def extract_task():
    if not os.path.exists(TASK_FILE):
        return None

    with open(TASK_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        return None

    current = lines[0].replace("ask_monday: ", "").strip()
    with open(TASK_FILE, "w") as f:
        f.writelines(lines[1:])  # remove first line

    return current

# === CHATGPT LAUNCH ===
def launch_chatgpt():
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", "ChatGPT"])
        elif system == "Linux":
            subprocess.Popen(["chatgpt"])  # Customize if needed
        elif system == "Windows":
            subprocess.Popen(["start", "", "ChatGPT"], shell=True)
        else:
            raise Exception("Unsupported OS for ChatGPT launch.")
        time.sleep(5)
        pyautogui.click()  # Focus window
        time.sleep(1)
    except Exception as e:
        log(f"[ERROR] Failed to launch ChatGPT app: {e}")

# === INTERACTION ===
def paste_and_enter(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")

def scroll_and_capture():
    time.sleep(10)
    screenshots = []

    for i in range(3):
        img = ImageGrab.grab(bbox=None)  # full screen
        path = os.path.join(SCREENSHOT_DIR, f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png")
        img.save(path)
        screenshots.append(path)
        pyautogui.scroll(-500)
        time.sleep(2)

    return screenshots

def ocr_images(paths):
    text_blocks = []
    for p in paths:
        try:
            img = ImageGrab.open(p)
            text = pytesseract.image_to_string(img)
            text_blocks.append(text.strip())
        except Exception as e:
            text_blocks.append("[OCR ERROR]")
    return "\n---\n".join(text_blocks)

# === FINAL STORAGE ===
def save_response(original, result):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = os.path.join(MEMORY_DIR, f"chat_response_{timestamp}.md")
    with open(fname, "w") as f:
        f.write(f"# Prompt:\n{original}\n\n# Response:\n{result}\n")
    log(f"Saved ChatGPT response to {fname}")

# === MAIN ===
def main():
    query = extract_task()
    if not query:
        log("No 'ask_monday' tasks found.")
        return

    log(f"Asking Monday: {query}")
    launch_chatgpt()
    paste_and_enter(query)
    images = scroll_and_capture()
    response = ocr_images(images)
    save_response(query, response)

if __name__ == "__main__":
    main()