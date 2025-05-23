#!/usr/bin/env python3

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

# run/ngrok_launcher.py

from pyngrok import ngrok
import toml
import qrcode

# Load config
config = toml.load("config/config.toml")

if not config.get("ngrok", {}).get("enabled", False):
    print("[NGROK] Disabled in config.")
    exit(0)

auth = config["ngrok"].get("authtoken")
region = config["ngrok"].get("region", "us")
subdomain = config["ngrok"].get("subdomain")

if auth:
    ngrok.set_auth_token(auth)

public_url = ngrok.connect(5000, region=region, subdomain=subdomain)
print(f"[NGROK] Public URL: {public_url}")

# Generate QR code for mobile access
img = qrcode.make(str(public_url))
img.save("run/ngrok_qr.png")
print("[NGROK] QR code saved to run/ngrok_qr.png")
