# GremlinGPT - ngrok Integration Guide

This document explains how ngrok is integrated into the GremlinGPT system and how to use it to access your dashboard from anywhere, including mobile devices.

---

## What is ngrok?

`ngrok` is a secure tunnel service that exposes your local GremlinGPT dashboard (`localhost:5000`) to the public internet using HTTPS.

GremlinGPT uses **pyngrok** to launch and manage this tunnel natively.

---

## When Is ngrok Used?

- If `[ngrok.enabled]` is set to `true` in `config/config.toml`
- Automatically triggered by: `run/start_all.sh`
- Tunneling handled by: `run/ngrok_launcher.py`

---

## 1. Enable ngrok

### Set your token in:

# config/config.toml

[ngrok]
enabled = true
authtoken = "YOUR_AUTHTOKEN_HERE"
region = "us"
subdomain = ""  # Optional Pro feature

⸻

2. Start the System
```bash
cd GremlinGPT
bash run/start_all.sh
```
This:
	•	Launches the backend server
	•	Starts ngrok
	•	Displays the HTTPS link publicly
	•	Saves the live public URL to:
run/current_ngrok_url.txt

⸻

3. Access the Dashboard on Your Phone

A. Manual Option
	•	Wait for [*] NGROK Public URL: https://... to print
	•	Open the URL on your phone
	•	Install the PWA (Add to Home Screen)

⸻

4. Auto QR Code for Fast Phone Setup

When enabled, GremlinGPT will:
	•	Auto-generate a scannable QR code for the ngrok URL
	•	Saves it to:
run/ngrok_qr.png

You can then:
	•	Open run/ngrok_qr.png on your laptop
	•	Scan with your phone
	•	Instantly access the mobile dashboard

⸻

File Outputs
run/current_ngrok_url.txt
Stores the current live public dashboard URL

run/ngrok_qr.png:
Dynamic QR code for easy mobile access (optional)

⸻

Troubleshooting
No QR generated:
Check that qrcode is installed

No URL printed:
Check ngrok config is enabled and authtoken is valid

QR opens localhost:
You must use the ngrok HTTPS URL, not localhost

⸻

Summary

With ngrok + QR, you can securely expose GremlinGPT to your mobile device in seconds 
- no USB tethering,
- no ports,
- no static IPs.

Just boot and scan.
