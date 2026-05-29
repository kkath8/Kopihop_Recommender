from flask_sqlalchemy import SQLAlchemy

# Single shared db instance used across the app
db = SQLAlchemy()


def init_db(app):
    """Bind the SQLAlchemy instance to the Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
