# sms_alert.py
from twilio.rest import Client

def send_sms_alert(account_sid, auth_token, from_number, to_number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )
    return message.sid
