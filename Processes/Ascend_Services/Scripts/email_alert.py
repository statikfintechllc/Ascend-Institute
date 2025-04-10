# email_alert.py
import smtplib
from email.mime.text import MIMEText

def send_email_alert(smtp_server, port, sender_email, password, receiver_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
