import os
from flask import (Flask,render_template)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("base.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/omx")
def omx():
    return render_template("omx.html")


@app.route("/stockmarket")
def stockmarket():
    return render_template("stockmarket.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/toolbox")
def toolbox():
    return render_template("toolbox.html")


if __name__=="__main__":
    app.run(
        os.environ.get("IP","0.0.0.0"),
        port=int(os.environ.get("PORT","5000")),
        debug=True)