import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
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
    stockinfo = list(mongo.db.stockinfo.find())
    return render_template("stockmarket.html", stockinfo=stockinfo)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if user already exists in DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("'{}' already exists in the system".format(
                            request.form.get("username")))
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "telephone": request.form.get("telephone"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        } 
        mongo.db.users.insert_one(register)

        # put the user into a session cokie
        session["user"] = request.form.get("username").lower()
        flash("Welcome {} your request have been received !".format(
                            request.form.get("username")))
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/omx")
def omx():
    return render_template("omx.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    #select session user's username from db
    username = mongo.db.users.find_one({"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)
    
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have been logout")
    session.pop("user")
    return redirect(url_for("login"))

@app.route("/toolbox")
def toolbox():
    return render_template("toolbox.html")


if __name__ == "__main__":
    app.run(
        os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)