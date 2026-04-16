from app import create_app, db
from app.models import Level

app = create_app()

LEVEL_INFO = [
    {
        "title": "The Broken Greeting",
        "description": "As you enter the country, you see the broken greeting stand. Citizens ask you to fix it.<br><br>Write function greet(name), which makes greeting in format 'Hello, <name>!'",
        "starter_code": "def greet(name):\n    pass",
        "order": 1,
        "checker_name": "level_1"
    },
    {
        "title": "Bridgemaker",
        "description": "After you successfully fixed The Greeting Machine, you go forward. One old person says you: 'All bridges are broken here. We can repair them, but we don't know how many bricks we need"
                       "'. Help citizens to count how many block they need to repair one bridge<br><br>Write function calculate(a, b) that return A + B.",
        "starter_code": "def calculate(a, b):\n    pass",
        "order": 2,
        "checker_name": "level_2"
    }
]

with app.app_context():
    for info in LEVEL_INFO:
        if not Level.query.filter_by(title=info["title"]).first():
            lvl = Level(**info)
            db.session.add(lvl)
    db.session.commit()