#!/usr/bin/env python3

# CLI entrypoint to talk to the GremlinGPT NLP engine
import readline
import sys
import os
from nlp_engine.parser import parse_nlp
from loguru import logger

# Fix sys.path for local imports
sys.path.append("/path/to/AscendAI/GremlinGPT")

from backend.chat_handler import chat

BANNER = """
🌩️  GremlinGPT Terminal v1.0.3 [NLP-Only Mode]
Type your command. Type 'exit' to leave.
"""

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
            print(f"- Tokens: {result['tokens']}")
            print(f"- POS tags: {result['pos'][:5]}...")  # show sample
            print(f"- Entities: {result['entities']}")
            print(f"- Financial terms: {result['financial_hits']}")
            print(f"- Code structures: {result['code_entities']}")

            # Call GremlinGPT's chat handler
            response = chat(user_input)
            print("🤖 GremlinGPT:", response.get("message", "[No response]"))

            print("-" * 40)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected. Shutting down.")
            break
        except Exception as e:
            logger.error(f"[CLI] Error during input handling: {e}")

if __name__ == "__main__":
    main()
