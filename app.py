import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
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


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    stockinfo = list(mongo.db.stockinfo.find({"$text": {"$search": query}}))
    return render_template("stockmarket.html", stockinfo=stockinfo)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if user already exists in DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            flash(
                "'{}' already exists in the system".format(request.form.get("username"))
            )
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "telephone": request.form.get("telephone"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)

        # put the user into a session cokie
        session["user"] = request.form.get("username").lower()
        flash(
            "Welcome {} your request have been received !".format(
                request.form.get("username")
            )
        )
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}
        )

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # select session user's username from db
    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    email = mongo.db.users.find_one({"username": session["user"]})["email"]
    phone = mongo.db.users.find_one({"username": session["user"]})["telephone"]

    if session["user"]:
        return render_template(
            "profile.html", username=username, email=email, phone=phone
        )

    return redirect(url_for("login"))


@app.route("/preference", methods=["GET", "POST"])
def preference():
    if request.method == "POST":
        # insert user preferences in to category collection in db
        RSI = "on" if request.form.get("RSI") else "off"
        MACD = "on" if request.form.get("MACD") else "off"
        Trend = "on" if request.form.get("Trend") else "off"
        EMA = "on" if request.form.get("EMA") else "off"
        Bollinger = "on" if request.form.get("Bollinger") else "off"
        SMA = "on" if request.form.get("SMA") else "off"
        info_phone = "on" if request.form.get("info_phone") else "off"
        info_mail = "on" if request.form.get("info_mail") else "off"
        preference = {
            "name": request.form.get("name"),
            "Email": request.form.get("Email"),
            "phone": request.form.get("phone"),
            "RSI": RSI,
            "MACD": MACD,
            "Trend": Trend,
            "EMA": EMA,
            "Bollinger": Bollinger,
            "SMA": SMA,
            "info_phone": info_phone,
            "info_mail": info_mail,
        }
        mongo.db.categories.insert_one(preference)
        session["name"] = request.form.get("name")
        return redirect(url_for("toolbox", username=session["user"],name=session["name"] ))

    return render_template("profile.html", username=username)

@app.route("/add_info", methods=["GET", "POST"])
def add_stock():
    if request.method == "POST":
        # insert info to stockinfo collection in db
        info = {
            "Company_name": request.form.get("company_name"),
            "Company_abbr": request.form.get("company_abbr"),
            "Date": request.form.get("date"),
            "Vol": request.form.get("volume"),
            "Opening_price": request.form.get("price_open"),
            "Closing_price": request.form.get("price_close"),
            "Daily_High": request.form.get("price_high"),
            "Daily_Low": request.form.get("price_low"),
        }
        mongo.db.stockinfo.insert_one(info)
        flash("Information added!")
        return redirect(url_for("get_stockinfo"))

    return render_template("add_stock.html")


@app.route("/edit_stock/<stockid>", methods=["GET", "POST"])
def edit_stock(stockid):
    if request.method == "POST":
        # insert info to stockinfo collection in db
        info = {
            "Company_name": request.form.get("company_name"),
            "Company_abbr": request.form.get("company_abbr"),
            "Date": request.form.get("date"),
            "Vol": request.form.get("volume"),
            "Opening_price": request.form.get("price_open"),
            "Closing_price": request.form.get("price_close"),
            "Daily_High": request.form.get("price_high"),
            "Daily_Low": request.form.get("price_low"),
        }
        mongo.db.stockinfo.update({"_id": ObjectId(stockid)}, info)
        flash("Information updated!")
        return redirect(url_for("get_stockinfo"))

    stockid = mongo.db.stockinfo.find_one({"_id": ObjectId(stockid)})
    return render_template("edit_stock.html", stockid=stockid)


@app.route("/delete_stock/<stockid>", methods=["GET", "POST"])
def delete_stock(stockid):
    # delete info from stockinfo collection in db
    mongo.db.stockinfo.remove({"_id": ObjectId(stockid)})
    flash("Information removed!")
    return redirect(url_for("get_stockinfo"))


@app.route("/logout")
# logout and remove session cookies
def logout():
    flash("You have been logout")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/toolbox/<username>", methods=["GET", "POST"])
def toolbox(username):
    username = mongo.db.users.find_one({"username": session["user"]})["username"]
    name = mongo.db.categories.find({"name": session["name"]})
    stockinfo = list(mongo.db.stockinfo.find())
    
    if session["name"]:
        return render_template("toolbox.html", name=name, stockinfo=stockinfo)

    return render_template("profile.html")

@app.route("/edit_preferences/<id>", methods=["GET", "POST"])
def edit_preferences(id):
    id = mongo.db.categories.find({"_id": ObjectId(id)})
    if request.method == "POST":
        # update user preferences in to category collection in db
        RSI = "on" if request.form.get("RSI") else "off"
        MACD = "on" if request.form.get("MACD") else "off"
        Trend = "on" if request.form.get("Trend") else "off"
        EMA = "on" if request.form.get("EMA") else "off"
        Bollinger = "on" if request.form.get("Bollinger") else "off"
        SMA = "on" if request.form.get("SMA") else "off"
        info_phone = "on" if request.form.get("info_phone") else "off"
        info_mail = "on" if request.form.get("info_mail") else "off"
        preferences = {
            "name": request.form.get("name"),
            "Email": request.form.get("Email"),
            "phone": request.form.get("phone"),
            "RSI": RSI,
            "MACD": MACD,
            "Trend": Trend,
            "EMA": EMA,
            "Bollinger": Bollinger,
            "SMA": SMA,
            "info_phone": info_phone,
            "info_mail": info_mail,
        }
        mongo.db.categories.update({"_id": ObjectId(id)}, preferences)
        flash("Your preferences has been updated")
        return redirect(url_for("toolbox", username=session["user"]))

    return render_template("edit_preferences.html", id=id)


if __name__ == "__main__":
    app.run(os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)
