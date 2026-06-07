from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Bind db to the Flask app and create all tables."""
    db.init_app(app)
    with app.app_context():
        from database.models import Cafe, MenuItem, UserSession, VoiceLog, Favorite  # 👈 add this
        db.session.execute(db.text("CREATE EXTENSION IF NOT EXISTS vector;"))
        db.session.commit()
        db.create_all()
        print("✅ Database ready.")