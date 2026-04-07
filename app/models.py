from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def __repr__(self):
        return f"<User {self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    starter_code = db.Column(db.Text)

    order = db.Column(db.Integer, unique=True)
    checker_name = db.Column(db.String(50), nullable=False)


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    level_id = db.Column(db.Integer, db.ForeignKey("level.id"))

    completed = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="progress")
    level = db.relationship("Level")