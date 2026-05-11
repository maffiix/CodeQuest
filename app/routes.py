from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, login_required, current_user, logout_user
from .models import User, Level, UserProgress, StoryProgress
from app.checker.runner import run_checker
from app import db, login_manager
import os
import json


main = Blueprint("main", __name__)


@main.route("/")
def index():
    levels = Level.query.order_by(Level.order).all()
    completed_ids = []
    try:
        completed_ids = {
            p.level_id
            for p in UserProgress.query.filter_by(user_id=current_user.id, completed=True)
        }
    except:
        completed_ids = []

    levels = levels[0:len(completed_ids) + 1]
    return render_template("index.html",
        levels=levels,
        completed_ids=completed_ids)


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
    if User.query.filter_by(username=username).first() is not None:
        return render_template("register.html", message="Username already exists")
    user = User()
    user.username = username
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for("main.login"))


@main.route("/level/<int:level_id>", methods=["GET"])
@login_required
def level(level_id):
    level = Level.query.get_or_404(level_id)
    
    if level.story_id and level.story_id > 0:
        story_progress = StoryProgress.query.filter_by(
            user_id=current_user.id,
            story_id=level.story_id,
            completed=True
        ).first()
        
        if not story_progress:
            return redirect(url_for("main.view_story", story_id=level.story_id))
    
    return render_template("level.html", level=level)


""" @main.route("/levels")
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
    ) """


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for("main.index"))

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

        return redirect(url_for("main.index"))

    return render_template(
        "level.html",
        level=level,
        error=message
    )


@main.route("/storytelling/<int:story_id>")
@login_required
def view_story(story_id):
    story_file = os.path.join(os.path.dirname(__file__), 'data', 'story.json')
    
    try:
        with open(story_file, 'r', encoding='utf-8') as f:
            stories = json.load(f)
    except FileNotFoundError:
        return "Файл сюжета не найден", 404
    
    story = None
    for key, value in stories.items():
        if value.get('id') == story_id:
            story = value
            story['key'] = key
            break
    
    if not story:
        return "Сюжет не найден", 404
    
    # Проверяем, прочитана ли уже история
    story_progress = StoryProgress.query.filter_by(
        user_id=current_user.id,
        story_id=story_id,
        completed=True
    ).first()
    
    story['is_read'] = story_progress is not None
    
    return render_template("story_template.html", story=story)


@main.route("/storytelling/<int:story_id>/complete", methods=["POST"])
@login_required
def complete_story(story_id):
    # Отмечаем историю как прочитанную
    progress = StoryProgress.query.filter_by(
        user_id=current_user.id,
        story_id=story_id
    ).first()
    
    if not progress:
        progress = StoryProgress()
        progress.user_id = current_user.id
        progress.story_id = story_id
        progress.completed = True
        db.session.add(progress)
        db.session.commit()
    
    # Ищем уровень с этой историей
    level = Level.query.filter_by(story_id=story_id).first()
    
    if level:
        return redirect(url_for("main.level", level_id=level.id))
    
    return redirect(url_for("main.index"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))