# !/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import json
from pathlib import Path
from backend.globals import CFG, logger
from datetime import datetime

STATE_FILE = Path(CFG["paths"].get("checkpoints_dir", "run/checkpoints/")) / "state_snapshot.json"
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                state = json.load(f)
                logger.debug(f"[STATE] Loaded state snapshot with keys: {list(state.keys())}")
                return state
        except Exception as e:
            logger.error(f"[STATE] Failed to load snapshot: {e}")
    return {}


def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        logger.info(f"[STATE] Snapshot saved @ {datetime.utcnow().isoformat()}")
    except Exception as e:
        logger.error(f"[STATE] Failed to save snapshot: {e}")
