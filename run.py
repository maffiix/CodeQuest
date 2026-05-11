from app import create_app
from migrate_db import migrate_db
from init_levels import init_levels

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # Проверяем есть ли таблицы
        from app.models import Level
        try:
            Level.query.first()
        except:
            print("Database not ready, running migrations...")
            migrate_db()
            init_levels()
    
    app.run(debug=True)