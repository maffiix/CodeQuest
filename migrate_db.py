from app import create_app, db

def migrate_db():
    with create_app().app_context():
        db.drop_all()
        print("Dropped all tables")
        
        db.create_all()
        print("Created all tables with current structure")

if __name__ == "__main__":
    migrate_db()