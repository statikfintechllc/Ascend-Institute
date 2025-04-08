
from twilio.rest import Client

TWILIO_SID = "PLACEHOLDER_TWILIO_SID"
TWILIO_AUTH_TOKEN = "PLACEHOLDER_TWILIO_AUTH"
TWILIO_PHONE_NUMBER = "+1234567890"
USER_PHONE_NUMBER = "+17854436288"

def send_sms_alert(message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=USER_PHONE_NUMBER
        )
        print(f"📲 SMS sent: {message.sid}")
    except Exception as e:
        print(f"❌ SMS send failed: {e}")
