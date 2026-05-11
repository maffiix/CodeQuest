from app import create_app, db
from app.models import User, Level, UserProgress, StoryProgress
import sqlite3

app = create_app()

with app.app_context():
    try:
        db.engine.execute('ALTER TABLE level ADD COLUMN story_id INTEGER DEFAULT 0')
        print("Added story_id to level table")
    except Exception as e:
        print(f"story_id might already exist: {e}")
    
    db.create_all()
    print("Tables updated successfully!")