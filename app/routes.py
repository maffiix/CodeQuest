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
    
    story_file = os.path.join(os.path.dirname(__file__), 'data', 'story.json')
    stories = []
    try:
        with open(story_file, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
            stories = list(story_data.values())
    except:
        pass
    
    completed_levels = set()
    completed_stories = set()
    if current_user.is_authenticated:
        completed_levels = {
            p.level_id for p in UserProgress.query.filter_by(
                user_id=current_user.id, completed=True
            )
        }
        completed_stories = {
            p.story_id for p in StoryProgress.query.filter_by(
                user_id=current_user.id, completed=True
            )
        }
    
    timeline = []
    added_story_ids = set()
    previous_level_completed = True

    for idx, level in enumerate(levels):
        current_story = None
        for story in stories:
            if story.get('id') == level.story_id:
                current_story = story
                break
        
        if current_story:
            story_can_access = previous_level_completed
            story_id = current_story.get('id')
            
            if story_id not in added_story_ids:
                current_story['is_completed'] = story_id in completed_stories
                current_story['can_access'] = story_can_access
                timeline.append(current_story)
                added_story_ids.add(story_id)
        
        level.can_access = level.story_id in completed_stories if level.story_id else True
        level.is_completed = level.id in completed_levels
        timeline.append(level)
        
        previous_level_completed = level.id in completed_levels
    
    return render_template("index.html", timeline=timeline)


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
    
    
    return redirect(url_for("main.index"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))