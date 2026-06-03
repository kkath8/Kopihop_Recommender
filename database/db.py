from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Bind db to the Flask app and create all tables."""
    db.init_app(app)
    with app.app_context():
        db.session.execute(db.text("CREATE EXTENSION IF NOT EXISTS vector;"))
        db.session.commit()
        db.create_all()
        print("✅ Database ready.")