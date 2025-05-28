<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE.md">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE.md">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

# GremlinGPT v1.0.2 – ngrok Integration Guide

This document explains how `ngrok` is integrated into the GremlinGPT system and how to use it to access your dashboard securely from anywhere — including mobile devices.

---

## What is ngrok?

[`ngrok`](https://ngrok.com) is a secure tunneling service that exposes your **local GremlinGPT dashboard (`localhost:5000`)** to the public internet via HTTPS.

GremlinGPT uses **`pyngrok`** to launch and manage this tunnel automatically.

---

## When Is ngrok Used?

- When `[ngrok.enabled] = true` in `config/config.toml`
- Automatically triggered by `run/start_all.sh`
- Handled by the script: `run/ngrok_launcher.py`

---

1. Enable ngrok

### Edit your token config in:

#### `config/config.toml`
```toml
[ngrok]
enabled = true
authtoken = "YOUR_AUTHTOKEN_HERE"
region = "us"
subdomain = ""  # Optional — requires ngrok Pro
```

⸻

2. Start the System
```bash
cd GremlinGPT
bash run/start_all.sh
```

### This will:
	•	Launch the backend server
	•	Start ngrok tunnel
	•	Print the live HTTPS URL
	•	Save that URL to:
	•	run/current_ngrok_url.txt

⸻

3.a. Access the Dashboard on Your Phone(Manual)

	•	Watch for console output like:

[*] NGROK Public URL: https://example.ngrok.io

	•	Open the link on your phone
	•	Tap “Add to Home Screen” to install the PWA

⸻

3.b. Auto QR Code for Mobile Setup(Autonatic)

When enabled, GremlinGPT will:
	•	Auto-generate a scannable QR code
	•	Save it as:
	•	run/ngrok_qr.png

### Use it by:
	•	Opening run/ngrok_qr.png on your laptop
	•	Scanning it with your phone
	•	Instantly accessing the mobile dashboard

⸻

## Output Files

File
Purpose
run/current_ngrok_url.txt
Live ngrok HTTPS link (public endpoint)
run/ngrok_qr.png
QR code for mobile connection

⸻

## Troubleshooting

Issue
Fix
QR not generated
Make sure qrcode Python package is installed
No URL printed
Check if ngrok is enabled and authtoken is valid
QR opens localhost
Use only the ngrok public HTTPS URL, not localhost
ngrok fails to connect
Ensure internet access and proper region in config


⸻

## Summary

### With ngrok + QR, you can expose your GremlinGPT system securely to any device:
	•	No ports
	•	No IP configuration
	•	No tethering required

## Just boot and scan.

