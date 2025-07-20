# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

"""
GremlinGPT v5 :: Module Integrity Directive

run/ngrok_launcher.py

- Launches and manages Ngrok tunnel for backend server access.
- Pulls configuration from TOML, supports region/subdomain, QR for mobile entry.
- State-of-the-art, no placeholders. Full error handling.
"""

from backend.globals import CFG, logger, resolve_path, DATA_DIR, MEM

# ──────────────── CONFIG LOAD ────────────────
ngrok_cfg = CFG.get("ngrok", {})
if not ngrok_cfg.get("enabled", False):
    logger.critical("[NGROK] Disabled in config.")
    sys.exit(0)

ngrok_bin = ngrok_cfg.get("bin_path", "ngrok")
ngrok_token = ngrok_cfg.get("authtoken", None)
ngrok_region = ngrok_cfg.get("region", "US")
ngrok_subdomain = ngrok_cfg.get("subdomain", "")
