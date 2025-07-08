#!/usr/bin/env python3
"""
GremlinGPT v1.0.3 :: run/chat_cli.py
Live CLI chat session for GremlinGPT using ChatSession.
"""
import sys
from nlp_engine.chat_session import ChatSession

def main():
    print("\nGremlinGPT CLI Chat (type 'exit' to quit)\n")
    session = ChatSession(user_id="cli_user")
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit"): break
            result = session.process_input(user_input)
            print(f"Gremlin: {result['response']}")
            if result.get("explanation"):
                print(f"[Reasoning] {result['explanation']}")
        except (KeyboardInterrupt, EOFError):
            print("\n[Session ended]")
            break
        except Exception as e:
            print(f"[Error] {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
