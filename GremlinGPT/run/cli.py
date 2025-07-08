#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Fair-Use License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

# utils/dash_cli.py

import readline
import sys
import os

# --- Set project root and sys.path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# --- Core Imports ---
import nltk
from utils.nltk_setup import setup_nltk_data  # ✅ PROPER FIX
from nlp_engine.parser import parse_nlp
from loguru import logger
from backend.api.chat_handler import chat

# --- Ensure NLTK Paths and Resources (centralized) ---
NLTK_DATA_DIR = setup_nltk_data()
if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.append(NLTK_DATA_DIR)

# --- Banner ---
BANNER = """
🌩️  GremlinGPT Terminal v1.0.3 [NLP-Only Mode]
Type your command. Type 'exit' to leave.
"""

# --- CLI Main ---
def main():
    print(BANNER)
    while True:
        try:
            user_input = input("👤 > ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("GremlinGPT going dark.")
                break

            logger.info(f"[CLI] Received input: {user_input}")
            result = parse_nlp(user_input)

            print("\n🧠 NLP Engine Output:")
            print(f"- Intent route: {result['route']}")
            print(f"- Tokens: {result['tokens'][:10]}...")
            print(f"- POS tags: {result['pos'][:5]}...")
            print(f"- Entities: {result['entities']}")
            print(f"- Financial terms: {result['financial_hits']}")
            print(f"- Code structures: {result['code_entities']}")

            response = chat(user_input)
            # Normalize response
            if isinstance(response, str):
                msg = response
            elif isinstance(response, dict):
                msg = response.get("response", next(iter(response.values()), ""))
            elif isinstance(response, tuple):
                val = response[0]
                if isinstance(val, dict):
                    msg = val.get("response", next(iter(val.values()), ""))
                else:
                    msg = str(val)
            else:
                msg = str(response)

            print("🤖 GremlinGPT:", msg)
            print("-" * 40)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Shutting down.")
            break
        except EOFError:
            print("\nEOF detected (Ctrl-D). Exiting CLI.")
            break
        except Exception as e:
            logger.exception(f"[CLI] Error during input handling: {e}")
            print(
                "An error occurred while handling your input. Please check the logs for details."
            )

if __name__ == "__main__":
    main()
