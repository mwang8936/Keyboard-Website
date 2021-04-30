from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import sqlalchemy

app = Flask(__name__)
app.secret_key = "bruh"

app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def home(): #sam.com/
    return render_template("index.html")

@app.route("/hello")
def hello():
    return render_template("test.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login Succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("email was saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))

@app.route("/test")
def test():
    return render_template("new.html")

if __name__ == "__main__":
    app.run(debug=True)
