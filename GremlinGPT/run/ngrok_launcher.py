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
