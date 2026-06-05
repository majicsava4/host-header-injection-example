import os
from datetime import datetime


def save_to_file(token):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reset_url = f"http://127.0.0.1:5000/reset-password?token={token}"
    entry = f"[{timestamp}] token: {token}\n    link: {reset_url}\n"

    # cuvamo token u fajl pored ovog fajla
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stolen_tokens.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"[ATTACKER] Token saved to {path}")

def send_email():
    print("")