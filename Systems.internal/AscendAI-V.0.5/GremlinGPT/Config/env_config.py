# config/env_config.py

from dotenv import load_dotenv
import os

# Load .env file from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Git Key
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

# Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Discord Settings
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Trading Credentials (if ever used)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# OpenAI (if used)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Custom model directory
MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral-7b-instruct.gguf")
