from app import create_app, db
from app.models import Level

app = create_app()

LEVEL_INFO = [
    {
        "title": "The Broken Greeting",
        "description": "Write function greet(name) that returns 'Hello, <name>!'",
        "starter_code": "def greet(name):\n    pass",
        "order": 1,
        "checker_name": "level_1"
    },
]

with app.app_context():
    for info in LEVEL_INFO:
        if not Level.query.filter_by(title=info["title"]).first():
            lvl = Level(**info)
            db.session.add(lvl)
    db.session.commit()