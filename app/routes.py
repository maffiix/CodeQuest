from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, login_required, current_user, logout_user
from .models import User, Level, UserProgress
from app.checker.runner import run_checker
from app import db, login_manager

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


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


@main.route("/level/<int:level_id>", method="GET")
@login_required
def level(level_id):
    level = Level.query.get_or_404(level_id)
    return render_template("level.html", level=level)


@main.route("/levels")
@login_required
def levels():

    levels = Level.query.order_by(Level.order).all()

    completed_ids = {
        p.level_id
        for p in UserProgress.query.filter_by(user_id=current_user.id, completed=True)
    }

    return render_template(
        "levels.html",
        levels=levels,
        completed_ids=completed_ids
    )


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for("main.levels"))

    return render_template("login.html", message="Invalid username or password")


@main.route("/level/<int:level_id>", methods=["POST"])
@login_required
def submit_solution(level_id):

    level = Level.query.get_or_404(level_id)

    code = request.form["code"]

    success, message = run_checker(level.checker_name, code)

    if success:
        progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            level_id=level.id
        ).first()

        if not progress:
            progress = UserProgress()
            progress.user_id = current_user.id
            progress.level_id = level.id
            progress.completed = True
            db.session.add(progress)
            db.session.commit()

        return redirect(url_for("main.levels"))

    return render_template(
        "level.html",
        level=level,
        error=message
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))