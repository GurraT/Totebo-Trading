import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_stockinfo")
def get_stockinfo():
    stockinfo=list(mongo.db.tasks.find())
    return render_template("stockmarket.html",tasks=stockinfo)


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
        os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)