import os
from datetime import datetime
from dotenv import load_dotenv

import smtplib
from email.mime.text import MIMEText

def save_to_file(token):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reset_url = f"http://127.0.0.1:5000/reset-password?token={token}"
    entry = f"[{timestamp}] token: {token}\n    link: {reset_url}\n"

    # cuvamo token u fajl pored ovog fajla
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stolen_tokens.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"[ATTACKER] Token saved to {path}")



def send_email(receiver_email, reset_link):

    sender_email = "tzoricic17223ri@raf.rs"

    load_dotenv()

    app_password = os.getenv("EMAIL_PASSWORD")

    

    subject = "Password Reset Request"

    body = f"""
            Hello,

            We received a request to reset your password.

            Click the link below:
            {reset_link}

            If this wasn't you, ignore this email.
            """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    print("[EMAIL] Connecting to SMTP server...")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("[EMAIL] Sent successfully to", receiver_email)