#!/bin/zsh

echo "[STOP] Terminating all GremlinGPT processes..."

pkill -f backend/server.py
pkill -f agent_core/fsm.py
pkill -f scraper/scraper_loop.py
pkill -f self_training/trainer.py

echo "[STOP] All subsystems stopped."

