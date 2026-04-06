from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, login_required
from .models import User
from app import db, login_manager

main = Blueprint("main", __name__)


@main.route("/")
def index():
    user = User()
    user.username = "maffiix"
    db.session.add(user)
    db.session.commit()

    return "User added!"


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]
    repeat = request.form["password_repeat"]
    if password != repeat:
        return render_template("register.html", message="Passwords don't match")
    if not password:
        return render_template("register.html", message="Password can't be empty")
    user = User()
    user.username = username
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("main.login"))


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for("main.dashboard"))

    return redirect(url_for("main.login"))


@login_required
@main.route("/dashboard")
def dashboard():
    return "SECRET PAGE NAHH"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))