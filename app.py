from flask import Flask, request, session, redirect, render_template_string
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from modules import send_email


app = Flask(__name__)

app.secret_key = "moj secret key"

# baza
users = {"victim@gmail.com": {"password": generate_password_hash("victim123")}}

reset_tokens = {}

LOGIN_HTML = """
<h2>Login</h2>

<form method = "POST">
    <input name = "email" placeholder = "email" required><br></br>
    <input name = "password" type = "password" placeholder = "password" required><br></br>
    <button type = "submit">Login</button>
</form>

<p><a href = "/forgot-password">Forgot password</a></p>

{% if error %}
    <p style = "color:red">{{error}}</p>
{% endif %}


"""


HOME_HTML = """

<h2> Welcome </h2>
<p>You are logged in as: {{email}} </p>
<a href = "/logout">Logout</a>

"""


FORGOT_HTML = """
<h2>Reset password</h2>

<form method = "POST">
    <input name = "email"  placeholder = "petarpetrovic@gmail.com" required><br></br>
    <button type = "submit"> Send reset link</button>
</form>

{% if reset_link %}
<hr>
<h3>Simulated email:</h3>
<p> {{reset_link}}</p>
<a href = "{{reset_link}}"> Open reset link</a>
{% endif %}


"""


RESET_HTML = """


<h2>Reset Password</h2>

<form method="POST">
    <input name="password" type="password" placeholder="new password" required><br><br>
    <button type="submit">Reset password</button>
</form>



"""



#home
@app.route("/")
def index():

        if "user" in session:
                return render_template_string(
                        HOME_HTML,
                        email=session["user"]
                )
        

        return redirect("/login")


#login

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    # klik na login
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if email in users:
            if check_password_hash(users[email]["password"], password):
                session["user"] = email
                return redirect("/")

        error = "No such username and password combo in database"

    return render_template_string(LOGIN_HTML, error=error)


#logout
@app.route("/logout")
def logout():
     
     session.clear()

     return redirect("/login")



#forgot password
@app.route("/forgot-password", methods = ["GET", "POST"])
def forgot_password():
     
     reset_link = None

     if request.method == "POST":
          
          email = request.form["email"]

          if email in users:
               
               token = secrets.token_urlsafe(16)

               reset_tokens[token] = email

               #RANJIVOST
               host = request.headers.get("Host")
               #formiramo reset link, problem sto verujemo korisniku za host
               reset_link = (
                    f"http://{host}/reset-password?token={token}"
               )
               print(f"Generated link: {reset_link}")
               send_email()

     return render_template_string(
          FORGOT_HTML,
          reset_link=reset_link
     )


#reset pass
@app.route("/reset-password", methods = ["GET", "POST"])
def reset_password():
     #uzimamo token iz url-a
     token = request.args.get("token")

     if token not in reset_tokens:
          
          return "<h2>Invalid token</h2>", 400
     email = reset_tokens[token]

     #ako salje novi password
     if request.method == "POST":
          
          new_password = request.form["password"]

          users[email]["password"] = (generate_password_hash(new_password))

          #token iskoriscen
          del reset_tokens[token]

          print("password changed")

          return """<h2>Password changed successfully</h2>
                    <a href="/login">Go to login</a>
          """
     return render_template_string(RESET_HTML)


#pokretanje servera
if __name__ == "__main__":
     app.run(
          host = "127.0.0.1",
          port = 5000,
          debug = True
     )




